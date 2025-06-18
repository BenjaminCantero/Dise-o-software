from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token != "Bearer secrettoken":
            return JSONResponse(status_code=401, content={"detail": "No autorizado"})
        return await call_next(request)