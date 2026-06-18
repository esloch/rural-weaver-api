from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.product import Product


class ProductRepository:
    """Persistence operations for products."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.name.asc())
        )
        return list(self.db.scalars(stmt).all())
