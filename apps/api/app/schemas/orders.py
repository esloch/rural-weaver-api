from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    """Order item payload."""

    item_type: str = Field(
        validation_alias=AliasChoices("item_type", "itemType"),
    )
    product_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("product_id", "productId"),
    )
    basket_type_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("basket_type_id", "basketTypeId"),
    )
    campaign_product_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("campaign_product_id", "campaignProductId"),
    )
    quantity: Decimal


class OrderCreate(BaseModel):
    """Customer order creation payload."""

    campaign_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("campaign_id", "campaignId"),
    )
    customer_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("customer_id", "customerId"),
    )
    pickup_point_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("pickup_point_id", "pickupPointId"),
    )
    delivery_zone_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("delivery_zone_id", "deliveryZoneId"),
    )
    payment_method_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("payment_method_id", "paymentMethodId"),
    )
    customer_name: str = Field(
        validation_alias=AliasChoices("customer_name", "customerName"),
    )
    customer_phone: str = Field(
        validation_alias=AliasChoices("customer_phone", "customerPhone"),
    )
    customer_email: str | None = Field(
        default=None,
        validation_alias=AliasChoices("customer_email", "customerEmail"),
    )
    delivery_type: str = Field(
        validation_alias=AliasChoices("delivery_type", "deliveryType"),
    )
    pickup_point: str | None = Field(
        default=None,
        validation_alias=AliasChoices("pickup_point", "pickupPoint"),
    )
    address: str | None = None
    neighborhood: str | None = None
    city: str | None = None
    complement: str | None = None
    delivery_agent: str | None = Field(
        default=None,
        validation_alias=AliasChoices("delivery_agent", "deliveryAgent"),
    )
    payment_method: str | None = Field(
        default=None,
        validation_alias=AliasChoices("payment_method", "paymentMethod"),
    )
    delivery_fee: Decimal = Field(
        default=Decimal("0"),
        validation_alias=AliasChoices("delivery_fee", "deliveryFee"),
    )
    notes: str | None = None
    items: list[OrderItemCreate]


class OrderRead(BaseModel):
    """Order representation with pricing and operational fields."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    campaign_id: UUID | None
    customer_id: UUID | None
    pickup_point_id: UUID | None
    delivery_zone_id: UUID | None
    payment_method_id: UUID | None
    source: str
    confirmation_status: str
    submitted_at: datetime | None
    confirmed_at: datetime | None
    customer_name: str
    customer_phone: str
    customer_email: str | None
    delivery_type: str
    pickup_point: str | None
    address: str | None
    neighborhood: str | None
    city: str | None
    complement: str | None
    delivery_agent: str | None
    status: str
    payment_method: str
    payment_status: str
    subtotal: Decimal
    delivery_fee: Decimal
    payment_fee_amount: Decimal | None
    net_total_after_fees: Decimal | None
    total: Decimal
    notes: str | None
    created_at: datetime
    updated_at: datetime
