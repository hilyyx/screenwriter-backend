import os
from datetime import datetime, timedelta

import bcrypt
import jwt
from dotenv import load_dotenv
from jose import JWTError
from jose import jwt as jose_jwt

load_dotenv()

ACCESS_EXPIRE_MINUTES = 60

# Загрузка приватного и публичного ключей из файлов
with open(os.path.join(os.path.dirname(__file__), '../../certs/private.pem'), 'r') as f:
    PRIVATE_KEY = f.read()
with open(os.path.join(os.path.dirname(__file__), '../../certs/public.pem'), 'r') as f:
    PUBLIC_KEY = f.read()

ALGORITHM = os.getenv("ALGORITHM")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(user) -> str:
    to_encode = user.dict() if hasattr(user, 'dict') else dict(user)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jose_jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

def encode_jwt(payload: dict,
               private_key: str = PRIVATE_KEY,
               algorithm: str = ALGORITHM):
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded

def decode_token(token: str):
    try:
        payload = jose_jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e