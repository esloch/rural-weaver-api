from decimal import Decimal

from pydantic import BaseModel

from apps.api.app.schemas.orders import OrderRead
from apps.api.app.schemas.products import ProductRead


class AdminDashboardRead(BaseModel):
    """Operational dashboard response."""

    total_orders: int
    pending_payments: int
    revenue_estimate: Decimal
    low_stock_products: int
    recent_orders: list[OrderRead]
    low_stock_items: list[ProductRead]
