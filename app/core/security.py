from passlib.context import CryptContext

from jose import jwt
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

security = HTTPBearer()

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain,hashed)

SECRET_KEY = "supersercret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=ALGORITHM)
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401,detail="Invaild token")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invaild token")
    
