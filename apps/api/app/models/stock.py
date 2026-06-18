from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class StockMovement(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "stock_movements"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    type: Mapped[str] = mapped_column(String(64))
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
