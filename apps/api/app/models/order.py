from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class Order(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "orders"

    campaign_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_campaigns.id"),
        nullable=True,
        index=True,
    )
    customer_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
        index=True,
    )
    pickup_point_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("pickup_points.id"),
        nullable=True,
    )
    delivery_zone_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("delivery_zones.id"),
        nullable=True,
    )
    payment_method_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("payment_methods.id"),
        nullable=True,
    )
    source: Mapped[str] = mapped_column(String(64), default="web")
    confirmation_status: Mapped[str] = mapped_column(
        String(32),
        default="pending",
    )
    order_number: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        unique=True,
        index=True,
    )
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_phone: Mapped[str] = mapped_column(String(64))
    customer_email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    delivery_type: Mapped[str] = mapped_column(String(32))
    pickup_point: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Phase 6.2 delivery/admin details from spreadsheets.
    neighborhood: Mapped[str | None] = mapped_column(String(120), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    country: Mapped[str | None] = mapped_column(String(120), nullable=True)
    complement: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_agent: Mapped[str | None] = mapped_column(String(120), nullable=True)

    status: Mapped[str] = mapped_column(String(32), default="submitted")
    payment_method: Mapped[str] = mapped_column(
        String(32),
        default="pix_manual",
    )
    payment_status: Mapped[str] = mapped_column(String(32), default="pending")
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    delivery_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    # Phase 6.2 financial reconciliation details.
    payment_fee_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    net_total_after_fees: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

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
    campaign_product_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("campaign_products.id"),
        nullable=True,
    )
    item_type: Mapped[str] = mapped_column(String(32))
    offer_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    name_snapshot: Mapped[str] = mapped_column(String(255))
    producer_name_snapshot: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Existing sale price snapshot kept for backwards compatibility.
    unit_price_snapshot: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    # Phase 6.2 cost/sale/margin snapshots.
    unit_cost_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    unit_sale_price_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    cost_total_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    sale_total_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    margin_total_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    total_snapshot: Mapped[Decimal] = mapped_column(Numeric(12, 2))
