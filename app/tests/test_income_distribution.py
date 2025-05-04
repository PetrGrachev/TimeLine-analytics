import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from get.get_income_distribution import get_income_distribution  # поправь путь, если отличается

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/test-income')
    def route():
        return get_income_distribution()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_income_distribution_missing_org_id(client):
    response = client.get('/test-income')
    assert response.status_code == 400
    assert response.get_json() == {"error": "org_id is required"}

@patch('get.get_income_distribution.get_db_connection')  # поправь путь к функции
def test_get_income_distribution_success(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, 3000, 4),
        (2, 4500, 6),
    ]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-income?org_id=1')
    data = response.get_json()

    assert response.status_code == 200
    assert "distribution" in data
    assert data["distribution"][0]["day_of_week"] == 1
    assert data["distribution"][0]["info"][0]["income"] == 3000
    assert data["distribution"][0]["info"][0]["bookings"] == 4
    assert data["distribution"][1]["day_of_week"] == 2

@patch('get.get_income_distribution.get_db_connection')
def test_get_income_distribution_no_data(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-income?org_id=1')
    data = response.get_json()

    assert response.status_code == 200
    assert data["distribution"] == []
