from decimal import Decimal


def calculate_item_total(
    unit_price: Decimal,
    quantity: Decimal,
) -> Decimal:
    """Calculate an order item total using price snapshot data."""

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    if unit_price < 0:
        raise ValueError("Unit price cannot be negative.")

    return (unit_price * quantity).quantize(Decimal("0.01"))


def ensure_stock_available(
    available: Decimal,
    requested: Decimal,
) -> None:
    """Validate that requested quantity is available."""

    if requested <= 0:
        raise ValueError("Requested quantity must be greater than zero.")

    if available - requested < 0:
        raise ValueError("Insufficient stock.")
