from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.campaign import CampaignProduct, SalesCampaign
from apps.api.app.models.order import Order, OrderItem
from apps.api.app.models.payment_method import PaymentMethod
from apps.api.app.models.product import BasketType, Product
from apps.api.app.models.stock import StockMovement
from apps.api.app.schemas.orders import OrderCreate
from packages.business_rules.orders import (
    calculate_item_total,
    ensure_stock_available,
)


ZERO = Decimal("0.00")


class OrderRepository:
    """Order creation and financial snapshot persistence."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: OrderCreate) -> Order:
        if not payload.items:
            raise ValueError("Order must contain at least one item.")

        campaign_id = payload.campaign_id or self._get_default_campaign_id()
        order_items: list[OrderItem] = []
        subtotal = ZERO

        for item in payload.items:
            if item.item_type == "campaign_product":
                campaign_product = self._get_campaign_product_for_order(
                    item.campaign_product_id,
                )
                available = (
                    campaign_product.available_quantity
                    - campaign_product.reserved_quantity
                )
                quantity = item.quantity
                ensure_stock_available(available, quantity)

                sale_price = (
                    campaign_product.sale_price_snapshot
                    or campaign_product.price
                )
                cost_price = campaign_product.cost_price_snapshot or ZERO
                sale_total = calculate_item_total(sale_price, quantity)
                cost_total = calculate_item_total(cost_price, quantity)
                margin_total = sale_total - cost_total
                subtotal += sale_total

                campaign_product.reserved_quantity += quantity

                order_items.append(
                    OrderItem(
                        product_id=campaign_product.product_id,
                        basket_type_id=None,
                        campaign_product_id=campaign_product.id,
                        item_type="campaign_product",
                        offer_type=campaign_product.offer_type,
                        name_snapshot=campaign_product.name_snapshot,
                        producer_name_snapshot=(
                            campaign_product.producer_name_snapshot
                        ),
                        unit_price_snapshot=sale_price,
                        unit_cost_snapshot=cost_price,
                        unit_sale_price_snapshot=sale_price,
                        cost_total_snapshot=cost_total,
                        sale_total_snapshot=sale_total,
                        margin_total_snapshot=margin_total,
                        quantity=quantity,
                        total_snapshot=sale_total,
                    ),
                )
            elif item.item_type == "product":
                product = self._get_product_for_order(str(item.product_id))
                quantity = item.quantity
                ensure_stock_available(product.stock_quantity, quantity)

                sale_price = product.sale_price or product.price
                cost_price = product.cost_price or ZERO
                sale_total = calculate_item_total(sale_price, quantity)
                cost_total = calculate_item_total(cost_price, quantity)
                margin_total = sale_total - cost_total
                subtotal += sale_total

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
                        campaign_product_id=None,
                        item_type="product",
                        offer_type=product.offer_type,
                        name_snapshot=product.name,
                        producer_name_snapshot=product.producer_name_snapshot,
                        unit_price_snapshot=sale_price,
                        unit_cost_snapshot=cost_price,
                        unit_sale_price_snapshot=sale_price,
                        cost_total_snapshot=cost_total,
                        sale_total_snapshot=sale_total,
                        margin_total_snapshot=margin_total,
                        quantity=quantity,
                        total_snapshot=sale_total,
                    ),
                )
            elif item.item_type == "basket":
                basket = self._get_basket_for_order(str(item.basket_type_id))
                sale_total = calculate_item_total(basket.base_price, item.quantity)
                subtotal += sale_total

                order_items.append(
                    OrderItem(
                        product_id=None,
                        basket_type_id=basket.id,
                        campaign_product_id=None,
                        item_type="basket",
                        offer_type="csa_basket",
                        name_snapshot=basket.name,
                        producer_name_snapshot="Delícias da Roça",
                        unit_price_snapshot=basket.base_price,
                        unit_cost_snapshot=ZERO,
                        unit_sale_price_snapshot=basket.base_price,
                        cost_total_snapshot=ZERO,
                        sale_total_snapshot=sale_total,
                        margin_total_snapshot=sale_total,
                        quantity=item.quantity,
                        total_snapshot=sale_total,
                    ),
                )
            else:
                raise ValueError(f"Invalid item type: {item.item_type}")

        delivery_fee = payload.delivery_fee or ZERO
        gross_total = subtotal + delivery_fee
        payment_fee_amount = self._calculate_payment_fee(
            payload.payment_method_id,
            gross_total,
        )
        net_total_after_fees = gross_total - payment_fee_amount
        payment_method = payload.payment_method or "pix_manual"

        order = Order(
            campaign_id=campaign_id,
            customer_id=payload.customer_id,
            pickup_point_id=payload.pickup_point_id,
            delivery_zone_id=payload.delivery_zone_id,
            payment_method_id=payload.payment_method_id,
            source="web",
            confirmation_status="pending",
            submitted_at=datetime.now(UTC),
            confirmed_at=None,
            customer_name=payload.customer_name,
            customer_phone=payload.customer_phone,
            customer_email=payload.customer_email,
            delivery_type=payload.delivery_type,
            pickup_point=payload.pickup_point,
            address=payload.address,
            neighborhood=payload.neighborhood,
            city=payload.city,
            complement=payload.complement,
            delivery_agent=payload.delivery_agent,
            status="submitted",
            payment_method=payment_method,
            payment_status="pending",
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            payment_fee_amount=payment_fee_amount,
            net_total_after_fees=net_total_after_fees,
            total=gross_total,
            notes=payload.notes,
        )
        self.db.add(order)
        self.db.flush()

        for order_item in order_items:
            order_item.order_id = order.id
            self.db.add(order_item)

        self.db.flush()
        return order

    def _calculate_payment_fee(
        self,
        payment_method_id: UUID | None,
        gross_total: Decimal,
    ) -> Decimal:
        if payment_method_id is None:
            return ZERO

        method = self.db.get(PaymentMethod, payment_method_id)
        if method is None:
            return ZERO

        fixed = method.fee_fixed or ZERO
        percent = method.fee_percent or ZERO
        variable = gross_total * percent / Decimal("100")
        return (fixed + variable).quantize(Decimal("0.01"))

    def _get_default_campaign_id(self) -> UUID | None:
        stmt = (
            select(SalesCampaign)
            .where(SalesCampaign.status == "open")
            .order_by(SalesCampaign.delivery_date.asc())
            .limit(1)
        )
        campaign = self.db.scalars(stmt).first()
        if campaign is None:
            return None
        return campaign.id

    def _get_campaign_product_for_order(
        self,
        campaign_product_id: UUID | None,
    ) -> CampaignProduct:
        if campaign_product_id is None:
            raise ValueError("campaign_product_id is required.")

        campaign_product = self.db.get(CampaignProduct, campaign_product_id)
        if campaign_product is None:
            raise ValueError("Campaign product not found.")

        if not campaign_product.is_active:
            raise ValueError("Inactive campaign product cannot be ordered.")

        return campaign_product

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
