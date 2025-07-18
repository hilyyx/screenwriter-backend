import re

def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError('Пароль должен быть не короче 8 символов')
    return password

def validate_email(email: str) -> str:
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise ValueError('Некорректный email')
    return email

def validate_name(name: str) -> str:
    if not name.isalpha():
        raise ValueError('Имя должно содержать только буквы')
    return name

def validate_surname(surname: str) -> str:
    if not surname.isalpha():
        raise ValueError('Фамилия должна содержать только буквы')
    return surname
