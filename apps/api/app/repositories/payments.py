from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.payment import PaymentSetting
from apps.api.app.schemas.payments import PaymentSettingUpdate


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

    def create_from_update(
        self,
        payload: PaymentSettingUpdate,
    ) -> PaymentSetting:
        values = payload.model_dump(exclude_unset=True)
        payment_setting = PaymentSetting(**values)
        self.db.add(payment_setting)
        self.db.flush()
        return payment_setting

    def update(
        self,
        payment_setting_id: UUID,
        payload: PaymentSettingUpdate,
    ) -> PaymentSetting:
        payment_setting = self.db.get(PaymentSetting, payment_setting_id)
        if payment_setting is None:
            raise ValueError("Payment setting not found.")

        values = payload.model_dump(exclude_unset=True)
        for field, value in values.items():
            setattr(payment_setting, field, value)

        self.db.flush()
        return payment_setting
