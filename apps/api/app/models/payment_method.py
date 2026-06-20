from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class PaymentMethod(UUIDMixin, TimestampMixin, Base):
    """Payment method offered to customers.

    Phase 6.2 includes financial fees used by campaign settlement.
    """

    __tablename__ = "payment_methods"

    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    requires_extra_data: Mapped[bool] = mapped_column(Boolean, default=False)
    fee_fixed: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    fee_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(7, 4),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
