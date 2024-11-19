from fastapi import FastAPI, Request
from opentelemetry import trace
from .observability.tracing import setup_tracing, instrument_app

tracer_provider = setup_tracing("learn-python-service", "http://localhost:4318/v1/traces")

app = FastAPI()
instrument_app(app, tracer_provider)

# Get tracer for this module
tracer = trace.get_tracer(__name__)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    with tracer.start_as_current_span("process_request"):
        response = await call_next(request)
    return response

@app.get("/")
async def index():
    with tracer.start_as_current_span("index"):
        return {"message": "Hello, World!"}

