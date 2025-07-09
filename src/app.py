from fastapi import FastAPI
from api.dialogue import router as dialogue_router
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

app = FastAPI(title="Screenwriter Dialogue API")
app.include_router(dialogue_router, prefix="/api")

