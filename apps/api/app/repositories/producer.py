from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.order import Order
from apps.api.app.models.producer import Producer
from apps.api.app.models.product import Product


class ProducerRepository:
    """Producer portal operations.

    The MVP uses the first active producer as a demo producer until JWT/RBAC is
    implemented.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_demo_producer(self) -> Producer | None:
        stmt = (
            select(Producer)
            .where(Producer.status == "active")
            .order_by(Producer.created_at.asc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()

    def list_demo_producer_products(self) -> list[Product]:
        producer = self.get_demo_producer()
        if producer is None:
            return []

        stmt = (
            select(Product)
            .where(Product.producer_id == producer.id)
            .order_by(Product.name.asc())
        )
        return list(self.db.scalars(stmt).all())

    def list_demo_producer_orders(self) -> list[Order]:
        stmt = select(Order).order_by(Order.created_at.desc())
        return list(self.db.scalars(stmt).all())
