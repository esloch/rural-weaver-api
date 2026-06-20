from datetime import time
from decimal import Decimal

from sqlalchemy import select

from apps.api.app.db.session import SessionLocal
from apps.api.app.models.campaign import (
    CampaignRule,
    DeliveryZone,
    PickupPoint,
    SalesCampaign,
)
from apps.api.app.models.payment_method import PaymentMethod
from apps.api.app.models.producer import Producer
from apps.api.app.models.product import BasketType, Product
from apps.api.app.models.subscription import SubscriptionPlan


def seed() -> None:
    """Seed operational data extracted from Alice's current materials."""

    db = SessionLocal()
    try:
        seed_delivery_zones(db)
        seed_pickup_points(db)
        seed_payment_methods(db)
        seed_basket_metadata_and_subscription_plans(db)
        seed_campaign_rules(db)
        seed_donation_product(db)
        db.commit()
        print("Alice operational data seeded successfully.")
    finally:
        db.close()


def seed_delivery_zones(db) -> None:
    rows = [
        {
            "name": "São Pedro de Alcântara",
            "city": "São Pedro de Alcântara",
            "area": "urbana",
            "fee": Decimal("9.00"),
            "restrictions": None,
        },
        {
            "name": "São José / Palhoça",
            "city": "São José / Palhoça",
            "area": None,
            "fee": Decimal("15.00"),
            "restrictions": None,
        },
        {
            "name": "Florianópolis Continente",
            "city": "Florianópolis",
            "area": "continente",
            "fee": Decimal("17.00"),
            "restrictions": None,
        },
        {
            "name": "Florianópolis Ilha",
            "city": "Florianópolis",
            "area": "ilha",
            "fee": Decimal("18.00"),
            "restrictions": (
                "Não atende Barra da Lagoa, Rio Vermelho, região e extremo norte."
            ),
        },
    ]

    for row in rows:
        exists = db.scalars(
            select(DeliveryZone).where(DeliveryZone.name == row["name"]),
        ).first()
        if exists is not None:
            continue

        db.add(
            DeliveryZone(
                **row,
                instructions="Entrega a domicílio mediante confirmação manual.",
                is_supported=True,
                is_active=True,
            ),
        )


def seed_pickup_points(db) -> None:
    rows = [
        {
            "name": "Papelaria Limas",
            "address": "SC 281, 7871 - Colônia Santana",
            "city": "São José",
            "neighborhood": "Colônia Santana",
            "weekday_availability": "Dia da entrega",
            "time_window": None,
            "is_condo_only": False,
        },
        {
            "name": "Floricultura Pauli",
            "address": "R. João Stahelin, 2269 - Boa Parada",
            "city": "São Pedro de Alcântara",
            "neighborhood": "Boa Parada",
            "weekday_availability": "Dia da entrega",
            "time_window": None,
            "is_condo_only": False,
        },
        {
            "name": "Armazém Campeche Produtos Naturais",
            "address": "Avenida Pequeno Príncipe, 2072 - Campeche",
            "city": "Florianópolis",
            "neighborhood": "Campeche",
            "weekday_availability": "Dia da entrega",
            "time_window": None,
            "is_condo_only": False,
        },
        {
            "name": "Adoça e Confeita",
            "address": (
                "Rua Antônio Scherer, 737, loja 13, Edifício Vancouver - Kobrasol"
            ),
            "city": "São José",
            "neighborhood": "Kobrasol",
            "weekday_availability": "Dia da entrega",
            "time_window": None,
            "is_condo_only": False,
        },
        {
            "name": "Condomínio Arquipélago",
            "address": "R. Lauro Linhares, 635 - Trindade",
            "city": "Florianópolis",
            "neighborhood": "Trindade",
            "weekday_availability": "Dia da entrega",
            "time_window": None,
            "is_condo_only": True,
        },
        {
            "name": "UFSC - DCE",
            "address": (
                "R. Eng. Agrônomo Andrei Cristian Ferreira, Centro de Convivência, sala do DCE"
            ),
            "city": "Florianópolis",
            "neighborhood": "Trindade",
            "weekday_availability": "Terças durante o ano letivo",
            "time_window": "13:00 às 15:00",
            "is_condo_only": False,
        },
    ]

    instructions = (
        "Retirada gratuita somente no dia da entrega. O ponto de coleta não "
        "guarda a cesta para outro dia e não possui freezer ou geladeira."
    )

    for row in rows:
        exists = db.scalars(
            select(PickupPoint).where(PickupPoint.name == row["name"]),
        ).first()
        if exists is not None:
            continue

        db.add(
            PickupPoint(
                **row,
                has_refrigeration=False,
                instructions=instructions,
                is_active=True,
            ),
        )


def seed_payment_methods(db) -> None:
    rows = [
        {
            "code": "pix",
            "name": "PIX",
            "instructions": (
                "Alice enviará a chave Pix e confirmará o pagamento manualmente."
            ),
            "requires_extra_data": False,
        },
        {
            "code": "bank_deposit",
            "name": "Depósito bancário / transferência",
            "instructions": "Pagamento via PagBank, Nubank ou sistema AILOS.",
            "requires_extra_data": False,
        },
        {
            "code": "boleto",
            "name": "Boleto à vista",
            "instructions": (
                "Pedido enviado somente mediante pagamento do boleto. "
                "Requer nome completo, CPF, endereço com CEP, e-mail e telefone."
            ),
            "requires_extra_data": True,
        },
        {
            "code": "card_link",
            "name": "Link de pagamento com cartão",
            "instructions": "Alice enviará o link de pagamento após confirmar o pedido.",
            "requires_extra_data": False,
        },
    ]

    for row in rows:
        exists = db.scalars(
            select(PaymentMethod).where(PaymentMethod.code == row["code"]),
        ).first()
        if exists is not None:
            continue
        db.add(PaymentMethod(**row, is_active=True))


def seed_basket_metadata_and_subscription_plans(db) -> None:
    medium = db.scalars(
        select(BasketType).where(BasketType.name.ilike("%média%")),
    ).first()
    large = db.scalars(
        select(BasketType).where(BasketType.name.ilike("%grande%")),
    ).first()

    if medium is not None:
        medium.base_price = Decimal("49.00")
        medium.average_items = 8
        medium.average_weight_kg = Decimal("4.500")
        medium.serves_people = "até 2 pessoas"
        medium.description = (
            "Cesta média com cerca de 8 itens e peso médio de 4,5 kg."
        )

    if large is not None:
        large.base_price = Decimal("69.00")
        large.average_items = 12
        large.average_weight_kg = Decimal("8.000")
        large.serves_people = "até 4 pessoas"
        large.description = (
            "Cesta grande com cerca de 12 itens e peso médio de 8 kg."
        )

    plans = [
        {
            "basket": medium,
            "name": "Cesta Média Unitária",
            "frequency": "one_time",
            "deliveries_per_month": 1,
            "price": Decimal("49.00"),
            "average_items": 8,
            "average_weight_kg": Decimal("4.500"),
            "serves_people": "até 2 pessoas",
        },
        {
            "basket": large,
            "name": "Cesta Grande Unitária",
            "frequency": "one_time",
            "deliveries_per_month": 1,
            "price": Decimal("69.00"),
            "average_items": 12,
            "average_weight_kg": Decimal("8.000"),
            "serves_people": "até 4 pessoas",
        },
        {
            "basket": medium,
            "name": "Assinatura Quinzenal Média",
            "frequency": "biweekly",
            "deliveries_per_month": 2,
            "price": Decimal("90.00"),
            "average_items": 8,
            "average_weight_kg": Decimal("4.500"),
            "serves_people": "até 2 pessoas",
        },
        {
            "basket": medium,
            "name": "Assinatura Semanal Média",
            "frequency": "weekly",
            "deliveries_per_month": 4,
            "price": Decimal("180.00"),
            "average_items": 8,
            "average_weight_kg": Decimal("4.500"),
            "serves_people": "até 2 pessoas",
        },
        {
            "basket": large,
            "name": "Assinatura Quinzenal Grande",
            "frequency": "biweekly",
            "deliveries_per_month": 2,
            "price": Decimal("130.00"),
            "average_items": 12,
            "average_weight_kg": Decimal("8.000"),
            "serves_people": "até 4 pessoas",
        },
        {
            "basket": large,
            "name": "Assinatura Semanal Grande",
            "frequency": "weekly",
            "deliveries_per_month": 4,
            "price": Decimal("260.00"),
            "average_items": 12,
            "average_weight_kg": Decimal("8.000"),
            "serves_people": "até 4 pessoas",
        },
    ]

    for plan in plans:
        if plan["basket"] is None:
            continue

        exists = db.scalars(
            select(SubscriptionPlan).where(SubscriptionPlan.name == plan["name"]),
        ).first()
        if exists is not None:
            continue

        db.add(
            SubscriptionPlan(
                basket_type_id=plan["basket"].id,
                name=plan["name"],
                frequency=plan["frequency"],
                deliveries_per_month=plan["deliveries_per_month"],
                price=plan["price"],
                average_items=plan["average_items"],
                average_weight_kg=plan["average_weight_kg"],
                serves_people=plan["serves_people"],
                description=(
                    "Plano CSA com composição variável conforme a colheita da semana."
                ),
                is_active=True,
            ),
        )


def seed_campaign_rules(db) -> None:
    campaigns = db.scalars(select(SalesCampaign)).all()
    instructions = (
        "Pedidos aos domingos e quintas-feiras, encerramento até 20:00. "
        "Pedido mínimo de R$ 50,00, exceto retirada na Floricultura Pauli. "
        "Alice confirma itens, valores e instruções de pagamento. "
        "Pedidos processados por ordem de envio até esgotarem os estoques."
    )

    for campaign in campaigns:
        exists = db.scalars(
            select(CampaignRule).where(CampaignRule.campaign_id == campaign.id),
        ).first()
        if exists is not None:
            continue

        db.add(
            CampaignRule(
                campaign_id=campaign.id,
                order_days=["domingo", "quinta-feira"],
                order_close_time=time(20, 0),
                minimum_order_value=Decimal("50.00"),
                minimum_order_exceptions="Retirada na Floricultura Pauli.",
                process_by_order_time=True,
                confirmation_required=True,
                proof_required=True,
                instructions=instructions,
            ),
        )


def seed_donation_product(db) -> None:
    producer = db.scalars(select(Producer).order_by(Producer.created_at.asc())).first()
    if producer is None:
        return

    exists = db.scalars(
        select(Product).where(Product.name == "Cesta de Doação"),
    ).first()
    if exists is not None:
        return

    db.add(
        Product(
            producer_id=producer.id,
            producer_name_snapshot="Delícias da Roça",
            name="Cesta de Doação",
            description=(
                "Cesta doada para comunidades indígenas na casa de passagem GOJ TY SÁ."
            ),
            category="doação",
            offer_type="donation",
            unit="unidade",
            price=Decimal("50.00"),
            stock_quantity=Decimal("9999"),
            image_url=None,
            is_refrigerated=False,
            is_frozen=False,
            is_addon=True,
            is_donation=True,
            is_active=True,
        ),
    )


if __name__ == "__main__":
    seed()
