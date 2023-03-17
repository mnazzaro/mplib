from sqlalchemy.sql import exists, _and

from ..model.util import current_session
from ..model.model import DBPlayerGame

def authorize_player_for_table (player_id: int, game_id: int) -> bool:
    return current_session().query(
        exists()
        .where(
            (DBPlayerGame.player_id == player_id) & \
            (DBPlayerGame.game_id == game_id)
            )
        ) \
        .scalar()