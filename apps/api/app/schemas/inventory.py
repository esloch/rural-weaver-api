from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from apps.api.app.schemas.products import ProductRead


class StockMovementRead(BaseModel):
    """Stock movement representation."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    type: str
    quantity: Decimal
    reason: str | None
    created_by: UUID | None
    created_at: datetime


class AdminInventoryRead(BaseModel):
    """Inventory screen response."""

    products: list[ProductRead]
    movements: list[StockMovementRead]


class StockAdjustmentRequest(BaseModel):
    """Payload for stock adjustments.

    Accepts both snake_case and camelCase names.
    """

    quantity_delta: Decimal = Field(
        validation_alias=AliasChoices("quantity_delta", "quantityDelta"),
    )
    reason: str | None = None
    type: str = "manual_adjustment"
