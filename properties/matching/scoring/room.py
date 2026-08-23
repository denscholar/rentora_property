from decimal import Decimal

from properties.matching.scoring.base import (
    BasePropertyScorer,
    MatchScore,
    SignalScore,
)


class RoomScorer(BasePropertyScorer):
    """
    Scores similarity between two room-based properties.

    Rooms are generally smaller and more location-sensitive than
    standalone houses or apartments. Therefore, area, property type,
    purpose, address/location, and bathroom configuration are important
    identity signals.
    """

    category = "room"

    WEIGHTS = {
        "area": Decimal("20"),
        "property_type": Decimal("15"),
        "purpose": Decimal("10"),
        "bedrooms": Decimal("10"),
        "bathrooms": Decimal("10"),
        "building_size": Decimal("5"),
        "land_size": Decimal("2"),
        "location": Decimal("18"),
        "price": Decimal("10"),
    }

    # ========================================================
    # PUBLIC SCORING METHOD
    # ========================================================

    def score(self, signals: dict) -> MatchScore:
        """
        Convert generated comparison signals into a complete
        room-property MatchScore.
        """

        signal_scores = [
            self._score_area(signals),
            self._score_property_type(signals),
            self._score_purpose(signals),
            self._score_bedrooms(signals),
            self._score_bathrooms(signals),
            self._score_building_size(signals),
            self._score_land_size(signals),
            self._score_location(signals),
            self._score_price(signals),
        ]

        return self.build_score(
            signals=signal_scores,
        )

    # ========================================================
    # AREA
    # ========================================================

    def _score_area(self, signals: dict) -> SignalScore:
        similarity = Decimal("100") if signals["same_area"] else Decimal("0")

        weight = self.WEIGHTS["area"]

        return SignalScore(
            name="area",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "same_area": signals["same_area"],
            },
        )

    # ========================================================
    # PROPERTY TYPE
    # ========================================================

    def _score_property_type(self, signals: dict) -> SignalScore:
        similarity = Decimal("100") if signals["same_property_type"] else Decimal("0")

        weight = self.WEIGHTS["property_type"]

        return SignalScore(
            name="property_type",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "same_property_type": signals["same_property_type"],
            },
        )

    # ========================================================
    # PURPOSE
    # ========================================================

    def _score_purpose(self, signals: dict) -> SignalScore:
        similarity = Decimal("100") if signals["same_purpose"] else Decimal("0")

        weight = self.WEIGHTS["purpose"]

        return SignalScore(
            name="purpose",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "same_purpose": signals["same_purpose"],
            },
        )

    # ========================================================
    # BEDROOMS
    # ========================================================

    def _score_bedrooms(self, signals: dict) -> SignalScore:
        difference = signals["bedroom_difference"]

        if difference is None:
            similarity = Decimal("0")
        elif difference == 0:
            similarity = Decimal("100")
        elif difference == 1:
            similarity = Decimal("50")
        else:
            similarity = Decimal("0")

        weight = self.WEIGHTS["bedrooms"]

        return SignalScore(
            name="bedrooms",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "difference": difference,
            },
        )

    # ========================================================
    # BATHROOMS
    # ========================================================

    def _score_bathrooms(self, signals: dict) -> SignalScore:
        difference = signals["bathroom_difference"]

        if difference is None:
            similarity = Decimal("0")
        elif difference == 0:
            similarity = Decimal("100")
        elif difference == 1:
            similarity = Decimal("50")
        else:
            similarity = Decimal("0")

        weight = self.WEIGHTS["bathrooms"]

        return SignalScore(
            name="bathrooms",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "difference": difference,
            },
        )

    # ========================================================
    # BUILDING SIZE
    # ========================================================

    def _score_building_size(self, signals: dict) -> SignalScore:
        difference = signals["building_size_difference_percent"]

        similarity = self._percentage_similarity(difference)

        weight = self.WEIGHTS["building_size"]

        return SignalScore(
            name="building_size",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "difference_percent": difference,
            },
        )

    # ========================================================
    # LAND SIZE
    # ========================================================

    def _score_land_size(self, signals: dict) -> SignalScore:
        difference = signals["land_size_difference_percent"]

        similarity = self._percentage_similarity(difference)

        weight = self.WEIGHTS["land_size"]

        return SignalScore(
            name="land_size",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "difference_percent": difference,
            },
        )

    # ========================================================
    # LOCATION
    # ========================================================

    def _score_location(self, signals: dict) -> SignalScore:
        """
        Location is particularly important for room listings.

        Same area:
            100%

        Same LGA but different area:
            50%

        Different LGA:
            0%
        """

        if signals["same_area"]:
            similarity = Decimal("100")
        elif signals["same_lga"]:
            similarity = Decimal("50")
        else:
            similarity = Decimal("0")

        weight = self.WEIGHTS["location"]

        return SignalScore(
            name="location",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "same_area": signals["same_area"],
                "same_lga": signals["same_lga"],
            },
        )

    # ========================================================
    # PRICE
    # ========================================================

    def _score_price(self, signals: dict) -> SignalScore:
        difference = signals["price_difference_percent"]

        similarity = self._percentage_similarity(difference)

        weight = self.WEIGHTS["price"]

        return SignalScore(
            name="price",
            similarity=similarity,
            weight=weight,
            contribution=(similarity / Decimal("100")) * weight,
            details={
                "difference_percent": difference,
            },
        )

    # ========================================================
    # HELPERS
    # ========================================================

    @staticmethod
    def _percentage_similarity(
        difference: Decimal | None,
    ) -> Decimal:
        """
        Convert percentage difference into similarity.

        0% difference:
            100% similarity

        10% difference:
            90% similarity

        25% difference:
            75% similarity

        100%+ difference:
            0% similarity
        """

        if difference is None:
            return Decimal("0")

        similarity = Decimal("100") - Decimal(difference)

        if similarity < 0:
            similarity = Decimal("0")

        return similarity.quantize(Decimal("0.01"))
