# 🧠 Screenwriter Backend

Проект backend-сервиса для генерации интерактивных диалогов между главным героем и NPC с использованием LLM (Large Language Model). Предназначен для сценаристов и разработчиков игр.

---

## 🚀 Возможности

- 📥 Прием параметров о мире, персонаже и NPC через API.
- 🤖 Генерация структуры диалога в формате ориентированного графа.
- 🧩 Работа с LLM через API DeepSeek (используя JSON-промпты).
- 🛡️ Базовая система авторизации (регистрация / вход).
- 💾 Работа с PostgreSQL с логированием всех действий.
- 📁 Четко организованная модульная архитектура проекта.

---

## 📦 Структура проекта

```bash
screenwriter-backend/
├── .env                      # переменные окружения
├── .gitignore
├── pyproject.toml            # зависимости (poetry)
├── poetry.lock
├── README.md                 # этот файл

├── db/
│   ├── __init__.py
│   └── database.py           # модуль работы с PostgreSQL и логированием

├── lib/
│   ├── __init__.py
│   ├── settings.py           # глобальные настройки
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth.py           # логика авторизации
│   ├── llm/
│   │   ├── __init__.py
│   │   └── generator.py      # генерация промптов и работа с LLM
│   └── models/
│       ├── __init__.py
│       └── schemas.py        # схемы Pydantic

├── src/
│   ├── __init__.py
│   ├── app.py                # инициализация FastAPI и маршрутов
│   ├── main.py               # точка входа
│   ├── auth/
│   │   ├── __init__.py
│   │   └── api/
│   │       ├── __init__.py
│   │       └── auth_endpoint # ручки /register и /login
│   └── llm/
│       ├── __init__.py
│       └── api/
│           ├── __init__.py
│           └── dialogue_endpoint # ручка /generate

├── resources/
│   ├── prompt_edges_content.txt
│   ├── prompt_nodes_content.txt
│   └── prompt_structure.txt  # шаблоны промптов

├── progress/
│   ├── 09_july.md
│   ├── 10_july.md
│   └── ...                   # журнал прогресса по дням

└── db.log                    # лог запросов к базе данных
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
OPENAI_API_KEY=your-key-here
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

4. Запусти сервер разработки:

```bash
poetry run uvicorn src.app:app --reload
```

---

## 📡 Эндпоинты

| Метод | URL              | Описание            |
|-------|------------------|---------------------|
| POST  | `/api/generate`  | Генерация диалога   |
| POST  | `/api/login`     | Вход                |
| POST  | `/api/register`  | Регистрация         |

---

## 💾 Работа с базой данных

Модуль `db/database.py` реализует полноценную работу с PostgreSQL:

- Поддерживаются CRUD-операции для:
  - Пользователей (`users`)
  - Игр (`games`)
  - Сцен (`scenes`)
  - Диалогов (`dialogues`)
  - Персонажей (`characters`)
- Все SQL-запросы логируются в файл `db.log` с временными метками.
- Используется `RealDictCursor` для удобной сериализации результатов.

Пример записи в лог:

```
2025-07-09 14:00:01 [INFO] Подключение к базе данных успешно
2025-07-09 14:00:03 [INFO] Создан пользователь: user@example.com
```

---

## 🗓️ Прогресс разработки

Смотри [progress/09_july.md](progress/09_july.md) и другие файлы в директории `progress/`.
