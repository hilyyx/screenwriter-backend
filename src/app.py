from fastapi import FastAPI
from src.llm.api.dialogue_endpoint import router as dialogue_router
from src.auth.api.auth_endpoint import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.db.api.db_endpoint import router as db_router

app = FastAPI(title="Screenwriter Dialogue API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://26.15.136.181:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(dialogue_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(db_router, prefix="/api")