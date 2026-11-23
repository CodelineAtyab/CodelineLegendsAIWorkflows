import hashlib
import hmac
import secrets

SCRYPT_COST = 2**14
SCRYPT_BLOCK_SIZE = 8
SCRYPT_PARALLELISM = 1
SALT_BYTES = 16


def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = secrets.token_bytes(SALT_BYTES)
    return salt, _scrypt(password, salt)


def verify_password(password: str, salt: bytes, expected_hash: bytes) -> bool:
    return hmac.compare_digest(_scrypt(password, salt), expected_hash)


def _scrypt(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_COST,
        r=SCRYPT_BLOCK_SIZE,
        p=SCRYPT_PARALLELISM,
    )
