from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.reference import ReferenceRepository
from apps.api.app.schemas.reference import (
    DeliveryZoneRead,
    PaymentMethodRead,
    PickupPointRead,
    SubscriptionPlanRead,
)

router = APIRouter()


@router.get("/pickup-points", response_model=list[PickupPointRead])
def list_pickup_points(
    db: Session = Depends(get_db),
) -> list[PickupPointRead]:
    return ReferenceRepository(db).list_pickup_points()


@router.get("/delivery-zones", response_model=list[DeliveryZoneRead])
def list_delivery_zones(
    db: Session = Depends(get_db),
) -> list[DeliveryZoneRead]:
    return ReferenceRepository(db).list_delivery_zones()


@router.get("/payment-methods", response_model=list[PaymentMethodRead])
def list_payment_methods(
    db: Session = Depends(get_db),
) -> list[PaymentMethodRead]:
    return ReferenceRepository(db).list_payment_methods()


@router.get("/subscription-plans", response_model=list[SubscriptionPlanRead])
def list_subscription_plans(
    db: Session = Depends(get_db),
) -> list[SubscriptionPlanRead]:
    return ReferenceRepository(db).list_subscription_plans()
