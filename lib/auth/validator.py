def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError('Пароль должен быть не короче 8 символов')
    return password
