# properties/matching/category.py

"""
Property category resolution for the duplicate matching engine.

The purpose of this module is to determine which matching
strategy should be used for a PropertySubmission.

This module does NOT determine whether two properties are
duplicates.
"""

from properties.matching.constants import (
    APARTMENT,
    COMMERCIAL,
    ESTATE,
    HOUSE,
    LAND,
    ROOM,
)
from properties.matching.normalization import normalize_text

# ============================================================
# PROPERTY TYPE ALIASES
# ============================================================

"""
Different PropertyType records may represent the same
matching category.

For example:

    "flat"
    "apartment"
    "self contained apartment"

may all belong to the APARTMENT category.

Likewise:

    "duplex"
    "detached house"
    "semi detached house"

may belong to the HOUSE category.

These aliases are intentionally kept here instead of being
spread throughout the matching engine.
"""


APARTMENT_TYPES = {
    "apartment",
    "flat",
    "flats",
    "self contained apartment",
    "self contained",
    "studio apartment",
    "mini flat",
    "miniflat",
    "penthouse",
}


HOUSE_TYPES = {
    "house",
    "duplex",
    "detached house",
    "semi detached house",
    "semi detached duplex",
    "terrace",
    "terrace house",
    "terraced house",
    "bungalow",
    "mansion",
    "villa",
}

ESTATE_TYPES = {
    "estate",
    "housing estate",
    "residential estate",
    "estate property",
    "gated estate",
}


ROOM_TYPES = {
    "room",
    "single room",
    "room and parlour",
    "room and parlor",
    "self contain",
    "self contained room",
    "shared room",
}


COMMERCIAL_TYPES = {
    "commercial",
    "commercial property",
    "office",
    "shop",
    "warehouse",
    "store",
    "retail shop",
    "showroom",
    "restaurant",
    "hotel",
    "guest house",
    "event centre",
    "event center",
    "factory",
    "industrial property",
}


LAND_TYPES = {
    "land",
    "plot",
    "plot of land",
    "residential land",
    "commercial land",
    "agricultural land",
    "farmland",
    "farm land",
    "industrial land",
}


# ============================================================
# CATEGORY RESOLVER
# ============================================================


def resolve_property_category(property_type):
    """
    Resolve a PropertyType instance into one of the six
    matching categories.

    Returns:

        HOUSE
        APARTMENT
        ESTATE
        ROOM
        COMMERCIAL
        LAND

    Raises:

        ValueError
            If the property type cannot be mapped safely.
    """

    if property_type is None:
        raise ValueError(
            "Property type is required before a matching category " "can be determined."
        )

    # --------------------------------------------------------
    # Get name
    # --------------------------------------------------------

    name = normalize_text(getattr(property_type, "name", ""))

    # --------------------------------------------------------
    # Get slug if the lookup model has one
    # --------------------------------------------------------

    slug = normalize_text(getattr(property_type, "slug", ""))

    # We try the slug first when it exists because slugs
    # are normally more stable than display names.
    candidates = []

    if slug:
        candidates.append(slug)

    if name:
        candidates.append(name)

    # --------------------------------------------------------
    # Match against known categories
    # --------------------------------------------------------

    for value in candidates:

        if value in APARTMENT_TYPES:
            return APARTMENT

        if value in HOUSE_TYPES:
            return HOUSE

        if value in ESTATE_TYPES:
            return ESTATE

        if value in ROOM_TYPES:
            return ROOM

        if value in COMMERCIAL_TYPES:
            return COMMERCIAL

        if value in LAND_TYPES:
            return LAND

    # --------------------------------------------------------
    # Unknown property type
    # --------------------------------------------------------

    raise ValueError(
        f"Unable to determine matching category for " f"property type '{name or slug}'."
    )
