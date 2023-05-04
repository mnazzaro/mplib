from typing import Tuple, Optional
from ..model.models import DBPlayer, db
from .passwords import check_password, is_ascii
from .exceptions import MalformedTokenError, ExpiredTokenError, \
    AuthenticationFailureError
from ..model.domain import Session, Authorizations
from .sessions.session_store import SessionStore
from .tokens.tokens import unpack_token

PasswordData = Tuple[bytes, bytes] # pass_hash, salt

def _get_user_by_email (email: str) -> Optional[DBPlayer]:
    return db.session.query(DBPlayer) \
        .filter_by(email=email) \
        .first()

def _get_user_by_id (user_id: int) -> Optional[DBPlayer]:
    return db.session.query(DBPlayer) \
        .filter_by(player_id=id) \
        .first()

def authenticate_password (email: str, password: str) -> DBPlayer:
    """Authenticate a player from their email/password"""

    if not password:
        raise ValueError('Passed empty password')
    if not isinstance(password, str):
        raise ValueError(f'Passed non-str password: {type(password)}')
    if not is_ascii(password):
        raise ValueError('Password non-ascii password')

    if not email:
        raise ValueError('Passed empty email')
    if not isinstance(email, str):
        raise ValueError(f'Passed non-str email: {type(email)}')
    if len(email) > 255:
        raise ValueError(f'Passed email too long: len {len(email)}')
    if not is_ascii(email):
        raise ValueError('Passed non-ascii email')
    
    user: DBPlayer = _get_user_by_email(email) # TODO: Handle DB unavailable
    if user is None:
        raise AuthenticationFailureError (f'No account exists corresponsing to {email}') # Careful there... email is dirty. TODO: throw a more descriptive error
    try:
        if check_password(password, user.salt, user.pass_hash):
            return user
    except:
        raise
    # except PasswordAuthenticationError as e:
    #     raise AuthenticationFailureError(f'Authentication failed with {e}')

def authenticate_token (token: str, secret: str) -> Session:
    """Authenticate a player from an access token"""

    if not token:
        raise ValueError('Passed empty token')
    if not isinstance(token, str):
        raise ValueError(f'Passed non-str token: {type(token)}')
    try:
        session: Session = unpack_token(token, secret)
    except MalformedTokenError as e:
        raise AuthenticationFailureError from e
    
    if session.expired:
        raise ExpiredTokenError
    
    return session

    