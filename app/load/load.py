from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config
from .summary_load import load_summary
from .booking_distribution import load_booking_distribution
from .income_distribution import load_income_distribution

def post_load_data():
    try:
        load_summary()
        load_booking_distribution()
        load_income_distribution()
        return jsonify({"status": "Data loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500