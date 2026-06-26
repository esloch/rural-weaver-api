from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator


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
    first_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("first_name", "firstName"),
    )
    last_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("last_name", "lastName"),
    )
    cpf: str | None = None
    email: str | None = None
    phone_country_code: str | None = Field(
        default=None,
        validation_alias=AliasChoices("phone_country_code", "phoneCountryCode"),
    )
    phone_area_code: str | None = Field(
        default=None,
        validation_alias=AliasChoices("phone_area_code", "phoneAreaCode"),
    )
    phone_number: str | None = Field(
        default=None,
        validation_alias=AliasChoices("phone_number", "phoneNumber"),
    )
    customer_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("customer_name", "customerName"),
    )
    customer_phone: str | None = Field(
        default=None,
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
    address_line: str | None = Field(
        default=None,
        validation_alias=AliasChoices("address_line", "addressLine"),
    )
    address_number: str | None = Field(
        default=None,
        validation_alias=AliasChoices("address_number", "addressNumber"),
    )
    address_complement: str | None = Field(
        default=None,
        validation_alias=AliasChoices("address_complement", "addressComplement"),
    )
    address: str | None = None
    neighborhood: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = Field(
        default=None,
        validation_alias=AliasChoices("postal_code", "postalCode"),
    )
    country: str | None = None
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

    @model_validator(mode="before")
    @classmethod
    def merge_nested_customer_and_address_payloads(cls, data):
        if not isinstance(data, dict):
            return data

        merged = dict(data)
        customer = merged.get("customer")
        if isinstance(customer, dict):
            field_map = {
                "first_name": ("first_name", "firstName"),
                "last_name": ("last_name", "lastName"),
                "cpf": ("cpf",),
                "email": ("email",),
                "phone_country_code": ("phone_country_code", "phoneCountryCode"),
                "phone_area_code": ("phone_area_code", "phoneAreaCode"),
                "phone_number": ("phone_number", "phoneNumber"),
            }
            for target, aliases in field_map.items():
                if merged.get(target) is None and all(merged.get(alias) is None for alias in aliases):
                    for alias in aliases:
                        if customer.get(alias) is not None:
                            merged[target] = customer.get(alias)
                            break

        delivery_address = merged.get("delivery_address") or merged.get("deliveryAddress")
        if isinstance(delivery_address, dict):
            field_map = {
                "address_line": ("address_line", "addressLine"),
                "address_number": ("address_number", "addressNumber"),
                "address_complement": ("address_complement", "addressComplement"),
                "neighborhood": ("neighborhood",),
                "city": ("city",),
                "state": ("state",),
                "postal_code": ("postal_code", "postalCode"),
                "country": ("country",),
            }
            for target, aliases in field_map.items():
                if merged.get(target) is None and all(merged.get(alias) is None for alias in aliases):
                    for alias in aliases:
                        if delivery_address.get(alias) is not None:
                            merged[target] = delivery_address.get(alias)
                            break

        return merged

    def has_registered_customer_payload(self) -> bool:
        return any(
            value
            for value in [
                self.first_name,
                self.last_name,
                self.cpf,
                self.email,
                self.phone_country_code,
                self.phone_area_code,
                self.phone_number,
            ]
        )


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
    order_number: str | None
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
    state: str | None
    postal_code: str | None
    country: str | None
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
