from rest_framework import serializers

from properties.models.property.eligibility import (
    EligibilityQuestionType,
    PropertyEligibilityOption,
    PropertyEligibilityQuestion,
    PropertyEligibilityTest,
    PropertyEligibilityRule,
)


class PropertyEligibilityOptionSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = PropertyEligibilityOption
        fields = [
            "uuid",
            "label",
            "value",
            "display_order",
            "is_active",
        ]
        read_only_fields = [
            "uuid",
        ]


class PropertyEligibilityRuleSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = PropertyEligibilityRule

        fields = [
            "uuid",
            "expected_text",
            "minimum_number",
            "maximum_number",
            "minimum_date",
            "maximum_date",
            "accepted_options",
        ]

        read_only_fields = [
            "uuid",
        ]


class PropertyEligibilityQuestionSerializer(
    serializers.ModelSerializer,
):
    options = PropertyEligibilityOptionSerializer(
        many=True,
        required=False,
    )

    rule = PropertyEligibilityRuleSerializer(
        required=False,
    )

    class Meta:
        model = PropertyEligibilityQuestion

        fields = [
            "uuid",
            "question",
            "question_type",
            "is_required",
            "display_order",
            "is_active",
            "options",
            "rule",
        ]

        read_only_fields = [
            "uuid",
        ]

    def validate(self, attrs):
        question_type = attrs.get("question_type")

        options = attrs.get(
            "options",
            [],
        )

        rule = attrs.get(
            "rule",
            {},
        )

        choice_types = {
            EligibilityQuestionType.SINGLE_CHOICE,
            EligibilityQuestionType.MULTIPLE_CHOICE,
        }

        if question_type in choice_types and not options:
            raise serializers.ValidationError(
                {"options": ("Options are required for " "choice-based questions.")}
            )

        if question_type not in choice_types and options:
            raise serializers.ValidationError(
                {
                    "options": (
                        "Options are only supported for " "choice-based questions."
                    )
                }
            )

        if question_type == EligibilityQuestionType.YES_NO:
            expected_text = rule.get("expected_text", "").strip().lower()

            if expected_text not in {
                "yes",
                "no",
            }:
                raise serializers.ValidationError(
                    {
                        "rule": (
                            "YES/NO questions require an "
                            "expected_text value of yes or no."
                        )
                    }
                )

        elif question_type == EligibilityQuestionType.NUMBER:
            minimum = rule.get("minimum_number")

            maximum = rule.get("maximum_number")

            if minimum is None and maximum is None:
                raise serializers.ValidationError(
                    {
                        "rule": (
                            "Number questions require " "a minimum or maximum value."
                        )
                    }
                )

            if minimum is not None and maximum is not None and minimum > maximum:
                raise serializers.ValidationError(
                    {
                        "rule": (
                            "Minimum number cannot be " "greater than maximum number."
                        )
                    }
                )

        elif question_type == EligibilityQuestionType.DATE:
            minimum_date = rule.get("minimum_date")

            maximum_date = rule.get("maximum_date")

            if minimum_date is None and maximum_date is None:
                raise serializers.ValidationError(
                    {"rule": ("Date questions require " "a minimum or maximum date.")}
                )

            if (
                minimum_date is not None
                and maximum_date is not None
                and minimum_date > maximum_date
            ):
                raise serializers.ValidationError(
                    {"rule": ("Minimum date cannot be " "after maximum date.")}
                )

        elif question_type in choice_types:
            accepted_options = rule.get(
                "accepted_options",
                [],
            )

            valid_options = {option.get("value") for option in options}

            if not accepted_options:
                raise serializers.ValidationError(
                    {"rule": ("At least one accepted option " "is required.")}
                )

            invalid_options = set(accepted_options) - valid_options

            if invalid_options:
                raise serializers.ValidationError(
                    {
                        "rule": (
                            "Accepted options must belong " "to the question's options."
                        )
                    }
                )

        elif question_type == EligibilityQuestionType.TEXT:
            expected_text = rule.get(
                "expected_text",
                "",
            ).strip()

            if not expected_text:
                raise serializers.ValidationError(
                    {"rule": ("Text questions require " "an expected_text value.")}
                )

        return attrs


class PropertyEligibilityTestSerializer(
    serializers.ModelSerializer,
):
    questions = PropertyEligibilityQuestionSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = PropertyEligibilityTest
        fields = [
            "uuid",
            "title",
            "description",
            "is_active",
            "questions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uuid",
            "created_at",
            "updated_at",
        ]
