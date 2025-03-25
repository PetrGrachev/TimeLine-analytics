from flask import Flask, request, jsonify
from summary.summary import get_aggregated_data
from distribution.distribution import get_booking_distribution
from load.load import post_load_data
from get.get_income_distribution import get_income_distribution

app = Flask(__name__)

@app.route('/analytics/summary', methods=['GET'])
def aggregated_data():
    return get_aggregated_data()

@app.route('/analytics/distribution/bookings', methods=['GET'])
def booking_distribution():
    return get_booking_distribution()

@app.route('/analytics/distribution/income', methods=['GET'])
def income_distribution():
    return get_income_distribution()

@app.route('/analytics/load', methods=['POST'])
def load_data():
    return post_load_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
