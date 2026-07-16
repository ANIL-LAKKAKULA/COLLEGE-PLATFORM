"""
  - hash_password() / verify_password() via passlib[bcrypt]
  - encode_jwt() / decode_jwt() via PyJWT, RS256, loading keys/ at startup
  - generate_default_password(date_of_birth) -> "Dob@DDMMYYYY" (ADR 0003)
"""

from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path

import jwt
from app.core.config import settings
from passlib.context import CryptContext

"""To hash password & verify inpu passowrd against hashed password"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Need to come up with a better solution
def generate_default_password(date_of_birth: date) -> str:
    """ADR 0003: default password for admin-provisioned accounts, e.g. Dob@15011999."""
    return f"Dob@{date_of_birth.strftime('%d%m%Y')}"


@lru_cache
def _load_private_key() -> str:
    return Path(settings.jwt_private_key_path).read_text()


@lru_cache
def _load_public_key() -> str:
    return Path(settings.jwt_public_key_path).read_text()


def encode_jwt(claims: dict, expires_minutes: int | None = None) -> str:
    expires_minutes = expires_minutes or settings.access_token_expire_minutes
    now = datetime.now(timezone.utc)
    payload = {
        **claims,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, _load_private_key(), algorithm=settings.jwt_algorithm)


def decode_jwt(token: str) -> dict:
    """Raises jwt.PyJWTError (expired, bad signature, malformed) — caller maps it to 401."""
    return jwt.decode(token, _load_public_key(), algorithms=[settings.jwt_algorithm])
