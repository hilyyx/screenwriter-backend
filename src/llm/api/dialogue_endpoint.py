from fastapi import APIRouter
from lib.models.schemas import Params, Graph
from lib.llm.generator import DialogGenerator
from fastapi import HTTPException

router = APIRouter()

class DialogueController:
    def __init__(self):
        self.generator_class = DialogGenerator

    def generate(self, params: Params):
        generator = self.generator_class(params.dict())
        generator.generate_structure()
        return generator.generate_dialogue()

dialogue_controller = DialogueController()

@router.post("/generate", tags=["Dialogue"])
def generate(params: Params):
    try:
        a = dialogue_controller.generate(params)
        return a
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dialogue generation error: {str(e)}")
