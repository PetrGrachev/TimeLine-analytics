import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from get.get_feedback_analysis import get_feedback_analysis

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True

    @app.route('/test-feedback-analysis')
    def route():
        return get_feedback_analysis()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_feedback_analysis_missing_org_id(client):
    response = client.get('/test-feedback-analysis')
    assert response.status_code == 400
    assert response.get_json() == {"error": "org_id is required"}

@patch('get.get_feedback_analysis.get_db_connection')
def test_get_feedback_analysis_success(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        '2024-01-01', '2024-01-31',
        [{"phrase": "вежливый персонал", "score": 0.82}],
        [{"phrase": "долгое ожидание", "score": 0.45}]
    )
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-feedback-analysis?org_id=1')
    data = response.get_json()

    assert response.status_code == 200
    assert data["keywords"]["positive"][0]["phrase"] == "вежливый персонал"
    assert data["keywords"]["negative"][0]["score"] == 0.45

@patch('get.get_feedback_analysis.get_db_connection')
def test_get_feedback_analysis_no_data(mock_db_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db_conn.return_value = mock_conn

    response = client.get('/test-feedback-analysis?org_id=999')
    assert response.status_code == 404
    assert response.get_json() == {"error": "No data found for this organization"}
