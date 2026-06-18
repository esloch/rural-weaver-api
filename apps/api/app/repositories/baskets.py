from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.product import BasketType


class BasketRepository:
    """Persistence operations for basket types."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[BasketType]:
        stmt = (
            select(BasketType)
            .where(BasketType.is_active.is_(True))
            .order_by(BasketType.base_price.asc())
        )
        return list(self.db.scalars(stmt).all())
