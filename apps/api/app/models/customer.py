from uuid import UUID

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class Customer(UUIDMixin, TimestampMixin, Base):
    """Customer profile created from order or subscription data."""

    __tablename__ = "customers"

    full_name: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[str] = mapped_column(String(64), index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(32), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    neighborhood: Mapped[str | None] = mapped_column(String(120), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Phase 7.2.3 customer identity foundation.
    tenant_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    customer_number: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        unique=True,
        index=True,
    )
    first_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cpf_normalized: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        index=True,
    )
    phone_country_code: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True,
    )
    phone_area_code: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True,
    )
    phone_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    phone_e164: Mapped[str | None] = mapped_column(String(32), nullable=True)
