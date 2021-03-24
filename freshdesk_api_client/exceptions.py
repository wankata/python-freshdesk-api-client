class FreshdeskClientError(Exception):
    """Base exception class for errors thrown by the Freshdesk API Client"""
    pass


class InvalidPostParams(FreshdeskClientError):
    """Provided dictionary includes unsupported keys"""
    pass


class UnsupportedResponseStatus(FreshdeskClientError):
    """Received unexpected status code"""
    pass
