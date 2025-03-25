from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def get_summary():
    org_id = request.args.get("org_id")
    if not org_id:
        return jsonify({"error": "org_id is required"}), 400
    try:
        conn = get_db_connection(Config.ANALYTICS_DB_CONFIG)
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