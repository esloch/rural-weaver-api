from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class CampaignProductRead(BaseModel):
    """Campaign-specific product availability and price."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    campaign_id: UUID
    product_id: UUID
    name_snapshot: str
    unit_snapshot: str
    producer_name_snapshot: str | None
    offer_type: str
    display_order: int
    price: Decimal
    cost_price_snapshot: Decimal | None
    sale_price_snapshot: Decimal | None
    margin_unit_snapshot: Decimal | None
    available_quantity: Decimal
    reserved_quantity: Decimal
    min_quantity: Decimal
    max_quantity: Decimal | None
    requires_confirmation: bool
    is_active: bool


class CampaignProductCreate(BaseModel):
    """Payload for adding a product to a campaign."""

    product_id: UUID = Field(
        validation_alias=AliasChoices("product_id", "productId"),
    )
    price: Decimal
    available_quantity: Decimal = Field(
        validation_alias=AliasChoices("available_quantity", "availableQuantity"),
    )
    reserved_quantity: Decimal = Field(
        default=Decimal("0"),
        validation_alias=AliasChoices("reserved_quantity", "reservedQuantity"),
    )
    producer_name_snapshot: str | None = Field(
        default=None,
        validation_alias=AliasChoices("producer_name_snapshot", "producerNameSnapshot"),
    )
    offer_type: str = Field(
        default="weekly_offer",
        validation_alias=AliasChoices("offer_type", "offerType"),
    )
    display_order: int = Field(
        default=0,
        validation_alias=AliasChoices("display_order", "displayOrder"),
    )
    cost_price_snapshot: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("cost_price_snapshot", "costPriceSnapshot"),
    )
    sale_price_snapshot: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("sale_price_snapshot", "salePriceSnapshot"),
    )
    min_quantity: Decimal = Field(
        default=Decimal("0"),
        validation_alias=AliasChoices("min_quantity", "minQuantity"),
    )
    max_quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("max_quantity", "maxQuantity"),
    )
    requires_confirmation: bool = Field(
        default=False,
        validation_alias=AliasChoices("requires_confirmation", "requiresConfirmation"),
    )
    is_active: bool = Field(
        default=True,
        validation_alias=AliasChoices("is_active", "isActive"),
    )


class CampaignProductUpdate(BaseModel):
    """Campaign product update payload."""

    price: Decimal | None = None
    available_quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("available_quantity", "availableQuantity"),
    )
    reserved_quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("reserved_quantity", "reservedQuantity"),
    )
    producer_name_snapshot: str | None = Field(
        default=None,
        validation_alias=AliasChoices("producer_name_snapshot", "producerNameSnapshot"),
    )
    offer_type: str | None = Field(
        default=None,
        validation_alias=AliasChoices("offer_type", "offerType"),
    )
    display_order: int | None = Field(
        default=None,
        validation_alias=AliasChoices("display_order", "displayOrder"),
    )
    cost_price_snapshot: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("cost_price_snapshot", "costPriceSnapshot"),
    )
    sale_price_snapshot: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("sale_price_snapshot", "salePriceSnapshot"),
    )
    min_quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("min_quantity", "minQuantity"),
    )
    max_quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("max_quantity", "maxQuantity"),
    )
    requires_confirmation: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("requires_confirmation", "requiresConfirmation"),
    )
    is_active: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("is_active", "isActive"),
    )


class CampaignRuleRead(BaseModel):
    """Operational rules applied to a weekly campaign."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    campaign_id: UUID
    order_days: list[str]
    order_close_time: time | None
    minimum_order_value: Decimal
    minimum_order_exceptions: str | None
    process_by_order_time: bool
    confirmation_required: bool
    proof_required: bool
    instructions: str | None


class SalesCampaignRead(BaseModel):
    """Weekly campaign representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    delivery_date: date
    order_open_at: datetime | None
    order_close_at: datetime | None
    status: str


class SalesCampaignDetailRead(SalesCampaignRead):
    """Campaign plus offer products and operational rules."""

    products: list[CampaignProductRead]
    rule: CampaignRuleRead | None = None


class SalesCampaignCreate(BaseModel):
    """Payload for creating a weekly campaign."""

    name: str
    description: str | None = None
    delivery_date: date = Field(
        validation_alias=AliasChoices("delivery_date", "deliveryDate"),
    )
    order_open_at: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices("order_open_at", "orderOpenAt"),
    )
    order_close_at: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices("order_close_at", "orderCloseAt"),
    )
    status: str = "draft"


class SalesCampaignUpdate(BaseModel):
    """Payload for updating a weekly campaign."""

    name: str | None = None
    description: str | None = None
    delivery_date: date | None = Field(
        default=None,
        validation_alias=AliasChoices("delivery_date", "deliveryDate"),
    )
    order_open_at: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices("order_open_at", "orderOpenAt"),
    )
    order_close_at: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices("order_close_at", "orderCloseAt"),
    )
    status: str | None = None
