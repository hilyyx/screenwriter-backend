from fastapi import APIRouter, HTTPException, Depends, Header
from lib.auth.auth import Auth
from lib.models.schemas import UserRegisterRequest, UserLoginRequest, UserResponse
from typing import Optional
from lib.auth.utils import decode_token, create_access_token

router = APIRouter()

auth_service = Auth()

@router.post("/register", tags=["Auth"])
def register(user: UserRegisterRequest):
    user_id, error = auth_service.register(user.mail, user.name, user.surname, user.password)
    if error == "User already exists":
        raise HTTPException(status_code=400, detail=error)
    if error == "Failed to create user":
        raise HTTPException(status_code=500, detail=error)
    if error:
        raise HTTPException(status_code=422, detail=error)
    return UserResponse(id=user_id, mail=user.mail, name=user.name, surname=user.surname)

@router.post("/login", tags=["Auth"])
def login(user: UserLoginRequest):
    return auth_service.login(user.mail, user.password)

@router.post("/refresh", tags=["Auth"])
def refresh(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        mail = payload.get("mail")
    except Exception:
        raise HTTPException(401, detail="Invalid refresh token")
    new_access_token = create_access_token({"mail": mail})
    return {"access_token": new_access_token}

@router.get("/protected", tags=["Auth"])
def protected(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, detail="Missing token")
    token = authorization.split(" ")[1]
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(401, detail="Invalid token")
    return {"message": f"Hello, {payload.get('mail')}"}

