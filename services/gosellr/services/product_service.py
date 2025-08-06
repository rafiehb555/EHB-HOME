import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from models.product import Product, ProductCategory, ProductStatus
from sqlalchemy.orm import Session


class ProductService:
    """Service for managing products and inventory"""

    def __init__(self, db: Session):
        self.db = db

    def create_product(self, seller_id: int, product_data: Dict[str, Any]) -> Product:
        """Create a new product"""
        product = Product(
            seller_id=seller_id,
            name=product_data["name"],
            description=product_data["description"],
            category=product_data["category"],
            price=product_data["price"],
            stock_quantity=product_data.get("stock_quantity", 0),
            sku=product_data.get("sku", str(uuid.uuid4())),
            images=product_data.get("images", []),
            specifications=product_data.get("specifications", {}),
            tags=product_data.get("tags", []),
            status=ProductStatus.DRAFT,
        )

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_seller_products(
        self,
        seller_id: int,
        status: Optional[ProductStatus] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Product]:
        """Get all products for a seller"""
        query = self.db.query(Product).filter(Product.seller_id == seller_id)

        if status:
            query = query.filter(Product.status == status)

        return query.offset(offset).limit(limit).all()

    def get_products(
        self,
        category: Optional[ProductCategory] = None,
        status: Optional[ProductStatus] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Product]:
        """Get products with filters"""
        query = self.db.query(Product)

        if category:
            query = query.filter(Product.category == category)
        if status:
            query = query.filter(Product.status == status)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        return query.offset(offset).limit(limit).all()

    def update_product(
        self, product_id: int, update_data: Dict[str, Any]
    ) -> Optional[Product]:
        """Update product information"""
        product = self.get_product(product_id)
        if not product:
            return None

        # Update fields
        for field, value in update_data.items():
            if hasattr(product, field) and value is not None:
                setattr(product, field, value)

        product.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(product)
        return product

    def publish_product(self, product_id: int) -> Dict[str, Any]:
        """Publish a product"""
        product = self.get_product(product_id)
        if not product:
            return {"error": "Product not found"}

        try:
            # Validate product before publishing
            if not self._validate_product_for_publishing(product):
                return {
                    "error": "Product validation failed. Please complete all required fields."
                }

            product.status = ProductStatus.ACTIVE
            product.published_at = datetime.utcnow()
            product.updated_at = datetime.utcnow()

            self.db.commit()

            return {
                "success": True,
                "product_id": product.id,
                "status": "published",
                "published_at": product.published_at.isoformat(),
            }

        except Exception as e:
            return {"error": f"Publishing failed: {str(e)}"}

    def _validate_product_for_publishing(self, product: Product) -> bool:
        """Validate product before publishing"""
        required_fields = ["name", "description", "category", "price", "seller_id"]

        for field in required_fields:
            if not getattr(product, field):
                return False

        return True

    def update_stock(self, product_id: int, quantity_change: int) -> Dict[str, Any]:
        """Update product stock quantity"""
        product = self.get_product(product_id)
        if not product:
            return {"error": "Product not found"}

        try:
            new_quantity = product.stock_quantity + quantity_change
            if new_quantity < 0:
                return {"error": "Stock cannot be negative"}

            product.stock_quantity = new_quantity
            product.updated_at = datetime.utcnow()

            # Update status based on stock
            if new_quantity == 0:
                product.status = ProductStatus.OUT_OF_STOCK
            elif product.status == ProductStatus.OUT_OF_STOCK and new_quantity > 0:
                product.status = ProductStatus.ACTIVE

            self.db.commit()

            return {
                "success": True,
                "product_id": product.id,
                "new_stock": new_quantity,
                "status": product.status.value,
            }

        except Exception as e:
            return {"error": f"Stock update failed: {str(e)}"}

    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        product = self.get_product(product_id)
        if not product:
            return False

        self.db.delete(product)
        self.db.commit()
        return True

    def get_product_statistics(self, seller_id: Optional[int] = None) -> Dict[str, Any]:
        """Get product statistics"""
        query = self.db.query(Product)

        if seller_id:
            query = query.filter(Product.seller_id == seller_id)

        total_products = query.count()
        active_products = query.filter(Product.status == ProductStatus.ACTIVE).count()
        draft_products = query.filter(Product.status == ProductStatus.DRAFT).count()
        out_of_stock_products = query.filter(
            Product.status == ProductStatus.OUT_OF_STOCK
        ).count()

        return {
            "total": total_products,
            "active": active_products,
            "draft": draft_products,
            "out_of_stock": out_of_stock_products,
        }

    def search_products(self, search_term: str, limit: int = 20) -> List[Product]:
        """Search products by name or description"""
        return (
            self.db.query(Product)
            .filter(
                Product.name.ilike(f"%{search_term}%")
                | Product.description.ilike(f"%{search_term}%")
            )
            .limit(limit)
            .all()
        )

    def archive_product(self, product_id: int) -> Dict[str, Any]:
        """Archive a product"""
        product = self.get_product(product_id)
        if not product:
            return {"error": "Product not found"}

        try:
            product.status = ProductStatus.ARCHIVED
            product.updated_at = datetime.utcnow()

            self.db.commit()

            return {"success": True, "product_id": product.id, "status": "archived"}

        except Exception as e:
            return {"error": f"Archiving failed: {str(e)}"}
