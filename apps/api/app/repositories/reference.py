from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.campaign import DeliveryZone, PickupPoint
from apps.api.app.models.payment_method import PaymentMethod
from apps.api.app.models.subscription import SubscriptionPlan


class ReferenceRepository:
    """Read-only operational reference data."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_pickup_points(self) -> list[PickupPoint]:
        stmt = (
            select(PickupPoint)
            .where(PickupPoint.is_active.is_(True))
            .order_by(PickupPoint.city.asc(), PickupPoint.name.asc())
        )
        return list(self.db.scalars(stmt).all())

    def list_delivery_zones(self) -> list[DeliveryZone]:
        stmt = (
            select(DeliveryZone)
            .where(DeliveryZone.is_active.is_(True))
            .order_by(DeliveryZone.city.asc(), DeliveryZone.name.asc())
        )
        return list(self.db.scalars(stmt).all())

    def list_payment_methods(self) -> list[PaymentMethod]:
        stmt = (
            select(PaymentMethod)
            .where(PaymentMethod.is_active.is_(True))
            .order_by(PaymentMethod.name.asc())
        )
        return list(self.db.scalars(stmt).all())

    def list_subscription_plans(self) -> list[SubscriptionPlan]:
        stmt = (
            select(SubscriptionPlan)
            .where(SubscriptionPlan.is_active.is_(True))
            .order_by(SubscriptionPlan.price.asc())
        )
        return list(self.db.scalars(stmt).all())
