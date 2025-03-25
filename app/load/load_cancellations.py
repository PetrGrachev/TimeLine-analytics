from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def load_cancellaions():
    try:
        conn_main = get_db_connection(Config.MAIN_DB_CONFIG)
        cursor_main = conn_main.cursor()
        cursor_main.execute("""
            WITH org_stats AS (
    SELECT 
        org_id,
        COUNT(*) AS total_records,
        SUM(CASE WHEN is_canceled THEN 1 ELSE 0 END) AS canceled_records
    FROM records
    GROUP BY org_id
),
reason_stats AS (
    SELECT 
        org_id, 
        cancel_reason,
        COUNT(*) AS reason_count,
        RANK() OVER (PARTITION BY org_id ORDER BY COUNT(*) DESC) AS rnk
    FROM records
    WHERE is_canceled = TRUE 
      AND cancel_reason <> ''
    GROUP BY org_id, cancel_reason
)
SELECT 
    o.org_id,
    o.canceled_records,
    ROUND(100.0 * o.canceled_records / o.total_records, 2) AS cancellation_percentage,
    r.cancel_reason AS most_common_cancel_reason
FROM org_stats o
LEFT JOIN reason_stats r ON o.org_id = r.org_id AND r.rnk = 1;
        """)
        distribution_data = cursor_main.fetchall()
        conn_main.close()

        conn_analytics = get_db_connection(Config.ANALYTICS_DB_CONFIG)
        cursor_analytics = conn_analytics.cursor()
        for row in distribution_data:
            org_id, canceled_records, cancellation_percentage, most_common_cancel_reason = row
            cursor_analytics.execute("""
                INSERT INTO cancellations (
                    org_id, canceled_records, cancellation_percentage, most_common_cancel_reason, period_start, period_end
                )
                VALUES (
                    %s, %s, %s, %s, CURRENT_DATE - INTERVAL '1 month', CURRENT_DATE
                )
                ON CONFLICT (org_id, period_start, period_end) DO UPDATE
                SET canceled_records = EXCLUDED.canceled_records,
                    cancellation_percentage = EXCLUDED.cancellation_percentage,
                    most_common_cancel_reason = EXCLUDED.most_common_cancel_reason;
            """, (org_id, canceled_records, cancellation_percentage, most_common_cancel_reason))
        conn_analytics.commit()
        conn_analytics.close()
        print("Cancellations data loaded successfully.")
    except Exception as e:
        print("Error loading cancellations: " + str(e))