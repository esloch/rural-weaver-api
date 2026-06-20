from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.api.app.models.campaign import (
    CampaignProduct,
    CampaignRule,
    SalesCampaign,
)
from apps.api.app.models.order import Order
from apps.api.app.models.product import Product
from apps.api.app.schemas.campaigns import (
    CampaignProductCreate,
    CampaignProductUpdate,
    SalesCampaignCreate,
    SalesCampaignDetailRead,
    SalesCampaignUpdate,
)


class CampaignRepository:
    """Campaign persistence and weekly-offer operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_campaigns(self) -> list[SalesCampaign]:
        stmt = select(SalesCampaign).order_by(
            SalesCampaign.delivery_date.desc(),
        )
        return list(self.db.scalars(stmt).all())

    def create_campaign(self, payload: SalesCampaignCreate) -> SalesCampaign:
        campaign = SalesCampaign(**payload.model_dump())
        self.db.add(campaign)
        self.db.flush()
        return campaign

    def update_campaign(
        self,
        campaign_id: UUID,
        payload: SalesCampaignUpdate,
    ) -> SalesCampaign | None:
        campaign = self.db.get(SalesCampaign, campaign_id)
        if campaign is None:
            return None

        values = payload.model_dump(exclude_unset=True)
        for field, value in values.items():
            setattr(campaign, field, value)

        self.db.flush()
        return campaign

    def get_active_detail(self) -> SalesCampaignDetailRead | None:
        stmt = (
            select(SalesCampaign)
            .where(SalesCampaign.status == "open")
            .order_by(SalesCampaign.delivery_date.asc())
            .limit(1)
        )
        campaign = self.db.scalars(stmt).first()
        if campaign is None:
            return None
        return self._to_detail(campaign)

    def get_detail(self, campaign_id: UUID) -> SalesCampaignDetailRead | None:
        campaign = self.db.get(SalesCampaign, campaign_id)
        if campaign is None:
            return None
        return self._to_detail(campaign)

    def list_campaign_orders(self, campaign_id: UUID) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.campaign_id == campaign_id)
            .order_by(Order.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def list_campaign_products(
        self,
        campaign_id: UUID,
    ) -> list[CampaignProduct]:
        stmt = (
            select(CampaignProduct)
            .where(CampaignProduct.campaign_id == campaign_id)
            .order_by(
                CampaignProduct.display_order.asc(),
                CampaignProduct.name_snapshot.asc(),
            )
        )
        return list(self.db.scalars(stmt).all())

    def get_campaign_rule(self, campaign_id: UUID) -> CampaignRule | None:
        stmt = (
            select(CampaignRule)
            .where(CampaignRule.campaign_id == campaign_id)
            .limit(1)
        )
        return self.db.scalars(stmt).first()

    def add_campaign_product(
        self,
        campaign_id: UUID,
        payload: CampaignProductCreate,
    ) -> CampaignProduct:
        campaign = self.db.get(SalesCampaign, campaign_id)
        if campaign is None:
            raise ValueError("Campaign not found.")

        product = self.db.get(Product, payload.product_id)
        if product is None:
            raise ValueError("Product not found.")

        sale_price = payload.sale_price_snapshot or payload.price
        cost_price = payload.cost_price_snapshot or product.cost_price
        margin_unit = (
            sale_price - cost_price
            if cost_price is not None
            else None
        )

        campaign_product = CampaignProduct(
            campaign_id=campaign.id,
            product_id=product.id,
            name_snapshot=product.name,
            unit_snapshot=product.unit,
            producer_name_snapshot=(
                payload.producer_name_snapshot
                or product.producer_name_snapshot
            ),
            offer_type=payload.offer_type or product.offer_type,
            display_order=payload.display_order,
            price=sale_price,
            cost_price_snapshot=cost_price,
            sale_price_snapshot=sale_price,
            margin_unit_snapshot=margin_unit,
            available_quantity=payload.available_quantity,
            reserved_quantity=payload.reserved_quantity,
            min_quantity=payload.min_quantity,
            max_quantity=payload.max_quantity,
            requires_confirmation=payload.requires_confirmation,
            is_active=payload.is_active,
        )
        self.db.add(campaign_product)
        self.db.flush()
        return campaign_product

    def update_campaign_product(
        self,
        campaign_product_id: UUID,
        payload: CampaignProductUpdate,
    ) -> CampaignProduct | None:
        campaign_product = self.db.get(CampaignProduct, campaign_product_id)
        if campaign_product is None:
            return None

        values = payload.model_dump(exclude_unset=True)
        for field, value in values.items():
            setattr(campaign_product, field, value)

        sale_price = campaign_product.sale_price_snapshot or campaign_product.price
        cost_price = campaign_product.cost_price_snapshot
        campaign_product.price = sale_price
        campaign_product.margin_unit_snapshot = (
            sale_price - cost_price
            if cost_price is not None
            else None
        )

        self.db.flush()
        return campaign_product

    def _to_detail(self, campaign: SalesCampaign) -> SalesCampaignDetailRead:
        products = self.list_campaign_products(campaign.id)
        rule = self.get_campaign_rule(campaign.id)

        return SalesCampaignDetailRead.model_validate(
            {
                **campaign.__dict__,
                "products": products,
                "rule": rule,
            },
        )
