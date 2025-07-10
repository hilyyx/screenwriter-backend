from pydantic import BaseModel
from typing import List, Dict, Any

class GlobalParams(BaseModel):
    name: str
    profession: str
    goal: str
    talk_style: str
    traits: str

class GoalParams(BaseModel):
    type: str
    object: str
    condition: str

class Dialogue(BaseModel):
    id: str
    info: str
    line: str

class DialogueData(BaseModel):
    id: str
    line: str
    to: Dialogue

class DialogueResponse(BaseModel):
    id: str
    name: str
    data: List[DialogueData]

class Params(BaseModel):
    npc: GlobalParams
    hero: GlobalParams
    world_settings: str
    NPC_to_hero_relation: str
    hero_to_NPC_relation: str
    mx_answers_cnt: int
    mn_answers_cnt: int
    mx_plot_branches_cnt: int
    mx_depth: int
    mn_depth: int
    goals: List[GoalParams]