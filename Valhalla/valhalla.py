from __future__ import annotations

import asyncio
import logging
import os
import threading
import time
from math import ceil
from typing import Optional, List

import yaml

from main import database
from models.entities import entity_table


class Vallhala:

    # @staticmethod
    # def get_all_pets():
    #
    #     pass

    @staticmethod
    async def get_pets_for_healing(move_status: int = 4) -> List or False:
        """
        The function gets all rabbits with move_status 4        Возможно можно будет её использовать как универсальную функцию для получения кролликов не только для Вальхаллы
        :param move_status: IN_HOSPITAL/ ...
        :return: False if there are no rabbits
        """
        await database.connect()
        q = entity_table.select().where(entity_table.c.move_status == move_status)
        data = await database.fetch_all(q)
        return [dict(i) for i in data] if data is not None else False

    @staticmethod
    def read_conf(file_path: str):
        with open(file_path) as f:
            d = yaml.safe_load(f)
            return d.values()  # returns dictionary values

    def run(self):
        """
        # TODO запустить celery тут в цикл событий
        """

        async def f():
            t = threading.Thread(target=self.start)
            t.start()
            await asyncio.sleep(2)  # time.sleep(2)
            t.join()

        while True:
            f()

    @staticmethod
    def rabbits_healing(rabbits: List, percentage_from_max_hp: int | float, points_to_heal: int | float):
        # TODO прикрутить сюда celery, возможно или же в отдельный роут / файл
        """
        Calculating the healing of the rabbits
        :param rabbits: list of dictionaries
        :param percentage_from_max_hp:  %   we want to heal a rabbit for 70%
        :param points_to_heal: 2 hp
        :return: the updated health of the rabbit
        """
        for i in range(len(rabbits)):
            rabbit_max_health, current_health, = rabbits[i].get('max_health'), rabbits[i].get('health')
            # print(f"Max health: {rabbit_max_health}")
            heal_to_hp = ceil(
                percentage_from_max_hp / rabbit_max_health * 100)  # getting the data where we are healing to
            points_to_heal = ceil(points_to_heal / rabbit_max_health * 100)  # getting the num of hp to heal
            if current_health <= heal_to_hp:
                rabbits[i].update(health=current_health + points_to_heal)  # updating
        return rabbits
        # print(f"Heal to hp: {heal_to_hp} Points to heal: {points_to_heal}")

    async def start(self):
        percentages_from_max_hp, points_to_heal = self.read_conf("valhalla_config.yaml")
        # tut netu smislav kazhdii raz ih poluchat iz konfiga mozhno sdelat attributom classa
        logging.info(f"percentages_from_max_hp:  {percentages_from_max_hp} %, points_to_heal {points_to_heal} %")
        rabbits = await self.get_pets_for_healing(move_status=4)
        # print(f"The rabbits {rabbits}")
        # print(f"The length of rabbits: {len(rabbits)}")

        print("Before:")
        print("-------------------------------------------------------------------------------")
        print(rabbits)
        print("After:")
        print("-------------------------------------------------------------------------------")
        print(self.rabbits_healing(rabbits, percentages_from_max_hp,
                                   points_to_heal))  # надо будет ещё раз прочекать и апдейтнуть БД
        for rabbit in rabbits:
            # users.update().where(users.c.id==5).values(name="some name")
            q = entity_table.update().where(entity_table.c.id == rabbit.get('id')).values(health=rabbit.get('health'))
            await database.execute(q)

        # q = entity_table.insert().values(rabbits)
        # await database.execute_many(q, rabbits)
        # RabbitModel.objects.bulk_update(rabbits, fields=['health', 'move_status', 'state'])


