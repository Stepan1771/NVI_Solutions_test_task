from fastapi import FastAPI

from .process_time import add_process_time_to_request


def register_middleware(app: FastAPI) -> None:
    app.middleware("http")(add_process_time_to_request)