"""
Этот модуль используется для настройки end пойнтов entities и обрабатываем конечные запросы взаимодействуя с БД
"""
from fastapi import APIRouter
from typing import List
from REST_API.schemas.entities import EntityResponse, EntityDetail, EntityThrow, EntityPickUp, EntityLevelUp
from REST_API.views import entities as entities_views

router = APIRouter()


@router.post("/pet_detail")  # response_model=EntityResponse
async def pet_detail(pet: EntityDetail):
    """
    The handling of the register route
    :param user: value for creation of the user
    :return: the user view
    """
    return await entities_views.pet_detail(pet)


@router.post('/throw_pet_to_island')
async def throw_pet_to_island(pet: EntityThrow):
    return await entities_views.throw_pet_to_island(pet)


@router.post('/pick_up_pet_from_island')
async def pick_up_pet_from_island(pet: EntityPickUp):
    return await entities_views.pick_up_pet_from_island(pet)


@router.post('/level_up')
async def level_up(pet: EntityLevelUp):
    return await entities_views.level_up(pet)


@router.post('/pairing')
async def pairing(pets: List[EntityDetail]):
    return await entities_views.pairing(pets)


@router.post('/test_get_one_pet')
async def test_get_one_pet(pet:EntityDetail):
    return await entities_views.test_get_one_pet(pet)