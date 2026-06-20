from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.api.app.models.base import Base, TimestampMixin, UUIDMixin


class CampaignFinancialAdjustment(UUIDMixin, TimestampMixin, Base):
    """Manual financial adjustment linked to a campaign.

    Examples:
    - payment_fee
    - delivery_cost
    - admin_share
    - donation_cost
    - extra_item
    - manual_discount
    - other
    """

    __tablename__ = "campaign_financial_adjustments"

    campaign_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_campaigns.id"),
        index=True,
    )
    adjustment_type: Mapped[str] = mapped_column(String(64), index=True)
    description: Mapped[str] = mapped_column(String(255))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
