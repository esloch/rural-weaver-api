from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from apps.api.app.models.order import Order
from apps.api.app.models.producer import Producer
from apps.api.app.models.product import Product
from apps.api.app.repositories.stock import StockRepository
from apps.api.app.schemas.admin import AdminDashboardRead
from apps.api.app.schemas.products import ProductCreate, ProductUpdate


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

    def create_product(self, payload: ProductCreate) -> Product:
        producer = self._resolve_producer(payload.producer_id)
        if producer is None:
            raise ValueError("No active producer available for product creation.")

        price = Decimal(payload.price)
        sale_price = (
            Decimal(payload.sale_price)
            if payload.sale_price is not None
            else price
        )
        cost_price = (
            Decimal(payload.cost_price)
            if payload.cost_price is not None
            else None
        )

        product = Product(
            producer_id=producer.id,
            producer_name_snapshot=(
                self._clean_text(payload.producer_name_snapshot) or producer.name
            ),
            name=self._required_text(payload.name, "name"),
            description=self._clean_text(payload.description),
            category=self._clean_text(payload.category) or "other",
            offer_type=self._clean_text(payload.offer_type) or "weekly_offer",
            unit=self._required_text(payload.unit, "unit"),
            price=price,
            cost_price=cost_price,
            sale_price=sale_price,
            stock_quantity=Decimal(payload.stock_quantity),
            image_url=self._clean_text(payload.image_url),
            is_refrigerated=payload.is_refrigerated,
            is_frozen=payload.is_frozen,
            is_addon=payload.is_addon,
            is_donation=payload.is_donation,
            is_active=payload.is_active,
        )
        self.db.add(product)
        self.db.flush()
        return product

    def update_product(
        self,
        product_id: UUID,
        payload: ProductUpdate,
    ) -> Product | None:
        product = self.db.get(Product, product_id)
        if product is None:
            return None

        if payload.producer_id is not None:
            producer = self._resolve_producer(payload.producer_id)
            if producer is None:
                raise ValueError("Producer not found.")
            product.producer_id = producer.id
            if not self._clean_text(payload.producer_name_snapshot):
                product.producer_name_snapshot = producer.name

        if payload.producer_name_snapshot is not None:
            product.producer_name_snapshot = self._clean_text(
                payload.producer_name_snapshot,
            )

        if payload.name is not None:
            product.name = self._required_text(payload.name, "name")

        if payload.description is not None:
            product.description = self._clean_text(payload.description)

        if payload.category is not None:
            product.category = self._clean_text(payload.category) or "other"

        if payload.offer_type is not None:
            product.offer_type = (
                self._clean_text(payload.offer_type) or product.offer_type
            )

        if payload.unit is not None:
            product.unit = self._required_text(payload.unit, "unit")

        if payload.price is not None:
            product.price = Decimal(payload.price)

        if payload.cost_price is not None:
            product.cost_price = Decimal(payload.cost_price)

        if payload.sale_price is not None:
            product.sale_price = Decimal(payload.sale_price)

        if payload.stock_quantity is not None:
            new_quantity = Decimal(payload.stock_quantity)
            delta = new_quantity - product.stock_quantity
            if delta != 0:
                movement_type = "restock" if delta > 0 else "adjustment"
                StockRepository(self.db).adjust_stock(
                    product_id=product.id,
                    quantity_delta=delta,
                    reason="Admin product edit",
                    movement_type=movement_type,
                    created_by=None,
                )

        if payload.image_url is not None:
            product.image_url = self._clean_text(payload.image_url)

        if payload.is_refrigerated is not None:
            product.is_refrigerated = payload.is_refrigerated

        if payload.is_frozen is not None:
            product.is_frozen = payload.is_frozen

        if payload.is_addon is not None:
            product.is_addon = payload.is_addon

        if payload.is_donation is not None:
            product.is_donation = payload.is_donation

        if payload.is_active is not None:
            product.is_active = payload.is_active

        if payload.sale_price is None and payload.price is not None:
            product.sale_price = product.price

        return product

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

    def _resolve_producer(self, producer_id: UUID | None) -> Producer | None:
        if producer_id is not None:
            return self.db.get(Producer, producer_id)

        stmt = (
            select(Producer)
            .where(Producer.status == "active")
            .order_by(Producer.created_at.asc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()

    def _clean_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    def _required_text(self, value: str, field_name: str) -> str:
        cleaned = self._clean_text(value)
        if cleaned is None:
            raise ValueError(f"Product {field_name} is required.")
        return cleaned
