from fastapi import APIRouter
from lib.models.schemas import Params, DialogueResponse
from lib.llm.generator import DialogGenerator

router = APIRouter()

@router.post("/generate")
def generate(params: Params):
    generator = DialogGenerator(params.dict())
    generator.generate_structure()
    return generator.generate_dialogue()

