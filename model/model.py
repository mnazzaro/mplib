from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric, Column, DateTime, LargeBinary, \
    ForeignKey, Index, Integer, SmallInteger, String, Text, text

db: SQLAlchemy = SQLAlchemy()

class DBPlayer (db.Model):

    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    join_date = Column(DateTime, nullable=False)
    pass_hash = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    account_balance = Column(Numeric(precision=8, scale=0), nullable=False)
    deposit_limit = Column(Numeric(precision=8, scale=0))
    wager_limit = Column(Numeric(precision=8, scale=0))
    time_limit = Column(Integer)

class DBGame (db.Model):

    __tablename__ = 'game'

    game_id = Column(Integer, primary_key=True)
    game_status = Column(Integer, nullable=False)
    format = Column(String(50), nullable=False)
    limit_type = Column(String(2), nullable=False)
    small_blind = Column(Numeric(precision=5, scale=0), nullable=False)
    big_blind = Column(Numeric(precision=5, scale=0), nullable=False)
    ante = Column(Numeric(precision=5, scale=0), nullable=False)

class DBPlayerGame (db.Model):
    __tablename__ = 'player_game'

    player_id = Column(ForeignKey('player.player_id'), primary_key=True)
    game_id = Column(ForeignKey('game.game_id'), primary_key=True)
    buy_in = Column(Numeric(precision=8, scale=0), nullable=False)