"""Exceptions raised by processes in mplib.auth"""

class InvalidTokenException (ValueError):
    """Raised on JWT decode error"""