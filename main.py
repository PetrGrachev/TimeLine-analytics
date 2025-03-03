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
            SELECT period_start, period_end, total_bookings, total_revenue, avg_booking_cost, unique_customers, popular_service_id, most_frequent_client_id, best_worker_id, best_worker_rating, worst_worker_id, worst_worker_rating, best_service_id, best_service_rating, worst_service_id, worst_service_rating
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
            "metrics":{
                "total_bookings": row[2],
                "total_revenue": row[3],
                "avg_booking_cost": row[4],
            },
            "clients":{
                "unique_customers": row[5],
                "most_frequent_client_id": row[7],
            },        
            "workers":{
                "best_worker": {
                    "worker_id": row[8],
                    "rating": row[9]
                },
                "worst_worker": {
                    "worker_id": row[10],
                    "rating": row[11]
                },
            },
            "services":{
                "popular_service_id": row[6],
                "best_service": {
                    "service_id": row[12],
                    "rating": row[13]
                },
                "worst_service": {
                    "service_id": row[14],
                    "rating": row[15]
                },
            },
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analytics/distribution', methods=['GET'])
def get_booking_distribution():
    org_id = request.args.get("org_id")
    if not org_id:
        return jsonify({"error": "org_id is required"}), 400
    try:
        conn = get_db_connection(ANALYTICS_DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT day_of_week, hour, total_bookings
            FROM booking_distribution
            WHERE org_id = %s
            ORDER BY day_of_week, hour;
        """, (org_id,))
        rows = cursor.fetchall()
        conn.close()

        # Группируем данные по дню недели
        distribution_dict = {}
        for row in rows:
            day = int(row[0])
            hour = int(row[1])
            bookings = row[2]
            if day not in distribution_dict:
                distribution_dict[day] = []
            distribution_dict[day].append({"hour": hour, "bookings": bookings})
        
        # Преобразуем словарь в список с нужной структурой
        distribution = []
        for day, hours in distribution_dict.items():
            distribution.append({
                "day_of_week": day,
                "hours": hours
            })

        return jsonify({"distribution": distribution}), 200
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
                s.service_id AS service_id
                FROM records r
                JOIN services s ON r.service_id = s.service_id
                GROUP BY r.org_id, s.service_id
                ORDER BY r.org_id, COUNT(*) DESC
            ),
                            
            most_frequent_client as (
                SELECT DISTINCT ON (org_id)
                org_id,
                user_id
                FROM records
                GROUP BY org_id, user_id
                ORDER BY org_id, COUNT(*) DESC
            ),
            
                            
            worker_ratings AS (
                SELECT 
                    w.org_id,
                    w.worker_id,
                    AVG(f.stars) AS avg_rating,
                    RANK() OVER (PARTITION BY w.org_id ORDER BY AVG(f.stars) DESC) AS best_rank,
                    RANK() OVER (PARTITION BY w.org_id ORDER BY AVG(f.stars) ASC) AS worst_rank
                FROM workers w
                JOIN records r ON w.worker_id = r.worker_id
                JOIN feedbacks f ON r.record_id = f.record_id
                WHERE r.reviewed = TRUE
                GROUP BY w.org_id, w.worker_id
            ),
                            
            best_workers AS (
                SELECT
                    org_id,
                    MAX(CASE WHEN best_rank = 1 THEN worker_id END) AS best_worker_id,
                    MAX(CASE WHEN best_rank = 1 THEN avg_rating END) AS best_worker_rating,
                    MAX(CASE WHEN worst_rank = 1 THEN worker_id END) AS worst_worker_id,
                    MAX(CASE WHEN worst_rank = 1 THEN avg_rating END) AS worst_worker_rating
                FROM worker_ratings
                GROUP BY org_id
            ),
                            
            service_ratings AS (
                SELECT 
                    s.org_id,
                    s.service_id,
                    AVG(f.stars) AS avg_rating,
                    RANK() OVER (PARTITION BY s.org_id ORDER BY AVG(f.stars) DESC) AS best_rank,
                    RANK() OVER (PARTITION BY s.org_id ORDER BY AVG(f.stars) ASC) AS worst_rank
                FROM services s
                JOIN records r ON s.service_id = r.service_id
                JOIN feedbacks f ON r.record_id = f.record_id
                WHERE r.reviewed = TRUE
                GROUP BY s.org_id, s.service_id
            ),
                            
            best_services AS (
                SELECT
                    org_id,
                    MAX(CASE WHEN best_rank = 1 THEN service_id END) AS best_service_id,
                    MAX(CASE WHEN best_rank = 1 THEN avg_rating END) AS best_service_rating,
                    MAX(CASE WHEN worst_rank = 1 THEN service_id END) AS worst_service_id,
                    MAX(CASE WHEN worst_rank = 1 THEN avg_rating END) AS worst_service_rating
                FROM service_ratings
                GROUP BY org_id
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
                   mps.service_id AS popular_service_id,
                   mfc.user_id AS most_frequent_client_id,
                   bw.best_worker_id AS best_worker_id,
                   bw.best_worker_rating AS best_worker_rating,
                   bw.worst_worker_id AS worst_worker_id,
                   bw.worst_worker_rating AS worst_worker_rating,
                   bse.best_service_id AS best_service_id,
                   bse.best_service_rating AS best_service_rating,
                   bse.worst_service_id AS worst_service_id,
                   bse.worst_service_rating AS worst_service_rating
            FROM booking_stats bs
            LEFT JOIN most_popular_service mps ON bs.org_id = mps.org_id
            LEFT JOIN most_frequent_client mfc ON mfc.org_id = bs.org_id
            LEFT JOIN best_workers bw ON bw.org_id = bs.org_id
            LEFT JOIN best_services bse ON bse.org_id = bs.org_id;
        """)
        data = cursor_main.fetchall()
        conn_main.close()

        # Подключаемся к аналитической БД и вставляем данные
        conn_analytics = get_db_connection(ANALYTICS_DB_CONFIG)
        cursor_analytics = conn_analytics.cursor()
        for row in data:
            cursor_analytics.execute("""
                INSERT INTO booking_stats (org_id, period_start, period_end, total_bookings, total_revenue, avg_booking_cost, unique_customers, popular_service_id, most_frequent_client_id, best_worker_id, best_worker_rating, worst_worker_id, worst_worker_rating, best_service_id, best_service_rating, worst_service_id, worst_service_rating)
                VALUES (%s, CURRENT_DATE - INTERVAL '1 month', CURRENT_DATE, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (org_id, period_end) DO UPDATE 
                SET total_bookings = EXCLUDED.total_bookings,
                    total_revenue = EXCLUDED.total_revenue,
                    avg_booking_cost = EXCLUDED.avg_booking_cost,
                    unique_customers = EXCLUDED.unique_customers,
                    popular_service_id = EXCLUDED.popular_service_id,
                    most_frequent_client_id = EXCLUDED.most_frequent_client_id,
                    best_worker_id = EXCLUDED.best_worker_id,
                    best_worker_rating = EXCLUDED.best_worker_rating,
                    worst_worker_id = EXCLUDED.worst_worker_id,
                    worst_worker_rating = EXCLUDED.worst_worker_rating,
                    best_service_id = EXCLUDED.best_service_id,
                    best_service_rating = EXCLUDED.best_service_rating,
                    worst_service_id = EXCLUDED.worst_service_id,
                    worst_service_rating = EXCLUDED.worst_service_rating;          
            """, row)
        conn_analytics.commit()
        conn_analytics.close()

        load_booking_distribution()

        return jsonify({"status": "Data loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def load_booking_distribution():
    """
    Функция загружает данные распределения бронирований по дню недели и часу
    из основной БД и вставляет их в таблицу booking_distribution аналитической БД.
    """
    try:
        conn_main = get_db_connection(MAIN_DB_CONFIG)
        cursor_main = conn_main.cursor()
        cursor_main.execute("""
            SELECT 
                r.org_id,
                EXTRACT(ISODOW FROM s.session_begin) AS day_of_week,
                EXTRACT(HOUR FROM s.session_begin) AS hour,
                COUNT(*) AS total_bookings
            FROM records r
            JOIN slots s ON r.slot_id = s.slot_id
            GROUP BY 
                r.org_id, 
                EXTRACT(ISODOW FROM s.session_begin), 
                EXTRACT(HOUR FROM s.session_begin)
            ORDER BY 
                r.org_id, day_of_week, hour;
        """)
        distribution_data = cursor_main.fetchall()
        conn_main.close()

        conn_analytics = get_db_connection(ANALYTICS_DB_CONFIG)
        cursor_analytics = conn_analytics.cursor()
        for row in distribution_data:
            org_id, day_of_week, hour, total_bookings = row
            cursor_analytics.execute("""
                INSERT INTO booking_distribution (
                    org_id, day_of_week, hour, total_bookings, period_start, period_end
                )
                VALUES (
                    %s, %s, %s, %s, CURRENT_DATE - INTERVAL '1 month', CURRENT_DATE
                )
                ON CONFLICT (org_id, day_of_week, hour, period_start, period_end) DO UPDATE
                SET total_bookings = EXCLUDED.total_bookings;
            """, (org_id, day_of_week, hour, total_bookings))
        conn_analytics.commit()
        conn_analytics.close()
        print("Booking distribution data loaded successfully.")
    except Exception as e:
        print("Error loading booking distribution: " + str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
