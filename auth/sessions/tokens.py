from ...model.domain import Session, session_from_dict
from ..exceptions import InvalidTokenException
import jwt

def encode (session: Session, secret: str) -> str:
    return jwt.encode(session.json_safe_dict(), secret) # Use HS256

def decode (token: str, secret: str) -> Session:
    try:
        data = dict(jwt.decode(token, secret, algorithms=['HS256']))
    except jwt.exceptions.DecodeError as e:
        raise InvalidTokenException('Not a valid token') from e
    return session_from_dict(data)