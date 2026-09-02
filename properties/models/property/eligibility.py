from django.db import models

from core.models import BaseModel
from properties.models.property.submission import PropertySubmission


class EligibilityAttemptStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", "In Progress"
    SUBMITTED = "submitted", "Submitted"
    PASSED = "passed", "Passed"
    FAILED = "failed", "Failed"


class EligibilityQuestionType(models.TextChoices):
    YES_NO = "yes_no", "Yes / No"
    SINGLE_CHOICE = "single_choice", "Single Choice"
    MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
    TEXT = "text", "Text"
    NUMBER = "number", "Number"
    DATE = "date", "Date"


# ======================================================
# ELIGIBILITY TEST
# ======================================================


class PropertyEligibilityTest(BaseModel):
    """
    Defines the tenant eligibility configuration for a property
    submission.

    A submission may have one eligibility test configuration.
    """

    submission = models.OneToOneField(
        PropertySubmission,
        on_delete=models.CASCADE,
        related_name="eligibility_test",
    )

    is_active = models.BooleanField(
        default=True,
    )

    title = models.CharField(
        max_length=255,
        default="Tenant Eligibility Test",
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Eligibility Test - {self.submission}"


# ===============================================
# ELIGIBILITY QUESTIONS
# ================================================


class PropertyEligibilityQuestion(BaseModel):
    """
    Represents one question in a property's eligibility test.
    """

    eligibility_test = models.ForeignKey(
        PropertyEligibilityTest,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question = models.CharField(
        max_length=500,
    )

    question_type = models.CharField(
        max_length=30,
        choices=EligibilityQuestionType.choices,
    )

    is_required = models.BooleanField(
        default=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "display_order",
            "created_at",
        ]

    def __str__(self):
        return self.question


# ==========================================
# ELIGIBILITY OPTIONS
# ==========================================


class PropertyEligibilityOption(BaseModel):
    """
    Represents an option belonging to a choice-based
    eligibility question.
    """

    question = models.ForeignKey(
        PropertyEligibilityQuestion,
        on_delete=models.CASCADE,
        related_name="options",
    )

    label = models.CharField(
        max_length=255,
    )

    value = models.CharField(
        max_length=100,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "display_order",
            "created_at",
        ]

    def __str__(self):
        return self.label


# =====================================
# ELIGIBILITY ATTEMPT MODEL
# ======================================


class PropertyEligibilityAttempt(BaseModel):
    """
    Represents one tenant's attempt at completing a property's
    eligibility test.
    """

    test = models.ForeignKey(
        PropertyEligibilityTest,
        on_delete=models.CASCADE,
        related_name="attempts",
    )

    tenant = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.PROTECT,
        related_name="property_eligibility_attempts",
    )

    status = models.CharField(
        max_length=30,
        choices=EligibilityAttemptStatus.choices,
        default=EligibilityAttemptStatus.IN_PROGRESS,
        db_index=True,
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
    )

    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    evaluated_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    passed = models.BooleanField(
        blank=True,
        null=True,
    )

    evaluation_note = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                    "status",
                ],
                name="elig_attempt_tenant_status_idx",
            ),
            models.Index(
                fields=[
                    "test",
                    "status",
                ],
                name="elig_attempt_test_status_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "test",
                    "tenant",
                ],
                condition=models.Q(
                    status=EligibilityAttemptStatus.IN_PROGRESS,
                ),
                name="one_active_attempt_per_tenant",
            ),
        ]

    def __str__(self):
        return (
            f"{self.tenant} - "
            f"{self.test.submission} - "
            f"{self.get_status_display()}"
        )


# =================================================
# ANSWER MODEL
# =================================================
class PropertyEligibilityAnswer(BaseModel):
    """
    Stores one tenant's answer to one eligibility question.
    """

    attempt = models.ForeignKey(
        PropertyEligibilityAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    question = models.ForeignKey(
        PropertyEligibilityQuestion,
        on_delete=models.PROTECT,
        related_name="answers",
    )

    answer_text = models.TextField(
        blank=True,
    )

    selected_options = models.JSONField(
        default=list,
        blank=True,
    )

    answer_number = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    answer_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["question__display_order"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "attempt",
                    "question",
                ],
                name="unique_attempt_question_answer",
            ),
        ]

    def __str__(self):
        return f"{self.attempt} - " f"{self.question.question}"




class PropertyEligibilityRule(BaseModel):
    """
    Defines the condition used to evaluate a tenant's answer
    to an eligibility question.

    Only the fields relevant to the question type are used.
    """

    question = models.OneToOneField(
        PropertyEligibilityQuestion,
        on_delete=models.CASCADE,
        related_name="rule",
    )

    # =====================================================
    # TEXT / YES-NO
    # =====================================================

    expected_text = models.CharField(
        max_length=255,
        blank=True,
    )

    # =====================================================
    # NUMBER
    # =====================================================

    minimum_number = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    maximum_number = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # =====================================================
    # DATE
    # =====================================================

    minimum_date = models.DateField(
        blank=True,
        null=True,
    )

    maximum_date = models.DateField(
        blank=True,
        null=True,
    )

    # =====================================================
    # CHOICE
    # =====================================================

    accepted_options = models.JSONField(
        default=list,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rule - {self.question.question}"