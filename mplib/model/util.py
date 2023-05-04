from typing import Generator

from flask import Flask
from contextlib import contextmanager

from .models import db

def init_app(app: Flask):
    if is_configured(app):
        print ('db is cofigured')
        db.init_app(app)
        return
    raise

def current_session():
    return db.session

def create_all():
    """Create all tables in the database"""
    db.create_all()

def drop_all():
    """Drop all the tables in the database"""
    db.drop_all()

@contextmanager
def transaction () -> Generator:
    try:
        yield db.session

        if db.session.new or db.session.dirty or db.session.deleted:
            db.session.commit()
    except Exception as e:
        # logger.warning('Commit failed, rolling back: %s', str(e))
        db.session.rollback()
        raise

def is_configured (app: Flask) -> bool:
    if 'SERVICE_TYPE_FOR_AUTH' in app.config and \
        'SQLALCHEMY_DATABASE_URI' in app.config:
        return True
    return False
