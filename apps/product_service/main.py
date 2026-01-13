"""
Main FastAPI application for product service.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logger import logger
from apps.product_service.api.v1.api import api_router
from apps.product_service.db.base import Base
from core.database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Product Service",
    version=settings.PROJECT_VERSION,
    description="Product management microservice"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Product service starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Product service shutting down...")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "product_service"}


if __name__ == "__main__":
    import uvicorn
    from apps.product_service.core.config import product_settings
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=product_settings.SERVICE_PORT,
        reload=True
    )
