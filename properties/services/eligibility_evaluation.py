from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from properties.models import (
    EligibilityAttemptStatus,
    EligibilityQuestionType,
    PropertyEligibilityAnswer,
    PropertyEligibilityAttempt,
)


class PropertyEligibilityEvaluationService:
    """
    Evaluates a tenant's answers against the eligibility
    rules configured for a property.
    """

    @classmethod
    @transaction.atomic
    def evaluate(cls, *, attempt):
        if attempt.status != EligibilityAttemptStatus.IN_PROGRESS:
            raise ValueError("This eligibility attempt has already been submitted.")

        questions = (
            attempt.test.questions.filter(
                is_active=True,
            )
            .prefetch_related(
                "options",
                "rule",
            )
            .order_by(
                "display_order",
            )
        )

        answers = {
            str(answer.question.uuid): answer for answer in attempt.answers.all()
        }

        results = []
        passed = True

        for question in questions:
            answer = answers.get(str(question.uuid))

            if question.is_required and answer is None:
                passed = False

                results.append(
                    {
                        "question": question.question,
                        "passed": False,
                        "reason": "Required question was not answered.",
                    }
                )

                continue

            if answer is None:
                results.append(
                    {
                        "question": question.question,
                        "passed": True,
                        "reason": "Optional question was not answered.",
                    }
                )

                continue

            question_passed, reason = cls.evaluate_answer(
                question=question,
                answer=answer,
            )

            if not question_passed:
                passed = False

            results.append(
                {
                    "question": question.question,
                    "passed": question_passed,
                    "reason": reason,
                }
            )

        now = timezone.now()

        attempt.status = (
            EligibilityAttemptStatus.PASSED
            if passed
            else EligibilityAttemptStatus.FAILED
        )

        attempt.passed = passed
        attempt.submitted_at = now
        attempt.evaluated_at = now
        attempt.evaluation_note = (
            "Eligibility test passed." if passed else "Eligibility test failed."
        )

        attempt.save(
            update_fields=[
                "status",
                "passed",
                "submitted_at",
                "evaluated_at",
                "evaluation_note",
                "updated_at",
            ]
        )

        return {
            "passed": passed,
            "results": results,
        }

    @classmethod
    def evaluate_answer(
        cls,
        *,
        question,
        answer,
    ):
        rule = getattr(
            question,
            "rule",
            None,
        )

        if rule is None:
            return (
                True,
                "No evaluation rule configured.",
            )

        question_type = question.question_type

        # =====================================================
        # YES / NO
        # =====================================================

        if question_type == EligibilityQuestionType.YES_NO:
            actual = (answer.answer_text or "").strip().lower()

            expected = (rule.expected_text or "").strip().lower()

            if actual == expected:
                return True, "Answer matched the requirement."

            return (
                False,
                "Answer did not match the requirement.",
            )

        # =====================================================
        # TEXT
        # =====================================================

        if question_type == EligibilityQuestionType.TEXT:
            actual = (answer.answer_text or "").strip().lower()

            expected = (rule.expected_text or "").strip().lower()

            if actual == expected:
                return True, "Answer matched the requirement."

            return (
                False,
                "Answer did not match the requirement.",
            )

        # =====================================================
        # NUMBER
        # =====================================================

        if question_type == EligibilityQuestionType.NUMBER:
            actual = answer.answer_number

            if actual is None:
                return (
                    False,
                    "A number was required.",
                )

            if rule.minimum_number is not None and actual < rule.minimum_number:
                return (
                    False,
                    "Answer is below the minimum requirement.",
                )

            if rule.maximum_number is not None and actual > rule.maximum_number:
                return (
                    False,
                    "Answer exceeds the maximum requirement.",
                )

            return (
                True,
                "Answer satisfied the numeric requirement.",
            )

        # =====================================================
        # DATE
        # =====================================================

        if question_type == EligibilityQuestionType.DATE:
            actual = answer.answer_date

            if actual is None:
                return (
                    False,
                    "A date was required.",
                )

            if rule.minimum_date is not None and actual < rule.minimum_date:
                return (
                    False,
                    "Date is earlier than allowed.",
                )

            if rule.maximum_date is not None and actual > rule.maximum_date:
                return (
                    False,
                    "Date is later than allowed.",
                )

            return (
                True,
                "Answer satisfied the date requirement.",
            )

        # =====================================================
        # SINGLE CHOICE
        # =====================================================

        if question_type == EligibilityQuestionType.SINGLE_CHOICE:
            selected = answer.selected_options or []

            if len(selected) != 1:
                return (
                    False,
                    "Exactly one option is required.",
                )

            if selected[0] in rule.accepted_options:
                return (
                    True,
                    "Selected option is accepted.",
                )

            return (
                False,
                "Selected option is not accepted.",
            )

        # =====================================================
        # MULTIPLE CHOICE
        # =====================================================

        if question_type == EligibilityQuestionType.MULTIPLE_CHOICE:
            selected = set(answer.selected_options or [])

            accepted = set(rule.accepted_options or [])

            if selected.issubset(accepted):
                return (
                    True,
                    "Selected options are accepted.",
                )

            return (
                False,
                "One or more selected options are not accepted.",
            )

        return (
            False,
            "Unsupported eligibility question type.",
        )
