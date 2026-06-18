from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.payment import PaymentSetting


class PaymentSettingsRepository:
    """Persistence operations for payment settings."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_active(self) -> PaymentSetting | None:
        stmt = (
            select(PaymentSetting)
            .where(PaymentSetting.is_active.is_(True))
            .order_by(PaymentSetting.updated_at.desc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()
