class DomainError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message: str):
        self.message = message
