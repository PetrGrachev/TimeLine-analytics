from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def get_workers_workload():
    org_id = request.args.get("org_id")
    if not org_id:
        return jsonify({"error": "org_id is required"}), 400
    try:
        conn = get_db_connection(Config.ANALYTICS_DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT period_start, period_end, worker_id, busy_slots, total_slots, workload_percentage
            FROM workers_workload
            WHERE org_id = %s
                       AND (period_start, period_end) = (
                            SELECT period_start, period_end
                            FROM workers_workload
                            WHERE org_id = %s
                            ORDER BY period_end DESC
                            LIMIT 1
                        )
            ORDER BY period_end DESC
            LIMIT 3;          
        """, (org_id, org_id))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({"error": "No data found for this organization"}), 404

        period_start, period_end = rows[0][0], rows[0][1]

        workers = []
        for row in rows:
            workers.append({
                "worker_id": row[2],
                "busy_slots": row[3],
                "total_slots": row[4],
                "workload_percentage": float(row[5])
            })

        response = {
            "period_start": period_start,
            "period_end": period_end,
            "workers": workers
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
