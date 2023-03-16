from typing import Optional

from flask_login import UserMixin
from ..model.model import db, DBPlayer
from ..model.util import current_session

class AuthUser (UserMixin):

    def __init__ (self, email: Optional[str], password: Optional[str], token: Optional[str]):
        self.email = email
        self.password = password
        self.token = token


    def get (self) -> Optional[DBPlayer]:
        # TODO: Add support for tokens?
        if self.email: # add checks for valid email and email
            return current_session().query(DBPlayer.email == self.email).first()
        return None