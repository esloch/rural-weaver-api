from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class SubscriptionPlan(UUIDMixin, TimestampMixin, Base):
    """CSA subscription plan offered by Delícias da Roça."""

    __tablename__ = "subscription_plans"

    basket_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("basket_types.id"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    frequency: Mapped[str] = mapped_column(String(32))
    deliveries_per_month: Mapped[int] = mapped_column(default=1)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    average_items: Mapped[int | None] = mapped_column(nullable=True)
    average_weight_kg: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 3),
        nullable=True,
    )
    serves_people: Mapped[str | None] = mapped_column(String(120), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Subscription(UUIDMixin, TimestampMixin, Base):
    """A customer's active, paused or cancelled CSA subscription."""

    __tablename__ = "subscriptions"

    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customers.id"))
    subscription_plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("subscription_plans.id"),
    )
    status: Mapped[str] = mapped_column(String(32), default="active")
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    preferred_pickup_point_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("pickup_points.id"),
        nullable=True,
    )
    delivery_zone_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("delivery_zones.id"),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
