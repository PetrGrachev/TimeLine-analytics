import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from get.get_cancellations import get_cancellations

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/test-cancellations')
    def route():
        return get_cancellations()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_cancellations_missing_org_id(client):
    response = client.get('/test-cancellations')
    assert response.status_code == 400
    assert response.get_json() == {"error": "org_id is required"}

@patch('get.get_cancellations.get_db_connection')
def test_get_cancellations_success(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        '2024-01-01', '2024-01-31', 12, 24.5, "Поздняя отмена"
    )
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-cancellations?org_id=1')
    data = response.get_json()

    assert response.status_code == 200
    assert data["info"]["canceled_records"] == 12
    assert data["info"]["cancellation_percentage"] == 24.5
    assert data["info"]["most_common_cancel_reason"] == "Поздняя отмена"

@patch('get.get_cancellations.get_db_connection')
def test_get_cancellations_no_data(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-cancellations?org_id=123')
    assert response.status_code == 404
    assert response.get_json() == {"error": "No data found for this organization"}
