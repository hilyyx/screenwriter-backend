import bcrypt
from db.database import Database
from lib.auth.validator import validate_password
from db.users_db import Users

class Auth:
    def __init__(self):
        self.db1 = Database()
        self.db = Users(self.db1)

    def register(self, mail, name, surname, password, is_deleted, data):
        try:
            password = validate_password(password)
        except ValueError as e:
            return None, str(e)

        user = self.db.db.get_user_by_mail(mail, include_deleted=True) if hasattr(self.db.db, 'get_user_by_mail') else self.db.get_user_by_mail(mail)
        if user:
            if user.get('is_deleted'):
                # Реактивация пользователя
                user_id = self.db.reactivate_user(mail, name, surname, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), data)
                return user_id, None
            return None, "User already exists"

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_id = self.db.create_user(mail, name, surname, password_hash, is_deleted, data)
        if user_id:
            return user_id, None
        return None, "Failed to create user"

    def login(self, mail, password):
        try:
            password = validate_password(password)
        except ValueError as e:
            return None, str(e)

        user = self.db.get_user_by_mail(mail)
        if not user:
            return None, "User not found"
        if user.get('is_deleted'):
            return None, "User not found"

        password_hash = user['password_hash']
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return user, None
        else:
            return None, "Wrong password"
