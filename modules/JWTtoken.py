from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from .schemas import TokenData

SECRET_KEY = "e70722186f0987d9f7d6ab48558874f28b0eb099c3d2a596291186cdeb711c2e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30




def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifyToken(credentials_exception, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception