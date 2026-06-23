from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ProductRead(BaseModel):
    """Public product representation with pricing metadata."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    producer_id: UUID
    producer_name_snapshot: str | None
    name: str
    description: str | None
    category: str
    offer_type: str
    unit: str
    price: Decimal
    cost_price: Decimal | None
    sale_price: Decimal | None
    stock_quantity: Decimal
    image_url: str | None
    is_refrigerated: bool
    is_frozen: bool
    is_addon: bool
    is_donation: bool
    is_active: bool


class ProductCreate(BaseModel):
    producer_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("producer_id", "producerId"),
    )
    producer_name_snapshot: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "producer_name_snapshot",
            "producerNameSnapshot",
        ),
    )
    name: str
    description: str | None = None
    category: str = "other"
    offer_type: str = Field(
        default="weekly_offer",
        validation_alias=AliasChoices("offer_type", "offerType"),
    )
    unit: str
    price: Decimal
    cost_price: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("cost_price", "costPrice"),
    )
    sale_price: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("sale_price", "salePrice"),
    )
    stock_quantity: Decimal = Field(
        default=Decimal("0"),
        validation_alias=AliasChoices("stock_quantity", "stockQuantity"),
    )
    image_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("image_url", "imageUrl"),
    )
    is_refrigerated: bool = Field(
        default=False,
        validation_alias=AliasChoices("is_refrigerated", "isRefrigerated"),
    )
    is_frozen: bool = Field(
        default=False,
        validation_alias=AliasChoices("is_frozen", "isFrozen"),
    )
    is_addon: bool = Field(
        default=False,
        validation_alias=AliasChoices("is_addon", "isAddon"),
    )
    is_donation: bool = Field(
        default=False,
        validation_alias=AliasChoices("is_donation", "isDonation"),
    )
    is_active: bool = Field(
        default=True,
        validation_alias=AliasChoices("is_active", "isActive"),
    )


class ProductUpdate(BaseModel):
    producer_id: UUID | None = Field(
        default=None,
        validation_alias=AliasChoices("producer_id", "producerId"),
    )
    producer_name_snapshot: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "producer_name_snapshot",
            "producerNameSnapshot",
        ),
    )
    name: str | None = None
    description: str | None = None
    category: str | None = None
    offer_type: str | None = Field(
        default=None,
        validation_alias=AliasChoices("offer_type", "offerType"),
    )
    unit: str | None = None
    price: Decimal | None = None
    cost_price: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("cost_price", "costPrice"),
    )
    sale_price: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("sale_price", "salePrice"),
    )
    stock_quantity: Decimal | None = Field(
        default=None,
        validation_alias=AliasChoices("stock_quantity", "stockQuantity"),
    )
    image_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("image_url", "imageUrl"),
    )
    is_refrigerated: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("is_refrigerated", "isRefrigerated"),
    )
    is_frozen: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("is_frozen", "isFrozen"),
    )
    is_addon: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("is_addon", "isAddon"),
    )
    is_donation: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("is_donation", "isDonation"),
    )
    is_active: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("is_active", "isActive"),
    )


class BasketTypeRead(BaseModel):
    """Public basket type representation with CSA metadata."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    base_price: Decimal
    average_items: int | None
    average_weight_kg: Decimal | None
    serves_people: str | None
    is_active: bool
