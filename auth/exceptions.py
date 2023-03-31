"""Exceptions raised by processes in mplib.auth"""

class InvalidTokenError (ValueError):
    """Raised on JWT decode error"""

class ConfigurationError (ValueError):
    """Raised on missing vars in config"""  

class PasswordAuthenticationError (ValueError):
    """Raised on password auth failure"""  

class AuthenticationFailureError (ValueError):
    """Raised on general auth failure"""