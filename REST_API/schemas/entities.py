"""
Этот модуль используется для настройки end пойнтов entities и обрабатываем конечные запросы взаимодействуя с БД
"""
from typing import Optional, Union

from pydantic import BaseModel, Json

class EntityDetail(BaseModel):
    """ Проверяет login запрос """
    # email: EmailStr
    hard_token: str
    pet_type: str
    pet_id: int


class EntityResponse(BaseModel):
    pet_type: str
    pet_id: int
    health: float
    prettiness: float
    coord_x: Union[int, None]
    coord_z: Union[int, None]
    saturation: float
    hydration: float
    speed: int
    vision_radius: int
    hearing_radius: int
    level: int
    appearance: str
    attraction: Union[int, None]
    race: Json
    name: str

#TODO change all comments

class Island(BaseModel):
    island_id: int
    square_num: int

class EntityThrow(BaseModel):
    """ Проверяет login запрос """
    hard_token: str
    pet_type: str
    pet_id: int
    island: Island         # how to get the island


class EntityPickUp(BaseModel):
    """Picking up pets"""
    hard_token: str
    pet_type: str
    pet_id: int
    all_pets: bool
