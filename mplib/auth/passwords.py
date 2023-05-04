from os import urandom
from hashlib import sha256
from .exceptions import PasswordAuthenticationError

def _generate_salt () -> bytes:
    return urandom(3)

# TODO: Swith to hashlib.pbkdf2_hmac
def _get_pass_hash (password: str, salt: bytes) -> bytes:
    pass_bytes = bytes(password, encoding='utf-8')
    hash = sha256()
    hash.update(pass_bytes)
    hash.update(salt)
    return hash.digest()

def check_password (password: str, salt: bytes, correct_hash: bytes) -> bool:
    # TODO: Add logging and maybe raise on exception
    try:
        return correct_hash == _get_pass_hash(password, salt)
    except:
        raise PasswordAuthenticationError('Password does not match')

def is_ascii(string):
    """Returns true if the string is only ascii chars."""
    try:
        string.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False
