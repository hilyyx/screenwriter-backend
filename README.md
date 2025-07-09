# 🧠 Screenwriter Backend

Проект backend-сервиса для генерации интерактивных диалогов между главным героем и NPC с использованием LLM (Large Language Model). Предназначен для сценаристов и разработчиков игр.

---

## 🚀 Возможности

- 📥 Прием параметров о мире, персонаже и NPC через API.
- 🤖 Генерация структуры диалога в формате ориентированного графа.
- 🧩 Работа с LLM через API DeepSeek (используя JSON-промпты).
- 🛡️ Базовая система авторизации (регистрация / вход).
- 📁 Четко организованная архитектура проекта.

---

## 📦 Структура проекта
```
screenwriter-backend/
├── .env # переменные окружения
├── .gitignore
├── pyproject.toml # зависимости (poetry)
├── resources/
│ └── prompt.txt # шаблон для генерации промптов
├── src/
│ ├── app.py # запуск FastAPI и подключение роутеров
│ └── api/
│ ├── dialogue.py # ручка /generate
│ └── auth.py # ручки /login, /register
├── lib/
│ ├── loaders.py # утилиты для загрузки ресурсов
│ ├── llm/
│ │ ├── client.py # обертка над DeepSeek
│ │ ├── prompt_builder.py # генерация промпта
│ │ └── parser.py # обработка ответа
│ ├── services/
│ │ ├── generator.py # основная логика генерации
│ │ └── auth.py # базовый класс Auth
│ └── models/
│ └── user.py # модели пользователя (по мере необходимости)
└── progress/
└── PROGRESS.md # журнал прогресса по дням
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
    ```

4. Запусти сервер разработки:

    ```bash
    poetry run uvicorn src.app:app --reload
    ```

---

## 📡 Эндпоинты

| Метод | URL             | Описание                    |
|-------|------------------|-----------------------------|
| POST  | `/api/generate`  | Генерация диалога           |
| POST  | `/api/login`     | Вход                        |
| POST  | `/api/register`  | Регистрация                 |

---

## 🗓️ Прогресс разработки

Смотри [progress/PROGRESS.md](progress/09_july.md)
