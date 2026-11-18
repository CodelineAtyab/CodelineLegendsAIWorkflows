import hashlib
import hmac
import os

SALT_BYTES = 16
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def _derive(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P
    )


def hash_password(password: str) -> str:
    """Return "<salt hex>$<hash hex>" using a fresh random salt."""
    salt = os.urandom(SALT_BYTES)
    return f"{salt.hex()}${_derive(password, salt).hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Check a password against a stored "<salt hex>$<hash hex>" value."""
    salt_hex, hash_hex = stored.split("$")
    candidate = _derive(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(candidate, bytes.fromhex(hash_hex))
