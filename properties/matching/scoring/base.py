from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from properties.matching.scoring.similarity import weighted_contribution

# ============================================================
# SCORE DATA STRUCTURES
# ============================================================


@dataclass(frozen=True)
class SignalScore:
    """
    Represents the score produced by one matching signal.
    """

    name: str
    similarity: Decimal
    weight: Decimal
    contribution: Decimal
    details: dict[str, Any]


@dataclass(frozen=True)
class MatchScore:
    """
    Represents the complete similarity score between two properties.
    """

    category: str
    score: Decimal
    signals: tuple[SignalScore, ...]


# ============================================================
# BASE SCORER
# ============================================================


class BasePropertyScorer:
    """
    Base implementation shared by all property-category scorers.
    """

    category: str = ""

    WEIGHTS: dict[str, Decimal] = {}

    # ========================================================
    # BUILD SIGNAL SCORE
    # ========================================================

    def build_signal_score(
        self,
        *,
        name: str,
        similarity: Decimal,
        details: dict[str, Any] | None = None,
    ) -> SignalScore:
        """
        Convert a similarity value into a weighted SignalScore.
        """

        weight = self.WEIGHTS.get(
            name,
            Decimal("0"),
        )

        contribution = weighted_contribution(
            similarity,
            weight,
        )

        return SignalScore(
            name=name,
            similarity=Decimal(str(similarity)).quantize(Decimal("0.01")),
            weight=weight,
            contribution=contribution,
            details=details or {},
        )

    # ========================================================
    # BUILD COMPLETE SCORE
    # ========================================================

    def build_score(
        self,
        *,
        signals: list[SignalScore],
    ) -> MatchScore:
        """
        Combine individual signal contributions into one
        overall similarity score.
        """

        total = sum(
            (signal.contribution for signal in signals),
            Decimal("0"),
        )

        return MatchScore(
            category=self.category,
            score=total.quantize(Decimal("0.01")),
            signals=tuple(signals),
        )
