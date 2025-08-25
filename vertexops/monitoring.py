from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

REQUEST_COUNT = Counter("vertexops_requests_total", "Total API requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("vertexops_request_latency_seconds", "Request latency", ["endpoint"])

def record_request(method: str, endpoint: str, status: str, latency: float):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

def metrics_response():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
