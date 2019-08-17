from typing import cast
import base64
import hashlib
import bcrypt

bcrypt_work_factor: int = 12


def preprocess_password(password: str) -> bytes:
    return base64.b64encode(
        hashlib.sha256(password.encode()).digest(),
    )


def hash_password(password: str) -> str:
    # we first base64 a sha256 hash of the password
    # in order to allow passwords of length > 72
    pre_processed_password = preprocess_password(password=password)
    hashed_password_bytes: bytes = bcrypt.hashpw(
        pre_processed_password,
        bcrypt.gensalt(bcrypt_work_factor),
    )
    return hashed_password_bytes.decode()


def compare_passwords(original: str, hashed_pwd: str) -> bool:
    return cast(bool, bcrypt.checkpw(
        preprocess_password(password=original),
        hashed_pwd.encode()
    ))
