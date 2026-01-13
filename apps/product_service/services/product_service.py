"""
Product service business logic.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from typing import List, Optional
from apps.product_service.db.models.product import Product
from apps.product_service.schemas.product import ProductCreate, ProductUpdate
from core.exceptions import NotFoundError


class ProductService:
    """Service for product operations."""
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate, user_id: Optional[int] = None) -> Product:
        """Create a new product."""
        db_product = Product(
            **product_data.model_dump(),
            created_by=user_id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Product]:
        """Get products with optional filters."""
        query = db.query(Product)
        
        if category:
            query = query.filter(Product.category == category)
        
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
        """Update product information."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundError("Product", str(product_id))
        
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Delete a product."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise NotFoundError("Product", str(product_id))
        
        db.delete(product)
        db.commit()
        return True
