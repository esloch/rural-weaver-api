from decimal import Decimal

from sqlalchemy.orm import Session

from apps.api.app.models.order import Order, OrderItem
from apps.api.app.models.product import BasketType, Product
from apps.api.app.models.stock import StockMovement
from apps.api.app.schemas.orders import OrderCreate
from packages.business_rules.orders import (
    calculate_item_total,
    ensure_stock_available,
)


class OrderRepository:
    """Order creation and snapshot persistence."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: OrderCreate) -> Order:
        if not payload.items:
            raise ValueError("Order must contain at least one item.")

        order_items: list[OrderItem] = []
        subtotal = Decimal("0.00")

        for item in payload.items:
            if item.item_type == "product":
                product = self._get_product_for_order(str(item.product_id))
                unit_price = product.price
                quantity = item.quantity
                ensure_stock_available(product.stock_quantity, quantity)
                total = calculate_item_total(unit_price, quantity)
                subtotal += total

                product.stock_quantity = product.stock_quantity - quantity
                self.db.add(
                    StockMovement(
                        product_id=product.id,
                        type="order_reserved",
                        quantity=-quantity,
                        reason="Order creation",
                        created_by=None,
                    ),
                )

                order_items.append(
                    OrderItem(
                        product_id=product.id,
                        basket_type_id=None,
                        item_type="product",
                        name_snapshot=product.name,
                        unit_price_snapshot=unit_price,
                        quantity=quantity,
                        total_snapshot=total,
                    ),
                )
            elif item.item_type == "basket":
                basket = self._get_basket_for_order(str(item.basket_type_id))
                unit_price = basket.base_price
                quantity = item.quantity
                total = calculate_item_total(unit_price, quantity)
                subtotal += total

                order_items.append(
                    OrderItem(
                        product_id=None,
                        basket_type_id=basket.id,
                        item_type="basket",
                        name_snapshot=basket.name,
                        unit_price_snapshot=unit_price,
                        quantity=quantity,
                        total_snapshot=total,
                    ),
                )
            else:
                raise ValueError(f"Invalid item type: {item.item_type}")

        order = Order(
            customer_name=payload.customer_name,
            customer_phone=payload.customer_phone,
            customer_email=payload.customer_email,
            delivery_type=payload.delivery_type,
            pickup_point=payload.pickup_point,
            address=payload.address,
            status="submitted",
            payment_method="pix_manual",
            payment_status="pending",
            subtotal=subtotal,
            total=subtotal,
            notes=payload.notes,
        )
        self.db.add(order)
        self.db.flush()

        for order_item in order_items:
            order_item.order_id = order.id
            self.db.add(order_item)

        self.db.flush()
        return order

    def _get_product_for_order(self, product_id: str) -> Product:
        if not product_id:
            raise ValueError("product_id is required for product items.")

        product = self.db.get(Product, product_id)
        if product is None:
            raise ValueError("Product not found.")

        if not product.is_active:
            raise ValueError("Inactive product cannot be ordered.")

        return product

    def _get_basket_for_order(self, basket_type_id: str) -> BasketType:
        if not basket_type_id:
            raise ValueError("basket_type_id is required for basket items.")

        basket = self.db.get(BasketType, basket_type_id)
        if basket is None:
            raise ValueError("Basket type not found.")

        if not basket.is_active:
            raise ValueError("Inactive basket cannot be ordered.")

        return basket
