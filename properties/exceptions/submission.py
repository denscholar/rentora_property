from .base import DomainException


class SubmissionNotOwned(DomainException):
    default_message = (
        "You do not own this property submission."
    )


class SubmissionNotEditable(DomainException):
    default_message = (
        "This submission can no longer be edited."
    )


class SubmissionAlreadyArchived(DomainException):
    default_message = (
        "This submission has already been archived."
    )


class InvalidSubmissionTransition(DomainException):
    default_message = (
        "This submission cannot transition to the requested status."
    )


class SubmissionIncomplete(DomainException):
    default_message = (
        "The submission is incomplete."
    )


class InvalidSubmissionRole(DomainException):
    default_message = (
        "Your account cannot submit properties."
    )


class SubmissionIncomplete(DomainException):

    def __init__(self, errors):
        self.errors = errors

        super().__init__(
            "Submission contains validation errors."
        )