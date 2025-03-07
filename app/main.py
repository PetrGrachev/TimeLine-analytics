from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config
from summary.summary import get_aggregated_data
from distribution.distribution import get_booking_distribution
from load.load import post_load_data

app = Flask(__name__)

# Эндпоинт для получения агрегированной информации из аналитической БД по org_id
@app.route('/analytics/summary', methods=['GET'])
def aggregated_data():
    return get_aggregated_data()

@app.route('/analytics/distribution', methods=['GET'])
def booking_distribution():
    return get_booking_distribution()

# Эндпоинт для загрузки агрегированных данных из главной БД в аналитическую
@app.route('/analytics/load', methods=['POST'])
def load_data():
    return post_load_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
