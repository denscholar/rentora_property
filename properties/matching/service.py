"""
Property duplicate-matching orchestration service.

This module coordinates the existing matching components.

It does not contain:
    - database queries
    - scoring weights
    - normalization rules
    - signal calculations
    - threshold definitions
    - grouping logic
    - agent representation logic
"""

from dataclasses import dataclass

from properties.matching.category import (
    resolve_property_category,
)
from properties.matching.decision import (
    MatchDecision,
    decide_match,
)
from properties.matching.normalization import (
    normalize_submission,
)
from properties.matching.scoring.base import (
    MatchScore,
)
from properties.matching.scoring.registry import (
    get_scorer,
)
from properties.matching.signals import (
    generate_signals,
)


@dataclass(frozen=True)
class PropertyMatchResult:
    """
    Complete result of comparing two properties.
    """

    category: str
    score: MatchScore
    decision: MatchDecision


class PropertyMatchingService:
    """
    Coordinates the property duplicate-matching engine.

    The service orchestrates the existing matching components.
    It does not implement their internal logic.
    """

    @staticmethod
    def match(
        *,
        left,
        right,
    ) -> PropertyMatchResult:
        """
        Compare two PropertySubmission objects and return
        the complete matching result.
        """

        # ====================================================
        # 1. NORMALIZE BOTH PROPERTIES
        # ====================================================

        left_normalized = normalize_submission(left)
        right_normalized = normalize_submission(right)

        # ====================================================
        # 2. RESOLVE CANONICAL CATEGORIES
        # ====================================================

        left_category = resolve_property_category(
            left.property_type,
        )

        right_category = resolve_property_category(
            right.property_type,
        )

        # ====================================================
        # 3. CATEGORIES MUST MATCH
        # ====================================================

        if left_category != right_category:
            raise ValueError(
                "Properties from different matching categories "
                "cannot be compared as duplicates."
            )

        category = left_category

        # ====================================================
        # 4. GENERATE COMPARISON SIGNALS
        # ====================================================

        signals = generate_signals(
            left=left_normalized,
            right=right_normalized,
            left_category=left_category,
            right_category=right_category,
        )

        # ====================================================
        # 5. GET CATEGORY-SPECIFIC SCORER
        # ====================================================

        scorer = get_scorer(category)

        # ====================================================
        # 6. CALCULATE MATCH SCORE
        # ====================================================

        match_score = scorer.score(
            signals=signals,
        )

        # ====================================================
        # 7. CONVERT SCORE INTO BUSINESS DECISION
        # ====================================================

        decision = decide_match(
            match_score,
        )

        # ====================================================
        # 8. RETURN COMPLETE RESULT
        # ====================================================

        return PropertyMatchResult(
            category=category,
            score=match_score,
            decision=decision,
        )
