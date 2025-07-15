import bcrypt
from db.database import Database
from lib.auth.validator import validate_email, validate_password

class Auth:
    def __init__(self):
        self.db = Database()

    def register(self, mail, name, surname, password):
        try:
            mail = validate_email(mail)
            password = validate_password(password)
        except ValueError:
            return None, ValueError
        user = self.db.get_user_by_name(name)
        if user:
            return None, 'User created earlier'
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_id = self.db.create_user(mail, name, surname, password_hash)
        if user_id:
            return user_id, None

    def login(self, mail, password):
        try:
            mail = validate_email(mail)
            password = validate_password(password)
        except ValueError:
            return None, ValueError
        user = self.db.get_user_by_mail(mail)
        if not user:
            return None, 'User not found'
        password_hash = user['password_hash']
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return user, None
        else:
            return user, "wrong password"