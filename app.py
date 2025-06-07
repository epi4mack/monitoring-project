from flask import Flask
import logging
from prometheus_client import generate_latest, Counter, Histogram # Импорт необходимых классов
from flask import Response # Для ответа на /metrics

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

requests_total = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
request_duration_seconds = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'endpoint'])


@app.route('/')
def home():
    logger.info('Received request on home page')
    requests_total.labels(method='GET', endpoint='/').inc() # Увеличиваем счетчик
    return 'Hello, Monitoring!'


@app.route('/metrics')
def metrics():
    # Экспорт метрик в формате Prometheus
    return Response(generate_latest(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
