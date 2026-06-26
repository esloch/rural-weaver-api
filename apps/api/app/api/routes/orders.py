from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.admin import AdminRepository
from apps.api.app.repositories.orders import OrderRepository
from apps.api.app.schemas.orders import OrderCreate, OrderRead
from packages.business_rules.customers import CustomerValidationError

router = APIRouter()


@router.get("", response_model=list[OrderRead])
def list_orders_for_smoke_test(
    db: Session = Depends(get_db),
) -> list[OrderRead]:
    """Temporary read-only order list."""

    return AdminRepository(db).list_orders()


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
) -> OrderRead:
    """Create a customer order with price snapshots and stock validation."""

    try:
        order = OrderRepository(db).create(payload)
    except CustomerValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    db.commit()
    db.refresh(order)
    return order
