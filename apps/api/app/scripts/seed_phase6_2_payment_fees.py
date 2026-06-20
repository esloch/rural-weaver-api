from decimal import Decimal

from sqlalchemy import select

from apps.api.app.db.session import SessionLocal
from apps.api.app.models.payment_method import PaymentMethod


def main() -> None:
    db = SessionLocal()
    try:
        rows = {
            "pix": {"fee_fixed": Decimal("0.00"), "fee_percent": Decimal("0.0000")},
            "bank_deposit": {"fee_fixed": Decimal("0.00"), "fee_percent": Decimal("0.0000")},
            # Review these values with Alice if the real provider fees differ.
            "boleto": {"fee_fixed": Decimal("3.49"), "fee_percent": Decimal("0.0000")},
            "card_link": {"fee_fixed": Decimal("0.00"), "fee_percent": Decimal("4.9900")},
        }

        for code, values in rows.items():
            method = db.scalars(
                select(PaymentMethod).where(PaymentMethod.code == code),
            ).first()
            if method is None:
                continue
            method.fee_fixed = values["fee_fixed"]
            method.fee_percent = values["fee_percent"]

        db.commit()
        print("Phase 6.2 payment fees seeded.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
