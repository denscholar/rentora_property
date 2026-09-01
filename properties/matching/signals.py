"""
Comparison signal generator.

This module compares TWO normalized properties and returns
objective signals.

It intentionally contains NO scoring logic.
"""

from decimal import Decimal
from difflib import SequenceMatcher

# ============================================================
# STRING SIMILARITY
# ============================================================


def similarity(a: str, b: str) -> float:
    """
    Returns similarity as a percentage.

    Example:
        "life camp"
        "life camp"

        => 100.0
    """

    if not a or not b:
        return 0.0

    return round(
        SequenceMatcher(None, a, b).ratio() * 100,
        2,
    )


# ============================================================
# PERCENT DIFFERENCE
# ============================================================


def percent_difference(
    value1,
    value2,
):
    """
    Returns percentage difference between two numbers.

    Example:

        4,500,000
        4,700,000

        => 4.44%
    """

    if value1 is None or value2 is None:
        return None

    value1 = Decimal(value1)
    value2 = Decimal(value2)

    larger = max(value1, value2)

    if larger == 0:
        return Decimal("0.00")

    difference = abs(value1 - value2)

    return round(
        (difference / larger) * 100,
        2,
    )


# ============================================================
# NUMERIC DIFFERENCE
# ============================================================


def numeric_difference(a, b):
    """
    Absolute difference between integers.

    Example:

        bedrooms:
            4 vs 3

        => 1
    """

    if a is None or b is None:
        return None

    return abs(a - b)


# ============================================================
# BOOLEAN MATCH
# ============================================================


def boolean_match(a, b):
    if a is None or b is None:
        return False

    return a == b


# ============================================================
# AREA MATCH
# ============================================================


def same_area(a, b):
    if not a or not b:
        return False

    return a["area_id"] == b["area_id"]


def same_lga(a, b):
    if not a or not b:
        return False

    return a["lga_id"] == b["lga_id"]


# ============================================================
# PROPERTY TYPE
# ============================================================


def same_property_type(a, b):
    return a["id"] == b["id"]


def same_property_category(category_a, category_b):
    return category_a == category_b


# ============================================================
# MAIN SIGNAL GENERATOR
# ============================================================


def generate_signals(
    *,
    left: dict,
    right: dict,
    left_category: str,
    right_category: str,
):
    """
    Compare two normalized properties.

    Returns only measurable facts.
    """

    return {
        # ----------------------------------------------------
        # Identity
        # ----------------------------------------------------
        "same_property_type": same_property_type(
            left["property_type"],
            right["property_type"],
        ),
        "same_category": same_property_category(
            left_category,
            right_category,
        ),
        "same_purpose": (left["purpose"]["id"] == right["purpose"]["id"]),
        # ----------------------------------------------------
        # Location
        # ----------------------------------------------------
        "same_area": same_area(
            left["area"],
            right["area"],
        ),
        "same_lga": same_lga(
            left["area"],
            right["area"],
        ),
        "street_similarity": similarity(
            left["address"]["street"],
            right["address"]["street"],
        ),
        "landmark_similarity": similarity(
            left["address"]["landmark"],
            right["address"]["landmark"],
        ),
        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------
        "title_similarity": similarity(
            left["title"],
            right["title"],
        ),
        # ----------------------------------------------------
        # Rooms
        # ----------------------------------------------------
        "bedroom_difference": numeric_difference(
            left["bedrooms"],
            right["bedrooms"],
        ),
        "bathroom_difference": numeric_difference(
            left["bathrooms"],
            right["bathrooms"],
        ),
        "toilet_difference": numeric_difference(
            left["toilets"],
            right["toilets"],
        ),
        # ----------------------------------------------------
        # Size
        # ----------------------------------------------------
        "same_size_unit": (left["size_unit"] == right["size_unit"]),
        "building_size_difference_percent": percent_difference(
            left["building_size"],
            right["building_size"],
        ),
        "land_size_difference_percent": percent_difference(
            left["land_size"],
            right["land_size"],
        ),
        # ----------------------------------------------------
        # Pricing
        # ----------------------------------------------------
        "price_difference_percent": percent_difference(
            left["proposed_price"],
            right["proposed_price"],
        ),
        "same_payment_frequency": (
            left["payment_frequency"] == right["payment_frequency"]
        ),
        # ----------------------------------------------------
        # Characteristics
        # ----------------------------------------------------
        "same_serviced": boolean_match(
            left["is_serviced"],
            right["is_serviced"],
        ),
        "same_new_build": boolean_match(
            left["is_new_build"],
            right["is_new_build"],
        ),
        "same_negotiable": boolean_match(
            left["is_negotiable"],
            right["is_negotiable"],
        ),
    }
