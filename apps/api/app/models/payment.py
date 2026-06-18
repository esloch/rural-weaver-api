from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class PaymentSetting(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "payment_settings"

    provider: Mapped[str] = mapped_column(String(64), default="pix_manual")
    pix_key: Mapped[str] = mapped_column(String(255))
    pix_key_type: Mapped[str] = mapped_column(String(64))
    recipient_name: Mapped[str] = mapped_column(String(255))
    recipient_document: Mapped[str] = mapped_column(String(64))
    bank_name: Mapped[str] = mapped_column(String(255))
    payment_instructions: Mapped[str] = mapped_column(Text)
    pix_copy_paste_hash: Mapped[str] = mapped_column(Text)
    qr_code_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
