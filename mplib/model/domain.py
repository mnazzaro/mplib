from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GeographicData (BaseModel):
    """Geography/address data"""
    country: str
    city: str
    street_address: str
    province: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    territory: Optional[str]

class UserProfile (BaseModel):
    """Public user profile data"""
    username: str
    country: str
    homepage_url: str
    remember_me: bool = True

class Scope (str):
    """Represents an authorization policy"""

    def __new__ (cls, domain, action=None, resource=None):
        """Handle __new__"""
        return str.__new__(cls, cls.from_parts(domain, action, resource))
    
    @property
    def domain (self) -> str:
        return self.parts[0]
    
    @property
    def action (self) -> Optional[str]:
        return self.parts[1]
    
    @property
    def resource (self) -> Optional[str]:
        return self.parts[2]
    
    @property
    def parts (self) -> List[str]:
        parts = self.split(':')
        return parts + ([None] * (3 - len(parts)))
    
    def for_resource (self, resource: str) -> 'Scope':
        return Scope(self.domain, self.action, resource)
    
    def as_global (self) -> 'Scope':
        return self.for_resource('*')
    
    @classmethod
    def from_parts (cls, domain, action=None, resource=None) -> 'Scope':
        return ':'.join([p for p in [domain, action, resource] if p is not None])
    
    @classmethod
    def to_parts (cls, scope_str: str) -> List[str]:
        parts = scope_str.split(':')
        return parts + ([None] * (3 - len(parts)))
    
    @classmethod
    def from_str(cls, scope_str: str) -> 'Scope':
        parts = cls.to_parts(scope_str)
        return cls(parts[0], parts[1], parts[2])

class Authorizations (BaseModel):
    """Authorization data associated with a session"""
    cap_code: int = 0 # Session capability code
    scopes: List[Scope] = [] # TODO: This might need to be List[str] and coerced... Doesn't matter yet

class User (BaseModel):
    username: str
    email: str
    user_id: Optional[int] = None # This is the player_id from player table. User does not exist if this is None
    # profile: Optional[UserProfile] = None
    verified: bool = False # is the user's email verified

class Client (BaseModel):
    owner_id: int # player_id from player table
    client_id: Optional[int] = None # unique id of this client
    uri: Optional[str] = None # resource identifier of this client

class Session (BaseModel):
    session_id: int 
    start_time: datetime # ISO UTC format
    end_time: datetime # ISO UTC format
    user: Optional[User] = None
    client: Optional[Client] = None
    authorizations: Optional[Authorizations] = None
    ip_address: Optional[str] = None # IP address of client
    remote_host: Optional[str] = None # hostname of client
    nonce: Optional[str] = None # pseudo-random nonce generated when session created

    def is_authorized (self, scope: Scope, resource: str) -> bool:
        return (self.authorizations is not None and (
                scope.as_global() in self.authorizations or
                scope.for_resource(resource) in self.authorizations.scopes))
    
    @property
    def expired (self) -> bool:
        return bool(self.end_time is not None and 
                    datetime.now(tz=datetime.UTC) >= self.end_time)
    
    @property
    def seconds_until_expires (self) -> Optional[int]:
        if self.end_time is None:
            return None
        seconds = int(self.end_time - datetime.now(tz=datetime.UTC))
        return max(0, seconds)
    
    def json_safe_dict (self) -> dict:
        out = self.dict()
        if self.start_time is not None:
            out['start_time'] = self.start_time.isoformat()
        if self.end_time is not None:
            out['end_time'] = self.end_time.isoformat()
        return out
    
def session_from_dict (data: dict) -> Session:
    return Session.parse_obj(data)

            







    
