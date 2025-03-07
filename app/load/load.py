from flask import Flask, request, jsonify
from db import get_db_connection
from config import Config
from .summary_load import load_summary
from .distribution import load_booking_distribution

def post_load_data():
    try:
        load_summary()
        load_booking_distribution()
    
        return jsonify({"status": "Data loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500