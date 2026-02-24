from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.config import settings


def hash_password(plain: str) -> str:
    """Return a bcrypt hash of the plaintext password."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if the plaintext matches the stored hash."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(subject: str | int, expires_delta: timedelta | None = None) -> str:
    """
    Create a signed JWT.
    `subject` is typically the user's id (stored in the 'sub' claim).
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> str:
    """
    Decode and verify a JWT. Returns the 'sub' claim (user id string).
    Raises JWTError if the token is invalid or expired.
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    sub: str | None = payload.get("sub")
    if sub is None:
        raise JWTError("Token missing 'sub' claim")
    return sub
