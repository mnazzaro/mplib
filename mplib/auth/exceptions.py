"""Exceptions raised by processes in mplib.auth"""

class InvalidTokenError (ValueError):
    """Raised on JWT decode error"""

class ConfigurationError (ValueError):
    """Raised on missing vars in config"""  

class PasswordAuthenticationError (ValueError):
    """Raised on password auth failure"""  

class AuthenticationFailureError (ValueError):
    """Raised on general auth failure"""

class SessionCreationError (ValueError):
    """Raised on failure to create session"""

class CookieUnpackError (ValueError):
    """Raised on failure to unpack cookie"""

class SessionRetrievalError (ValueError):
    """Raised on failure to retrieve session from cookie data"""

class CookieValidationError (ValueError):
    """Raised on failure to validate well formed cookie"""

class ExpiredTokenError (ValueError):
    """Raised on token past expiry"""

class MalformedTokenError (ValueError):
    """Raised on token decode failure"""
