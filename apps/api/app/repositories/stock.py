from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.product import Product
from apps.api.app.models.stock import StockMovement
from apps.api.app.schemas.inventory import AdminInventoryRead


class StockRepository:
    """Inventory and stock movement operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_movements(self) -> list[StockMovement]:
        stmt = select(StockMovement).order_by(StockMovement.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get_inventory(self) -> AdminInventoryRead:
        products = list(
            self.db.scalars(select(Product).order_by(Product.name.asc())).all(),
        )
        movements = self.list_movements()[:50]
        return AdminInventoryRead(products=products, movements=movements)

    def adjust_stock(
        self,
        product_id: UUID,
        quantity_delta: Decimal,
        reason: str | None,
        movement_type: str,
        created_by: UUID | None,
    ) -> Product:
        product = self.db.get(Product, product_id)
        if product is None:
            raise ValueError("Product not found.")

        new_quantity = product.stock_quantity + quantity_delta
        if new_quantity < 0:
            raise ValueError("Stock cannot become negative.")

        product.stock_quantity = new_quantity

        movement = StockMovement(
            product_id=product.id,
            type=movement_type,
            quantity=quantity_delta,
            reason=reason,
            created_by=created_by,
        )
        self.db.add(movement)
        self.db.flush()
        return product
