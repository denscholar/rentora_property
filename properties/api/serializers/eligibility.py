from rest_framework import serializers

from properties.models.property.eligibility import EligibilityQuestionType, PropertyEligibilityOption, PropertyEligibilityQuestion, PropertyEligibilityTest


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


class PropertyEligibilityQuestionSerializer(
    serializers.ModelSerializer,
):
    options = PropertyEligibilityOptionSerializer(
        many=True,
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
        ]
        read_only_fields = [
            "uuid",
        ]

    def validate(self, attrs):
        question_type = attrs.get(
            "question_type"
        )

        options = attrs.get(
            "options",
            [],
        )

        choice_types = {
            EligibilityQuestionType.SINGLE_CHOICE,
            EligibilityQuestionType.MULTIPLE_CHOICE,
        }

        if (
            question_type in choice_types
            and not options
        ):
            raise serializers.ValidationError(
                {
                    "options": (
                        "Options are required for "
                        "choice-based questions."
                    )
                }
            )

        if (
            question_type not in choice_types
            and options
        ):
            raise serializers.ValidationError(
                {
                    "options": (
                        "Options are only supported for "
                        "choice-based questions."
                    )
                }
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