from fastapi import APIRouter
from lib.models.schemas import Params, ParamsRegen
from lib.llm.generator import Orchestrator

router = APIRouter()

class DialogueController:
    def __init__(self):
        self.generator_class = Orchestrator

    def generate(self, params: Params):
        generator = self.generator_class(params.dict())
        return generator.create_dialog()
    
    def regenerate(self, params: Params, dialog_structure, node_id, prompt):
        generator = self.generator_class(params.dict())
        return generator.regenerate_dialog(dialog_structure, node_id, prompt)

dialogue_controller = DialogueController()

@router.post("/generate")
def generate(params: Params):
    a = dialogue_controller.generate(params)
    print(a)
    return a

@router.post("/regenerate")
def regenerate(params: ParamsRegen):
    a = dialogue_controller.regenerate(params)
    print(a)
    return a
