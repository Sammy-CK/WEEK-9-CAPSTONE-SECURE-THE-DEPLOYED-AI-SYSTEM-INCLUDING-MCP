"""Week 6 JWT auth — boot fails closed without JWT_SECRET (Week 9)."""
import os
import time

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

def get_secret() -> str:
    key = os.getenv("JWT_SECRET", "").strip()
    if not key:
        raise RuntimeError("missing JWT_SECRET — set in environment before starting the API")
    return key

TOKEN_LIFETIME_SECONDS = 30 * 60

USERS = {
    "mercy": {
        "password_hash": bcrypt.hashpw(b"logistics2026", bcrypt.gensalt()),
        "role": "coordinator",
        "mcp_role": "clinical_ops",
    },
    "nurse": {
        "password_hash": bcrypt.hashpw(b"nurse2026", bcrypt.gensalt()),
        "role": "nurse",
        "mcp_role": "partner_clinic",
    },
}


def check_password(username: str, password: str) -> bool:
    user = USERS.get(username)
    if user is None:
        return False
    return bcrypt.checkpw(password.encode(), user["password_hash"])


def create_token(username: str) -> str:
    user = USERS[username]
    payload = {
        "sub": username,
        "role": user["role"],
        "mcp_role": user["mcp_role"],
        "exp": int(time.time()) + TOKEN_LIFETIME_SECONDS,
    }
    return jwt.encode(payload, get_secret(), algorithm="HS256")


bearer = HTTPBearer()


def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials, get_secret(), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return payload
