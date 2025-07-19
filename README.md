# 🧠 Screenwriter Backend

Проект backend-сервиса для генерации интерактивных диалогов между главным героем и NPC с использованием LLM (Large Language Model). Предназначен для сценаристов и разработчиков игр.

---

## 🚀 Возможности

- 📥 Прием параметров о мире, персонаже и NPC через API.
- 🤖 Генерация структуры диалога и сценария с помощью DeepSeek Reasoner (LLM).
- 🧩 Работа с LLM через API DeepSeek (используя JSON-промпты).
- 🛡️ JWT-авторизация: регистрация, вход, refresh токена, защита эндпоинтов.
- 💾 Работа с PostgreSQL с логированием всех действий.
- 🗑️ Поддержка soft-delete пользователей (is_deleted) и автоматическое восстановление аккаунта при повторной регистрации.
- 🌐 CORS-настройки для работы с конкретным фронтендом.
- 📁 Четко организованная модульная архитектура проекта.

---

## 📦 Структура проекта

```bash
screenwriter-backend/
├── .env                      # переменные окружения
├── certs/                    # приватный и публичный ключи для JWT (private.pem, public.pem)
├── pyproject.toml            # зависимости (poetry)
├── README.md                 # этот файл
│
├── db/
│   ├── __init__.py
│   ├── database.py           # модуль работы с PostgreSQL и логированием
│   ├── users_db.py           # работа с пользователями (is_deleted, восстановление)
│   └── db_CRUD/              # CRUD для игр, сцен, диалогов, персонажей
│
├── lib/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth.py           # логика авторизации и восстановления
│   │   ├── utils.py          # JWT, bcrypt, работа с ключами
│   │   └── validator.py      # валидация
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── generator.py      # генерация промптов и работа с LLM
│   │   └── settings.py       # настройки моделей
│   └── models/
│       ├── __init__.py
│       └── schemas.py        # схемы Pydantic
│
├── src/
│   ├── __init__.py
│   ├── app.py                # инициализация FastAPI, CORS, маршруты
│   ├── main.py               # точка входа
│   ├── auth/
│   │   ├── __init__.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── auth_endpoint.py # ручки /register, /login, /refresh, /protected
│   ├── db/
│   │   └── api/db_endpoint.py   # ручки для работы с пользователями и данными
│   └── llm/
│       ├── __init__.py
│       └── api/
│           ├── __init__.py
│           └── dialogue_endpoint.py # ручка /generate
│
├── resources/
│   ├── prompt_edges_content.txt
│   ├── prompt_nodes_content.txt
│   └── prompt_structure.txt
│
└── logs/
    └── db.log                # лог запросов к базе данных
```

---

## 🛠️ Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/hilyyx/screenwriter-backend.git
cd screenwriter-backend
```

2. Установи зависимости через Poetry:

```bash
poetry install
```

3. Создай файл `.env` в корне проекта и укажи свои переменные окружения:

```env
# DeepSeek API
DEEPSEEK_API_KEY=your-key-here
MODEL_TYPE_STRUCTURE_GENERATION=deepseek-reasoner
MODEL_TYPE_DIALOGUE_GENERATION=deepseek-chat
MODEL_TYPE_STRUCTURE_VALIDATION=deepseek-reasoner
MODEL_TYPE_DIALOGUE_VALIDATION=deepseek-chat
MODEL_TYPE_STRUCTURE_REGENERATION=deepseek-reasoner
MODEL_TYPE_DIALOGUE_REGENERATION=deepseek-chat
MODEL_MAX_TOKENS_STRUCTURE_GENERATION=20000
MODEL_MAX_TOKENS_DIALOGUE_GENERATION=8192
MODEL_MAX_TOKENS_STRUCTURE_VALIDATION=20000
MODEL_MAX_TOKENS_DIALOGUE_VALIDATION=8192
MODEL_MAX_TOKENS_STRUCTURE_REGENERATION=20000
MODEL_MAX_TOKENS_DIALOGUE_REGENERATION=8192

# Database
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# JWT
ALGORITHM=RS256
# Ключи хранятся в certs/private.pem и certs/public.pem

# Прочее
APP_ENV=development
LOG_LEVEL=INFO
```

4. Сгенерируй приватный и публичный ключи для JWT:

```bash
openssl genrsa -out certs/private.pem 2048
openssl rsa -in certs/private.pem -pubout -out certs/public.pem
```

5. Запусти сервер разработки:

```bash
poetry run uvicorn src.app:app --reload
```

---

## 📡 Эндпоинты

| Метод | URL                             | Описание                                 |
|-------|---------------------------------|------------------------------------------|
| POST  | `/api/generate`                 | Генерация диалога                        |
| POST  | `/api/login`                    | Вход, возвращает JWT и user.id           |
| POST  | `/api/register`                 | Регистрация или восстановление аккаунта   |
| POST  | `/api/refresh`                  | Обновление access_token                  |
| GET   | `/api/protected`                | Проверка токена                          |
| GET   | `/api/users/{user_id}`          | Получить пользователя (если не удалён)   |
| GET   | `/api/get/users/{user_id}/data` | Получить данные пользователя             |
| POST  | `/api/users/{user_id}/data`     | Обновить данные пользователя             |
| PUT   | `/api/users/{user_id}/name`     | Обновить имя и фамилию                   |
| PUT   | `/api/users/{user_id}/password` | Обновить пароль                      |
| DELETE| `/api/users/{user_id}`          | Удалить пользователя (soft-delete)       |

---

## 🛡️ JWT и авторизация

- Для всех защищённых эндпоинтов требуется JWT access_token.
- Ключи для подписи и проверки токенов хранятся в certs/private.pem и certs/public.pem.
- Токены создаются с помощью алгоритма RS256.
- После логина фронтенд получает user.id для дальнейших запросов.
- При регистрации, если пользователь был удалён (is_deleted=True), аккаунт автоматически восстанавливается.

---

## 🌐 CORS

В файле `src/app.py` разрешён доступ только с нужного фронтенда:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://10.82.249.105:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 💾 Работа с базой данных

- Все SQL-запросы логируются в logs/db.log с временными метками.
- Используется soft-delete пользователей через поле is_deleted.
- Реализовано восстановление пользователя при повторной регистрации.
- Используется RealDictCursor для сериализации результатов.

---

## 🧠 DeepSeek Reasoner

- Используется для генерации и валидации структуры сценария и диалогов.
- Работает с длинными контекстами (до 20 000 токенов).
- Позволяет строить сложные структуры и цепочки рассуждений.
- Все параметры моделей настраиваются через .env.

---
Спасибо за ваше внимание и проявленный интерес к нашей разработке