"""
Single FastAPI application that combines auth and product services.
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logger import logger
from core.database import engine

from apps.auth_service.api.v1.api import api_router as auth_api_router
from apps.product_service.api.v1.api import api_router as product_api_router

from apps.auth_service.db.base import Base as AuthBase
from apps.product_service.db.base import Base as ProductBase

# Import all models to ensure they're registered with their bases
from apps.auth_service.db.models.user import User  # noqa
from apps.product_service.db.models.product import Product  # noqa

# Note: We don't create tables here anymore - use migrations instead
# Base.metadata.create_all(bind=engine)  # Disabled - use 'python manage.py migrate'


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Monolithic FastAPI application combining auth and product features.",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers under a single API prefix
app.include_router(auth_api_router, prefix=settings.API_V1_PREFIX)
app.include_router(product_api_router, prefix=settings.API_V1_PREFIX)


from scripts.check_migrations import check_migrations_on_startup


@app.on_event("startup")
async def startup_event():
    logger.info("Unified application starting up...")
    # Check for pending migrations (warning only, doesn't stop startup)
    check_migrations_on_startup(strict=False)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Unified application shutting down...")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "monolith"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "apps.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

