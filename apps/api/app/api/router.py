from fastapi import APIRouter

from apps.api.app.api.routes import (
    admin,
    baskets,
    campaigns,
    health,
    orders,
    payments,
    producer,
    products,
    reference,
    settlements,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(
    baskets.router,
    prefix="/basket-types",
    tags=["basket-types"],
)
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(reference.router, prefix="/reference", tags=["reference"])
api_router.include_router(
    payments.router,
    prefix="/payment-settings",
    tags=["payments"],
)
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(settlements.router, prefix="/admin", tags=["admin-settlements"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(
    producer.router,
    prefix="/producer",
    tags=["producer"],
)
