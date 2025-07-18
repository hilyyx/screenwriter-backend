from fastapi import APIRouter
from lib.models.schemas import Params, DialogueResponse
from lib.llm.generator import Orchestrator

router = APIRouter()

class DialogueController:
    def __init__(self):
        self.generator_class = Orchestrator

    def generate(self, params: Params):
        generator = self.generator_class(params.dict())
        return generator.create_dialog()

dialogue_controller = DialogueController()

@router.post("/generate")
def generate(params: Params):
    a = dialogue_controller.generate(params)
    print(a)
    return a
