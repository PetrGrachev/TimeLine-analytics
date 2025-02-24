from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Конфигурация аналитической БД (используйте переменные окружения, переданные из docker-compose)
ANALYTICS_DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "analytics_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "secret"),
    "host": os.getenv("DB_HOST", "postgres_analytics"),
    "port": os.getenv("DB_PORT", "5432")
}

# Конфигурация главной БД
MAIN_DB_CONFIG = {
    "dbname": os.getenv("MAIN_DB_NAME", "main_db"),
    "user": os.getenv("MAIN_DB_USER", "postgres"),
    "password": os.getenv("MAIN_DB_PASSWORD", "secret"),
    "host": os.getenv("MAIN_DB_HOST", "postgres_main"),
    "port": os.getenv("MAIN_DB_PORT", "5432")
}

def get_db_connection(config):
    return psycopg2.connect(**config)

# Эндпоинт для получения агрегированной информации из аналитической БД по org_id
@app.route('/analytics/summary', methods=['GET'])
def get_aggregated_data():
    org_id = request.args.get("org_id")
    if not org_id:
        return jsonify({"error": "org_id is required"}), 400
    try:
        conn = get_db_connection(ANALYTICS_DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT period_start, period_end, total_bookings, total_revenue, avg_booking_cost, unique_customers, popular_service
            FROM booking_stats
            WHERE org_id = %s
            ORDER BY period_end DESC
            LIMIT 1
        """, (org_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return jsonify({"error": "No data found for this organization"}), 404
        response = {
            "period_start": row[0],
            "period_end": row[1],
            "total_bookings": row[2],
            "total_revenue": row[3],
            "avg_booking_cost": row[4],
            "unique_customers": row[5],
            "popular_service": row[6]
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Эндпоинт для загрузки агрегированных данных из главной БД в аналитическую
@app.route('/analytics/load', methods=['POST'])
def load_data():
    try:
        # Подключаемся к главной БД и получаем агрегированные данные
        conn_main = get_db_connection(MAIN_DB_CONFIG)
        cursor_main = conn_main.cursor()
        cursor_main.execute("""
            WITH most_popular_service as (
                SELECT DISTINCT ON (r.org_id)
                r.org_id,
                s.name AS service_name
                FROM records r
                JOIN services s ON r.service_id = s.service_id
                GROUP BY r.org_id, s.name
                ORDER BY r.org_id, COUNT(*) DESC
            ),
            booking_stats AS (             
            SELECT r.org_id,
                   COUNT(*) AS total_bookings,
                   SUM(s.cost) AS total_revenue,
                   AVG(s.cost) AS avg_booking_cost,
                   COUNT(DISTINCT user_id) AS unique_customers
            FROM records r
            JOIN services s ON r.service_id = s.service_id
            GROUP BY r.org_id
            )
            
            SELECT bs.org_id,
                   bs.total_bookings,
                   bs.total_revenue,
                   bs.avg_booking_cost,
                   bs.unique_customers,
                   mps.service_name AS popular_service
            FROM booking_stats bs
            LEFT JOIN most_popular_service mps ON bs.org_id = mps.org_id;
        """)
        data = cursor_main.fetchall()
        conn_main.close()

        # Подключаемся к аналитической БД и вставляем данные
        conn_analytics = get_db_connection(ANALYTICS_DB_CONFIG)
        cursor_analytics = conn_analytics.cursor()
        for row in data:
            cursor_analytics.execute("""
                INSERT INTO booking_stats (org_id, period_start, period_end, total_bookings, total_revenue, avg_booking_cost, unique_customers, popular_service)
                VALUES (%s, CURRENT_DATE - INTERVAL '1 month', CURRENT_DATE, %s, %s, %s, %s, %s)
                ON CONFLICT (org_id, period_end) DO UPDATE 
                SET total_bookings = EXCLUDED.total_bookings,
                    total_revenue = EXCLUDED.total_revenue,
                    avg_booking_cost = EXCLUDED.avg_booking_cost,
                    unique_customers = EXCLUDED.unique_customers,
                    popular_service = EXCLUDED.popular_service;
            """, row)
        conn_analytics.commit()
        conn_analytics.close()
        return jsonify({"status": "Data loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
