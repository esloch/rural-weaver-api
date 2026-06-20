from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

# Import all SQLAlchemy models so foreign keys such as orders.customer_id
# can resolve referenced tables during ORM flush/commit.
import apps.api.app.db.base  # noqa: F401

from apps.api.app.models.order import Order
from apps.api.app.models.order_payment import OrderPaymentDetail, PaymentConfirmation
from apps.api.app.schemas.payment_reconciliation import (
    CampaignPaymentSummaryRead,
    OrderPaymentDetailUpsert,
    OrderPaymentReconciliationRead,
    PaymentConfirmationCreate,
    PaymentMethodBreakdownRow,
    PaymentStatusUpdate,
)

ZERO = Decimal("0.00")


class PaymentReconciliationRepository:
    """Manual payment reconciliation workflow for admin operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_order(self, order_id: UUID) -> Order | None:
        return self.db.get(Order, order_id)

    def list_order_confirmations(self, order_id: UUID) -> list[PaymentConfirmation]:
        stmt = (
            select(PaymentConfirmation)
            .where(PaymentConfirmation.order_id == order_id)
            .order_by(PaymentConfirmation.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def get_payment_detail(self, order_id: UUID) -> OrderPaymentDetail | None:
        stmt = (
            select(OrderPaymentDetail)
            .where(OrderPaymentDetail.order_id == order_id)
            .order_by(OrderPaymentDetail.created_at.desc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()

    def get_order_payment_state(
        self,
        order_id: UUID,
    ) -> OrderPaymentReconciliationRead | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        return OrderPaymentReconciliationRead(
            order_id=order.id,
            payment_status=order.payment_status,
            confirmation_status=order.confirmation_status,
            payment_method=order.payment_method,
            subtotal=order.subtotal,
            delivery_fee=order.delivery_fee,
            total=order.total,
            payment_fee_amount=order.payment_fee_amount,
            net_total_after_fees=order.net_total_after_fees,
            payment_detail=self.get_payment_detail(order_id),
            confirmations=self.list_order_confirmations(order_id),
        )

    def upsert_payment_detail(
        self,
        order_id: UUID,
        payload: OrderPaymentDetailUpsert,
    ) -> OrderPaymentDetail | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        detail = self.get_payment_detail(order_id)
        if detail is None:
            detail = OrderPaymentDetail(
                order_id=order.id,
                method_code=payload.method_code,
            )
            self.db.add(detail)

        values = payload.model_dump(exclude_unset=True)
        for field, value in values.items():
            setattr(detail, field, value)

        if payload.proof_received is True:
            order.payment_status = "proof_received"
            order.confirmation_status = "requires_review"

        self.db.flush()
        return detail

    def create_confirmation(
        self,
        order_id: UUID,
        payload: PaymentConfirmationCreate,
        confirmed_by: UUID | None = None,
    ) -> PaymentConfirmation | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        now = datetime.now(UTC)
        confirmation = PaymentConfirmation(
            order_id=order.id,
            method_code=payload.method_code,
            status=payload.status,
            amount=payload.amount,
            confirmed_at=now if payload.status == "confirmed" else None,
            confirmed_by=confirmed_by,
            notes=payload.notes,
        )
        self.db.add(confirmation)

        detail = self.get_payment_detail(order.id)
        if detail is not None:
            detail.proof_received = payload.proof_received
            if payload.status == "confirmed":
                detail.confirmed_at = now

        self._apply_payment_status_from_confirmation(order, payload.status)
        self.db.flush()
        return confirmation

    def update_payment_status(
        self,
        order_id: UUID,
        payload: PaymentStatusUpdate,
    ) -> Order | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        order.payment_status = payload.payment_status
        if payload.confirmation_status is not None:
            order.confirmation_status = payload.confirmation_status

        if payload.notes:
            existing_notes = order.notes or ""
            order.notes = (
                f"{existing_notes}\n[Payment] {payload.notes}".strip()
                if existing_notes
                else f"[Payment] {payload.notes}"
            )

        self.db.flush()
        return order

    def mark_proof_received(self, order_id: UUID) -> Order | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        order.payment_status = "proof_received"
        order.confirmation_status = "requires_review"

        detail = self.get_payment_detail(order.id)
        if detail is not None:
            detail.proof_received = True

        self.db.flush()
        return order

    def confirm_payment(self, order_id: UUID) -> Order | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        order.payment_status = "confirmed"
        order.confirmation_status = "confirmed"
        order.confirmed_at = datetime.now(UTC)

        detail = self.get_payment_detail(order.id)
        if detail is not None:
            detail.proof_received = True
            detail.confirmed_at = order.confirmed_at

        self.db.flush()
        return order

    def cancel_payment(self, order_id: UUID) -> Order | None:
        order = self.get_order(order_id)
        if order is None:
            return None

        order.payment_status = "cancelled"
        order.confirmation_status = "cancelled"
        self.db.flush()
        return order

    def campaign_payment_summary(
        self,
        campaign_id: UUID,
    ) -> CampaignPaymentSummaryRead:
        orders = self._campaign_orders(campaign_id)

        pending_orders = [
            order for order in orders if order.payment_status == "pending"
        ]
        proof_received_orders = [
            order for order in orders if order.payment_status == "proof_received"
        ]
        confirmed_orders = [
            order for order in orders if order.payment_status == "confirmed"
        ]
        cancelled_orders = [
            order for order in orders if order.payment_status == "cancelled"
        ]
        refunded_orders = [
            order for order in orders if order.payment_status == "refunded"
        ]

        breakdown_map: dict[str, dict[str, Decimal | int]] = {}

        for order in orders:
            key = order.payment_method or "unknown"
            if key not in breakdown_map:
                breakdown_map[key] = {
                    "orders_count": 0,
                    "gross_amount": ZERO,
                    "payment_fee_amount": ZERO,
                    "net_amount": ZERO,
                }

            breakdown_map[key]["orders_count"] += 1
            breakdown_map[key]["gross_amount"] += order.total or ZERO
            breakdown_map[key]["payment_fee_amount"] += (
                order.payment_fee_amount or ZERO
            )
            breakdown_map[key]["net_amount"] += (
                order.net_total_after_fees
                if order.net_total_after_fees is not None
                else (order.total or ZERO) - (order.payment_fee_amount or ZERO)
            )

        rows = [
            PaymentMethodBreakdownRow(
                method_code=method_code,
                orders_count=int(values["orders_count"]),
                gross_amount=self._money(values["gross_amount"]),
                payment_fee_amount=self._money(values["payment_fee_amount"]),
                net_amount=self._money(values["net_amount"]),
            )
            for method_code, values in sorted(breakdown_map.items())
        ]

        confirmed_amount = self._sum(order.total for order in confirmed_orders)
        payment_fee_total = self._sum(
            order.payment_fee_amount or ZERO
            for order in orders
        )

        return CampaignPaymentSummaryRead(
            campaign_id=campaign_id,
            total_orders=len(orders),
            pending_orders=len(pending_orders),
            proof_received_orders=len(proof_received_orders),
            confirmed_orders=len(confirmed_orders),
            cancelled_orders=len(cancelled_orders),
            refunded_orders=len(refunded_orders),
            pending_amount=self._sum(order.total for order in pending_orders),
            proof_received_amount=self._sum(
                order.total for order in proof_received_orders
            ),
            confirmed_amount=confirmed_amount,
            cancelled_amount=self._sum(order.total for order in cancelled_orders),
            refunded_amount=self._sum(order.total for order in refunded_orders),
            gross_amount=self._sum(order.total for order in orders),
            payment_fee_total=payment_fee_total,
            net_confirmed_amount=self._sum(
                (
                    order.net_total_after_fees
                    if order.net_total_after_fees is not None
                    else (order.total or ZERO) - (order.payment_fee_amount or ZERO)
                )
                for order in confirmed_orders
            ),
            orders_by_payment_method=rows,
        )

    def _apply_payment_status_from_confirmation(
        self,
        order: Order,
        status: str,
    ) -> None:
        if status == "confirmed":
            order.payment_status = "confirmed"
            order.confirmation_status = "confirmed"
            order.confirmed_at = datetime.now(UTC)
        elif status == "proof_received":
            order.payment_status = "proof_received"
            order.confirmation_status = "requires_review"
        elif status == "cancelled":
            order.payment_status = "cancelled"
            order.confirmation_status = "cancelled"
        elif status == "refunded":
            order.payment_status = "refunded"
            order.confirmation_status = "requires_review"
        else:
            order.payment_status = "pending"
            order.confirmation_status = "pending"

    def _campaign_orders(self, campaign_id: UUID) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.campaign_id == campaign_id)
            .order_by(Order.created_at.asc())
        )
        return list(self.db.scalars(stmt).all())

    def _sum(self, values) -> Decimal:
        total = ZERO
        for value in values:
            total += value or ZERO
        return self._money(total)

    def _money(self, value) -> Decimal:
        return (value or ZERO).quantize(Decimal("0.01"))
