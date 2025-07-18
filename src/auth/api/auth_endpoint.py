from fastapi import APIRouter, HTTPException
from lib.auth.auth import Auth
from lib.models.schemas import UserRegisterRequest, UserLoginRequest, UserResponse

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
    user_data, error = auth_service.login(user.mail, user.password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return UserResponse(id=user_data['id'], mail=user_data['mail'], name=user_data['name'], surname=user_data['surname'])

