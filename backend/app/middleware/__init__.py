from fastapi import FastAPI

from app.middleware.logging import RequestLoggingMiddleware

def register_middleware(app: FastAPI):
    app.add_middleware(RequestLoggingMiddleware)