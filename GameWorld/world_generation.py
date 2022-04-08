import json
from typing import Dict, List

import numpy as np
from matplotlib.pyplot import figure, imshow, show

from main import database
from models.worlds import world_table
from water_generation import WaterGenerator
import pickle

import asyncio

# вызвать метод генерации воды в сборке общих методов

import pickle

class WorldGenerator:

    def __init__(self, world_map=None):
        self.world_map = np.zeros((1000, 1000), dtype=int)

    def get_map(self):
        return self.world_map

    def load_map(self, world_map: np.array):
        self.world_map = world_map

    def generate_map(self, map_size=1000, dirt_square=0.3, trees_square=0.15, grass_square=0.2, other_square=0.2):
        """
        Можно продумать, и нужно выбрать проценты таким образом, чтобы не выходило за площадь
        Не вставляться будет последний элемент, который в словаре находится --> лучше отсортировать по важности
        Выше --> важнее
        :param map_size:
        :param dirt_square, trees_square grass_square, other_square:  the percentage of the coverage
        """
        total_square = map_size ** 2

        if dirt_square + trees_square + grass_square * other_square < 1:
            dirt_square *= total_square
            trees_square *= total_square
            grass_square *= total_square
            other_square *= total_square

        # надо будет уточнить как передавать 0 у Дани
        values = {'dirt': np.random.randint(low=8, high=20, size=int(dirt_square)),
                  'trees': np.random.randint(low=40, high=60, size=int(dirt_square)),
                  'grass': np.random.randint(low=60, high=80, size=int(grass_square)),
                  'other': np.random.randint(low=80, high=160, size=int(other_square))
                  }
        return values

    def coverage(self):
        # Finding coverage of the map
        square = self.world_map.shape[0] ** 2
        return len(np.flatnonzero(self.world_map)) / square

    def draw_the_map(self):
        # The function literally draws the map
        figure(figsize=(50, 50))
        imshow(self.world_map)
        show()

    @staticmethod
    def generateRandomPoint():
        # функция возвращает кортеж из двух рандомных точек
        return np.random.randint(1000, size=2)

    def create_map(self, percentage_to_cover: float, elements_cords=list()):
        """
        The function generates map within specific coords and serializes data
        :param percentage_to_cover:
        :param elements_cords: The dictionary coords of the map
        :return: all coords data with specific location
        """
        elements = self.generate_map()  # получаем список словарей рандомных, если нужно д
        while self.coverage() < percentage_to_cover:
            for key in elements.keys():
                before_fill_coverage = self.coverage()

                # if key not in elements_cords.keys():
                #     # elements_cords = {grass: (12,22) --> список кортежей всех координат всех элементов конкретно травы
                #     elements_cords[key] = []  # если ключ новый, то присваеваем второй список

                iterations = self.world_map.shape[0] ** 2  # кол-во итераций (1 млн)
                if before_fill_coverage + len(elements[key]) / (
                        self.world_map.shape[0] ** 2) > percentage_to_cover - 0.05:
                    # ПРОВЕРЯЕМ, ЧТО СУМАРНАЯ ПЛОЩАДЬ, КОТОРУЮ МЫ ХОТИМ ВСТАВИТЬ БОЛЬШЕ
                    iterations = int((percentage_to_cover - before_fill_coverage) * self.world_map.shape[0] ** 2)
                for value in elements[key]:  # выбрали в словаре e.g grass --> и итерируемся по точкам словарям
                    x, y = self.generateRandomPoint()  # генерируем рандомную точку
                    while self.world_map[x][y] != 0:  # ищем рандомную точку где есть пустое место (0)
                        x, y = self.generateRandomPoint()
                    self.world_map[x][y] = value  # вставляем значение например другое 66
                    if key == 'grass':
                        elements_cords.append([(int(x), int(y)), 150])
                    # elements_cords[key].append(
                    #     (int(x), int(y), int(value)))  # тут мы добавляем в наш словарь все координаты травы
                    iterations -= 1
                    if iterations <= 0:  # выходим из цикла, что бы избавиться от лишних итераций и выйти из цикла
                        break
            if iterations <= 0:
                break
            if key == list(elements.keys())[-1]:  # на входе проверяем
                break
        return elements_cords

    @staticmethod
    def write_data_to_file(elements_coords: Dict):
        """The function writes data to the file with all coords """
        with open("world_coords.json", 'w') as input_file:
            json.dump(elements_coords, input_file)

    def create_world(self):
        """The function creates the world  можно так же загрузить карту"""
        water_inst = WaterGenerator()
        self.world_map = water_inst.create_world_with_water()
        print(f"The coverage of the water is: {self.coverage()}")
        elements_coords = self.create_map(percentage_to_cover=0.92)  # сколько точек добавить
        # print(elements_coords.keys())
        # with open('el_coords.pickle', 'wb') as f:
        #     pickle.dump(elements_coords, f)
        data = self.world_map
        with open('world_map.pickle', 'wb') as f:
            pickle.dump(data, f)

        with open('element_coords.pickle', 'wb') as f:
            pickle.dump(elements_coords, f)
        print(f"The coverage of the water + other elements is: {self.coverage()}")
        # self.draw_the_map()
        # self.write_data_to_file(elements_coords)

        # если надо добить покрытие, то можно использовать функцию повторно --> первую только допишет
        # добавить чтобы элементы, которые будут заполняться как словарь
        return self.world_map.tolist()




async def load_to_db(w_map):
    q = world_table.insert().values(world_map=w_map, world_name="Test1", running=False,
                                    grass_map=None)
    await database.connect()
    await database.fetch_one(q)


world = WorldGenerator()
world_map = world.create_world()
asyncio.run(load_to_db(world_map))


