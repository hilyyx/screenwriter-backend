from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

class Params(BaseModel):
    world: Dict[str, Any]
    character: Dict[str, Any]
    npc: List[Dict[str, Any]]


class Dialogue(BaseModel):
    id: int
    info: str
    line: str

class DialogueData(BaseModel):
    id: int
    line: str
    to: Dialogue

class DialogueResponse(BaseModel):
    id: int
    name: str
    data: List[DialogueData]

@app.post("/generate")
def generate_dialogue(params: Params):

    return [
        {
            "id": 1,
            "name": "name npc",
            "data": [
                {
                    "id": 1,
                    "line": "Phrase",
                    "to": {
                        "id": 2,
                        "info": "Info something",
                        "line": "Phrase about important"
                    }
                }
            ]
        }
    ]
