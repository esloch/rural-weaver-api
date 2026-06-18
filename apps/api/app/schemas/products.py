from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, HttpUrl


class ProductRead(BaseModel):
    """Public product representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    producer_id: UUID
    name: str
    description: str | None
    category: str
    unit: str
    price: Decimal
    stock_quantity: Decimal
    image_url: HttpUrl | None
    is_active: bool


class BasketTypeRead(BaseModel):
    """Public basket type representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    base_price: Decimal
    is_active: bool
