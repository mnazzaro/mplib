from flask import current_app, request
from flask_login import login_user
from werkzeug.datastructures import MultiDict

from typing import Tuple

from wtforms import StringField, PasswordField, Form
from wtforms.validators import DataRequired

from .authenticate import _authenticate_password

from os import urandom
from hashlib import sha256

from .sessions.session_store import SessionStore
from ..model.models import DBPlayer
from ..model.domain import Session, User
from .exceptions import AuthenticationFailureError

ResponseData = Tuple[dict, int, dict]

class LoginForm(Form):
    """Log in form."""
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


# def _authenticate_user (user: AuthUser) -> bool:
#     if not (user.email and user.password):
#         raise Exception("Authentication failed: missing email and/or password")
    
#     db_user = user.get()
#     if db_user:
#         return db_user.pass_hash == _get_pass_hash(user.password, db_user.salt)
#     return False

# def _authenticate_user (user: AuthUser) -> bool:
#     if not (user.email and user.password):
#         raise Exception("Authentication failed: missing email and/or password")
    
#     db_user = user.get()
#     if db_user:
#         return db_user.pass_hash == _get_pass_hash(user.password, db_user.salt)
#     return False

# def try_login (user: AuthUser) -> bool:
#     if _authenticate_user (user):
#         with current_app.app_context():
#             login_user(user)
#             return True
#     return False
    # try:
    #     if _authenticate_user (user):
    #         login_user(user)
    #         return True
    # except Exception as e:
    #     print (e)
    #     return False

def _create_session (user: DBPlayer) -> Session:
    """Take db user data and create a session in redis"""
    try:
        session_store = SessionStore.current_session()
    except: 
        raise
    try:
        print (type(user.player_id))
        print (user.player_id)
        return session_store.create(
            '',
            request.remote_addr,
            request.host, # TODO: This might be wrong or unneccesary
            User(
                username=user.username,
                email=user.email,
                user_id=user.player_id,
                verified=True # TODO: Make a utility function for this, or a class method in domain
            ),
            None,
            None
        )
    except: 
        raise


# def login (form_data: MultiDict) -> Session:
#     """
#     - Log the user in with their email and password.
#     - Create a new session for them
#     - Return their session
#     """
#     form = LoginForm(form_data)
#     if not form.validate() and \
#         form.email and form.password:
#         # TODO: Add logging
#         # TODO: Make these separate checks?
#         return form_data, 400, {}
#     # TODO: will have to start checking geo compliance
#     try:
#         user: DBPlayer = _authenticate_password(form.email.data, form.password.data)
#     except:
#         raise
#     try:
#         session = _create_session(user)
#     except:
#         raise

#     return session

def login (data: dict) -> Session:
    """
    - Log the user in with their email and password.
    - Create a new session for them
    - Return their session
    """
    if not data or (not data.get('email')) \
        or (not data.get('password')):
        # TODO: Add logging
        # TODO: Make these separate checks?
        return data, 400, {}
    # TODO: will have to start checking geo compliance
    try:
        user: DBPlayer = _authenticate_password(data['email'], data['password'])
    except Exception as e:
        raise AuthenticationFailureError from e
    try:
        session = _create_session(user)
    except Exception as e:
        raise AuthenticationFailureError from e

    return session