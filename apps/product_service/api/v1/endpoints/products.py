"""
Product endpoints.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from apps.product_service.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from apps.product_service.services.product_service import ProductService
from core.exceptions import NotFoundError

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    # user_id: int = Depends(get_current_user_id)  # Add if auth is needed
):
    """Create a new product."""
    product = ProductService.create_product(db, product_data)
    return product


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all products with optional filters."""
    products = ProductService.get_products(
        db, skip=skip, limit=limit, category=category, is_active=is_active
    )
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get product by ID."""
    product = ProductService.get_product(db, product_id)
    if not product:
        raise NotFoundError("Product", str(product_id))
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
    # current_user = Depends(get_current_user)  # Add if auth is needed
):
    """Update product information."""
    product = ProductService.update_product(db, product_id, product_data)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
    # current_user = Depends(get_admin_user)  # Add if auth is needed
):
    """Delete a product."""
    ProductService.delete_product(db, product_id)
    return None
