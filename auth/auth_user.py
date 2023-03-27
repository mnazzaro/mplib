from typing import Optional

from flask_login import UserMixin

from ..model.model import db, DBPlayer
from ..model.util import current_session

class AuthUser (UserMixin):

    def __init__ (self, email: Optional[str], password: Optional[str], token: Optional[str]):
        self.email = email
        self.password = password
        self.token = token
        self.db_player = None


    def get (self) -> Optional[DBPlayer]:
        # TODO: Add support for tokens?
        if self.email: # add checks for valid email and email
            self.db_player = current_session().query(DBPlayer).filter_by(email=self.email).first()
            return self.db_player
        return None
    
    def get_id (self) -> int:
        if self.db_player:
            return self.db_player.player_id
        else:
            return self.get().player_id