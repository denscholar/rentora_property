from django.db import transaction

from properties.models.property.eligibility import (
    PropertyEligibilityOption,
    PropertyEligibilityQuestion,
    PropertyEligibilityTest,
)


class PropertyEligibilityService:
    """
    Handles creation and replacement of a property's
    eligibility test configuration.
    """

    @staticmethod
    @transaction.atomic
    def configure_test(
        *,
        submission,
        title="Tenant Eligibility Test",
        description="",
        is_active=True,
        questions=None,
    ):
        """
        Create or replace the eligibility test for a submission.
        """
        PropertyEligibilityService.validate_submission_for_configuration(submission)

        questions = questions or []

        test, _ = PropertyEligibilityTest.objects.get_or_create(
            submission=submission,
            defaults={
                "title": title,
                "description": description,
                "is_active": is_active,
            },
        )

        test.title = title
        test.description = description
        test.is_active = is_active
        test.save()

        # Replace existing configuration.
        test.questions.all().delete()

        for question_data in questions:
            options = question_data.pop(
                "options",
                [],
            )

            question = PropertyEligibilityQuestion.objects.create(
                eligibility_test=test,
                **question_data,
            )

            for option_data in options:
                PropertyEligibilityOption.objects.create(
                    question=question,
                    **option_data,
                )

        return test

    @staticmethod
    def validate_submission_for_configuration(submission):
        if submission.is_archived:
            raise ValueError(
                "An archived property cannot have its "
                "eligibility configuration changed."
            )

        if submission.status != submission.Status.DRAFT:
            raise ValueError(
                "Eligibility configuration can only be changed "
                "while the property is a draft."
            )

    @staticmethod
    @transaction.atomic
    def disable_test(*, submission):
        PropertyEligibilityService.validate_submission_for_configuration(submission)

        test = getattr(
            submission,
            "eligibility_test",
            None,
        )

        if test is None:
            return None

        test.is_active = False
        test.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return test
