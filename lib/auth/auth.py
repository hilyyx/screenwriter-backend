import os
from datetime import datetime, timedelta
from lib.auth.utils import hash_password, verify_password, create_access_token
from lib.models.schemas import UserResponse
from db.database import Database
from db.users_db import Users
from fastapi import HTTPException

class Auth:
    def __init__(self):
        self.db1 = Database()
        self.db = Users(self.db1)

    def register(self, mail, name, surname, password):
        user = self.db.get_user_by_mail(mail)
        if user:
            if user.get('is_deleted'):
                # Восстановление пользователя
                password_hash = hash_password(password)
                user_id = self.db.reactivate_user(mail, name, surname, password_hash)
                return user_id, None
            raise HTTPException(400, detail="User already exists")
        password_hash = hash_password(password)
        user_id = self.db.create_user(mail, name, surname, password_hash)
        if not user_id:
            raise HTTPException(500, detail="Failed to create user")
        return user_id, None

    def login(self, mail, password):
        user = self.db.get_user_by_mail(mail)
        if not user or user.get('is_deleted'):
            raise HTTPException(401, detail="User not found")
        if not verify_password(password, user['password_hash']):
            raise HTTPException(401, detail="Wrong password")
        user_response = UserResponse(
            id=user["id"],
            mail=user["mail"],
            name=user["name"],
            surname=user["surname"]
        )
        access_token = create_access_token(user_response)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_response
        }
