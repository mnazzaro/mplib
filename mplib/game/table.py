from typing import List

from ..model.models import DBPlayer, DBPlayerGame
from ..model.util import current_session


def get_players (game_id: int) -> List[DBPlayer]:
    return current_session().query(DBPlayerGame) \
            .filter_by(game_id=game_id)