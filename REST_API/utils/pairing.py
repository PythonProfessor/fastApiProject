from copy import copy
import yaml

import time

from sqlalchemy import or_

from REST_API.utils.entities import Entity
from main import database
from models.entities import entity_table
from models.parinig import pairing_table, pairing_bid_table


def read_config_data(path: str):
    """here we are parsing data from the yaml file into the class attributes"""
    with open(path) as f:
        d = yaml.safe_load(f)
        # l = d.keys()
        return list(d.values()), list(d.keys())  # returns dictionary values


from config.margin import margin_dict


class Pairing:
    """The class represents Pairing"""

    list_of_margins, child_args = list(margin_dict.values()), list(margin_dict.keys())

    def __init__(self, start_time, finish_time, pet_type, pet_id_1, pet_id_2, child_data, closed):
        # initializing a pairing table
        """Here has to be an update in db  (closed)!!!!!!!!"""
        self.start_time = start_time
        self.finish_time = finish_time
        self.pet_type = pet_type
        self.pet_id_1 = pet_id_1
        self.pet_id_2 = pet_id_2
        self.child_data = child_data
        self.closed = closed

    @staticmethod
    async def get_pairing_id_by_pet_id(pet_id):
        paring_table_query = pairing_table.select().where(or_(
            pairing_table.c.pet_id_1 == pet_id,
            pairing_table.c.pet_id_2 == pet_id)
        )
        pairing_id = dict(await database.fetch_one(paring_table_query))['id']
        return pairing_id

    @staticmethod
    async def pairing(pets):

        start_time = time.time()
        finish_time = start_time + 10  # 12 * 3600
        child_data = Pairing.generate_child_data(pets)
        # sql QUERY
        q = pairing_table.insert().values(
            start_time=start_time,
            finish_time=finish_time,
            pet_type=pets[0].pet_type,
            pet_id_1=pets[0].id,  # maybe c.id        ??????
            pet_id_2=pets[1].id,  # maybe c.id        ??????
            child_data=child_data,
            closed=True
        )

        await database.fetch_one(q)

    @staticmethod
    def generate_child_data(pets):
        """
        The method must generate approximate child data approxiamate [min,max] before writing it to the database
        :param pets: 2 pets of the Entity model
        :return: child data
        P.S maybe it can be re-written somehow in better style
        """
        list_of_margins, child_args = Pairing.list_of_margins, Pairing.child_args  # getting data from the files
        pet1_data_values = [pets[0].make_dict().get(child_args[key]) for key in range(len(child_args))]
        # here we get_values for the first and second pet
        pet2_data_values = [pets[1].make_dict().get(child_args[key]) for key in range(len(child_args))]

        # мб можно будет переписать, но пока так
        print(f"Аргументы для нахождения величин {child_args}")
        print(f"Фактические параметры на которые уменьшаем/ увиличиваем {list_of_margins}")
        min_data_values, max_data_values, child_data = [], [], []  # список для того, чтобы сохранять все минимальные значения
        for i in range(len(pet1_data_values)):
            parents_params = [pet1_data_values[i], pet2_data_values[i]]
            parents_params.sort()
            min_value = int(
                parents_params[0] - list_of_margins[i])  # каждый элемент отнимаем, для получения минимальных значений
            max_value = int(parents_params[1] + list_of_margins[i])
            if min_value <= 0:  # проверяем на левел и на остальные параметры
                min_value = 1
            elif max_value <= 0:
                max_value = 1
            min_data_values.append(min_value)
            max_data_values.append(max_value)
            child_data.append([min_value, max_value])  # here we
        return dict(zip(child_args, child_data))

    @staticmethod
    async def serialize_average_params(pet_id: int):
        # Получаем айдишник конктретного кролика --> делаем запрос в БД
        """
        Метод будет вызываться, если человек приймет ставку
        The method generates serialized params for the rabbit
        :param pet: rabbit model
        :param child_data: the dictionary of params
         Output must be
        {'max_saturation': [92, 102, 99], 'max_health': [100, 102, 115], 'max_hydration': [93, 103, 128],
        'speed': [1, 4.0, 14.0], 'vision_radius': [9.0, 14.0, 15.0], 'hearing_radius': [10.0, 20.0, 29.0],
        'level': [1, 1.0, 2.0], 'id': 83, 'pet_type': 'rabbit'}
        """
        paring_table_query = pairing_table.select().where(or_(
            pairing_table.c.pet_id_1 == pet_id,
            pairing_table.c.pet_id_2 == pet_id)
        )
        # тут получаем данные из таблицы pairing [child data]
        child_data = dict(await database.fetch_one(paring_table_query))['child_data']
        # используем функцию для создания тех параметров, которых нужно обновить
        values_to_update = await Entity.make_dict(pet_id)
        for key in child_data:
            child_data[key].insert(1, values_to_update.get(key))
        # child_data.update({"id": pet_tabl, "pet_type": pet.pet_type})         ???
        return child_data

    def __repr__(self):
        return f"start_time = {self.start_time}   " \
               f"finish_time = {self.finish_time}   " \
               f"pet_type = {self.pet_type}   " \
               f"pet_id_1 = {repr(self.pet_id_1)}   " \
               f"pet_id_2 = {repr(self.pet_id_2)}   " \
               f"child_data = {self.child_data}   "


class PairingBid:

    def __init__(self, bid_count, owner_id, pairing):
        self.bid_time = time.time()
        self.bid_count = bid_count
        self.owner_id = owner_id
        self.pairing = pairing

    @classmethod
    async def make_a_bet(cls, bid_count, owner_id, pairing):
        """Creating a function which creates an instance of the pairing bid and inserts data to the db"""
        instance = PairingBid(bid_count, owner_id, pairing)
        q = pairing_bid_table.insert().values(**instance.__dict__)  # .returning(
        #            pairing_bid_table.c.bid_time,
        #            pairing_bid_table.c.count,
        #            pairing_bid_table.c.onwer
        #        )
        pairing_bid = dict(await database.fetch_one(q))
        print(pairing_bid)
        return pairing_bid

    @staticmethod
    async def get_the_bid_by_id(owner_id):
        """Getting the bid by id"""
        q = pairing_bid_table.select().where(pairing_bid_table.c.owner_id == owner_id)
        data = await database.fetch_one(q)
        return data

    @staticmethod
    async def check_if_bid_exists(owner_id):
        """Проверяем, если ставка сущетсвует, то пишем, что"""
        data = await PairingBid.get_the_bid_by_id(owner_id)
        return dict(data) if data else True
            # return {
            #
            # }
