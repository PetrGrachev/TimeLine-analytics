import json
from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config
from load.ai.get_keywords import get_keywords

def load_feedback_analysis():

    conn_main = get_db_connection(Config.MAIN_DB_CONFIG)
    cursor_main = conn_main.cursor()

    # Получаем список всех организаций
    cursor_main.execute("SELECT org_id FROM orgs;")
    org_ids = [row[0] for row in cursor_main.fetchall()]

    for org_id in org_ids:
        # Получаем отзывы для текущей организации за последнюю неделю
        cursor_main.execute("""
            SELECT f.feedback
            FROM feedbacks f
            JOIN records r ON f.record_id = r.record_id
            WHERE f.feedback IS NOT NULL
              AND f.feedback != ''
              AND f.created_at >= CURRENT_DATE - INTERVAL '7 days'
              AND r.org_id = %s;
        """, (org_id,))
        feedback_rows = cursor_main.fetchall()

        feedback_texts = [row[0] for row in feedback_rows]

        if not feedback_texts:
            print(f"No feedback found for org_id={org_id}, skipping analysis.")
            continue  # Пропускаем организации без отзывов

        # Анализ ключевых слов
        keywords = get_keywords(feedback_texts)

        # Сохраняем результаты в аналитическую БД
        conn_analytics = get_db_connection(Config.ANALYTICS_DB_CONFIG)
        cursor_analytics = conn_analytics.cursor()

        cursor_analytics.execute("""
            INSERT INTO feedback_analysis (
                org_id, positive_keywords, negative_keywords, period_start, period_end
            )
            VALUES (%s, %s, %s, CURRENT_DATE - INTERVAL '7 days', CURRENT_DATE)
            ON CONFLICT (org_id, period_start, period_end) DO UPDATE
            SET positive_keywords = EXCLUDED.positive_keywords,
                negative_keywords = EXCLUDED.negative_keywords;
        """, (
            org_id,
            json.dumps(keywords["positive_keywords"]),
            json.dumps(keywords["negative_keywords"])
        ))

        conn_analytics.commit()
        conn_analytics.close()

        print(f"Feedback analysis loaded successfully for org_id={org_id}")

    conn_main.close()