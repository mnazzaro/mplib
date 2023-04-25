from typing import Tuple

from ...model.domain import Session
from ..exceptions import CookieUnpackError

import jwt

from datetime import datetime

"""
A Metal Poker Session Cookie is a regular JWT containing...
    - session_id
    - user_id
    - nonce
    - expires (expiration time)
"""

CookieData = Tuple[int, int, str, datetime]

def generate_cookie (session: Session, secret: str) -> str:
    if session.end_time is None:
        raise RuntimeError('Session has no expiry')
    if session.user is None:
        raise RuntimeError('Session user is not set')
    return jwt.encode({
        'session_id': session.session_id,
        'user_id': session.user.user_id,
        'nonce': session.nonce,
        'expires': session.end_time.isoformat()
        }, 
        key=secret)

def unpack_cookie (cookie: str, secret: str) -> CookieData:
    try:
        unpacked = dict(jwt.decode(cookie, secret, algorithms=['HS256']))
    except Exception as e:
        raise CookieUnpackError (f"Malformed cookie: {e}")
    return unpacked['session_id'], unpacked['user_id'], \
            unpacked['nonce'], unpacked['expires']