from pydantic import EmailStr, ValidationError

def validate_email(email: str):
    try:
        if type(email) == EmailStr:
            return str(email)
    except (ValidationError, ValueError):
        raise ValueError('Некорректный email адрес')

def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError('Пароль должен быть не короче 8 символов')
    return password
