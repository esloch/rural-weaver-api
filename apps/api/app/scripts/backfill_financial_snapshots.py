from decimal import Decimal

from sqlalchemy import select

from apps.api.app.db.session import SessionLocal

# Import all SQLAlchemy models so foreign keys such as orders.customer_id
# can resolve referenced tables during ORM flush/commit.
import apps.api.app.db.base  # noqa: F401
from apps.api.app.models.campaign import CampaignProduct
from apps.api.app.models.order import Order, OrderItem
from apps.api.app.models.product import Product


ZERO = Decimal("0.00")


def main() -> None:
    db = SessionLocal()
    updated_items = 0
    updated_orders = 0

    try:
        items = db.scalars(select(OrderItem)).all()
        for item in items:
            sale_price = item.unit_sale_price_snapshot or item.unit_price_snapshot
            cost_price = item.unit_cost_snapshot

            if cost_price is None and item.campaign_product_id is not None:
                campaign_product = db.get(CampaignProduct, item.campaign_product_id)
                if campaign_product is not None:
                    cost_price = campaign_product.cost_price_snapshot or ZERO
                    sale_price = (
                        campaign_product.sale_price_snapshot
                        or campaign_product.price
                        or sale_price
                    )
                    item.producer_name_snapshot = (
                        item.producer_name_snapshot
                        or campaign_product.producer_name_snapshot
                    )
                    item.offer_type = item.offer_type or campaign_product.offer_type

            if cost_price is None and item.product_id is not None:
                product = db.get(Product, item.product_id)
                if product is not None:
                    cost_price = product.cost_price or ZERO
                    sale_price = product.sale_price or product.price or sale_price
                    item.producer_name_snapshot = (
                        item.producer_name_snapshot
                        or product.producer_name_snapshot
                    )
                    item.offer_type = item.offer_type or product.offer_type

            cost_price = cost_price or ZERO
            sale_total = sale_price * item.quantity
            cost_total = cost_price * item.quantity
            margin_total = sale_total - cost_total

            item.unit_sale_price_snapshot = sale_price
            item.unit_cost_snapshot = cost_price
            item.sale_total_snapshot = sale_total
            item.cost_total_snapshot = cost_total
            item.margin_total_snapshot = margin_total
            item.total_snapshot = sale_total
            item.unit_price_snapshot = sale_price
            updated_items += 1

        orders = db.scalars(select(Order)).all()
        for order in orders:
            order.payment_fee_amount = order.payment_fee_amount or ZERO
            order.net_total_after_fees = (
                order.net_total_after_fees
                or (order.total - order.payment_fee_amount)
            )
            updated_orders += 1

        db.commit()
        print(f"Backfilled {updated_items} order items.")
        print(f"Backfilled {updated_orders} orders.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
