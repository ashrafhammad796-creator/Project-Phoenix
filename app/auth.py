import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# JWT CONFIGURATION
# ==================================================

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-secret-key"
)

ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)

# ==================================================
# PASSWORD HASHING
# ==================================================

password_hash = PasswordHash.recommended()

# ==================================================
# OAUTH2
# ==================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token"
)

# ==================================================
# ADMIN ACCOUNT
# ==================================================

DEMO_USERNAME = os.getenv(
    "ADMIN_USERNAME",
    "hammad"
)

DEMO_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "phoenix123"
)

DEMO_PASSWORD_HASH = password_hash.hash(
    DEMO_PASSWORD
)

# ==================================================
# AUTHENTICATE USER
# ==================================================

def authenticate_user(
    username: str,
    password: str
):
    if username != DEMO_USERNAME:
        return False

    return password_hash.verify(
        password,
        DEMO_PASSWORD_HASH
    )

# ==================================================
# VERIFY PASSWORD
# ==================================================

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return password_hash.verify(
        plain_password,
        hashed_password
    )

# ==================================================
# HASH PASSWORD
# ==================================================

def hash_password(
    password: str
):
    return password_hash.hash(
        password
    )

# ==================================================
# CREATE JWT TOKEN
# ==================================================

def create_access_token(
    username: str
):
    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# ==================================================
# GET CURRENT USER
# ==================================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        if username != DEMO_USERNAME:
            raise credentials_exception

        return username

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    except jwt.InvalidTokenError:
        raise credentials_exception