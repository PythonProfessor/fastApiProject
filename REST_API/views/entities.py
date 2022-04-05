"""
Этот модуль отвечает за логи  которая принимает Web-запрос и возвращает Web-ответы + взаимодействует с БД, игровым миром
конкретно для животинок
"""
from typing import List

from REST_API.schemas.entities import EntityResponse, EntityDetail, EntityThrow, EntityPickUp, EntityLevelUp
from REST_API.utils.entities import Entity

from REST_API.decorators import auth

from functools import wraps

# TODO значит, везде нужно менять state/move_status  into the CRUD operations
from REST_API.utils.pairing import Pairing

"""
В общем и целом можно использовать класс EntityViews какой-то для удобства взаимодействия с юзером
"""


@auth
async def pet_detail(pet: EntityDetail):
    """
    Получаем питомца по pet id
    :param pet: EntityDetail validation class
    :return: pet object
    """
    pet = await Entity.get_entity_by_pet_id(pet.pet_id)
    return pet


@auth
async def throw_pet_to_island(pet: EntityThrow):
    island_id, square_num = pet.island.island_id, pet.island.square_num  # custom field in schemas
    if 1 > square_num > 24:  # here has to be additional validation
        return {"impossible to place": False}
    pet = await Entity.throw_pet(pet.pet_id, pet.pet_type, island_id=island_id)
    return {"success": True}


@auth
async def pick_up_pet_from_island(pet: EntityPickUp):
    print(pet.pet_type, pet.hard_token, pet.all_pets)
    return await Entity.pick_up_pets(hard_token=pet.hard_token, pet_id=pet.pet_id,
                                     pet_type=pet.pet_type, all_pets=pet.all_pets)


@auth
async def level_up(pet: EntityLevelUp):
    return await Entity.level_up(hard_token=pet.hard_token, pet_id=pet.pet_id, pet_type=pet.pet_type)


@auth
async def pairing(pets: List[EntityDetail]):
    return await Pairing.pairing(pets)


@auth
async def test_get_one_pet(pet: EntityDetail):
    return await Entity.get_pet_from_db(hard_token=pet.hard_token, pet_id=pet.pet_id, pet_type=pet.pet_type)

# event_pack / event_details -- not so necessesarily

# level up
# heal pet
# pairing
# pairing bid
# parents tree


# """ Создает нового пользователя в БД    UserCreate используется для ввода данных, тоесть фактически Fast Api юзает это!"""
# salt = get_random_string()
# hashed_password = hash_password(user.password, salt)
# query = users_table.insert().values(
#     username=user.username, hashed_password=f"{salt}${hashed_password}",
#     is_active=True, is_staff=False)
# user_id = await database.execute(query)     # getting the specific user
# tokens = await User.create_user_token(user_id)      # creating tokens for specific user
# token_dict = {"hard_token": tokens["hard_token"], "soft_token": tokens["soft_token"]}
# await Entity.generate_test_pets(user_id)
# response = {**user.dict(), "id": user_id, "is_active": True}
# response.update(token_dict)
# return response
