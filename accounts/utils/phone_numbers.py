import re

import phonenumbers
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
)


def normalize_phone_number(
    value: str,
    default_region: str = "NG",
) -> str:
    raw = re.sub(r"[\s().-]", "", value.strip())

    if raw.startswith("00"):
        raw = f"+{raw[2:]}"
    elif raw.startswith("234"):
        raw = f"+{raw}"

    try:
        parsed = phonenumbers.parse(
            raw,
            None if raw.startswith("+") else default_region,
        )
    except NumberParseException as exc:
        raise ValueError("Invalid phone number.") from exc

    if not phonenumbers.is_valid_number(parsed):
        raise ValueError("Invalid phone number.")

    return phonenumbers.format_number(
        parsed,
        PhoneNumberFormat.E164,
    )