from decimal import Decimal

from properties.matching.scoring.base import (
    BasePropertyScorer,
    MatchScore,
)
from properties.matching.scoring.similarity import (
    boolean_similarity,
    numeric_difference_similarity,
    percentage_difference_similarity,
)


class ApartmentScorer(BasePropertyScorer):
    """
    Scores similarity between two apartment/flat properties.
    """

    category = "apartment"

    WEIGHTS = {
        "area": Decimal("20"),
        "property_type": Decimal("15"),
        "purpose": Decimal("10"),
        "bedrooms": Decimal("12"),
        "bathrooms": Decimal("8"),
        "building_size": Decimal("10"),
        "land_size": Decimal("5"),
        "location": Decimal("15"),
        "price": Decimal("5"),
    }

    def score(
        self,
        *,
        signals: dict,
    ) -> MatchScore:
        """
        Convert raw apartment comparison signals into
        weighted SignalScore objects and return the
        complete MatchScore.
        """

        signal_scores = []

        # ====================================================
        # AREA
        # ====================================================

        area_similarity = boolean_similarity(
            signals["same_area"]
        )

        signal_scores.append(
            self.build_signal_score(
                name="area",
                similarity=area_similarity,
                details={
                    "same_area": signals["same_area"],
                },
            )
        )

        # ====================================================
        # PROPERTY TYPE
        # ====================================================

        property_type_similarity = boolean_similarity(
            signals["same_property_type"]
        )

        signal_scores.append(
            self.build_signal_score(
                name="property_type",
                similarity=property_type_similarity,
                details={
                    "same_property_type": (
                        signals["same_property_type"]
                    ),
                },
            )
        )

        # ====================================================
        # PURPOSE
        # ====================================================

        purpose_similarity = boolean_similarity(
            signals["same_purpose"]
        )

        signal_scores.append(
            self.build_signal_score(
                name="purpose",
                similarity=purpose_similarity,
                details={
                    "same_purpose": signals["same_purpose"],
                },
            )
        )

        # ====================================================
        # BEDROOMS
        # ====================================================

        bedroom_similarity = numeric_difference_similarity(
            signals["bedroom_difference"],
            maximum_difference=2,
        )

        signal_scores.append(
            self.build_signal_score(
                name="bedrooms",
                similarity=bedroom_similarity,
                details={
                    "difference": (
                        signals["bedroom_difference"]
                    ),
                },
            )
        )

        # ====================================================
        # BATHROOMS
        # ====================================================

        bathroom_similarity = numeric_difference_similarity(
            signals["bathroom_difference"],
            maximum_difference=2,
        )

        signal_scores.append(
            self.build_signal_score(
                name="bathrooms",
                similarity=bathroom_similarity,
                details={
                    "difference": (
                        signals["bathroom_difference"]
                    ),
                },
            )
        )

        # ====================================================
        # BUILDING SIZE
        # ====================================================

        building_size_similarity = (
            percentage_difference_similarity(
                signals["building_size_difference_percent"]
            )
        )

        signal_scores.append(
            self.build_signal_score(
                name="building_size",
                similarity=building_size_similarity,
                details={
                    "difference_percent": (
                        signals[
                            "building_size_difference_percent"
                        ]
                    ),
                },
            )
        )

        # ====================================================
        # LAND SIZE
        # ====================================================

        land_size_similarity = (
            percentage_difference_similarity(
                signals["land_size_difference_percent"]
            )
        )

        signal_scores.append(
            self.build_signal_score(
                name="land_size",
                similarity=land_size_similarity,
                details={
                    "difference_percent": (
                        signals[
                            "land_size_difference_percent"
                        ]
                    ),
                },
            )
        )

        # ====================================================
        # LOCATION
        # ====================================================

        location_similarity = (
            (
                boolean_similarity(
                    signals["same_area"]
                )
                +
                boolean_similarity(
                    signals["same_lga"]
                )
            )
            / Decimal("2")
        )

        signal_scores.append(
            self.build_signal_score(
                name="location",
                similarity=location_similarity,
                details={
                    "same_area": signals["same_area"],
                    "same_lga": signals["same_lga"],
                    "street_similarity": signals[
                        "street_similarity"
                    ],
                    "landmark_similarity": signals[
                        "landmark_similarity"
                    ],
                },
            )
        )

        # ====================================================
        # PRICE
        # ====================================================

        price_similarity = (
            percentage_difference_similarity(
                signals["price_difference_percent"]
            )
        )

        signal_scores.append(
            self.build_signal_score(
                name="price",
                similarity=price_similarity,
                details={
                    "difference_percent": (
                        signals["price_difference_percent"]
                    ),
                },
            )
        )

        # ====================================================
        # FINAL SCORE
        # ====================================================

        return self.build_score(
            signals=signal_scores,
        )