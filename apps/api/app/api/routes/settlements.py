import csv
from io import StringIO
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.settlements import SettlementRepository
from apps.api.app.schemas.settlements import (
    CampaignFinancialAdjustmentCreate,
    CampaignFinancialAdjustmentRead,
    CampaignFinancialSummaryRead,
    OrderMatrixRead,
    ProducerSettlementRead,
)

router = APIRouter()


@router.get(
    "/campaigns/{campaign_id}/financial-summary",
    response_model=CampaignFinancialSummaryRead,
)
def get_campaign_financial_summary(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> CampaignFinancialSummaryRead:
    return SettlementRepository(db).financial_summary(campaign_id)


@router.get(
    "/campaigns/{campaign_id}/producer-settlement",
    response_model=ProducerSettlementRead,
)
def get_campaign_producer_settlement(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> ProducerSettlementRead:
    return SettlementRepository(db).producer_settlement(campaign_id)


@router.get(
    "/campaigns/{campaign_id}/order-matrix",
    response_model=OrderMatrixRead,
)
def get_campaign_order_matrix(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> OrderMatrixRead:
    return SettlementRepository(db).order_matrix(campaign_id)


@router.get(
    "/campaigns/{campaign_id}/financial-adjustments",
    response_model=list[CampaignFinancialAdjustmentRead],
)
def list_campaign_financial_adjustments(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> list[CampaignFinancialAdjustmentRead]:
    return SettlementRepository(db).list_adjustments(campaign_id)


@router.post(
    "/campaigns/{campaign_id}/financial-adjustments",
    response_model=CampaignFinancialAdjustmentRead,
)
def create_campaign_financial_adjustment(
    campaign_id: UUID,
    payload: CampaignFinancialAdjustmentCreate,
    db: Session = Depends(get_db),
) -> CampaignFinancialAdjustmentRead:
    adjustment = SettlementRepository(db).create_adjustment(campaign_id, payload)
    db.commit()
    db.refresh(adjustment)
    return adjustment


@router.delete("/financial-adjustments/{adjustment_id}", status_code=204)
def delete_campaign_financial_adjustment(
    adjustment_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    deleted = SettlementRepository(db).delete_adjustment(adjustment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Adjustment not found.")
    db.commit()
    return Response(status_code=204)


@router.get("/campaigns/{campaign_id}/producer-settlement.csv")
def export_campaign_producer_settlement_csv(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    settlement = SettlementRepository(db).producer_settlement(campaign_id)
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "Produtor",
            "Quantidade total",
            "Total venda",
            "Total revenda",
            "Margem",
            "Pedidos",
        ],
    )

    for row in settlement.rows:
        writer.writerow(
            [
                row.producer_name,
                row.quantity_total,
                row.sale_total,
                row.cost_total,
                row.margin_total,
                row.orders_count,
            ],
        )

    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f"attachment; filename=producer-settlement-{campaign_id}.csv"
            ),
        },
    )


@router.get("/campaigns/{campaign_id}/financial-summary.csv")
def export_campaign_financial_summary_csv(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    summary = SettlementRepository(db).financial_summary(campaign_id)
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Métrica", "Valor"])
    writer.writerow(["Total pedidos", summary.total_orders])
    writer.writerow(["Receita bruta", summary.gross_revenue])
    writer.writerow(["Total venda produtos", summary.product_sales_total])
    writer.writerow(["Total revenda produtos", summary.product_cost_total])
    writer.writerow(["Margem produtos", summary.product_margin_total])
    writer.writerow(["Taxas de entrega", summary.delivery_fee_total])
    writer.writerow(["Custos de pagamento", summary.payment_fee_total])
    writer.writerow(["Valor confirmado", summary.confirmed_amount])
    writer.writerow(["Valor pendente", summary.pending_amount])
    writer.writerow(["Valor cancelado", summary.cancelled_amount])
    writer.writerow(["Ajustes manuais", summary.manual_adjustments_total])
    writer.writerow(["Resultado líquido estimado", summary.net_estimated_result])
    writer.writerow(["Ticket médio", summary.average_ticket])

    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f"attachment; filename=financial-summary-{campaign_id}.csv"
            ),
        },
    )


@router.get("/campaigns/{campaign_id}/order-matrix.csv")
def export_campaign_order_matrix_csv(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> StreamingResponse:
    matrix = SettlementRepository(db).order_matrix(campaign_id)
    buffer = StringIO()
    writer = csv.writer(buffer)

    writer.writerow(
        [
            "Produto",
            "Produtor",
            "Preço venda",
            "Preço revenda",
            *matrix.customer_names,
            "Quantidade total",
            "Total venda",
            "Total revenda",
            "Margem",
        ],
    )

    for row in matrix.rows:
        writer.writerow(
            [
                row.product_name,
                row.producer_name,
                row.unit_price,
                row.cost_price,
                *[row.customers.get(customer, 0) for customer in matrix.customer_names],
                row.quantity_total,
                row.sale_total,
                row.cost_total,
                row.margin_total,
            ],
        )

    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f"attachment; filename=order-matrix-{campaign_id}.csv"
            ),
        },
    )
