from fastapi import APIRouter, Depends, HTTPException, Header
from lib.models.schemas import Params
from lib.llm.generator import Orchestrator
from db.database import Database
from db.users_db import Users
from src.db.api.db_endpoint import get_current_user_id
import json

router = APIRouter()

db = Database()
user_service = Users(db)

class DialogueController:
    def __init__(self):
        self.generator_class = Orchestrator

    def generate(self, params: Params):
        generator = self.generator_class(params.dict())
        return generator.create_dialog()

dialogue_controller = DialogueController()

@router.post("/generate", tags=["Dialogue"])
def generate(params: Params, user_id: int = Depends(get_current_user_id)):
    a = dialogue_controller.generate(params)

    try:
        a_dict = json.loads(a)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to parse generated dialogue")

    user_data = user_service.get_user_data(user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User data not found")
    if isinstance(user_data, str):
        user_data = json.loads(user_data)

    game_id = params.game_id
    scene_id = params.scene_id
    script_id = params.script_id
    if script_id is None:
        raise HTTPException(status_code=400, detail="script_id должен быть передан в params или я в чем-то ошибся, анлак")

    # Поиск по структуре
    for game in user_data.get("games", []):
        if str(game.get("id")) == str(game_id):
            for scene in game.get("scenes", []):
                if scene.get("id") == scene_id:
                    if "scripts" not in scene:
                        scene["scripts"] = []

                    found = False
                    for script in scene["scripts"]:
                        if str(script.get("id")) == str(script_id):
                            script["result"] = a_dict
                            found = True
                            break
                    if not found:
                        new_script = {"id": script_id, "result": a_dict}
                        scene["scripts"].append(new_script)
                    break
            break
    success = user_service.update_user_data(user_id, user_data)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update user data")
    return {"ok": True}

