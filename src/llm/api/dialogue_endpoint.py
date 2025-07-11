from fastapi import APIRouter
from lib.models.schemas import Params, DialogueResponse
from lib.llm.generator import DialogGenerator

router = APIRouter()

class DialogueController:
    def __init__(self):
        self.generator_class = DialogGenerator

    def generate(self, params: Params):
        generator = self.generator_class(params.dict())
        generator.generate_structure()
        return generator.generate_dialogue()

dialogue_controller = DialogueController()

@router.post("/generate")
def generate(params: Params):
    return dialogue_controller.generate(params)

