from datetime import date
from decimal import Decimal

from apps.api.app.db.session import SessionLocal
from apps.api.app.models.campaign import (
    CampaignProduct,
    DeliveryZone,
    PickupPoint,
    SalesCampaign,
)
from apps.api.app.models.order import Order
from apps.api.app.models.product import Product


def seed() -> None:
    """Seed the first weekly campaign for Alice's operation."""

    db = SessionLocal()
    try:
        existing = (
            db.query(SalesCampaign)
            .filter(SalesCampaign.name == "16 de Junho - Cesta Agroecológica")
            .one_or_none()
        )
        if existing is not None:
            print("Campaign seed already exists. Nothing to do.")
            return

        campaign = SalesCampaign(
            name="16 de Junho - Cesta Agroecológica",
            description=(
                "Campanha semanal para pedidos da cesta agroecológica, "
                "com retirada na UFSC - DCE."
            ),
            delivery_date=date(2026, 6, 16),
            status="open",
        )
        db.add(campaign)
        db.flush()

        products = db.query(Product).filter(Product.is_active.is_(True)).all()
        for product in products:
            db.add(
                CampaignProduct(
                    campaign_id=campaign.id,
                    product_id=product.id,
                    name_snapshot=product.name,
                    unit_snapshot=product.unit,
                    price=product.price,
                    available_quantity=product.stock_quantity,
                    reserved_quantity=Decimal("0"),
                    is_active=True,
                ),
            )

        db.add(
            PickupPoint(
                name="UFSC - DCE",
                address="Universidade Federal de Santa Catarina",
                instructions="Retirada das 13:00 às 15:00.",
                is_active=True,
            ),
        )
        db.add(
            DeliveryZone(
                name="Entrega local",
                fee=Decimal("10.00"),
                instructions="Entrega conforme confirmação manual.",
                is_active=True,
            ),
        )

        demo_orders = db.query(Order).filter(Order.campaign_id.is_(None)).all()
        for order in demo_orders:
            order.campaign_id = campaign.id

        db.commit()
        print("Campaign seed created successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
