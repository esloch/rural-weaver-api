from decimal import Decimal

from apps.api.app.db.session import SessionLocal
from apps.api.app.models.order import Order, OrderItem
from apps.api.app.models.payment import PaymentSetting
from apps.api.app.models.producer import Producer
from apps.api.app.models.product import BasketType, Product
from apps.api.app.models.stock import StockMovement
from apps.api.app.models.user import User


def seed() -> None:
    """Seed demo data for the Delícias da Roça pilot."""

    db = SessionLocal()
    try:
        existing = (
            db.query(Producer)
            .filter(Producer.name == "Delícias da Roça")
            .one_or_none()
        )
        if existing is not None:
            print("Seed data already exists. Nothing to do.")
            return

        admin = User(
            email="admin@tejidorural.local",
            password_hash="not-used-yet",
            role="admin",
            full_name="Admin Tejido Rural",
            phone=None,
        )
        producer_user = User(
            email="produtor@deliciasdaroca.local",
            password_hash="not-used-yet",
            role="producer",
            full_name="Delícias da Roça",
            phone="+55 48 99999-0000",
        )
        db.add_all([admin, producer_user])
        db.flush()

        producer = Producer(
            user_id=producer_user.id,
            name="Delícias da Roça",
            description=(
                "Agricultura familiar agroecológica com cestas, produtos "
                "sazonais e compras coletivas."
            ),
            location="São Pedro de Alcântara, SC, Brasil",
            status="active",
        )
        db.add(producer)
        db.flush()

        products = [
            Product(
                producer_id=producer.id,
                name="Alface agroecológica",
                description="Folhas frescas da colheita da semana.",
                category="hortifruti",
                unit="unidade",
                price=Decimal("5.00"),
                stock_quantity=Decimal("30"),
                image_url="https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1",
                is_active=True,
            ),
            Product(
                producer_id=producer.id,
                name="Banana",
                description="Banana da agricultura familiar.",
                category="frutas",
                unit="kg",
                price=Decimal("7.50"),
                stock_quantity=Decimal("25"),
                image_url="https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e",
                is_active=True,
            ),
            Product(
                producer_id=producer.id,
                name="Geleia artesanal",
                description="Geleia de produção artesanal.",
                category="processados",
                unit="pote",
                price=Decimal("18.00"),
                stock_quantity=Decimal("12"),
                image_url="https://images.unsplash.com/photo-1606914501449-5a96b6ce24ca",
                is_active=True,
            ),
            Product(
                producer_id=producer.id,
                name="Ovos caipiras",
                description="Ovos caipiras de produção local.",
                category="proteínas",
                unit="dúzia",
                price=Decimal("16.00"),
                stock_quantity=Decimal("8"),
                image_url="https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f",
                is_active=True,
            ),
            Product(
                producer_id=producer.id,
                name="Mel local",
                description="Mel de pequenos produtores parceiros.",
                category="compras-coletivas",
                unit="frasco",
                price=Decimal("32.00"),
                stock_quantity=Decimal("4"),
                image_url="https://images.unsplash.com/photo-1587049352846-4a222e784d38",
                is_active=True,
            ),
        ]
        db.add_all(products)

        baskets = [
            BasketType(
                name="Cesta Pequena",
                description="Seleção semanal reduzida de hortifruti.",
                base_price=Decimal("50.00"),
                is_active=True,
            ),
            BasketType(
                name="Cesta Média",
                description="Cesta semanal com hortifruti variado.",
                base_price=Decimal("75.00"),
                is_active=True,
            ),
            BasketType(
                name="Cesta Grande",
                description="Cesta semanal ampliada para famílias.",
                base_price=Decimal("100.00"),
                is_active=True,
            ),
        ]
        db.add_all(baskets)

        payment_setting = PaymentSetting(
            provider="pix_manual",
            pix_key="pix@tejidorural.local",
            pix_key_type="email",
            recipient_name="Tejido Rural Operações",
            recipient_document="12.345.678/0001-99",
            bank_name="Banco Cooperativo Rural",
            payment_instructions=(
                "Faça o pagamento via Pix e envie o comprovante pelo "
                "WhatsApp para confirmação manual."
            ),
            pix_copy_paste_hash=(
                "00020126580014BR.GOV.BCB.PIX0114pix@tejidorural.local"
                "520400005303986540550.005802BR5925TEJIDO RURAL "
                "OPERACOES6009SAOPAULO62070503***6304ABCD"
            ),
            qr_code_image_url="https://placehold.co/320x320?text=Pix+QR",
            is_active=True,
        )
        db.add(payment_setting)
        db.flush()

        order = Order(
            customer_name="Cliente Demo",
            customer_phone="+55 48 98888-0000",
            customer_email="cliente.demo@example.com",
            delivery_type="pickup",
            pickup_point="UFSC - DCE",
            address=None,
            status="submitted",
            payment_method="pix_manual",
            payment_status="pending",
            subtotal=Decimal("75.00"),
            total=Decimal("75.00"),
            notes="Pedido demo criado pelo seed.",
        )
        db.add(order)
        db.flush()

        db.add(
            OrderItem(
                order_id=order.id,
                product_id=None,
                basket_type_id=baskets[1].id,
                item_type="basket",
                name_snapshot="Cesta Média",
                unit_price_snapshot=Decimal("75.00"),
                quantity=Decimal("1"),
                total_snapshot=Decimal("75.00"),
            ),
        )

        for product in products:
            db.add(
                StockMovement(
                    product_id=product.id,
                    type="restock",
                    quantity=product.stock_quantity,
                    reason="Seed inicial",
                    created_by=admin.id,
                ),
            )

        db.commit()
        print("Seed data created successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
