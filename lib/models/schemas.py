from typing import List, Dict, Optional

from pydantic import BaseModel, EmailStr


#-------СОЗДАНИЕ ПАРАМЕТРОВ ИГРЫ-----------#
class GlobalParams(BaseModel):
    name: str
    profession: str
    talk_style: str
    traits: str
    look: str
    extra: str

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
    mx_depth: int
    mn_depth: int
    scene: str
    genre: str
    epoch: str
    tonality: str
    extra: str
    context: str
    goals: List[GoalParams]

#-------РЕГИСТРАЦИЯ И ВХОД-----------#
class UserRegisterRequest(BaseModel):
    mail: EmailStr
    name: str
    surname: str
    password: str

class UserLoginRequest(BaseModel):
    mail: str
    password: str

class UserResponse(BaseModel):
    id: int
    mail: EmailStr
    name: str
    surname: str


#-------РУЧКИ ДЛЯ БД-----------#
class UserRegister(BaseModel):
    mail: EmailStr
    name: str
    surname: str
    password_hash: str
    data: Optional[Dict] = None

class UserUpdateName(BaseModel):
    name: str
    surname: str

class UserUpdatePassword(BaseModel):
    password_hash: str

class UserUpdateData(BaseModel):
    user_id: int
    data: Dict

class DeleteUser(BaseModel):
    user_id: int