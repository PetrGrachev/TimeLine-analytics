import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from get.get_workers_workload import get_workers_workload

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/test-workload')
    def route():
        return get_workers_workload()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_workers_workload_missing_org_id(client):
    response = client.get('/test-workload')
    assert response.status_code == 400
    assert response.get_json() == {"error": "org_id is required"}

@patch('get.get_workers_workload.get_db_connection')
def test_get_workers_workload_success(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ('2024-01-01', '2024-01-31', 101, 15, 20, 75.0),
        ('2024-01-01', '2024-01-31', 102, 10, 20, 50.0),
        ('2024-01-01', '2024-01-31', 103, 18, 20, 90.0),
    ]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-workload?org_id=1')
    data = response.get_json()

    assert response.status_code == 200
    assert data["period_start"] == '2024-01-01'
    assert data["period_end"] == '2024-01-31'
    assert len(data["workers"]) == 3
    assert data["workers"][0]["worker_id"] == 101
    assert data["workers"][1]["workload_percentage"] == 50.0

@patch('get.get_workers_workload.get_db_connection')
def test_get_workers_workload_no_data(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-workload?org_id=2')
    assert response.status_code == 404
    assert response.get_json() == {"error": "No data found for this organization"}
