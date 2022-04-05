import logging
from math import floor
from random import randint, choice
from typing import List
import json
import numpy as np

matrix1 = [[20, 20, 20, 20],
           [20, 20, 20, 20],
           [20, 20, 1, 20],
           [0, 20, 20, 0]]

matrix2 = [[0, 20, 20, 20, 0],
           [20, 20, 20, 20, 20],
           [20, 20, 2, 20, 20],
           [20, 20, 20, 20, 20],
           [0, 20, 20, 20, 0], ]

matrix3 = [[20, 20, 20],
           [20, 3, 20],
           [20, 20, 20]]

matrix4 = [[20, 20, 0],
           [20, 4, 20],
           [0, 20, 20]]

matrix5 = [[0, 0, 20, 20, 20, 0, 0],
           [0, 0, 20, 20, 20, 20, 0],
           [0, 20, 20, 20, 20, 20, 20],
           [0, 20, 20, 5, 20, 20, 20],
           [20, 20, 20, 20, 20, 20, 20],
           [20, 20, 20, 20, 20, 20, 20],
           [0, 20, 20, 20, 20, 20, 20], ]

matrix6 = [[0, 20, 20, 20, 0, 0, 0],
           [0, 20, 20, 20, 20, 0, 0],
           [0, 20, 20, 20, 20, 20, 0],
           [0, 20, 20, 6, 20, 20, 0],
           [20, 20, 20, 20, 20, 20, 20],
           [20, 20, 20, 20, 20, 20, 20],
           [20, 20, 20, 20, 20, 20, 20], ]

# # additional try to generate matrix
list_of_all_matrix = [matrix1, matrix2, matrix3, matrix4, matrix5, matrix6]  # creating list of all matrixes


def choose_matrix():
    # the function gets random matrix and returns it
    return choice(list_of_all_matrix)


def lakes_type():
    # the function gets the type of lakes basically
    # 1 = [[20,20,20],[20,20,20],[20,20,20]]
    matrix_indexes = [i for i in range(len(list_of_all_matrix))]
    return dict(zip(matrix_indexes, list_of_all_matrix))


class WaterGenerator:  # the map of the world

    world_size = 1000
    __margin_x = 5  # if we need more % -> less the margin
    __margin_z = 5
    world_map = np.zeros((world_size, world_size), dtype=int)
    lakes_list = []

    @staticmethod
    def get_random_points():
        """
        The function looks for a random point and forms a list from them
        :return: the points array       e.g (points[11,11])
        """
        #  7 , world_size - 7               # cheeck
        # ЕСЛИ НЕТУ 20

        random_point1 = randint(7, WaterGenerator.world_size - 7)  # within special area
        random_point2 = randint(7, WaterGenerator.world_size - 7)  # within special area

        points = [random_point1] + [random_point2]  # get the coords of this dot on the map
        return points

    @staticmethod
    def validate_coords(row_from, row_to):
        # + matrix_width
        # the function which validates the coords of the map range
        return False if row_from < 0 or row_to > 1000 else True

    @staticmethod
    def find_matrix_center(matrix):
        """
        The function gets the coords of matrix
        :param matrix: MATRIX to find center
        :return: center of the matrix
        """
        center = [floor(len(matrix[0]) / 2), floor(len(matrix) / 2)]
        return center

    @staticmethod
    def find_center_of_the_lake_on_the_map(random_points, lake_center):
        center_on_the_map = [random_points[0] + lake_center[0], random_points[1] + lake_center[1]]
        print(f"The center on the map {center_on_the_map}")
        return center_on_the_map

    @staticmethod
    def find_id(chosen_matrix, x, z):
        return chosen_matrix[x][z]

    def generate_lake(self):
        """
        The function generates one lake according to the algorithm
        1) We choose matrix from the given patterns
        2) Get its width and length (anyway they are all equal)
        3) Get the random coords on the map ( for instance [25,25]
        4) Finding the coverage area to check ( the nearest location( if the lake is present in this area)
        5) Finding the center of the lake  in matrix    ( for matrix 3x3) it is  [1,1], we have to find the center of the lake on the map
        6) if the area is valid to draw a lake , we make a slice from initial area
        ---------------------------------------------------------------------------------
        world_map[x:x + matrix_width, z:z + matrix_length] = chosen_matrix
        :return:
        """
        chosen_matrix = choose_matrix()
        matrix_width, matrix_length = np.shape(chosen_matrix)
        print("Width: ", matrix_width, "Length: ", matrix_length)
        print("Chosen matrix")
        print(np.array(chosen_matrix))
        x, z = self.check_lake_presence(matrix_width)
        print("Random coords are:", x, z)
        lake_center = (self.find_matrix_center(chosen_matrix))
        center_on_the_map = self.find_center_of_the_lake_on_the_map([x, z], lake_center)
        print(f"The center of the lake is: {lake_center}")
        print(f"The center on the map is : {center_on_the_map}")
        lake_id = self.find_id(chosen_matrix, x=lake_center[0], z=lake_center[1])
        self.make_list_with_lakes(lake_id, center_on_the_map)  # maybe chosen matrix
        self.world_map[x:x + matrix_width, z:z + matrix_length] = chosen_matrix

    # генерация озёр пока не покроет определённый процент от карты

    def get_coverage_range(self, x_coord, z_coord, matrix_width):
        """
        В функции мы получаем ту область, которую хотим проверить на наличие озёр
        :param matrix_width: ширина матрицы
        :return: точки, от которых будет делаться срез по карте и вставление озера
        """
        # x_coord, z_coord = cls.get_random_points()
        coords_1, coords_2 = x_coord - self.__margin_x, x_coord + self.__margin_x + matrix_width
        coords_3, coords_4 = z_coord - self.__margin_z, z_coord + self.__margin_z + matrix_width
        if coords_1 < 0:
            coords_1 = 0  # обязательно зануляем, так как
        elif coords_3 < 0:
            coords_3 = 0
        return coords_1, coords_2, coords_3, coords_4

    def check_lake_presence(self, matrix_width):
        """
        Проверяет наличие озера в заданном диапазоне
        :return: координаты куда вставлять озеро
        """
        x_coord, z_coord = self.get_random_points()
        coords_1, coords_2, coords_3, coords_4 = self.get_coverage_range(x_coord, z_coord, matrix_width)

        while 20 in self.world_map[coords_1:coords_2, coords_3:coords_4]:
            x_coord, z_coord = self.get_random_points()
            coords_1, coords_2, coords_3, coords_4 = self.get_coverage_range(x_coord, z_coord, matrix_width)
        return x_coord, z_coord

    def generate_n_lakes(self, n=5000):  # 18k точек - центр
        # we are generating n lakes
        for i in range(n):
            self.generate_lake()
            # print(i)

    def make_map_from_np_array(self):
        # the function returns normal 2-d list from numpy 2-d array
        return self.world_map.tolist()

    def draw_the_map(self):
        # draw the plot of the map
        from matplotlib.pyplot import figure, imshow, show
        # import matplotlib.pyplot as plt
        figure(figsize=(50, 50))  # abadok
        imshow(self.world_map)
        show()

    def write_coverage_statistic(self, water_param):
        with open("world_statistic.json", 'w', encoding='utf-8') as world_file:
            data = {
                "water_coverage": water_param,
                "trees_coverage": None,
                "rabbits_coverage": None,
            }
            data = json.dumps(data, indent=2)
            world_file.write(data)

    def create_world_with_water(self):
        self.generate_n_lakes(2000)  # generating 4k lakes
        self.draw_the_map()        # draw the map
        word_cov = self.coverage_method()
        self.write_coverage_statistic(word_cov)
        self.make_json_with_data(world_id=1)  # here we are making a dict from json
        #world_arr = self.make_map_from_np_array()
        return self.world_map

    def coverage_method(self):
        """
        The main goal of this function is to count the percentage of the coverage of different objects on the map
        :param: int number e.g   20 - the lake
        :return:
        """
        water_amount_on_the_map = np.flatnonzero(self.world_map).__len__() / (self.world_size ** 2) * 100
        return round(water_amount_on_the_map, 2)

    def gen_water(self, world_id, lakes=2000):
        self.generate_n_lakes(lakes)
        self.make_json_with_data(world_id=world_id)  # here we are making a list
        self.lakes_list = []
        return self.make_map_from_np_array()

    def make_list_with_lakes(self, lake_id: int, lake_center_on_the_map: List):
        dict_lake = {
            "id": lake_id,
            "lake_center_on_the_map": lake_center_on_the_map
        }
        self.lakes_list.append(dict_lake)
        return self.lakes_list

    def make_json_with_data(self, world_id):
        """
        The function gets a world_id parametr which lets
        :param world_id:
        :return:
        """
        path = "water.json"
        try:
            with open(path, "w") as outfile:
                json.dump(self.lakes_list, outfile)
        except FileExistsError or FileNotFoundError as e:
            logging.error(f"The {e} has occurred")
            raise
