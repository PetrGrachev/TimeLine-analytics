import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from get.get_booking_distribution import get_booking_distribution

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/test-booking-distribution')
    def route():
        return get_booking_distribution()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_booking_distribution_missing_org_id(client):
    response = client.get('/test-booking-distribution')
    assert response.status_code == 400
    assert response.get_json() == {"error": "org_id is required"}

@patch('get.get_booking_distribution.get_db_connection')
def test_get_booking_distribution_success(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, 10, 5),
        (1, 11, 3),
        (2, 9, 2)
    ]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-booking-distribution?org_id=1')
    assert response.status_code == 200
    data = response.get_json()

    expected = {
        "distribution": [
            {
                "day_of_week": 1,
                "hours": [
                    {"hour": 10, "bookings": 5},
                    {"hour": 11, "bookings": 3}
                ]
            },
            {
                "day_of_week": 2,
                "hours": [
                    {"hour": 9, "bookings": 2}
                ]
            }
        ]
    }

    assert data == expected

@patch('get.get_booking_distribution.get_db_connection')
def test_get_booking_distribution_no_data(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-booking-distribution?org_id=1')
    assert response.status_code == 200
    assert response.get_json() == {"distribution": []}
