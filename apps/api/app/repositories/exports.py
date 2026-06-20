import csv
import io
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.order import Order, OrderItem


class ExportRepository:
    """CSV exports used by weekly operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def campaign_labels_csv(self, campaign_id: UUID) -> str:
        orders = self._campaign_orders(campaign_id)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["customer_name", "phone", "delivery", "address"])
        for order in orders:
            writer.writerow(
                [
                    order.customer_name,
                    order.customer_phone,
                    order.pickup_point or order.delivery_type,
                    order.address or "",
                ],
            )
        return output.getvalue()

    def campaign_picking_list_csv(self, campaign_id: UUID) -> str:
        items = self.db.execute(
            select(OrderItem.name_snapshot, OrderItem.quantity)
            .join(Order, OrderItem.order_id == Order.id)
            .where(Order.campaign_id == campaign_id),
        ).all()

        totals: dict[str, float] = {}
        for name, quantity in items:
            totals[name] = totals.get(name, 0.0) + float(quantity)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["item", "total_quantity"])
        for name, quantity in sorted(totals.items()):
            writer.writerow([name, quantity])
        return output.getvalue()

    def _campaign_orders(self, campaign_id: UUID) -> list[Order]:
        return list(
            self.db.scalars(
                select(Order)
                .where(Order.campaign_id == campaign_id)
                .order_by(Order.created_at.asc()),
            ).all(),
        )
