from typing import Callable

from werkzeug.exceptions import Unauthorized, InternalServerError

from ...base.base_middleware import BaseMiddleware, WSGIRequest
from ..exceptions import ConfigurationError, InvalidTokenError
from ...model.domain import Session
from ..tokens.tokens import unpack_token
from ..authenticate import authenticate_token

import os

class TokenAuthMiddleware (BaseMiddleware):

    def before(self, environ: dict, start_response: Callable) -> WSGIRequest:
        environ['session'] = None
        environ['token'] = None
        token = environ.get('HTTP_AUTHORIZATION') # TODO: Change to Authorization
        if token is None:
            # TODO: Add logging
            return environ, start_response
        
        secret = environ.get('JWT_SECRET', os.environ.get('JWT_SECRET'))
        if secret is None:
            raise ConfigurationError('Missing decryption secret')
        
        try:
            session: Session = authenticate_token(token, secret)
            environ['session'] = session
            environ['token'] = token
        except InvalidTokenError as e:
            # TODO: Add logging
            environ['session'] = Unauthorized('Invalid token auth')
        except Exception as e:
            # TODO: Add logging
            environ['session'] = InternalServerError(f'Unhandled {e}')

        return environ, start_response
        