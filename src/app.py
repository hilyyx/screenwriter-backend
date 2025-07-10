from fastapi import FastAPI
from src.llm.api.dialogue import router as dialogue_router


app = FastAPI(title="Screenwriter Dialogue API")
app.include_router(dialogue_router, prefix="/api")

