from dataclasses import fields

from properties.dto import SubmissionDraftDTO


def apply_submission_draft(
    *,
    submission,
    draft: SubmissionDraftDTO,
):
    """
    Copies values from a DTO into a PropertySubmission model.
    """

    for field in fields(draft):

        if field.name == "amenities":
            continue

        setattr(
            submission,
            field.name,
            getattr(
                draft,
                field.name,
            ),
        )

    return submission