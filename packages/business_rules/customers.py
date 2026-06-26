import re
from dataclasses import dataclass


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class CustomerValidationError(ValueError):
    """Raised when customer identity data is invalid."""


@dataclass(frozen=True)
class NormalizedPhone:
    country_code: str
    area_code: str | None
    phone_number: str
    phone_e164: str | None


def only_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def normalize_cpf(value: str) -> str:
    return only_digits(value)


def validate_cpf(value: str) -> bool:
    digits = normalize_cpf(value)
    if len(digits) != 11:
        return False
    if digits == digits[0] * 11:
        return False

    first_sum = sum(int(digit) * weight for digit, weight in zip(digits[:9], range(10, 1, -1)))
    first_check = (first_sum * 10) % 11
    if first_check == 10:
        first_check = 0
    if first_check != int(digits[9]):
        return False

    second_sum = sum(int(digit) * weight for digit, weight in zip(digits[:10], range(11, 1, -1)))
    second_check = (second_sum * 10) % 11
    if second_check == 10:
        second_check = 0
    return second_check == int(digits[10])


def normalize_email(value: str) -> str:
    return (value or "").strip().lower()


def validate_email(value: str) -> bool:
    return bool(EMAIL_RE.match(normalize_email(value)))


def normalize_phone(
    country_code: str,
    area_code: str | None,
    phone_number: str,
) -> NormalizedPhone:
    normalized_country_code = "+" + only_digits(country_code)
    normalized_area_code = only_digits(area_code or "") or None
    normalized_phone_number = only_digits(phone_number)

    if normalized_country_code == "+":
        raise CustomerValidationError("phone_country_code is required.")
    if not normalized_phone_number:
        raise CustomerValidationError("phone_number is required.")

    if normalized_country_code == "+55":
        if not normalized_area_code:
            raise CustomerValidationError("phone_area_code is required for Brazil.")
        if len(normalized_area_code) != 2:
            raise CustomerValidationError("Brazilian phone area code must have 2 digits.")
        if len(normalized_phone_number) not in {8, 9}:
            raise CustomerValidationError("Brazilian phone number must have 8 or 9 digits.")
    elif len(normalized_phone_number) < 6:
        raise CustomerValidationError("invalid phone.")

    e164 = normalized_country_code
    if normalized_area_code:
        e164 += normalized_area_code
    e164 += normalized_phone_number

    return NormalizedPhone(
        country_code=normalized_country_code,
        area_code=normalized_area_code,
        phone_number=normalized_phone_number,
        phone_e164=e164,
    )


def split_full_name(full_name: str | None) -> tuple[str | None, str | None]:
    value = (full_name or "").strip()
    if not value:
        return None, None

    parts = value.split()
    if len(parts) == 1:
        return parts[0], None
    return parts[0], " ".join(parts[1:])


def build_full_name(first_name: str, last_name: str) -> str:
    return f"{first_name.strip()} {last_name.strip()}".strip()


def build_address_snapshot(address_line: str, address_number: str) -> str:
    return f"{address_line.strip()}, {address_number.strip()}"
