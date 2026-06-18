from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    """Order item payload.

    Accepts both snake_case and camelCase field names.
    """

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
    quantity: Decimal


class OrderCreate(BaseModel):
    """Customer order creation payload.

    Accepts both snake_case and camelCase field names.
    """

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
    notes: str | None = None
    items: list[OrderItemCreate]


class OrderRead(BaseModel):
    """Order representation for admin and producer screens."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_name: str
    customer_phone: str
    customer_email: str | None
    delivery_type: str
    pickup_point: str | None
    address: str | None
    status: str
    payment_method: str
    payment_status: str
    subtotal: Decimal
    total: Decimal
    notes: str | None
