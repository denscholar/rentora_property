"""
Candidate evaluation for the property duplicate matching engine.

This module evaluates the candidates produced by candidate discovery.

It does NOT:
    - generate candidates
    - normalize properties
    - generate signals
    - calculate scoring weights
    - define thresholds
    - create duplicate groups
    - manage agent representations
"""

from dataclasses import dataclass
from typing import Optional

from properties.models import PropertySubmission

from properties.matching.candidates import (
    get_duplicate_candidates,
)
from properties.matching.constants import (
    ADMIN_REVIEW,
    AUTO_MATCH,
    NOT_DUPLICATE,
)
from properties.matching.service import (
    PropertyMatchResult,
    PropertyMatchingService,
)


@dataclass(frozen=True)
class CandidateMatch:
    """
    Represents one candidate and the result of comparing it
    against the submitted property.
    """

    candidate: PropertySubmission
    result: PropertyMatchResult


@dataclass(frozen=True)
class CandidateEvaluationResult:
    """
    Complete evaluation result for a property submission.
    """

    submission: PropertySubmission

    matches: tuple[CandidateMatch, ...]

    @property
    def auto_matches(self) -> tuple[CandidateMatch, ...]:
        return tuple(
            match for match in self.matches if match.result.decision.is_auto_match
        )

    @property
    def admin_reviews(self) -> tuple[CandidateMatch, ...]:
        return tuple(
            match
            for match in self.matches
            if match.result.decision.requires_admin_review
        )

    @property
    def possible_duplicates(self) -> tuple[CandidateMatch, ...]:
        return self.auto_matches + self.admin_reviews


class PropertyCandidateEvaluator:
    """
    Evaluates duplicate candidates for a PropertySubmission.
    """

    @staticmethod
    def evaluate(
        *,
        submission: PropertySubmission,
    ) -> CandidateEvaluationResult:

        candidates = get_duplicate_candidates(
            submission=submission,
        )

        matches = []

        for candidate in candidates:

            result = PropertyMatchingService.match(
                left=submission,
                right=candidate,
            )

            matches.sort(
                key=lambda match: match.result.score.score,
                reverse=True,
            )

        return CandidateEvaluationResult(
            submission=submission,
            matches=tuple(matches),
        )
