from typing import Tuple, Optional

from ...model.domain import Session, session_from_dict
from ..exceptions import MalformedTokenError, ExpiredTokenError

import jwt
import secrets

import datetime as dt
from datetime import datetime
from pytz import UTC

# TODO: We need to encrypt these... Make them opaque

"""
A Metal Poker access token is a regular JWT containing...
    - user_id
    - nonce
    - expires (expiration time)
"""

def generate_token (session: Session, secret: str) -> str:
    return jwt.encode(session.json_safe_dict(), secret) # Uses HS256

def unpack_token (token: str, secret: str) -> Session:
    try:
        data = dict(jwt.decode(token, secret, algorithms=['HS256']))
    except jwt.exceptions.DecodeError as e:
        raise MalformedTokenError('Not a valid token') from e
    return session_from_dict(data)
