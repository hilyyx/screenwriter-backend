from fastapi import APIRouter
from src.models.schemas import Params, DialogueResponse
from lib.llm.generator import generate_dialogue_from_params

router = APIRouter()

@router.post("/generate", response_model=list[DialogueResponse])
def generate(params: Params):
    result = generate_dialogue_from_params(params.dict())
    return result
