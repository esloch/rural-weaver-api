from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import func, select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from apps.api.app.models.customer import Customer
from apps.api.app.schemas.orders import OrderCreate
from packages.business_rules.customers import (
    CustomerValidationError,
    NormalizedPhone,
    build_address_snapshot,
    build_full_name,
    normalize_cpf,
    normalize_email,
    normalize_phone,
    only_digits,
    split_full_name,
    validate_cpf,
    validate_email,
)


@dataclass(frozen=True)
class ResolvedCustomerIdentity:
    first_name: str
    last_name: str
    full_name: str
    cpf_normalized: str
    email: str
    phone_country_code: str
    phone_area_code: str | None
    phone_number: str
    phone_e164: str | None
    address: str | None
    neighborhood: str | None
    city: str | None


class CustomerRepository:
    """Customer validation, lookup, and upsert for order creation."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def upsert_from_order(self, payload: OrderCreate) -> Customer:
        identity = self.resolve_identity(payload)
        customer = self._get_by_cpf(identity.cpf_normalized)

        if customer is None:
            customer = Customer(
                full_name=identity.full_name,
                phone=identity.phone_e164 or identity.phone_number,
                email=identity.email,
                cpf=identity.cpf_normalized,
                address=identity.address,
                neighborhood=identity.neighborhood,
                city=identity.city,
                customer_number=self._next_customer_number(),
                first_name=identity.first_name,
                last_name=identity.last_name,
                cpf_normalized=identity.cpf_normalized,
                phone_country_code=identity.phone_country_code,
                phone_area_code=identity.phone_area_code,
                phone_number=identity.phone_number,
                phone_e164=identity.phone_e164,
            )
            self.db.add(customer)
            self.db.flush()
            return customer

        customer.full_name = identity.full_name
        customer.phone = identity.phone_e164 or identity.phone_number
        customer.email = identity.email
        customer.cpf = identity.cpf_normalized
        customer.address = identity.address
        customer.neighborhood = identity.neighborhood
        customer.city = identity.city
        customer.first_name = identity.first_name
        customer.last_name = identity.last_name
        customer.cpf_normalized = identity.cpf_normalized
        customer.phone_country_code = identity.phone_country_code
        customer.phone_area_code = identity.phone_area_code
        customer.phone_number = identity.phone_number
        customer.phone_e164 = identity.phone_e164
        if not customer.customer_number:
            customer.customer_number = self._next_customer_number()
        self.db.flush()
        return customer

    def resolve_identity(self, payload: OrderCreate) -> ResolvedCustomerIdentity:
        first_name = (payload.first_name or "").strip()
        last_name = (payload.last_name or "").strip()
        if not first_name or not last_name:
            legacy_first_name, legacy_last_name = split_full_name(payload.customer_name)
            first_name = first_name or (legacy_first_name or "")
            last_name = last_name or (legacy_last_name or "")

        if not first_name:
            raise CustomerValidationError("missing first_name.")
        if not last_name:
            raise CustomerValidationError("missing last_name.")

        cpf_input = payload.cpf or ""
        cpf_normalized = normalize_cpf(cpf_input)
        if not cpf_normalized:
            raise CustomerValidationError("missing cpf.")
        if not validate_cpf(cpf_normalized):
            raise CustomerValidationError("invalid CPF.")

        email_input = payload.email or payload.customer_email or ""
        email = normalize_email(email_input)
        if not email:
            raise CustomerValidationError("missing email.")
        if not validate_email(email):
            raise CustomerValidationError("invalid email.")

        phone = self._resolve_phone(payload)
        address = self._resolve_delivery_address(payload)

        return ResolvedCustomerIdentity(
            first_name=first_name,
            last_name=last_name,
            full_name=build_full_name(first_name, last_name),
            cpf_normalized=cpf_normalized,
            email=email,
            phone_country_code=phone.country_code,
            phone_area_code=phone.area_code,
            phone_number=phone.phone_number,
            phone_e164=phone.phone_e164,
            address=address,
            neighborhood=payload.neighborhood,
            city=payload.city,
        )

    def _resolve_phone(self, payload: OrderCreate) -> NormalizedPhone:
        country_code = payload.phone_country_code
        area_code = payload.phone_area_code
        phone_number = payload.phone_number

        if not country_code and payload.customer_phone:
            digits = only_digits(payload.customer_phone)
            if digits.startswith("55") and len(digits) >= 12:
                country_code = "+55"
                area_code = digits[2:4]
                phone_number = digits[4:]

        return normalize_phone(country_code or "", area_code, phone_number or "")

    def _resolve_delivery_address(self, payload: OrderCreate) -> str | None:
        if payload.delivery_type != "delivery":
            return payload.address

        if payload.address_line and payload.address_number:
            required_fields = {
                "neighborhood": payload.neighborhood,
                "city": payload.city,
                "state": payload.state,
                "postal_code": payload.postal_code,
                "country": payload.country,
            }
            if any(not value for value in required_fields.values()):
                raise CustomerValidationError(
                    "delivery address required when delivery_type is delivery.",
                )
            return build_address_snapshot(payload.address_line, payload.address_number)

        if payload.address and payload.neighborhood and payload.city:
            return payload.address

        raise CustomerValidationError(
            "delivery address required when delivery_type is delivery.",
        )

    def _get_by_cpf(self, cpf_normalized: str) -> Customer | None:
        stmt = select(Customer).where(Customer.cpf_normalized == cpf_normalized)
        return self.db.scalars(stmt).first()

    def _next_customer_number(self) -> str:
        return f"CLI-{self._next_sequence_value('customer_number_seq'):06d}"

    def _next_sequence_value(self, sequence_name: str) -> int:
        try:
            result = self.db.execute(text(f"SELECT nextval('{sequence_name}')"))
            return int(result.scalar_one())
        except DBAPIError:
            stmt = select(func.count(Customer.id))
            current = self.db.execute(stmt).scalar_one()
            return int(current) + 1
