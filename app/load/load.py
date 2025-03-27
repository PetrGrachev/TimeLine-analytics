from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config
from .summary_load import load_summary
from .booking_distribution import load_booking_distribution
from .income_distribution import load_income_distribution
from .load_cancellations import load_cancellaions
from .load_workers_workload import load_workers_workload
from .load_feedback_analysis import load_feedback_analysis
def post_load_data():
    try:
        load_summary()
        load_booking_distribution()
        load_income_distribution()
        load_cancellaions()
        load_workers_workload()
        load_feedback_analysis()
        return jsonify({"status": "Data loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500