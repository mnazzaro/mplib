from typing import Optional

import secrets
import uuid

from datetime import datetime, timedelta
from pytz import UTC

from ...model.domain import Authorizations, User, \
    Client, Session

def _generate_nonce (length: int = 32):
    return secrets.token_urlsafe(length)

def create_session (self, authorizations: Authorizations, 
        ip_address: str, remote_host: str, 
        user: Optional[User] = None, 
        client: Optional[Client] = None,
        session_id: Optional[str] = None) -> Session:
    if session_id is None:
        session_id = uuid.uuid4().int # TODO: This may be a security vulnerability and/or have overlap
    start_time = datetime.now(tz=UTC)
    end_time = start_time + timedelta(seconds=self._duration)
    return Session(
        session_id=session_id,
        user=user,
        client=client,
        start_time=start_time,
        end_time=end_time,
        authorizations=authorizations,
        ip_address=ip_address,
        remote_host=remote_host,
        nonce=_generate_nonce()
    )