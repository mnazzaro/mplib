from auth_user import AuthUser
from hashlib import sha256

def _authenticate_user (user: AuthUser) -> None:
    if not (user.email and user.password):
        raise Exception("Authentication failed: missing email and/or password")
    db_user = user.get()
    if db_user is None:
        raise Exception(f"Authentication failed: no player associated with email {user.email}")
    return db_user.pass_hash == _make_pass_hash(user.password, db_user.salt)

def _make_pass_hash (password: str, salt: bytes) -> bytes:
    pass_bytes = bytes(password, encoding='utf-8')
    hash = sha256()
    hash.update(pass_bytes)
    hash.update(salt)
    return hash.digest()
