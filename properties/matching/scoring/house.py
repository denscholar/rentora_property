from decimal import Decimal

from properties.matching.scoring.base import BasePropertyScorer


class HouseScorer(BasePropertyScorer):
    """
    Scores similarity between two standalone residential houses,
    duplexes and similar house-type properties.
    """

    category = "house"

    WEIGHTS = {
        "area": Decimal("20"),
        "property_type": Decimal("15"),
        "bedrooms": Decimal("15"),
        "bathrooms": Decimal("8"),
        "building_size": Decimal("10"),
        "land_size": Decimal("8"),
        "location": Decimal("15"),
        "price": Decimal("5"),
        "purpose": Decimal("4"),
    }
