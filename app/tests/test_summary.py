import pytest
from flask import Flask
from get.get_summary import get_summary

# Определяем фиктивные классы для имитации подключения к БД
class DummyCursor:
    def execute(self, query, params):
        self.params = params
    def fetchone(self):
        # Пример данных: period_start, period_end, total_bookings, total_revenue,
        # avg_booking_cost, unique_customers, popular_service_id, most_frequent_client_id,
        # best_worker_id, best_worker_rating, worst_worker_id, worst_worker_rating,
        # best_service_id, best_service_rating, worst_service_id, worst_service_rating
        return ("2025-01-01", "2025-01-31", 10, 1000.0, 100.0, 5, 1, 2, 3, 4.5, 6, 1.2, 7, 4.8, 8, 2.0)
    def close(self):
        pass

class DummyConnection:
    def cursor(self):
        return DummyCursor()
    def close(self):
        pass

def dummy_get_db_connection(config):
    return DummyConnection()

# Фикстура для создания тестового приложения
@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    # Регистрируем тестовый маршрут, привязанный к функции get_aggregated_data
    app.add_url_rule('/analytics/summary', view_func=get_summary, methods=['GET'])
    return app

@pytest.fixture
def client(app):
    return app.test_client()

#########################
# Тесты для get_aggregated_data
#########################

def test_get_aggregated_data_no_org_id(client):
    """Если параметр org_id не передан, функция должна вернуть ошибку 400."""
    response = client.get('/analytics/summary')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "org_id is required"

def test_get_aggregated_data_no_data(monkeypatch, client):
    """Если функция fetchone возвращает None, должна вернуться ошибка 404."""
    class DummyCursorNoData:
        def execute(self, query, params):
            pass
        def fetchone(self):
            return None
        def close(self):
            pass

    class DummyConnectionNoData:
        def cursor(self):
            return DummyCursorNoData()
        def close(self):
            pass

    monkeypatch.setattr("summary.summary.get_db_connection", lambda config: DummyConnectionNoData())
    response = client.get('/analytics/summary?org_id=1')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No data found for this organization"

def test_get_aggregated_data_success(monkeypatch, client):
    """При валидном org_id функция должна вернуть корректный JSON-ответ."""
    monkeypatch.setattr("summary.summary.get_db_connection", dummy_get_db_connection)
    response = client.get('/analytics/summary?org_id=1')
    assert response.status_code == 200
    data = response.get_json()
    # Проверяем наличие ключей
    assert "period_start" in data
    assert "period_end" in data
    assert "metrics" in data
    assert "workers" in data
    assert "services" in data
    # Пример: проверим, что значение total_bookings равно 10
    assert data["metrics"]["total_bookings"] == 10
