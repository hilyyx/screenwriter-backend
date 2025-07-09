from pydantic import BaseModel
from typing import List, Dict, Any

class Params(BaseModel):
    world: Dict[str, Any]
    character: Dict[str, Any]
    npc: List[Dict[str, Any]]

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
