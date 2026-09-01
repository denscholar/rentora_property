from rest_framework import serializers

from properties.models.property.eligibility import (
    PropertyEligibilityAnswer,
    PropertyEligibilityAttempt,
)


class PropertyEligibilityAnswerSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = PropertyEligibilityAnswer

        fields = [
            "uuid",
            "question",
            "answer_text",
            "selected_options",
            "answer_number",
            "answer_date",
        ]

        read_only_fields = [
            "uuid",
            "question",
        ]


class PropertyEligibilityAttemptSerializer(
    serializers.ModelSerializer,
):
    answers = PropertyEligibilityAnswerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = PropertyEligibilityAttempt

        fields = [
            "uuid",
            "test",
            "status",
            "started_at",
            "submitted_at",
            "evaluated_at",
            "passed",
            "evaluation_note",
            "answers",
        ]

        read_only_fields = [
            "uuid",
            "tenant",
            "status",
            "started_at",
            "submitted_at",
            "evaluated_at",
            "passed",
            "evaluation_note",
            "answers",
        ]


class EligibilityAnswerInputSerializer(
    serializers.Serializer,
):
    question = serializers.UUIDField()

    answer_text = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    selected_options = serializers.ListField(
        child=serializers.CharField(
            max_length=100,
        ),
        required=False,
        allow_empty=True,
    )

    answer_number = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    answer_date = serializers.DateField(
        required=False,
        allow_null=True,
    )


class SubmitEligibilityAttemptSerializer(
    serializers.Serializer,
):
    answers = EligibilityAnswerInputSerializer(
        many=True,
    )

    def validate(self, attrs):
        attempt = self.context.get("attempt")

        if attempt is None:
            raise serializers.ValidationError("Eligibility attempt is required.")

        questions = {
            str(question.uuid): question
            for question in (
                attempt.test.questions.filter(
                    is_active=True,
                ).prefetch_related(
                    "options",
                )
            )
        }

        submitted_question_ids = set()

        for answer in attrs["answers"]:
            question_uuid = str(answer["question"])

            if question_uuid in submitted_question_ids:
                raise serializers.ValidationError(
                    {"answers": ["A question may only be answered once."]}
                )

            submitted_question_ids.add(question_uuid)

            question = questions.get(question_uuid)

            if question is None:
                raise serializers.ValidationError(
                    {
                        "answers": [
                            "One or more questions do not belong to this eligibility test."
                        ]
                    }
                )

            question_type = question.question_type

            if question_type == "yes_no":
                value = (answer.get("answer_text") or "").strip().lower()

                if value not in {
                    "yes",
                    "no",
                }:
                    raise serializers.ValidationError(
                        {
                            "answers": [
                                f"Question '{question.question}' requires yes or no."
                            ]
                        }
                    )

            elif question_type in {
                "single_choice",
                "multiple_choice",
            }:
                selected_options = answer.get(
                    "selected_options",
                    [],
                )

                valid_options = {
                    option.value
                    for option in question.options.filter(
                        is_active=True,
                    )
                }

                invalid_options = set(selected_options) - valid_options

                if invalid_options:
                    raise serializers.ValidationError(
                        {
                            "answers": [
                                (
                                    f"Invalid option supplied "
                                    f"for question '{question.question}'."
                                )
                            ]
                        }
                    )

                if question_type == "single_choice" and len(selected_options) != 1:
                    raise serializers.ValidationError(
                        {
                            "answers": [
                                (
                                    f"Question '{question.question}' "
                                    "requires exactly one option."
                                )
                            ]
                        }
                    )

            elif question_type == "number":
                if answer.get("answer_number") is None:
                    raise serializers.ValidationError(
                        {
                            "answers": [
                                f"Question '{question.question}' " "requires a number."
                            ]
                        }
                    )

            elif question_type == "date":
                if answer.get("answer_date") is None:
                    raise serializers.ValidationError(
                        {
                            "answers": [
                                f"Question '{question.question}' " "requires a date."
                            ]
                        }
                    )

            elif question_type == "text":
                if not (answer.get("answer_text") or "").strip():
                    raise serializers.ValidationError(
                        {
                            "answers": [
                                f"Question '{question.question}' " "requires an answer."
                            ]
                        }
                    )

        required_questions = {
            str(question.uuid)
            for question in questions.values()
            if question.is_required
        }

        missing_questions = required_questions - submitted_question_ids

        if missing_questions:
            raise serializers.ValidationError(
                {"answers": ["All required eligibility questions must be answered."]}
            )

        return attrs
