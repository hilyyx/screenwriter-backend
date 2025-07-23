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
def generate(params: Params, user_id: int = Depends(get_current_user_id)):
    # a = dialogue_controller.generate(params)
    a = {"x": 1}
    # try:
    #     a_dict = json.loads(a)
    # except Exception:
    #     raise HTTPException(status_code=500, detail="Failed to parse generated dialogue")

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
    if game_id is None:
        raise HTTPException(status_code=400, detail="game_id должен быть передан в params или я в чем-то ошибся, анлак")
    if scene_id is None:
        raise HTTPException(status_code=400, detail="scene_id должен быть передан в params или я в чем-то ошибся, анлак")
    # Поиск по структуре
    # for game in user_data.get("games", []):
    #     if str(game.get("id")) == str(game_id):
    #         for scene in game.get("scenes", []):
    #             if str(scene.get("id")) == str(scene_id):
    #                 # if "scripts" not in scene:
    #                 #     scene["scripts"] = []

    #                 found = False
    #                 for script in scene.get("scripts", []):
    #                     if str(script.get("id")) == str(script_id):
    #                         script["result"] = a
    #                         found = True
    #                         break
    #                 if not found:
    #                     raise HTTPException(status_code=400, detail="script_id не валидный")
    #                 break
    #         break
    for game_index in range(len(user_data.get("games", []))):
        game = user_data["games"][game_index]
        if str(game.get("id")) == str(game_id):
            for scene_index in range(len(game.get("scenes", []))):
                scene = game["scenes"][scene_index]
                if str(scene.get("id")) == str(scene_id):
                    found = 0
                    for script_index in range(len(scene.get("scripts", []))):
                        script = scene["scripts"][script_index]
                        if str(script.get("id")) == str(script_id):
                            user_data["games"][game_index]["scenes"][scene_index]["scripts"][script_index] = a
                            found = 1
                            break
                    if not found:
                        raise HTTPException(status_code=400, detail="script_id не валидный")
                    break
            break
                        
    success = user_service.update_user_data(user_id, user_data)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update user data")
    
    return {"ok": True}
