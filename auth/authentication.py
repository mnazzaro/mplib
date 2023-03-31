from flask import current_app, st
from flask_login import login_user
from werkzeug.datastructures import MultiDict

from typing import Tuple

from wtforms import StringField, PasswordField, Form
from wtforms.validators import DataRequired

from .auth_user import AuthUser

from os import urandom
from hashlib import sha256

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

def _authenticate_user (user: AuthUser) -> bool:
    if not (user.email and user.password):
        raise Exception("Authentication failed: missing email and/or password")
    
    db_user = user.get()
    if db_user:
        return db_user.pass_hash == _get_pass_hash(user.password, db_user.salt)
    return False

def try_login (user: AuthUser) -> bool:
    if _authenticate_user (user):
        with current_app.app_context():
            login_user(user)
            return True
    return False
    # try:
    #     if _authenticate_user (user):
    #         login_user(user)
    #         return True
    # except Exception as e:
    #     print (e)
    #     return False


# TODO: will have to start checking geo compliance
def login (form_data: MultiDict, ip: str) -> ResponseData:
    """
    Log the user in with their email and password.
    Create a new session for them
    """
    form = LoginForm(form_data)
    if not form.validate():
        # TODO: Add logging
        return form_data, 400, {}
    