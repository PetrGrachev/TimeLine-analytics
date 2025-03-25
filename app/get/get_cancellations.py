from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def get_cancellations():
    org_id = request.args.get("org_id")
    if not org_id:
        return jsonify({"error": "org_id is required"}), 400
    try:
        conn = get_db_connection(Config.ANALYTICS_DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT period_start, period_end, canceled_records, cancellation_percentage, most_common_cancel_reason
            FROM cancellations
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
            "info":{
                "canceled_records": row[2],
                "cancellation_percentage": row[3],
                "most_common_cancel_reason": row[4],
            }
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500