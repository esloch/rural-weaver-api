from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text, Time
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class SalesCampaign(UUIDMixin, TimestampMixin, Base):
    """Weekly order campaign replacing a Google Form cycle."""

    __tablename__ = "sales_campaigns"

    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_date: Mapped[date] = mapped_column(Date, index=True)
    order_open_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    order_close_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)


class CampaignProduct(UUIDMixin, TimestampMixin, Base):
    """Product availability and campaign-specific pricing."""

    __tablename__ = "campaign_products"

    campaign_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_campaigns.id"),
        index=True,
    )
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    name_snapshot: Mapped[str] = mapped_column(String(255))
    unit_snapshot: Mapped[str] = mapped_column(String(50))
    producer_name_snapshot: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    offer_type: Mapped[str] = mapped_column(String(64), default="weekly_offer")
    display_order: Mapped[int] = mapped_column(default=0)

    # price is kept for backwards compatibility and represents sale price.
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    # Phase 6.2 spreadsheet pricing model.
    cost_price_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    sale_price_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    margin_unit_snapshot: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    available_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    reserved_quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        default=0,
    )
    min_quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), default=0)
    max_quantity: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 3),
        nullable=True,
    )
    requires_confirmation: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PickupPoint(UUIDMixin, TimestampMixin, Base):
    """Configurable pickup point for campaign orders."""

    __tablename__ = "pickup_points"

    name: Mapped[str] = mapped_column(String(255), index=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    neighborhood: Mapped[str | None] = mapped_column(String(120), nullable=True)
    weekday_availability: Mapped[str | None] = mapped_column(String(255), nullable=True)
    time_window: Mapped[str | None] = mapped_column(String(120), nullable=True)
    has_refrigeration: Mapped[bool] = mapped_column(Boolean, default=False)
    is_condo_only: Mapped[bool] = mapped_column(Boolean, default=False)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class DeliveryZone(UUIDMixin, TimestampMixin, Base):
    """Configurable delivery zone and fee."""

    __tablename__ = "delivery_zones"

    name: Mapped[str] = mapped_column(String(255), index=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    area: Mapped[str | None] = mapped_column(String(120), nullable=True)
    fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    estimated_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    restrictions: Mapped[str | None] = mapped_column(Text, nullable=True)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_supported: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class CampaignRule(UUIDMixin, TimestampMixin, Base):
    """Operational rules applied to a campaign/order window."""

    __tablename__ = "campaign_rules"

    campaign_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_campaigns.id"),
        index=True,
    )
    order_days: Mapped[list[str]] = mapped_column(
        ARRAY(String(16)),
        default=list,
    )
    order_close_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    minimum_order_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    minimum_order_exceptions: Mapped[str | None] = mapped_column(Text, nullable=True)
    process_by_order_time: Mapped[bool] = mapped_column(Boolean, default=True)
    confirmation_required: Mapped[bool] = mapped_column(Boolean, default=True)
    proof_required: Mapped[bool] = mapped_column(Boolean, default=True)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
