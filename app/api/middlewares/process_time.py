import time

from typing import (
    Callable,
    Awaitable,
)

from fastapi import (
    Request,
    Response,
)


async def add_process_time_to_request(
        request: Request,
        call_next: Callable[
            [Request],
            Awaitable[Response],
        ],
) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.5f}"
    return response