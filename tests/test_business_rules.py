from decimal import Decimal

import pytest

from packages.business_rules.orders import (
    calculate_item_total,
    ensure_stock_available,
)


def test_calculate_item_total() -> None:
    assert calculate_item_total(
        Decimal("12.50"),
        Decimal("2"),
    ) == Decimal("25.00")


def test_calculate_item_total_rejects_zero_quantity() -> None:
    with pytest.raises(ValueError, match="Quantity"):
        calculate_item_total(Decimal("12.50"), Decimal("0"))


def test_stock_available_allows_valid_quantity() -> None:
    ensure_stock_available(Decimal("10"), Decimal("3"))


def test_stock_available_rejects_negative_balance() -> None:
    with pytest.raises(ValueError, match="Insufficient stock"):
        ensure_stock_available(Decimal("2"), Decimal("3"))
