from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Import User model and get_db, adjust paths as necessary if they are different
# from . import models, schemas # Assuming models and schemas are in the same directory
# from .database import SessionLocal # Assuming get_db is defined in database.py

from .database import SessionLocal # Assuming get_db is defined here or accessible
from . import models, schemas, services # For User model and get_user_by_username service

# Dependency to get DB session (copied from main.py or defined centrally)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "b7711f4ee6c751d6cb0713156d7304473e21b46d70608c21763d111cc2513f01"  # Replace with your actual secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token") # Relative to application root

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token Creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT Token Verification and User Retrieval
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = services.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Optional: If you need to distinguish between an active and inactive user
# async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
#     if not current_user.is_active:  # Assuming your User model has an is_active field
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
