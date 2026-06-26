import pytest

from packages.business_rules.customers import (
    CustomerValidationError,
    normalize_cpf,
    normalize_email,
    normalize_phone,
    validate_cpf,
    validate_email,
)


def test_normalize_cpf_removes_formatting() -> None:
    assert normalize_cpf("123.456.789-09") == "12345678909"


def test_validate_cpf_accepts_valid_digits() -> None:
    assert validate_cpf("52998224725") is True


def test_validate_cpf_rejects_repeated_digits() -> None:
    assert validate_cpf("11111111111") is False


def test_validate_email_lowercases_input() -> None:
    assert normalize_email(" Cliente@Example.COM ") == "cliente@example.com"
    assert validate_email("cliente@example.com") is True


def test_normalize_phone_requires_brazilian_area_code() -> None:
    with pytest.raises(CustomerValidationError, match="phone_area_code"):
        normalize_phone("+55", None, "999999999")


def test_normalize_phone_returns_e164() -> None:
    phone = normalize_phone("+55", "48", "99999-0000")
    assert phone.phone_e164 == "+5548999990000"
