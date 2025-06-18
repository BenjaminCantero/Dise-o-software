from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-API-Version"] = "1.0"
        return response