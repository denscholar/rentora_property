"""
Match decision engine.

This module converts a MatchScore into a business decision.

It does not:
    - query the database
    - generate signals
    - calculate similarity
    - know anything about agents
    - create duplicate groups

Its only responsibility is deciding what a calculated score means.
"""

from dataclasses import dataclass
from decimal import Decimal

from properties.matching.constants import (
    ADMIN_REVIEW,
    AUTO_MATCH,
    CATEGORY_THRESHOLDS,
    NOT_DUPLICATE,
)
from properties.matching.scoring.base import MatchScore

# ============================================================
# DECISION RESULT
# ============================================================


@dataclass(frozen=True)
class MatchDecision:
    """
    Represents the business decision produced from a MatchScore.
    """

    category: str
    score: Decimal
    decision: str
    auto_match_threshold: Decimal
    admin_review_threshold: Decimal

    @property
    def is_auto_match(self) -> bool:
        return self.decision == AUTO_MATCH

    @property
    def requires_admin_review(self) -> bool:
        return self.decision == ADMIN_REVIEW

    @property
    def is_not_duplicate(self) -> bool:
        return self.decision == NOT_DUPLICATE


# ============================================================
# THRESHOLD LOOKUP
# ============================================================


def get_thresholds(category: str) -> dict[str, Decimal]:
    """
    Return the configured thresholds for a property category.
    """

    try:
        thresholds = CATEGORY_THRESHOLDS[category]
    except KeyError:
        raise ValueError(f"Unsupported property matching category: {category!r}")

    return {
        "auto_match": Decimal(str(thresholds["auto_match"])),
        "admin_review": Decimal(str(thresholds["admin_review"])),
    }


# ============================================================
# DECISION
# ============================================================


def decide_match(match_score: MatchScore) -> MatchDecision:
    """
    Convert a MatchScore into a business decision.

    Rules:

        score >= auto_match threshold
            -> AUTO_MATCH

        score >= admin review threshold
            -> ADMIN_REVIEW

        score < admin review threshold
            -> NOT_DUPLICATE
    """

    thresholds = get_thresholds(match_score.category)

    auto_match_threshold = thresholds["auto_match"]
    admin_review_threshold = thresholds["admin_review"]

    score = match_score.score

    if score >= auto_match_threshold:
        decision = AUTO_MATCH

    elif score >= admin_review_threshold:
        decision = ADMIN_REVIEW

    else:
        decision = NOT_DUPLICATE

    return MatchDecision(
        category=match_score.category,
        score=score,
        decision=decision,
        auto_match_threshold=auto_match_threshold,
        admin_review_threshold=admin_review_threshold,
    )
