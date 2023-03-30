from typing import Callable

from werkzeug.exceptions import Unauthorized, InternalServerError

from .base_middleware import BaseMiddleware, WSGIRequest
from ..exceptions import ConfigurationError, InvalidTokenError
from ...model.domain import Session
from ..sessions.tokens import decode

import os

class TokenAuthMiddleware (BaseMiddleware):

    def before(self, environ: dict, start_response: Callable) -> WSGIRequest:
        environ['session'] = None
        environ['token'] = None
        token = environ.get('HTTP_AUTHORIZATION')
        if token is None:
            # TODO: Add logging
            return environ, start_response
        
        secret = environ.get('JWT_SECRET', os.environ.get('JWT_SECRET'))
        if secret is None:
            raise ConfigurationError('Missing decryption token')
        
        try:
            session: Session = decode(token, secret)
            environ['session'] = Session
            environ['token'] = token
        except InvalidTokenError as e:
            # TODO: Add logging
            environ['session'] = Unauthorized('Invalid token auth')
        except Exception as e:
            # TODO: Add logging
            environ['session'] = InternalServerError(f'Unhandled {e}')

        return environ, start_response
        