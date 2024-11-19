from fastapi import FastAPI, Request
from opentelemetry import trace
from .observability.tracing import setup_tracing, instrument_app

tracer_provider = setup_tracing("learn-python-service", "http://localhost:4318/v1/traces")

app = FastAPI()
instrument_app(app, tracer_provider)

# Get tracer for this module
tracer = trace.get_tracer(__name__)

@app.get("/")
async def index():
    return {"message": "Hello, World!"}
