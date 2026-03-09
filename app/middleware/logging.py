import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.db import crud
from fastapi import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        response_time_ms = (time.time() - start) * 1000
        prediction_id = getattr(request.state, "prediction_id", None)
        db = request.app.state.SessionLocal()
        try:
            crud.log_request(
                db=db,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                response_time_ms=round(response_time_ms, 2),
                prediction_id=prediction_id,
            )
        finally:
            db.close()
        return response
