from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def load_income_distribution():
    try:
        conn_main = get_db_connection(Config.MAIN_DB_CONFIG)
        cursor_main = conn_main.cursor()
        cursor_main.execute("""
            SELECT 
                r.org_id,
                EXTRACT(ISODOW FROM s.session_begin) AS day_of_week,
                SUM(se.cost) AS total_income,
                COUNT(*) AS total_bookings
            FROM records r
            JOIN slots s ON r.slot_id = s.slot_id
            JOIN services se ON r.service_id = se.service_id
            GROUP BY 
                r.org_id, 
                EXTRACT(ISODOW FROM s.session_begin)
            ORDER BY 
                r.org_id, day_of_week;
        """)
        distribution_data = cursor_main.fetchall()
        conn_main.close()

        conn_analytics = get_db_connection(Config.ANALYTICS_DB_CONFIG)
        cursor_analytics = conn_analytics.cursor()
        for row in distribution_data:
            org_id, day_of_week, total_bookings, total_income = row
            cursor_analytics.execute("""
                INSERT INTO income_distribution (
                    org_id, day_of_week, total_bookings, total_income, period_start, period_end
                )
                VALUES (
                    %s, %s, %s, %s, CURRENT_DATE - INTERVAL '1 month', CURRENT_DATE
                )
                ON CONFLICT (org_id, day_of_week, period_start, period_end) DO UPDATE
                SET total_bookings = EXCLUDED.total_bookings,
                    total_income = EXCLUDED.total_income;
            """, (org_id, day_of_week, total_bookings, total_income))
        conn_analytics.commit()
        conn_analytics.close()
        print("Income distribution data loaded successfully.")
    except Exception as e:
        print("Error loading Income distribution: " + str(e))