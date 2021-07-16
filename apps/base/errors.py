class RevertError(Exception):
    """Exception thrown when something goes wrong with reverting a model."""


class RevisionManagementError(Exception):
    """Exception that is thrown when something goes wrong with version managment."""


class RegistrationError(Exception):
    """Exception thrown when registration with revision goes wrong."""

class PermissionDenied(Exception):
    """Exception raised when try to access without permission"""