from .model import db

def current_session():
    return db.session