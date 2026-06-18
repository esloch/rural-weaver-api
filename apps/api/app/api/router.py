from fastapi import APIRouter

from apps.api.app.api.routes import health, payments, products

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(
    payments.router,
    prefix="/payment-settings",
    tags=["payments"],
)
