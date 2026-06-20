from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.campaigns import CampaignRepository
from apps.api.app.repositories.exports import ExportRepository
from apps.api.app.schemas.campaigns import (
    CampaignProductCreate,
    CampaignProductRead,
    CampaignProductUpdate,
    SalesCampaignCreate,
    SalesCampaignDetailRead,
    SalesCampaignRead,
    SalesCampaignUpdate,
)
from apps.api.app.schemas.orders import OrderRead

router = APIRouter()


@router.get("/campaigns", response_model=list[SalesCampaignRead])
def list_campaigns(db: Session = Depends(get_db)) -> list[SalesCampaignRead]:
    return CampaignRepository(db).list_campaigns()


@router.post(
    "/campaigns",
    response_model=SalesCampaignRead,
    status_code=status.HTTP_201_CREATED,
)
def create_campaign(
    payload: SalesCampaignCreate,
    db: Session = Depends(get_db),
) -> SalesCampaignRead:
    campaign = CampaignRepository(db).create_campaign(payload)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/campaigns/{campaign_id}", response_model=SalesCampaignDetailRead)
def get_campaign(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> SalesCampaignDetailRead:
    campaign = CampaignRepository(db).get_detail(campaign_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found.")
    return campaign


@router.patch("/campaigns/{campaign_id}", response_model=SalesCampaignRead)
def update_campaign(
    campaign_id: UUID,
    payload: SalesCampaignUpdate,
    db: Session = Depends(get_db),
) -> SalesCampaignRead:
    campaign = CampaignRepository(db).update_campaign(campaign_id, payload)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found.")
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/campaigns/{campaign_id}/orders", response_model=list[OrderRead])
def list_campaign_orders(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> list[OrderRead]:
    return CampaignRepository(db).list_campaign_orders(campaign_id)


@router.get(
    "/campaigns/{campaign_id}/products",
    response_model=list[CampaignProductRead],
)
def list_campaign_products(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> list[CampaignProductRead]:
    return CampaignRepository(db).list_campaign_products(campaign_id)


@router.post(
    "/campaigns/{campaign_id}/products",
    response_model=CampaignProductRead,
    status_code=status.HTTP_201_CREATED,
)
def add_campaign_product(
    campaign_id: UUID,
    payload: CampaignProductCreate,
    db: Session = Depends(get_db),
) -> CampaignProductRead:
    try:
        campaign_product = CampaignRepository(db).add_campaign_product(
            campaign_id,
            payload,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    db.commit()
    db.refresh(campaign_product)
    return campaign_product


@router.patch(
    "/campaign-products/{campaign_product_id}",
    response_model=CampaignProductRead,
)
def update_campaign_product(
    campaign_product_id: UUID,
    payload: CampaignProductUpdate,
    db: Session = Depends(get_db),
) -> CampaignProductRead:
    campaign_product = CampaignRepository(db).update_campaign_product(
        campaign_product_id,
        payload,
    )
    if campaign_product is None:
        raise HTTPException(status_code=404, detail="Campaign product not found.")

    db.commit()
    db.refresh(campaign_product)
    return campaign_product


@router.get("/campaigns/{campaign_id}/labels")
def campaign_labels(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    data = ExportRepository(db).campaign_labels_csv(campaign_id)
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=labels.csv"},
    )


@router.get("/campaigns/{campaign_id}/picking-list")
def campaign_picking_list(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    data = ExportRepository(db).campaign_picking_list_csv(campaign_id)
    return Response(
        content=data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=picking-list.csv",
        },
    )
