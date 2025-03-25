from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config

def get_booking_distribution():
    org_id = request.args.get("org_id")
    if not org_id:
        return jsonify({"error": "org_id is required"}), 400
    try:
        conn = get_db_connection(Config.ANALYTICS_DB_CONFIG)
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