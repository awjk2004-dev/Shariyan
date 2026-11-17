import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .database import Base, engine
from .routers import admin, auth, donors, messages, notifications, requests

app_env = os.getenv("APP_ENV", "development").strip().lower()
production = app_env == "production"
origins = [origin.strip().rstrip("/") for origin in os.getenv("CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500").split(",") if origin.strip()]
if "*" in origins:
    raise RuntimeError("CORS_ORIGINS must list explicit trusted origins.")
if production and (
    not origins
    or any(
        not origin.startswith("https://")
        or "localhost" in origin
        or "127.0.0.1" in origin
        for origin in origins
    )
):
    raise RuntimeError("Set CORS_ORIGINS to the deployed HTTPS frontend origin in production.")

bootstrap_token = os.getenv("ADMIN_BOOTSTRAP_TOKEN", "")
bootstrap_markers = ("change-this", "development", "dev-", "replace-with", "example", "test-")
if production and (
    len(bootstrap_token) < 32
    or any(marker in bootstrap_token.lower() for marker in bootstrap_markers)
):
    raise RuntimeError("Set ADMIN_BOOTSTRAP_TOKEN to a random value of at least 32 characters.")

app = FastAPI(
    title="Shريان API",
    version="1.1.0",
    description="API لمنصة التبرع بالدم والطلبات والإشعارات والإدارة.",
    docs_url=None if production else "/docs",
    redoc_url=None if production else "/redoc",
    openapi_url=None if production else "/openapi.json",
)
app.state.limiter = auth.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Admin-Bootstrap-Token"],
)
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(donors.router, prefix="/api/donors", tags=["donors"])
app.include_router(requests.router, prefix="/api/requests", tags=["requests"])
app.include_router(messages.router, prefix="/api/messages", tags=["messages"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


@app.get("/api/health")
def health(request: Request) -> dict[str, str]:
    return {"status": "ok"}
