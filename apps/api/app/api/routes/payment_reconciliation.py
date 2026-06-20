import csv
from io import StringIO
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.payment_reconciliation import (
    PaymentReconciliationRepository,
)
from apps.api.app.schemas.orders import OrderRead
from apps.api.app.schemas.payment_reconciliation import (
    CampaignPaymentSummaryRead,
    OrderPaymentDetailRead,
    OrderPaymentDetailUpsert,
    OrderPaymentReconciliationRead,
    PaymentConfirmationCreate,
    PaymentConfirmationRead,
    PaymentStatusUpdate,
)

router = APIRouter()


@router.get(
    "/orders/{order_id}/payment-reconciliation",
    response_model=OrderPaymentReconciliationRead,
)
def get_order_payment_reconciliation(
    order_id: UUID,
    db: Session = Depends(get_db),
) -> OrderPaymentReconciliationRead:
    state = PaymentReconciliationRepository(db).get_order_payment_state(order_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    return state


@router.get(
    "/orders/{order_id}/payment-confirmations",
    response_model=list[PaymentConfirmationRead],
)
def list_order_payment_confirmations(
    order_id: UUID,
    db: Session = Depends(get_db),
) -> list[PaymentConfirmationRead]:
    return PaymentReconciliationRepository(db).list_order_confirmations(order_id)


@router.post(
    "/orders/{order_id}/payment-confirmations",
    response_model=PaymentConfirmationRead,
)
def create_order_payment_confirmation(
    order_id: UUID,
    payload: PaymentConfirmationCreate,
    db: Session = Depends(get_db),
) -> PaymentConfirmationRead:
    confirmation = PaymentReconciliationRepository(db).create_confirmation(
        order_id=order_id,
        payload=payload,
    )
    if confirmation is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    db.commit()
    db.refresh(confirmation)
    return confirmation


@router.get(
    "/orders/{order_id}/payment-detail",
    response_model=OrderPaymentDetailRead | None,
)
def get_order_payment_detail(
    order_id: UUID,
    db: Session = Depends(get_db),
) -> OrderPaymentDetailRead | None:
    order = PaymentReconciliationRepository(db).get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    return PaymentReconciliationRepository(db).get_payment_detail(order_id)


@router.put(
    "/orders/{order_id}/payment-detail",
    response_model=OrderPaymentDetailRead,
)
def upsert_order_payment_detail(
    order_id: UUID,
    payload: OrderPaymentDetailUpsert,
    db: Session = Depends(get_db),
) -> OrderPaymentDetailRead:
    detail = PaymentReconciliationRepository(db).upsert_payment_detail(
        order_id=order_id,
        payload=payload,
    )
    if detail is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    db.commit()
    db.refresh(detail)
    return detail


@router.patch("/orders/{order_id}/payment-status", response_model=OrderRead)
def update_order_payment_status(
    order_id: UUID,
    payload: PaymentStatusUpdate,
    db: Session = Depends(get_db),
) -> OrderRead:
    order = PaymentReconciliationRepository(db).update_payment_status(
        order_id=order_id,
        payload=payload,
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/{order_id}/mark-proof-received", response_model=OrderRead)
def mark_order_proof_received(
    order_id: UUID,
    db: Session = Depends(get_db),
) -> OrderRead:
    order = PaymentReconciliationRepository(db).mark_proof_received(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/{order_id}/confirm-payment", response_model=OrderRead)
def confirm_order_payment(
    order_id: UUID,
    db: Session = Depends(get_db),
) -> OrderRead:
    order = PaymentReconciliationRepository(db).confirm_payment(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    db.commit()
    db.refresh(order)
    return order


@router.post("/orders/{order_id}/cancel-payment", response_model=OrderRead)
def cancel_order_payment(
    order_id: UUID,
    db: Session = Depends(get_db),
) -> OrderRead:
    order = PaymentReconciliationRepository(db).cancel_payment(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    db.commit()
    db.refresh(order)
    return order


@router.get(
    "/campaigns/{campaign_id}/payment-summary",
    response_model=CampaignPaymentSummaryRead,
)
def get_campaign_payment_summary(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> CampaignPaymentSummaryRead:
    return PaymentReconciliationRepository(db).campaign_payment_summary(campaign_id)


@router.get("/campaigns/{campaign_id}/payments.csv")
def export_campaign_payments_csv(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    repo = PaymentReconciliationRepository(db)
    orders = repo._campaign_orders(campaign_id)

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "Pedido",
            "Cliente",
            "Telefone",
            "Método",
            "Status pagamento",
            "Status confirmação",
            "Subtotal",
            "Taxa entrega",
            "Total",
            "Custo pagamento",
            "Total líquido",
            "Criado em",
            "Confirmado em",
        ],
    )

    for order in orders:
        writer.writerow(
            [
                order.id,
                order.customer_name,
                order.customer_phone,
                order.payment_method,
                order.payment_status,
                order.confirmation_status,
                order.subtotal,
                order.delivery_fee,
                order.total,
                order.payment_fee_amount,
                order.net_total_after_fees,
                order.created_at,
                order.confirmed_at,
            ],
        )

    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f"attachment; filename=campaign-payments-{campaign_id}.csv"
            ),
        },
    )
