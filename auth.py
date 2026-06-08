from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from schemas import UserInDB

SECRET_KEY = "10738ae3595dd041555af21258a083c0aba787db68feab423d38194b91817331" #need to hide this
ALGORITHM = "HS256" #need to hide this
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #need to hide this

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy")


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def get_user(db, username):
    if username in db:
        # print("db[username] : ",db[username])
        return UserInDB(**db[username])

def authenticate_user(fake_db, username, password):
    user = get_user(fake_db, username)
    print("user is : ",user)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )