from flask import Flask, request, jsonify
from flasgger import Swagger
import os
from get.get_summary import get_summary
from get.get_booking_distribution import get_booking_distribution
from load.load import post_load_data
from get.get_income_distribution import get_income_distribution
from get.get_cancellations import get_cancellations
from get.get_workers_workload import get_workers_workload
from get.get_feedback_analysis import get_feedback_analysis

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/analytics/summary', methods=['GET'])
def aggregated_data():
    """
    Получить агрегированную статистику

    ---
    tags:
      - Analytics
    parameters:
      - name: org_id
        in: query
        type: integer
        required: true
        description: ID организации
    responses:
      200:
        description: Успешный ответ с аналитикой
        schema:
          type: object
          properties:
            period_start:
              type: string
              format: date
            period_end:
              type: string
              format: date
            metrics:
              type: object
              properties:
                total_bookings:
                  type: integer
                total_revenue:
                  type: number
                avg_booking_cost:
                  type: number
            clients:
              type: object
              properties:
                unique_customers:
                  type: integer
                most_frequent_client_id:
                  type: integer
            workers:
              type: object
              properties:
                best_worker:
                  type: object
                  properties:
                    worker_id:
                      type: integer
                    rating:
                      type: number
                worst_worker:
                  type: object
                  properties:
                    worker_id:
                      type: integer
                    rating:
                      type: number
            services:
              type: object
              properties:
                popular_service_id:
                  type: integer
                best_service:
                  type: object
                  properties:
                    service_id:
                      type: integer
                    rating:
                      type: number
                worst_service:
                  type: object
                  properties:
                    service_id:
                      type: integer
                    rating:
                      type: number
      400:
        description: Не передан org_id
      404:
        description: Нет данных
    """
    return get_summary()


@app.route('/analytics/distribution/bookings', methods=['GET'])
def booking_distribution():
    """
    Получить распределение бронирований по дням недели и часам

    ---
    tags:
      - Distribution
    parameters:
      - name: org_id
        in: query
        type: integer
        required: true
        description: ID организации
    responses:
      200:
        description: Распределение бронирований по часам
        schema:
          type: object
          properties:
            distribution:
              type: array
              items:
                type: object
                properties:
                  day_of_week:
                    type: integer
                    description: День недели (1 — Пн, 7 — Вс)
                  hours:
                    type: array
                    items:
                      type: object
                      properties:
                        hour:
                          type: integer
                          description: Час (0–23)
                        bookings:
                          type: integer
                          description: Количество бронирований
      400:
        description: Не указан org_id
      500:
        description: Ошибка при получении данных
    """
    return get_booking_distribution()

@app.route('/analytics/distribution/income', methods=['GET'])
def income_distribution():
    """
    Получить распределение доходов по дням недели

    ---
    tags:
      - Distribution
    parameters:
      - name: org_id
        in: query
        type: integer
        required: true
        description: ID организации
    responses:
      200:
        description: Распределение доходов и количества бронирований по дням недели
        schema:
          type: object
          properties:
            distribution:
              type: array
              items:
                type: object
                properties:
                  day_of_week:
                    type: integer
                    description: День недели (1 — Пн, 7 — Вс)
                  info:
                    type: array
                    items:
                      type: object
                      properties:
                        income:
                          type: number
                          format: float
                          description: Общий доход за этот день
                        bookings:
                          type: integer
                          description: Количество бронирований
      400:
        description: Не указан org_id
      500:
        description: Ошибка при получении данных
    """
    return get_income_distribution()

@app.route('/analytics/cancellations', methods=['GET'])
def cancellations():
    """
    Получить статистику отмен бронирований по организации

    ---
    tags:
      - Analytics
    parameters:
      - name: org_id
        in: query
        type: integer
        required: true
        description: ID организации
    responses:
      200:
        description: Статистика отмен бронирований
        schema:
          type: object
          properties:
            period_start:
              type: string
              format: date
              description: Начало периода анализа
            period_end:
              type: string
              format: date
              description: Конец периода анализа
            info:
              type: object
              properties:
                canceled_records:
                  type: integer
                  description: Количество отмен за период
                cancellation_percentage:
                  type: number
                  format: float
                  description: Доля отмен от всех записей (в %)
                most_common_cancel_reason:
                  type: string
                  description: Самая частая причина отмен
      400:
        description: Не указан org_id
      404:
        description: Данные не найдены
      500:
        description: Ошибка сервера при получении данных
    """
    return get_cancellations()

@app.route('/analytics/workload', methods=['GET'])
def workers_workload():
    """
    Получить загрузку работников по организации

    ---
    tags:
      - Analytics
    parameters:
      - name: org_id
        in: query
        type: integer
        required: true
        description: ID организации
    responses:
      200:
        description: Загрузка работников по количеству занятых слотов
        schema:
          type: object
          properties:
            period_start:
              type: string
              format: date
              description: Начало анализируемого периода
            period_end:
              type: string
              format: date
              description: Конец анализируемого периода
            workers:
              type: array
              items:
                type: object
                properties:
                  worker_id:
                    type: integer
                    description: ID работника
                  busy_slots:
                    type: integer
                    description: Количество занятых слотов
                  total_slots:
                    type: integer
                    description: Общее количество слотов
                  workload_percentage:
                    type: number
                    format: float
                    description: Загрузка в процентах
      400:
        description: Не указан org_id
      404:
        description: Нет данных по загрузке
      500:
        description: Внутренняя ошибка сервера
    """
    return get_workers_workload()

@app.route('/analytics/ai/feedbacks', methods=['GET'])
def feedback_analysis():
    """
    Получить анализ отзывов на основе ключевых фраз

    ---
    tags:
      - AI Analysis
    parameters:
      - name: org_id
        in: query
        type: integer
        required: true
        description: ID организации
    responses:
      200:
        description: Ключевые положительные и отрицательные фразы из отзывов клиентов
        schema:
          type: object
          properties:
            period_start:
              type: string
              format: date
              description: Начало анализируемого периода
            period_end:
              type: string
              format: date
              description: Конец анализируемого периода
            keywords:
              type: object
              properties:
                positive:
                  type: array
                  items:
                    type: object
                    properties:
                      phrase:
                        type: string
                        description: Положительная фраза
                      score:
                        type: number
                        format: float
                        description: Важность ключевой фразы
                negative:
                  type: array
                  items:
                    type: object
                    properties:
                      phrase:
                        type: string
                        description: Отрицательная фраза
                      score:
                        type: number
                        format: float
                        description: Важность ключевой фразы
      400:
        description: Не указан org_id
      404:
        description: Нет данных анализа по организации
      500:
        description: Внутренняя ошибка при обработке запроса
    """
    return get_feedback_analysis()

@app.route('/analytics/load', methods=['POST'])
def load_data():
    """
    Запустить обновление аналитических данных

    ---
    tags:
      - Internal
    summary: Загрузка агрегированной статистики и ИИ-аналитики
    description: Выполняет пересчёт и загрузку всех аналитических данных в базу.
    responses:
      200:
        description: Данные успешно загружены
        schema:
          type: object
          properties:
            status:
              type: string
              example: Data loaded successfully
      500:
        description: Внутренняя ошибка сервера при выполнении загрузки
        schema:
          type: object
          properties:
            error:
              type: string
              example: Internal server error
    """
    return post_load_data()

@app.route('/analytics/health', methods=['GET'])
def health_check():
    """
    Проверка состояния сервиса

    ---
    tags:
      - Health
    summary: Проверка состояния микросервиса
    description: Проверка работоспособности контейнера (Docker healthcheck).
    responses:
      200:
        description: Сервис работает корректно
        content:
          application/json:
            example:
              status: ok
    """
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host='0.0.0.0', port=port)
