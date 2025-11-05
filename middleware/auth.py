from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

SECRET = "your-secret"
ALGS = ["HS256"]  # match your issuer

def validate_jwt(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=ALGS)  # add audience/issuer checks if needed

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("authorization", "")
        token = auth.replace("Bearer ", "") if auth.startswith("Bearer ") else None
        request.state.claims = None
        if token:
            try:
                request.state.claims = validate_jwt(token)
            except:
                # leave claims=None; dependency will reject
                pass
        return await call_next(request)
