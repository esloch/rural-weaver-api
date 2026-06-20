from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.campaigns import CampaignRepository
from apps.api.app.schemas.campaigns import SalesCampaignDetailRead

router = APIRouter()


@router.get("/active", response_model=SalesCampaignDetailRead)
def get_active_campaign(
    db: Session = Depends(get_db),
) -> SalesCampaignDetailRead:
    """Return the current open campaign for the public order form."""

    campaign = CampaignRepository(db).get_active_detail()
    if campaign is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active sales campaign configured.",
        )
    return campaign


@router.get("/{campaign_id}", response_model=SalesCampaignDetailRead)
def get_campaign(
    campaign_id: UUID,
    db: Session = Depends(get_db),
) -> SalesCampaignDetailRead:
    """Return a campaign with its available products."""

    campaign = CampaignRepository(db).get_detail(campaign_id)
    if campaign is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found.",
        )
    return campaign
