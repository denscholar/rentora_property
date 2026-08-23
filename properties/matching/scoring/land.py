from decimal import Decimal

from properties.matching.scoring.base import (
    BasePropertyScorer,
    MatchScore,
    SignalScore,
)


class LandScorer(BasePropertyScorer):
    """
    Scores similarity between two land properties.

    Land is treated differently from buildings because the physical
    land parcel itself is the primary identity.

    Location and land size therefore carry significantly more weight
    than characteristics such as bedrooms or bathrooms, which do not
    apply to land.
    """

    category = "land"

    WEIGHTS = {
        "area": Decimal("20"),
        "property_type": Decimal("15"),
        "purpose": Decimal("10"),
        "land_size": Decimal("20"),
        "location": Decimal("25"),
        "price": Decimal("10"),
    }

    # ========================================================
    # PUBLIC SCORING METHOD
    # ========================================================

    def score(self, signals: dict) -> MatchScore:
        """
        Convert generated comparison signals into a complete
        land-property MatchScore.
        """

        signal_scores = [
            self._score_area(signals),
            self._score_property_type(signals),
            self._score_purpose(signals),
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
        Location is the strongest signal for land.

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
