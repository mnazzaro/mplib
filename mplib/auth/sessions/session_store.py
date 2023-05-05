from typing import Optional, Tuple

from datetime import datetime, timedelta
from pytz import UTC

import redis
# import rediscluster

import jwt
import uuid
import os
import secrets

from ...model.domain import Authorizations, Session, \
    Client, User, session_from_dict
from ..exceptions import SessionCreationError, CookieUnpackError, \
    SessionRetrievalError, CookieValidationError
from .cookies import generate_cookie, unpack_cookie
from ...base.globals import get_application_config, get_application_global


CookieData = Tuple[int, int, str, datetime]

def _generate_nonce(length: int = 32):
    return secrets.token_urlsafe(length)

class SessionStore:

    def __init__(self, host: str, port: int, db: int, secret: str,
                 duration: int = 7200, cluster: bool = True, 
                 fake: bool = False) -> None:
        self._secret = secret
        self._duration = duration
        # TODO: Add fakeredis for testing

        # TODO: FIX PYTHON VERSION TO ALLOW FOR STRICTREDISCLUSTER
        # if cluster:
        #     self.r = redis.StrictRedisCluster(
        #         startup_nodes=[{'host': host, 'port': str(port)}],
        #         skip_full_coverage_check=True # TODO: We will probably have to reevaluate this later
        #     )
        # else:
        #     self.r = redis.StrictRedis(host=host, port=port)
        self.r = redis.StrictRedis(host=host, port=port)

    def create (self, authorizations: Authorizations, 
                ip_address: str, remote_host: str, 
                user: Optional[User] = None, 
                client: Optional[Client] = None,
                session_id: Optional[str] = None) -> Session:
        if session_id is None:
            session_id = uuid.uuid4().int # TODO: This may be a security vulnerability and/or have overlap
        start_time = datetime.now(tz=UTC)
        end_time = start_time + timedelta(seconds=self._duration)
        session = Session(
            session_id=session_id,
            user=user,
            client=client,
            start_time=start_time,
            end_time=end_time,
            authorizations=authorizations,
            nonce=_generate_nonce())
        try:
            self.r.set(session_id, 
                       jwt.encode(session.json_safe_dict(), self._secret),
                       ex=self._duration)
        except redis.exceptions.ConnectionError as e:
            raise SessionCreationError(f'Connection failed: {e}') from e
        except Exception as e:
            raise SessionCreationError(f'Failed to create: {e}') from e
        return session
    
    
    def validate_cookie (self, cookie: str) -> Session:
        # TODO: Totally freeballed this one. Will need to test extensively
        try:
            session_id, user_id, nonce, expires = unpack_cookie(cookie, self._secret)
        except CookieUnpackError:
            # TODO: Add logging
            raise
        if type(user_id) != int or type(session_id) != int or \
            type(nonce) != str or type(expires) != datetime:
            raise SessionRetrievalError (f'Failed to retrieve session with malformed cookie: {cookie}')
        try:
            data = self.r.get(str(session_id))
        except Exception as e: # TODO: Do better here
            raise SessionRetrievalError (f'Session store unavailable: {e}')
        if data is not None:
            session = session_from_dict(data)
        else:
            raise RuntimeError ('Failed to create session from cookie')
        
        # If the following three checks don't match, it is probably a malicious login
        # This should raise flags in the system, so we throw a different type of exception
        if session.user.user_id != user_id:
            raise CookieValidationError (f'Failed to validate session {session_id}: provided user_id ({user_id}) \
                                          does not match expected user_id ({session.user.user_id})')
        if session.expired:
            raise CookieValidationError (f'Session {session_id} is expired')
        if session.nonce != nonce:
            raise CookieValidationError (f'Failed to validate session {session_id}: provided nonce ({nonce}) \
                                          does not match expected nonce ({session.nonce})')
        return session
    
    # TODO: Change these to our values later
    @classmethod
    def init_app(cls, app: object = None) -> None:
        """Set default configuration parameters for an application instance."""
        config = get_application_config(app)
        config.setdefault('REDIS_HOST', '127.0.0.1')
        config.setdefault('REDIS_PORT', '6379')
        config.setdefault('REDIS_DATABASE', '0')
        config.setdefault('REDIS_TOKEN', None)
        config.setdefault('REDIS_CLUSTER', '1')
        config.setdefault('JWT_SECRET', 'foosecret')
        config.setdefault('SESSION_DURATION', '7200')
        config.setdefault('REDIS_FAKE', False)

    @classmethod
    def get_session(cls, app: object = None) -> 'SessionStore':
        """Get a new session with the search index."""
        config = get_application_config(app)
        host = config.get('REDIS_HOST', 'localhost')
        port = int(config.get('REDIS_PORT', '6379'))
        db = int(config.get('REDIS_DATABASE', '0'))
        # token = config.get('REDIS_TOKEN', None)
        cluster = config.get('REDIS_CLUSTER', '1') == '1'
        secret = config.get('JWT_SECRET', 'foosecret')
        duration = int(config.get('SESSION_DURATION', '7200'))
        fake = config.get('REDIS_FAKE', False)
        return cls(host, port, db, secret, duration, # token=token,
                   cluster=cluster, fake=fake)

    @classmethod
    def current_session(cls) -> 'SessionStore':
        """Get/create :class:`.SearchSession` for this context."""
        g = get_application_global()
        if not g:
            return cls.get_session()
        if 'redis' not in g:
            g.redis = cls.get_session()
        return g.redis      # type: ignore


    