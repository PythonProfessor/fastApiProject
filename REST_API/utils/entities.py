"""
Этот модуль используется фактически для CRUD операций над базой данных используя модель entity
"""
import sqlalchemy
from sqlalchemy import and_

from REST_API.utils.tokens import Token
from REST_API.utils.users import User
from main import database
from models.tokens import token_table
from models.users import users_table
from models.entities import entity_table


class Entity:
    # тут нужно подумать за метод генерации, который будет делать рандомные параметры питомцев при создания юзера
    def __init__(self, user_id: int = None, world_id: int = None):
        self.coord_x = None
        self.coord_z = None
        self.health = 100
        self.saturation = 100
        self.hydration = 100
        self.speed = 100
        self.vision_radius = 5
        self.hearing_radius = 5
        self.max_health = 100
        self.max_saturation = 100
        self.max_hydration = 100
        self.level = 1
        self.state = 0
        self.move_status = 0
        self.pet_type = 'rabbit'
        self.owner_id = user_id
        self.world_id = world_id
        self.attraction = 70
        self.race = [
            {
                "race": "forest",
                "value": 100,
            }
        ]
        self.name = "It's a cat"

    @staticmethod
    async def get_entity_by_pet_id(pet_id):
        #     q = users_table.select().where(users_table.c.username == user.username) # sql statement
        q = entity_table.select().where(entity_table.c.id == pet_id)
        data = await database.fetch_one(q)
        return dict(data)

    @staticmethod  # maybe class
    async def generate_test_pets(user_id: int):
        """The function generates 5 pets for the specific user"""
        instance = Entity(user_id=user_id)
        print(instance.__dict__)
        for i in range(5):
            query = entity_table.insert().values(**instance.__dict__)  # -1 pet
            await database.fetch_one(query=query)

    @staticmethod
    async def pick_up_pets(hard_token: str, pet_type: str, all_pets: bool, pet_id: int = None):
        """
        The function picks up pets from the island
        :param hard_token:  hard??1648734611.4342415
        :param pet_type:    rabbit
        :param pet_id:      None/Integer
        :param all_pets:    True/False
        :return:        {"success response"}
        """
        user = dict(await User.get_user_by_token(hard_token=hard_token))
        if not all_pets:
            # filtering the pet according to id and updating database
            query = entity_table.update().where(and_(entity_table.c.owner_id == user['id'],
                                                     entity_table.c.id == pet_id,
                                                     entity_table.c.pet_type == pet_type)).values(world_id=None)
        else:
            # filtering the pet according to id
            query = entity_table.update().where(entity_table.c.owner_id == user['id']).values(world_id=None)
        data = await database.fetch_all(query)
        print(dict(data))
        return {"success": True}

        # d = {} --> it is an opprotunity to iterate through all pets NOTE: will be usefull for Valhalla
        # for entity in list(data):
        #     print(dict(entity))     # словарь питомцев получаем !

    """
    Check validation after all
    class TrowPetToIslandView(GenericAPIView):
    serializer_class = serializers.TrowPetToIslandSerializer

    @auth
    def post(self, request):
        data = request.data
        pet_type, pet_id, island = data.get('pet_type'), data.get('pet_id'), data.get('island')
        if not all([pet_type, pet_id, island]):
            return Response({'success': False, 'error': 'data is not valid'})
        if not all([island.get('island_id') is not None, island.get('square_num') is not None]):
            return Response({'success': False, 'error': 'Island data is ot valid'})
        if not 0 <= island.get('square_num') <= 24:
            return Response({'success': False, 'error': 'Square num is ot valid'})
        # owner = Token.objects.get(hard_token=data.get('hard_token')).user
        pet = engine_models.pet_models[pet_type].objects.only('move_status', 'island_id').get(
            owner__token__hard_token=data.get('hard_token'), pk=pet_id)
        if pet.move_status != pet.MoveStatus.in_pocket.value:
            return Response({'success': False, 'error': 'pet is out of pocket'})
        if pet.state == -1:
            return Response({'success': False, 'error': 'pet injured'})
        island_model = engine_models.GameWorldModel.objects.get(pk=island.get('island_id'))
        pet.coord_x, pet.coord_z = self.get_square_cords(island.get('square_num'))
        pet.island = island_model
        pet.move_status = pet.MoveStatus.in_wait_trow_to_island.value
        pet.change_move_status_timestamp = time.time()
        pet.save()
        return Response({'success': True})
    """

    @staticmethod
    async def throw_pet(pet_id: int, pet_type: str, island_id: int):
        q = entity_table.update().where(and_(entity_table.c.id == pet_id, pet_type == pet_type)). \
            values(
            world_id=island_id)  # когда будет движок, нужно будет так же обновлять координаты по функции get_square_cords
        await database.fetch_one(q)

    # @staticmethod
    # async def throw_pet_to_island(hard_token, pet_id, island_id):
    #     q = User.get_user_by_token(hard_token=token)
    #     entity_table.insert()

    def pet_detail(self):
        return self.__dict__
