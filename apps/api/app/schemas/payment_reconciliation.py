from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class PaymentConfirmationCreate(BaseModel):
    """Manual payment confirmation payload.

    Accepts both snake_case and camelCase fields.
    """

    method_code: str = Field(
        validation_alias=AliasChoices("method_code", "methodCode"),
    )
    status: str = "confirmed"
    amount: Decimal
    proof_received: bool = Field(
        default=True,
        validation_alias=AliasChoices("proof_received", "proofReceived"),
    )
    notes: str | None = None


class PaymentConfirmationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    method_code: str
    status: str
    amount: Decimal
    confirmed_at: datetime | None
    confirmed_by: UUID | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class PaymentStatusUpdate(BaseModel):
    payment_status: str = Field(
        validation_alias=AliasChoices("payment_status", "paymentStatus"),
    )
    confirmation_status: str | None = Field(
        default=None,
        validation_alias=AliasChoices("confirmation_status", "confirmationStatus"),
    )
    notes: str | None = None


class OrderPaymentDetailUpsert(BaseModel):
    method_code: str = Field(
        validation_alias=AliasChoices("method_code", "methodCode"),
    )
    cpf: str | None = None
    billing_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("billing_name", "billingName"),
    )
    billing_address: str | None = Field(
        default=None,
        validation_alias=AliasChoices("billing_address", "billingAddress"),
    )
    billing_email: str | None = Field(
        default=None,
        validation_alias=AliasChoices("billing_email", "billingEmail"),
    )
    billing_phone: str | None = Field(
        default=None,
        validation_alias=AliasChoices("billing_phone", "billingPhone"),
    )
    payment_link: str | None = Field(
        default=None,
        validation_alias=AliasChoices("payment_link", "paymentLink"),
    )
    proof_received: bool | None = Field(
        default=None,
        validation_alias=AliasChoices("proof_received", "proofReceived"),
    )
    notes: str | None = None


class OrderPaymentDetailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    method_code: str
    cpf: str | None
    billing_name: str | None
    billing_address: str | None
    billing_email: str | None
    billing_phone: str | None
    payment_link: str | None
    proof_received: bool
    confirmed_at: datetime | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class PaymentMethodBreakdownRow(BaseModel):
    method_code: str
    orders_count: int
    gross_amount: Decimal
    payment_fee_amount: Decimal
    net_amount: Decimal


class CampaignPaymentSummaryRead(BaseModel):
    campaign_id: UUID
    total_orders: int
    pending_orders: int
    proof_received_orders: int
    confirmed_orders: int
    cancelled_orders: int
    refunded_orders: int
    pending_amount: Decimal
    proof_received_amount: Decimal
    confirmed_amount: Decimal
    cancelled_amount: Decimal
    refunded_amount: Decimal
    gross_amount: Decimal
    payment_fee_total: Decimal
    net_confirmed_amount: Decimal
    orders_by_payment_method: list[PaymentMethodBreakdownRow]


class OrderPaymentReconciliationRead(BaseModel):
    order_id: UUID
    payment_status: str
    confirmation_status: str
    payment_method: str
    subtotal: Decimal
    delivery_fee: Decimal
    total: Decimal
    payment_fee_amount: Decimal | None
    net_total_after_fees: Decimal | None
    payment_detail: OrderPaymentDetailRead | None
    confirmations: list[PaymentConfirmationRead]
