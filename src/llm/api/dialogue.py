from fastapi import APIRouter
from lib.models.schemas import Params, DialogueResponse
from lib.llm.generator import generate_dialogue_from_params

router = APIRouter()

@router.post("/generate")
def generate(params: Params):
    result = generate_dialogue_from_params(params.dict())
    return result
