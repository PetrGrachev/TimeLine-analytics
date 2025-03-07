from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def load_summary():
    try:
        # Подключаемся к главной БД и получаем агрегированные данные
        conn_main = get_db_connection(Config.MAIN_DB_CONFIG)
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
        conn_analytics = get_db_connection(Config.ANALYTICS_DB_CONFIG)
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

        print("Summary data loaded successfully.")
    except Exception as e:
        print("Error loading summary: " + str(e))