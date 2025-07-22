from fastapi import APIRouter
from lib.models.schemas import Params
from lib.llm.generator import Orchestrator
from fastapi import HTTPException

router = APIRouter()

class DialogueController:
    def __init__(self):
        self.generator_class = Orchestrator

    def generate(self, params: Params):
        generator = self.generator_class(params.dict())
        return generator.create_dialog()

dialogue_controller = DialogueController()

@router.post("/generate", tags=["Dialogue"])
def generate(params: Params):
    try:
        a = dialogue_controller.generate(params)
        print(a)
        return a
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dialogue generation error: {str(e)}")
