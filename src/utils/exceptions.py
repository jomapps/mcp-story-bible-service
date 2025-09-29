"""Custom exception hierarchy for the Story Bible Service."""


class ServiceError(Exception):
    """Base exception for service-level errors."""


class PayloadCMSException(ServiceError):
    """Raised when PayloadCMS operations fail."""


class BrainServiceException(ServiceError):
    """Raised when Brain Service integrations fail."""


class AuthorizationError(ServiceError):
    """Raised when authorization checks fail."""
