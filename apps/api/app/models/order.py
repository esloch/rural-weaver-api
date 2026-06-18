from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class Order(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "orders"

    customer_name: Mapped[str] = mapped_column(String(255))
    customer_phone: Mapped[str] = mapped_column(String(64))
    customer_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    delivery_type: Mapped[str] = mapped_column(String(32))
    pickup_point: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="submitted")
    payment_method: Mapped[str] = mapped_column(
        String(32),
        default="pix_manual",
    )
    payment_status: Mapped[str] = mapped_column(String(32), default="pending")
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class OrderItem(UUIDMixin, Base):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("products.id"),
        nullable=True,
    )
    basket_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("basket_types.id"),
        nullable=True,
    )
    item_type: Mapped[str] = mapped_column(String(32))
    name_snapshot: Mapped[str] = mapped_column(String(255))
    unit_price_snapshot: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    total_snapshot: Mapped[Decimal] = mapped_column(Numeric(12, 2))
