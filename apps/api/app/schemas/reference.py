from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PickupPointRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    address: str | None
    city: str | None
    neighborhood: str | None
    weekday_availability: str | None
    time_window: str | None
    has_refrigeration: bool
    is_condo_only: bool
    instructions: str | None
    is_active: bool


class DeliveryZoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    city: str | None
    area: str | None
    fee: Decimal
    restrictions: str | None
    instructions: str | None
    is_supported: bool
    is_active: bool


class PaymentMethodRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    instructions: str | None
    requires_extra_data: bool
    is_active: bool


class SubscriptionPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    basket_type_id: UUID | None
    name: str
    frequency: str
    deliveries_per_month: int
    price: Decimal
    average_items: int | None
    average_weight_kg: Decimal | None
    serves_people: str | None
    description: str | None
    is_active: bool
