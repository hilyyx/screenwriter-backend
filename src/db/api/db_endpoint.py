from fastapi import APIRouter, HTTPException

from db.database import Database
from db.users_db import Users
from lib.models.schemas import *

router = APIRouter()
db = Database()
user_service = Users(db)


@router.get("/users/{user_id}", tags=["Users"])
def get_user_by_id(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/get/users/{user_id}/data", tags=["Users"])
def get_user_data(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    data = user_service.get_user_data(user_id)
    if data:
        return {"data": data}
    raise HTTPException(status_code=404, detail="User data not found")

@router.post("/users/{user_id}/data", tags=["Users"])
def update_user_data(new_data: UserUpdateData):
    user = user_service.get_user_by_id(new_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    success = user_service.update_user_data(new_data.user_id, new_data.data)
    if success:
        return {"message": "User data updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update data")


@router.put("/users/{user_id}/name", tags=["Users"])
def update_user_name(user_id: int, new_name: UserUpdateName):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    success = user_service.update_user_name(user_id, new_name.name, new_name.surname)
    if success:
        return {"message": "User name updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update name")


@router.put("/users/{user_id}/password", tags=["Users"])
def update_user_password(user_id: int, new_pass: UserUpdatePassword):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    success = user_service.update_user_password(user_id, new_pass.password_hash)
    if success:
        return {"message": "Password updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update password")


@router.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    success = user_service.delete_user(user_id)
    if success:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=400, detail="Failed to delete user")
