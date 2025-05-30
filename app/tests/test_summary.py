import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from get.get_summary import get_summary

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/test-summary')
    def route():
        return get_summary()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_summary_missing_org_id(client):
    response = client.get('/test-summary')
    assert response.status_code == 400
    assert response.get_json() == {"error": "org_id is required"}

@patch('get.get_summary.get_db_connection')
def test_get_summary_success(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        '2024-01-01', '2024-01-31', 100, 50000, 500,
        80, 1, 5, 10, 4.7, 11, 2.3, 20, 4.8, 21, 2.1
    )
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-summary?org_id=1')
    data = response.get_json()

    assert response.status_code == 200
    assert data['metrics']['total_bookings'] == 100
    assert data['clients']['unique_customers'] == 80
    assert data['workers']['best_worker']['worker_id'] == 10

@patch('get.get_summary.get_db_connection')
def test_get_summary_no_data(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-summary?org_id=999')
    assert response.status_code == 404
    assert response.get_json() == {"error": "No data found for this organization"}
