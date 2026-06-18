from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from apps.api.app.models.order import Order
from apps.api.app.models.product import Product
from apps.api.app.schemas.admin import AdminDashboardRead


class AdminRepository:
    """Read/write operations used by admin endpoints."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_products(self) -> list[Product]:
        stmt = select(Product).order_by(Product.name.asc())
        return list(self.db.scalars(stmt).all())

    def list_orders(self) -> list[Order]:
        stmt = select(Order).order_by(Order.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get_dashboard(self) -> AdminDashboardRead:
        total_orders = self.db.scalar(select(func.count(Order.id))) or 0
        pending_payments = (
            self.db.scalar(
                select(func.count(Order.id)).where(
                    Order.payment_status == "pending",
                ),
            )
            or 0
        )
        revenue = (
            self.db.scalar(
                select(func.coalesce(func.sum(Order.total), Decimal("0"))),
            )
            or Decimal("0")
        )
        low_stock_products = (
            self.db.scalar(
                select(func.count(Product.id)).where(
                    Product.stock_quantity <= 5,
                    Product.is_active.is_(True),
                ),
            )
            or 0
        )

        return AdminDashboardRead(
            total_orders=int(total_orders),
            pending_payments=int(pending_payments),
            revenue_estimate=Decimal(revenue),
            low_stock_products=int(low_stock_products),
            recent_orders=self.list_orders()[:5],
            low_stock_items=self._list_low_stock_products(),
        )

    def _list_low_stock_products(self) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.stock_quantity <= 5, Product.is_active.is_(True))
            .order_by(Product.stock_quantity.asc())
            .limit(10)
        )
        return list(self.db.scalars(stmt).all())

    def update_order_status(
        self,
        order_id: UUID,
        status_value: str | None,
        payment_status: str | None,
    ) -> Order | None:
        order = self.db.get(Order, order_id)
        if order is None:
            return None

        if status_value is not None:
            order.status = status_value

        if payment_status is not None:
            order.payment_status = payment_status

        return order
