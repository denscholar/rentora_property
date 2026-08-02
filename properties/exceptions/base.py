class DomainException(Exception):
    """
    Base class for all business rule violations.

    Services should raise subclasses of DomainException instead of
    Django ValidationError.
    """

    default_message = "A business rule has been violated."

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)