from collections import defaultdict
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.financial import CampaignFinancialAdjustment
from apps.api.app.models.order import Order, OrderItem
from apps.api.app.schemas.settlements import (
    CampaignFinancialAdjustmentCreate,
    CampaignFinancialSummaryRead,
    OrderMatrixProductRow,
    OrderMatrixRead,
    ProducerSettlementRead,
    ProducerSettlementRow,
)


ZERO = Decimal("0.00")


class SettlementRepository:
    """Financial reporting and producer settlement calculations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_adjustments(
        self,
        campaign_id: UUID,
    ) -> list[CampaignFinancialAdjustment]:
        stmt = (
            select(CampaignFinancialAdjustment)
            .where(CampaignFinancialAdjustment.campaign_id == campaign_id)
            .order_by(CampaignFinancialAdjustment.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def create_adjustment(
        self,
        campaign_id: UUID,
        payload: CampaignFinancialAdjustmentCreate,
    ) -> CampaignFinancialAdjustment:
        adjustment = CampaignFinancialAdjustment(
            campaign_id=campaign_id,
            adjustment_type=payload.adjustment_type,
            description=payload.description,
            amount=payload.amount,
            notes=payload.notes,
        )
        self.db.add(adjustment)
        self.db.flush()
        return adjustment

    def delete_adjustment(self, adjustment_id: UUID) -> bool:
        adjustment = self.db.get(CampaignFinancialAdjustment, adjustment_id)
        if adjustment is None:
            return False
        self.db.delete(adjustment)
        self.db.flush()
        return True

    def financial_summary(self, campaign_id: UUID) -> CampaignFinancialSummaryRead:
        orders = self._campaign_orders(campaign_id)
        order_ids = [order.id for order in orders]
        items = self._order_items(order_ids)
        adjustments = self.list_adjustments(campaign_id)

        active_orders = [order for order in orders if order.status != "cancelled"]
        cancelled_orders = [order for order in orders if order.status == "cancelled"]

        gross_revenue = self._sum(order.total for order in active_orders)
        confirmed_amount = self._sum(
            order.total
            for order in active_orders
            if order.payment_status == "confirmed"
        )
        pending_amount = self._sum(
            order.total
            for order in active_orders
            if order.payment_status == "pending"
        )
        cancelled_amount = self._sum(order.total for order in cancelled_orders)

        product_sales_total = self._sum(
            self._sale_total(item)
            for item in items
        )
        product_cost_total = self._sum(
            self._cost_total(item)
            for item in items
        )
        product_margin_total = product_sales_total - product_cost_total
        delivery_fee_total = self._sum(
            order.delivery_fee
            for order in active_orders
        )
        payment_fee_total = self._sum(
            order.payment_fee_amount or ZERO
            for order in active_orders
        )
        manual_adjustments_total = self._sum(
            adjustment.amount
            for adjustment in adjustments
        )

        net_estimated_result = (
            product_margin_total
            + delivery_fee_total
            - payment_fee_total
            + manual_adjustments_total
        )

        average_ticket = (
            gross_revenue / Decimal(len(active_orders))
            if active_orders
            else ZERO
        )

        return CampaignFinancialSummaryRead(
            campaign_id=campaign_id,
            total_orders=len(orders),
            gross_revenue=gross_revenue,
            product_sales_total=product_sales_total,
            product_cost_total=product_cost_total,
            product_margin_total=product_margin_total,
            delivery_fee_total=delivery_fee_total,
            payment_fee_total=payment_fee_total,
            confirmed_amount=confirmed_amount,
            pending_amount=pending_amount,
            cancelled_amount=cancelled_amount,
            manual_adjustments_total=manual_adjustments_total,
            net_estimated_result=net_estimated_result,
            average_ticket=average_ticket,
        )

    def producer_settlement(self, campaign_id: UUID) -> ProducerSettlementRead:
        orders = self._campaign_orders(campaign_id)
        active_order_ids = [
            order.id
            for order in orders
            if order.status != "cancelled"
        ]
        items = self._order_items(active_order_ids)

        grouped: dict[str, dict[str, Decimal | set[UUID]]] = defaultdict(
            lambda: {
                "quantity_total": ZERO,
                "sale_total": ZERO,
                "cost_total": ZERO,
                "margin_total": ZERO,
                "orders": set(),
            },
        )

        for item in items:
            producer = item.producer_name_snapshot or "Sem produtor informado"
            sale_total = self._sale_total(item)
            cost_total = self._cost_total(item)
            margin_total = sale_total - cost_total

            grouped[producer]["quantity_total"] += item.quantity
            grouped[producer]["sale_total"] += sale_total
            grouped[producer]["cost_total"] += cost_total
            grouped[producer]["margin_total"] += margin_total
            grouped[producer]["orders"].add(item.order_id)

        rows = [
            ProducerSettlementRow(
                producer_name=producer,
                quantity_total=values["quantity_total"],
                sale_total=values["sale_total"],
                cost_total=values["cost_total"],
                margin_total=values["margin_total"],
                orders_count=len(values["orders"]),
            )
            for producer, values in grouped.items()
        ]
        rows.sort(key=lambda row: row.producer_name.lower())

        return ProducerSettlementRead(
            campaign_id=campaign_id,
            rows=rows,
            sale_total=self._sum(row.sale_total for row in rows),
            cost_total=self._sum(row.cost_total for row in rows),
            margin_total=self._sum(row.margin_total for row in rows),
        )

    def order_matrix(self, campaign_id: UUID) -> OrderMatrixRead:
        orders = [
            order
            for order in self._campaign_orders(campaign_id)
            if order.status != "cancelled"
        ]
        order_by_id = {order.id: order for order in orders}
        customer_names = sorted({order.customer_name for order in orders})
        items = self._order_items(list(order_by_id.keys()))

        grouped: dict[str, dict] = {}

        for item in items:
            key = item.name_snapshot
            order = order_by_id[item.order_id]
            sale_total = self._sale_total(item)
            cost_total = self._cost_total(item)

            if key not in grouped:
                grouped[key] = {
                    "product_name": item.name_snapshot,
                    "producer_name": item.producer_name_snapshot,
                    "unit_price": item.unit_sale_price_snapshot or item.unit_price_snapshot,
                    "cost_price": item.unit_cost_snapshot,
                    "customers": defaultdict(lambda: Decimal("0")),
                    "quantity_total": Decimal("0"),
                    "sale_total": Decimal("0"),
                    "cost_total": Decimal("0"),
                    "margin_total": Decimal("0"),
                }

            grouped[key]["customers"][order.customer_name] += item.quantity
            grouped[key]["quantity_total"] += item.quantity
            grouped[key]["sale_total"] += sale_total
            grouped[key]["cost_total"] += cost_total
            grouped[key]["margin_total"] += sale_total - cost_total

        rows = [
            OrderMatrixProductRow(
                product_name=value["product_name"],
                producer_name=value["producer_name"],
                unit_price=value["unit_price"],
                cost_price=value["cost_price"],
                customers=dict(value["customers"]),
                quantity_total=value["quantity_total"],
                sale_total=value["sale_total"],
                cost_total=value["cost_total"],
                margin_total=value["margin_total"],
            )
            for value in grouped.values()
        ]
        rows.sort(key=lambda row: row.product_name.lower())

        return OrderMatrixRead(
            campaign_id=campaign_id,
            customer_names=customer_names,
            rows=rows,
        )

    def _campaign_orders(self, campaign_id: UUID) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.campaign_id == campaign_id)
            .order_by(Order.created_at.asc())
        )
        return list(self.db.scalars(stmt).all())

    def _order_items(self, order_ids: list[UUID]) -> list[OrderItem]:
        if not order_ids:
            return []
        stmt = select(OrderItem).where(OrderItem.order_id.in_(order_ids))
        return list(self.db.scalars(stmt).all())

    def _sale_total(self, item: OrderItem) -> Decimal:
        return item.sale_total_snapshot or item.total_snapshot or ZERO

    def _cost_total(self, item: OrderItem) -> Decimal:
        return item.cost_total_snapshot or ZERO

    def _sum(self, values) -> Decimal:
        total = ZERO
        for value in values:
            total += value or ZERO
        return total.quantize(Decimal("0.01"))
