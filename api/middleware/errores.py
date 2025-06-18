from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            # Aquí puedes loguear el error si quieres
            return JSONResponse(
                status_code=500,
                content={"detail": "Error interno del servidor."}
            )