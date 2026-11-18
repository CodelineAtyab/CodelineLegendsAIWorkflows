import hashlib
import hmac
import os

SALT_SIZE = 16


def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


def make_password_record(password: str) -> tuple[str, str]:
    salt = os.urandom(SALT_SIZE)
    return salt.hex(), hash_password(password, salt).hex()


def is_password_correct(password: str, salt_hex: str, hash_hex: str) -> bool:
    new_hash = hash_password(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(new_hash.hex(), hash_hex)
