from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def load_workers_workload():
   
    conn_main = get_db_connection(Config.MAIN_DB_CONFIG)
    cursor_main = conn_main.cursor()
    cursor_main.execute("""
    WITH busy_slots AS (
    SELECT
        worker_id,
        COUNT(*) AS busy_count
    FROM slots
    WHERE busy = TRUE
    GROUP BY worker_id
),
available_slots AS (
    SELECT
        ws.worker_id,
        SUM(EXTRACT(EPOCH FROM (ws.over - ws.start)) / 60 / w.session_duration) AS total_slots
    FROM worker_schedules ws
    JOIN workers w ON w.worker_id = ws.worker_id
    GROUP BY ws.worker_id
)
SELECT
    w.org_id,
    w.worker_id,
    COALESCE(bs.busy_count, 0) AS busy_slots,
    av.total_slots::INT AS total_slots,
    ROUND(100.0 * COALESCE(bs.busy_count, 0) / NULLIF(av.total_slots, 0), 2) AS workload_percentage
FROM workers w
LEFT JOIN busy_slots bs ON w.worker_id = bs.worker_id
LEFT JOIN available_slots av ON w.worker_id = av.worker_id
ORDER BY w.org_id, workload_percentage DESC;
        """)
    distribution_data = cursor_main.fetchall()
    conn_main.close()

    conn_analytics = get_db_connection(Config.ANALYTICS_DB_CONFIG)
    cursor_analytics = conn_analytics.cursor()
    for row in distribution_data:
        org_id, worker_id, busy_slots, total_slots, workload_percentage = row
        cursor_analytics.execute("""
            INSERT INTO workers_workload (
                org_id, worker_id, busy_slots, total_slots, workload_percentage, period_start, period_end
            )
            VALUES (
                %s, %s, %s, %s, %s, CURRENT_DATE - INTERVAL '1 month', CURRENT_DATE
            )
            ON CONFLICT (org_id, worker_id, period_start, period_end) DO UPDATE
            SET busy_slots = EXCLUDED.busy_slots,
                total_slots = EXCLUDED.total_slots,
                workload_percentage = EXCLUDED.workload_percentage;
        """, (org_id, worker_id, busy_slots, total_slots, workload_percentage))
    conn_analytics.commit()
    conn_analytics.close()