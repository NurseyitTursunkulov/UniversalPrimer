from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from utils import get_password_hash, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "john": {
        "username": "john",
        "fullname": "john doe",
        "email": "john@mail.cir",
        "hashed_password": get_password_hash("secret"),
    }
}


def get_user(db, username: str):
    if username in db:
        return db[username]
    return None


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user
