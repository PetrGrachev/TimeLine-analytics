from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def load_booking_distribution():
    """
    Функция загружает данные распределения бронирований по дню недели и часу
    из основной БД и вставляет их в таблицу booking_distribution аналитической БД.
    """
    try:
        conn_main = get_db_connection(Config.MAIN_DB_CONFIG)
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

        conn_analytics = get_db_connection(Config.ANALYTICS_DB_CONFIG)
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