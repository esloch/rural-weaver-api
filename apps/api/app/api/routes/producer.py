from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.producer import ProducerRepository
from apps.api.app.repositories.stock import StockRepository
from apps.api.app.schemas.inventory import StockAdjustmentRequest
from apps.api.app.schemas.orders import OrderRead
from apps.api.app.schemas.products import ProductRead

router = APIRouter()


@router.get("/products", response_model=list[ProductRead])
def list_producer_products(db: Session = Depends(get_db)) -> list[ProductRead]:
    """List products visible to the producer portal.

    MVP note: authentication/RBAC is deferred. The first producer is used as
    the demo producer until JWT permissions are implemented.
    """

    return ProducerRepository(db).list_demo_producer_products()


@router.patch("/products/{product_id}/stock", response_model=ProductRead)
def update_producer_product_stock(
    product_id: UUID,
    payload: StockAdjustmentRequest,
    db: Session = Depends(get_db),
) -> ProductRead:
    """Update stock for a producer product.

    MVP note: producer ownership checks are deferred to JWT/RBAC phase.
    """

    try:
        product = StockRepository(db).adjust_stock(
            product_id=product_id,
            quantity_delta=payload.quantity_delta,
            reason=payload.reason,
            movement_type=payload.type,
            created_by=None,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    db.commit()
    db.refresh(product)
    return product


@router.get("/orders", response_model=list[OrderRead])
def list_producer_orders(db: Session = Depends(get_db)) -> list[OrderRead]:
    """List orders visible to the producer portal."""

    return ProducerRepository(db).list_demo_producer_orders()
