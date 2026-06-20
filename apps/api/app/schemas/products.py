from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


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
    image_url: HttpUrl | None
    is_refrigerated: bool
    is_frozen: bool
    is_addon: bool
    is_donation: bool
    is_active: bool


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
