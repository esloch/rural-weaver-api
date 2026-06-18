from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.payments import PaymentSettingsRepository
from apps.api.app.schemas.payments import PaymentSettingRead

router = APIRouter()


@router.get("/active", response_model=PaymentSettingRead)
def get_active_payment_setting(
    db: Session = Depends(get_db),
) -> PaymentSettingRead:
    """Return the active manual Pix payment configuration."""

    payment_setting = PaymentSettingsRepository(db).get_active()
    if payment_setting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active payment setting configured.",
        )
    return payment_setting
