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
