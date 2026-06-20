from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CampaignFinancialAdjustmentCreate(BaseModel):
    adjustment_type: str
    description: str
    amount: Decimal
    notes: str | None = None


class CampaignFinancialAdjustmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    campaign_id: UUID
    adjustment_type: str
    description: str
    amount: Decimal
    notes: str | None
    created_at: datetime
    updated_at: datetime


class CampaignFinancialSummaryRead(BaseModel):
    campaign_id: UUID
    total_orders: int
    gross_revenue: Decimal
    product_sales_total: Decimal
    product_cost_total: Decimal
    product_margin_total: Decimal
    delivery_fee_total: Decimal
    payment_fee_total: Decimal
    confirmed_amount: Decimal
    pending_amount: Decimal
    cancelled_amount: Decimal
    manual_adjustments_total: Decimal
    net_estimated_result: Decimal
    average_ticket: Decimal


class ProducerSettlementRow(BaseModel):
    producer_name: str
    quantity_total: Decimal
    sale_total: Decimal
    cost_total: Decimal
    margin_total: Decimal
    orders_count: int


class ProducerSettlementRead(BaseModel):
    campaign_id: UUID
    rows: list[ProducerSettlementRow]
    sale_total: Decimal
    cost_total: Decimal
    margin_total: Decimal


class OrderMatrixProductRow(BaseModel):
    product_name: str
    producer_name: str | None
    unit_price: Decimal
    cost_price: Decimal | None
    customers: dict[str, Decimal]
    quantity_total: Decimal
    sale_total: Decimal
    cost_total: Decimal
    margin_total: Decimal


class OrderMatrixRead(BaseModel):
    campaign_id: UUID
    customer_names: list[str]
    rows: list[OrderMatrixProductRow]
