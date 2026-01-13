"""
API v1 router aggregation.
"""
from fastapi import APIRouter
from apps.product_service.api.v1.endpoints import products

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
