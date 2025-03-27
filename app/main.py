from flask import Flask, request, jsonify
from get.get_summary import get_summary
from get.get_booking_distribution import get_booking_distribution
from load.load import post_load_data
from get.get_income_distribution import get_income_distribution
from get.get_cancellations import get_cancellations
from get.get_workers_workload import get_workers_workload
from get.get_feedback_analysis import get_feedback_analysis
app = Flask(__name__)

@app.route('/analytics/summary', methods=['GET'])
def aggregated_data():
    return get_summary()

@app.route('/analytics/distribution/bookings', methods=['GET'])
def booking_distribution():
    return get_booking_distribution()

@app.route('/analytics/distribution/income', methods=['GET'])
def income_distribution():
    return get_income_distribution()

@app.route('/analytics/cancellations', methods=['GET'])
def cancellations():
    return get_cancellations()

@app.route('/analytics/workload', methods=['GET'])
def workers_workload():
    return get_workers_workload()

@app.route('/analytics/ai/feedbacks', methods=['GET'])
def feedback_analysis():
    return get_feedback_analysis()

@app.route('/analytics/load', methods=['POST'])
def load_data():
    return post_load_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
