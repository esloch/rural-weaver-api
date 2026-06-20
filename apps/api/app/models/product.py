from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class Product(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "products"

    producer_id: Mapped[UUID] = mapped_column(ForeignKey("producers.id"))
    producer_name_snapshot: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(120), index=True)
    offer_type: Mapped[str] = mapped_column(String(64), default="weekly_offer")
    unit: Mapped[str] = mapped_column(String(50))

    # price is kept for backwards compatibility and represents sale price.
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    # Phase 6.2 pricing model.
    cost_price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    sale_price: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    stock_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), default=0)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_refrigerated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_frozen: Mapped[bool] = mapped_column(Boolean, default=False)
    is_addon: Mapped[bool] = mapped_column(Boolean, default=False)
    is_donation: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class BasketType(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "basket_types"

    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    base_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    average_items: Mapped[int | None] = mapped_column(nullable=True)
    average_weight_kg: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 3),
        nullable=True,
    )
    serves_people: Mapped[str | None] = mapped_column(String(120), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
