from typing import List

from ..model.model import DBPlayer, DBPlayerGame
from ..model.util import current_session


def get_players (game_id: int) -> List[DBPlayer]:
    return current_session().query(DBPlayerGame) \
            .filter(DBPlayerGame.game_id == game_id)