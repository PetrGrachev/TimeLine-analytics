from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, request
import time

# Счетчики запросов и ошибок
REQUEST_COUNT = Counter(
    'app_request_count', 'Количество HTTP-запросов',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 'Время отклика в секундах',
    ['endpoint']
)

# Middleware для сбора метрик
def before_request():
    request.start_time = time.time()

def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

# Ручка /metrics
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
