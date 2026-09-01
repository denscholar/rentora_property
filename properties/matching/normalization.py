"""
Property matching normalization utilities.

This module prepares property data for duplicate matching.

IMPORTANT:
Normalization does NOT determine whether two properties are
duplicates. It only converts values into a consistent form
that the matching engine can safely compare.
"""

import re
import unicodedata
from decimal import Decimal
from typing import Optional

from properties.models import PropertySubmission

# ============================================================
# TEXT NORMALIZATION
# ============================================================


def normalize_text(value: Optional[str]) -> str:
    """
    Normalize ordinary text for comparison.

    Examples:

        "  Life Camp  "
            -> "life camp"

        "LIFE-CAMP"
            -> "life camp"

        "Life   Camp"
            -> "life camp"
    """

    if not value:
        return ""

    value = str(value)

    # Remove accents / unicode differences.
    value = unicodedata.normalize(
        "NFKD",
        value,
    )

    value = "".join(
        character for character in value if not unicodedata.combining(character)
    )

    # Lowercase.
    value = value.lower()

    # Treat separators as spaces.
    value = re.sub(
        r"[-_/]+",
        " ",
        value,
    )

    # Remove punctuation.
    value = re.sub(
        r"[^\w\s]",
        " ",
        value,
    )

    # Collapse repeated whitespace.
    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    return value.strip()


# ============================================================
# LOCATION NORMALIZATION
# ============================================================


def normalize_area(area) -> str:
    """
    Normalize an Area instance for text comparison.

    We intentionally use the structured Area relationship
    separately from this value.

    The normalized name is therefore only a supporting signal.
    """

    if not area:
        return ""

    return normalize_text(
        area.name,
    )


def get_area_identity(area) -> Optional[dict]:
    """
    Return structured identity information for an Area.

    Example:

        {
            "area_id": 12,
            "area_slug": "fct-abuja-amac-guzape",
            "lga_id": 3,
            "name": "guzape",
        }
    """

    if not area:
        return None

    return {
        "area_id": area.pk,
        "area_slug": normalize_text(area.slug),
        "lga_id": area.lga_id,
        "name": normalize_area(area),
    }


# ============================================================
# PROPERTY TYPE
# ============================================================


def normalize_property_type(property_type) -> dict:
    """
    Normalize PropertyType lookup information.

    We retain both the structured ID/code and normalized name.

    The code is the authoritative structured value.
    """

    if not property_type:
        return {
            "id": None,
            "code": "",
            "name": "",
        }

    return {
        "id": property_type.pk,
        "code": normalize_text(property_type.code),
        "name": normalize_text(property_type.name),
    }


# ============================================================
# PROPERTY PURPOSE
# ============================================================


def normalize_property_purpose(purpose) -> dict:
    """
    Normalize PropertyPurpose lookup information.

    The database code remains the authoritative structured
    value.
    """

    if not purpose:
        return {
            "id": None,
            "code": "",
            "name": "",
        }

    return {
        "id": purpose.pk,
        "code": normalize_text(purpose.code),
        "name": normalize_text(purpose.name),
    }


# ============================================================
# ADDRESS
# ============================================================


def normalize_address(
    *,
    street_address: Optional[str] = None,
    landmark: Optional[str] = None,
) -> dict:
    """
    Normalize private address information.

    Address information is useful for duplicate detection but
    should NOT automatically determine that two properties
    are duplicates.

    A matching address is a strong signal, not the entire
    decision.
    """

    normalized_street = normalize_text(
        street_address,
    )

    normalized_landmark = normalize_text(
        landmark,
    )

    return {
        "street": normalized_street,
        "landmark": normalized_landmark,
    }


# ============================================================
# TITLE
# ============================================================


def normalize_title(title: Optional[str]) -> str:
    """
    Normalize a property title.

    Examples:

        "Luxury 4 Bedroom Duplex"
            -> "luxury 4 bedroom duplex"

        "4-Bedroom Duplex"
            -> "4 bedroom duplex"
    """

    return normalize_text(
        title,
    )


# ============================================================
# DESCRIPTION
# ============================================================


def normalize_description(
    description: Optional[str],
) -> str:
    """
    Normalize description text.

    Description is deliberately kept as a supporting signal.
    We will NOT perform sophisticated NLP here.
    """

    return normalize_text(
        description,
    )


# ============================================================
# DECIMAL NORMALIZATION
# ============================================================


def normalize_decimal(
    value,
) -> Optional[Decimal]:
    """
    Convert a numeric value into Decimal.

    Returns None when no usable value exists.
    """

    if value is None or value == "":
        return None

    try:
        return Decimal(str(value))
    except (TypeError, ValueError):
        return None


# ============================================================
# BOOLEAN NORMALIZATION
# ============================================================


def normalize_boolean(
    value,
) -> Optional[bool]:
    """
    Normalize boolean values.

    Returns None when the value is unavailable.
    """

    if value is None:
        return None

    return bool(value)


# ============================================================
# PROPERTY SUBMISSION
# ============================================================


def normalize_submission(
    submission: PropertySubmission,
) -> dict:
    """
    Convert a PropertySubmission into a normalized structure
    suitable for the matching engine.

    IMPORTANT:

    This function does NOT modify the database record.
    """

    property_type = normalize_property_type(
        submission.property_type,
    )

    purpose = normalize_property_purpose(
        submission.purpose,
    )

    area = get_area_identity(
        submission.area,
    )

    address = normalize_address(
        street_address=submission.street_address,
        landmark=submission.landmark,
    )

    return {
        # ----------------------------------------------------
        # Identity
        # ----------------------------------------------------
        "id": submission.pk,
        "uuid": str(submission.uuid),
        # ----------------------------------------------------
        # Classification
        # ----------------------------------------------------
        "property_type": property_type,
        "purpose": purpose,
        # ----------------------------------------------------
        # Location
        # ----------------------------------------------------
        "area": area,
        "address": address,
        # ----------------------------------------------------
        # Basic property information
        # ----------------------------------------------------
        "title": normalize_title(
            submission.title,
        ),
        "description": normalize_description(
            submission.description,
        ),
        "bedrooms": submission.bedrooms,
        "bathrooms": submission.bathrooms,
        "toilets": submission.toilets,
        "parking_spaces": submission.parking_spaces,
        # ----------------------------------------------------
        # Size
        # ----------------------------------------------------
        "size_unit": normalize_text(
            submission.size_unit,
        ),
        "land_size": normalize_decimal(
            submission.land_size,
        ),
        "building_size": normalize_decimal(
            submission.building_size,
        ),
        # ----------------------------------------------------
        # Pricing
        # ----------------------------------------------------
        "proposed_price": normalize_decimal(
            submission.proposed_price,
        ),
        "payment_frequency": normalize_text(
            submission.payment_frequency,
        ),
        "service_charge": normalize_decimal(
            submission.service_charge,
        ),
        "caution_fee": normalize_decimal(
            submission.caution_fee,
        ),
        "legal_fee": normalize_decimal(
            submission.legal_fee,
        ),
        "agency_fee": normalize_decimal(
            submission.agency_fee,
        ),
        # ----------------------------------------------------
        # Property characteristics
        # ----------------------------------------------------
        "floors": submission.floors,
        "units_available": submission.units_available,
        "year_built": submission.year_built,
        "is_new_build": normalize_boolean(
            submission.is_new_build,
        ),
        "is_serviced": normalize_boolean(
            submission.is_serviced,
        ),
        "is_negotiable": normalize_boolean(
            submission.is_negotiable,
        ),
        "available_from": submission.available_from,
        "minimum_stay": submission.minimum_stay,
        # ----------------------------------------------------
        # Matching metadata
        # ----------------------------------------------------
        "status": submission.status,
        "is_archived": submission.is_archived,
    }
