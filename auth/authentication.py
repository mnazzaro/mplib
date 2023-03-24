from flask_login import login_user

from .auth_user import AuthUser

from os import urandom
from hashlib import sha256

def _authenticate_user (user: AuthUser) -> bool:
    if not (user.email and user.password):
        raise Exception("Authentication failed: missing email and/or password")
    
    db_user = user.get()
    if db_user is None:
        raise Exception(f"Authentication failed: no player associated with email {user.email}")
    print (f"{db_user.pass_hash}\t{_get_pass_hash(user.password, db_user.salt)}")
    return db_user.pass_hash == _get_pass_hash(user.password, db_user.salt)

def _generate_salt () -> bytes:
    return urandom(3)

# TODO: Swith to hashlib.pbkdf2_hmac
def _get_pass_hash (password: str, salt: bytes) -> bytes:
    pass_bytes = bytes(password, encoding='utf-8')
    hash = sha256()
    hash.update(pass_bytes)
    hash.update(salt)
    return hash.digest()

def try_login (user: AuthUser) -> bool:
    try:
        if _authenticate_user (user):
            login_user(user)
            return True
    except Exception as e:
        print (e)
        return False