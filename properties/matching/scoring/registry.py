"""
Scorer registry.

This module provides a single entry point for retrieving
the scorer responsible for a property category.

It contains no database queries and no matching business logic.
"""

from properties.matching.constants import (
    APARTMENT,
    COMMERCIAL,
    ESTATE,
    HOUSE,
    LAND,
    ROOM,
)
from properties.matching.scoring.apartment import ApartmentScorer
from properties.matching.scoring.commercial import CommercialScorer
from properties.matching.scoring.estate import EstateScorer
from properties.matching.scoring.house import HouseScorer
from properties.matching.scoring.land import LandScorer
from properties.matching.scoring.room import RoomScorer

# ============================================================
# SCORER REGISTRY
# ============================================================

SCORER_REGISTRY = {
    HOUSE: HouseScorer,
    APARTMENT: ApartmentScorer,
    ESTATE: EstateScorer,
    ROOM: RoomScorer,
    COMMERCIAL: CommercialScorer,
    LAND: LandScorer,
}


# ============================================================
# GET SCORER
# ============================================================


def get_scorer(category: str):
    """
    Return the scorer instance for a property category.

    Example:

        scorer = get_scorer("apartment")

    Returns:

        ApartmentScorer()
    """

    try:
        scorer_class = SCORER_REGISTRY[category]
    except KeyError:
        raise ValueError(f"Unsupported property matching category: {category!r}")

    return scorer_class()
