from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.app.db.session import get_db
from apps.api.app.repositories.admin import AdminRepository
from apps.api.app.repositories.payments import PaymentSettingsRepository
from apps.api.app.repositories.stock import StockRepository
from apps.api.app.schemas.admin import AdminDashboardRead
from apps.api.app.schemas.inventory import (
    AdminInventoryRead,
    StockAdjustmentRequest,
    StockMovementRead,
)
from apps.api.app.schemas.orders import OrderRead
from apps.api.app.schemas.payments import (
    PaymentSettingRead,
    PaymentSettingUpdate,
)
from apps.api.app.schemas.products import ProductRead

router = APIRouter()


@router.get("/dashboard", response_model=AdminDashboardRead)
def get_admin_dashboard(db: Session = Depends(get_db)) -> AdminDashboardRead:
    """Return operational dashboard metrics."""

    return AdminRepository(db).get_dashboard()


@router.get("/orders", response_model=list[OrderRead])
def list_admin_orders(db: Session = Depends(get_db)) -> list[OrderRead]:
    """List orders for admin screens."""

    return AdminRepository(db).list_orders()


@router.get("/products", response_model=list[ProductRead])
def list_admin_products(db: Session = Depends(get_db)) -> list[ProductRead]:
    """List all products for admin screens."""

    return AdminRepository(db).list_products()


@router.get("/inventory", response_model=AdminInventoryRead)
def get_admin_inventory(db: Session = Depends(get_db)) -> AdminInventoryRead:
    """Return products and stock movements for the inventory screen."""

    return StockRepository(db).get_inventory()


@router.get("/stock-movements", response_model=list[StockMovementRead])
def list_stock_movements(
    db: Session = Depends(get_db),
) -> list[StockMovementRead]:
    """List stock movement history."""

    return StockRepository(db).list_movements()


@router.patch("/products/{product_id}/stock", response_model=ProductRead)
def update_admin_product_stock(
    product_id: UUID,
    payload: StockAdjustmentRequest,
    db: Session = Depends(get_db),
) -> ProductRead:
    """Adjust product stock and create an immutable stock movement."""

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


@router.get("/payment-settings", response_model=PaymentSettingRead)
def get_admin_payment_settings(
    db: Session = Depends(get_db),
) -> PaymentSettingRead:
    """Return active payment settings for admin editing."""

    payment_setting = PaymentSettingsRepository(db).get_active()
    if payment_setting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active payment setting configured.",
        )
    return payment_setting


@router.patch("/payment-settings", response_model=PaymentSettingRead)
def update_admin_payment_settings(
    payload: PaymentSettingUpdate,
    db: Session = Depends(get_db),
) -> PaymentSettingRead:
    """Update active manual Pix payment settings."""

    repo = PaymentSettingsRepository(db)
    payment_setting = repo.get_active()

    if payment_setting is None:
        payment_setting = repo.create_from_update(payload)
    else:
        payment_setting = repo.update(payment_setting.id, payload)

    db.commit()
    db.refresh(payment_setting)
    return payment_setting


@router.patch("/orders/{order_id}", response_model=OrderRead)
def update_order_status(
    order_id: UUID,
    payload: dict[str, str],
    db: Session = Depends(get_db),
) -> OrderRead:
    """Update basic order status fields."""

    order = AdminRepository(db).update_order_status(
        order_id=order_id,
        status_value=payload.get("status"),
        payment_status=payload.get("payment_status"),
    )
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    db.commit()
    db.refresh(order)
    return order
