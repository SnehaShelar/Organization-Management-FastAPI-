from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    This function creates a JWT token containing the provided 'data' (such as user info),
    with an optional expiration time ('expires_delta'). If no expiration is provided,
    a default value of 15 minutes is used.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})  # Add the expiration time to the data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the token
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    This function compares the given plain password with a stored hashed password
    to check if they match.
    """
    return pwd_context.verify(plain_password, hashed_password)


def decode_jwt_token(token: str) -> dict:
    """
    This function decodes the given JWT token using the secret key and verifies
    its authenticity. If the token is valid, it returns the payload (decoded data).
    If the token is invalid or expired, an HTTPException is raised.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
