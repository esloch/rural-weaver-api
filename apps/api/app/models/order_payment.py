from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class OrderPaymentDetail(UUIDMixin, TimestampMixin, Base):
    """Additional billing/payment details required by selected method."""

    __tablename__ = "order_payment_details"

    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"), index=True)
    method_code: Mapped[str] = mapped_column(String(64))
    cpf: Mapped[str | None] = mapped_column(String(32), nullable=True)
    billing_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    billing_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    billing_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    billing_phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payment_link: Mapped[str | None] = mapped_column(Text, nullable=True)
    proof_received: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class PaymentConfirmation(UUIDMixin, TimestampMixin, Base):
    """Manual payment confirmation log."""

    __tablename__ = "payment_confirmations"

    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"), index=True)
    method_code: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), default="pending")
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    confirmed_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
