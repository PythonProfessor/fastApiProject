import pickle
import sys

import numpy as np
from matplotlib.pyplot import figure, imshow, show
import time

# трава в grass coords
# sys.setrecursionlimit(1500)

"""Поменять название файла (было в черновичке) """
with open('world_map.pickle', 'rb') as f:
    # значит кароч
    world_map = pickle.load(f)
    world_map = np.array(world_map)

with open('element_coords.pickle', 'rb') as f1:
    grass_cords = pickle.load(f1)


def generateRandomPoint():
    # нельзя добавить кроллика дальше этих координат, потому что граница будет меньше чем вижн рэдиус
    return np.random.randint(45, 920, size=2)


def wait(start, timeWait=2):
    """
    высчитываем тики    кароче, выполняем действия без учёта время выполнения кода
    :param start: Время начала отсчёта --__-- ( конец хода )
    :param timeWait: Скок сек ожидать       ( на треды или корутины пересчитать )
    :return:
    """
    end = time.time()

    while end - start < timeWait:
        end = time.time()

    return True


def float_cords(coord_x, coord_z):
    # >>На вход получаем координаты, а на выход эти же коорды с рандомной дробной частью<<
    # ЧТОБЫ НЕ БЫЛО ШАХМАТ!
    # Как я понял, Миша брал какую-то рандомную координату и добавлял её через радианы, тут реализована логика такая
    # же самая, только без 3х бесполезных функций , которые добавляет её через рандомную радиану!!!
    return (round(coord_x + np.random.random(), 2), round(coord_z + np.random.random(), 2))


def generate_rabbits(rabits_counts=1):
    rabbits_dict = dict()
    dirt_id = list(range(8, 20)) + [0]  #
    check_valid = []
    for idRabbit in range(rabits_counts):
        coord_x, coord_z = generateRandomPoint()
        cordinate = coord_x, coord_z
        # print( (coord_x, coord_z), (tuple([coord_x, coord_z]) in rabits_cords))
        #  or cordinate in check_valid
        while world_map[coord_x, coord_z] not in dirt_id or cordinate in check_valid:
            coord_x, coord_z = generateRandomPoint()
            cordinate = coord_x, coord_z  # всегда в бд должны быть интовые , а в мув логах - флотовые
        check_valid.append((coord_x, coord_z))  # чтобы кролик не вставали на одну и ту же самую точку

        rabbits_dict[idRabbit] = {
            #"id":1,
            'coord_x': coord_x,  # всегда в бд должны быть интовые , а в мув логах - флотовые
            'coord_z': coord_z,  # всегда в бд должны быть интовые , а в мув логах - флотовые
            'target_point': (0, 0),
            'max_health': 100,
            'health': 100,
            'max_saturation': 100,
            'saturation': 100,
            'max_hydration': 100,
            'hydration': 100,
            'vision_radius': np.random.randint(4, 7),  # если вижин radius <= speed + 1
            'move_log': [float_cords(coord_x, coord_z)],
            'level': 1,
            'attraction': 50,
            'move_status': 1,  # move status???
            'state': 0,
            'speed': np.random.randint(2, 3),  # учитываем 1 в дальнейших функциях
            'action_log': []  # доп поле по action log, кlaссная идея для отладки

        }

    return rabbits_dict, check_valid


def calculate_cords(border1, border2, border3, border4):
    # вычисляем все кординаты в области vision_radius кролика, возрашает матрицу размером равным матрицы vision(из функции vision_obl), внутри матрицы хранятся кординаты большой карты.
    """
    :param border1-4: граница вижина в какую-то сторону
    :return: 
    [[112, 122],
        [112, 123],
        [112, 124],
        [112, 125],
        [112, 126]],
        
        ...
       [[116, 122],
        [116, 123],
        [116, 124],
        [116, 125],
        [116, 126]]
    """
    vision = []
    iters = 0
    for x in range(border1, border2):
        vision.append([])
        for z in range(border3, border4):
            input_cord = (x, z)
            vision[iters].append(input_cord)
        iters += 1
    return np.array(vision)


def vision_obl(cordinate_x, cordinate_z,radius=1):  # выводит область зрения кролика вида элементов и вида кординат на реальной карте
    """
    Рассчёт вижин области 
    :param cordinate_x: фактические координаты кролика на карте
    :param cordinate_z: фактические координаты кролика на карте
    :param radius:  во все стороны на 5 клеток зрений (25 клеток)
    :return:

    например кролик стоит на координате 114, 123 , его область видимости - 4 ,
    (--> border1 = 110
    --> border2 = 115      +1 для границе среза)
    """
    border1, border2 = (cordinate_x - radius), (cordinate_x + radius + 1)  # вычисление границы
    border3, border4 = (cordinate_z - radius), (cordinate_z + radius + 1)

    if border1 < 0: border1 = 0  # границы видимости валидирование, если вдруг выйдем за ренж карту
    if border2 > 1000: border3 = 1000
    if border3 < 0: border3 = 0
    if border4 > 1000: border3 = 1000

    vision = world_map[border1:border2, border3:border4]
    # получаем такую матрицу: --> область видимости по карте
    """
    [ 20,  17,  11,  17,   0],
    [ 20,   0,  11,  16, 148],
    [ 20,  49,  75,  48,  46],
    [124,  67,  15,  57,  10],
    [ 41,  54,  77,  72,  62]
    """
    cordinates = calculate_cords(border1, border2, border3, border4)
    # тут мы вернём такой же самый массив точек на карте
    return vision, cordinates, radius


def find_target_cord(objects: dict, objects_id: list):  # возращает
    '''
    Получаем на вход objects |><|
    :param objects:   { 20: (11,22) ... }
    :param objects_id: тот обьект, который нам нужен (трава, вода, земля)
    :return: тут вернём список всех координат , нужных нам айдищников
    '''
    output_cords = []
    for key in objects:
        if key in objects_id:
            output_cords += objects[key]

    return output_cords


def find_object(vision, input_radius, speed=1):  # нахождение всех кординат на растояние speed от центра
    """
    ==================================================================================================
    Кароче, вкратце, мы находим все обьекты в поле радиуса и создаём их в виде словаря
    :return{ 20: (11,22) ... }
    ==================================================================================================
    :param vision - это матрица:
    :param input_radius: vision_radius of the rabbit
    :param speed: сколько мы клеточек можем походить

    # рассчёты тут конченные, если хватит нервов, то поставь отладку и свечку в церкве за здравие
    """
    def add_to_dict(input_dict, key, value):  # Составляем словарь вида id(элемента):список кординат в матрице vision,
        if key not in input_dict.keys():
            input_dict[key] = [value]
        else:
            if value not in input_dict[key]:  # проверка чтобы элементы не повторялись
                input_dict[key].append(value)
        return input_dict

    def block_cord(border, cord, output=dict()):  # Просчет всех кординат для матрицы cordinates
        inp = (border, cord)
        inp1 = (cord, border)
        if inp == inp1:
            output = add_to_dict(output, vision[inp], inp)
        else:
            output = add_to_dict(output, vision[inp], inp)
            output = add_to_dict(output, vision[inp1], inp1)
        return output

    x_start = input_radius - speed
    y_start = input_radius + speed

    if x_start < 0: x_start = 0
    if y_start < 0: y_start = 0
    output = {}

    for cord in range(x_start, y_start + 1):
        output = block_cord(x_start, cord)
        output = block_cord(y_start, cord, output=output)
    return output


def heal_grass(grass_elements, heal_per_time):
    for element in range(len(grass_cords)):
        health = grass_elements[element][1]
        if health != 150:
            health += heal_per_time
        if health > 150: health = 150

        grass_elements[element][1] = health

    return grass_elements


def choose_random_parametr(params):
    # полу
    return np.random.choice(params)


def find_grass_by_coord(cord):
    for iteration in range(len(grass_cords)):
        if grass_cords[iteration][0] == cord:
            return iteration


def validate_dirt_cords(list_real_cords, radius):
    radius = radius * 2 + 1
    output = []
    for cord in list_real_cords:
        cord_x, cord_z = cord
        if (cord_x - radius) <= 0 or (cord_x + radius) >= 1000 or (cord_z - radius) <= 0 or (cord_z + radius) >= 1000:
            pass
        else:
            output.append(cord)

    return output


def find_all_dirt_speed(inp_vision, inp_cordinates, speed, dirt_id, input_radius,
                        maximum=False):  # все кординаты на которые кролик может походить в области speed

    """Как по мне, ГЕНИАЛЬНАЯ ФУНКЦИЯ передвижения кроля , дял того, чтобы рандомно мувать кролика, мы проверяем
    сначала самую максимальную границу движения нашего кролика -> |> в его speed возможностях, и итерируемся только
    по куску той области, если же грязи нету, на его максимальной границе, то тогда мы скидываем её на 1 единицу вниз,
    и прыгаем туда"""

    start_border = 0  # параметр нужен для того что найти самые дальние клетки грязи которые возможны
    if maximum:
        start_border = speed

    list_real_cords = []
    for inner_speed in range(start_border, speed + 1):
        step_vision = find_object(inp_vision, input_radius=input_radius,
                                  speed=inner_speed)  # объекты на которые кролик может прийти с шагом inner_speed
        cord_step_vision = find_target_cord(step_vision, dirt_id)  # кординаты на настояшей карте.
        for cord in cord_step_vision:
            appended_cord = tuple(inp_cordinates[cord])
            list_real_cords.append(appended_cord)

    if len(list_real_cords) == 0 and maximum:  # если на максимальном шаге клеток грязи не найдено, то ищем клетки грязи на speed-1
        return find_all_dirt_speed(inp_vision, inp_cordinates, speed - 1, dirt_id, input_radius, maximum=True)

    list_real_cords = validate_dirt_cords(list_real_cords, input_radius)        # ?>>>>>>>

    return list_real_cords


# %%time - jupyter stuff

def update_cord_rabit(inp_rabits, inp_rabits_cords, cords, key, target_point=(), can_remove=[], remove=False,exceptions=[]):
    """
    Сравнивает
    :param inp_rabits: --> все кролики
    :param inp_rabits_cords: --> все координаты кролликов
    :param cords: --> фактически , где находится кроллик   --> isn't used!
    :param key: --> айдишник кроллика
    :param target_point:   при спаривании
    :param can_remove:   при спаривании
    :param remove:   при спаривании
    :param exceptions:   при спаривании
    :return:
    """
    def redact_rabits_cords(inp_rabits_cords):
        if cords not in inp_rabits_cords:
            inp_rabits_cords[cords] = {key: inp_rabits[key]['attraction']}
        else:
            inp_rabits_cords[cords][key] = inp_rabits[key]['attraction']

        return inp_rabits_cords

    def merge_keys(can_remove, cord_dict):
        output = []
        for key in cord_dict:
            if key in can_remove:
                output.append(key)

        return output

    before_step_cord = inp_rabits[key]['coord_x'], inp_rabits[key]['coord_z']
    # координата где мы находимся
    work_rabit = inp_rabits_cords[before_step_cord] #

    if not remove:
        if len(work_rabit) == 1:
            inp_rabits_cords.pop(before_step_cord)
            inp_rabits_cords = redact_rabits_cords(inp_rabits_cords)
        else:
            inp_rabits_cords[before_step_cord].pop(key)
            inp_rabits_cords = redact_rabits_cords(inp_rabits_cords)

        return inp_rabits_cords, []

    else:       # isn't used ( it is for pairing )
        parthert_keys = merge_keys(can_remove, list(inp_rabits_cords[target_point].keys()))  # находим
        # print(parthert_keys)
        random_parther = np.random.choice(parthert_keys)
        parther_rabit = inp_rabits_cords[target_point]

        # print(parthert_keys, random_parther, parther_rabit)
        delit_key = [key, random_parther]

        if len(work_rabit) == 1:
            inp_rabits_cords.pop(before_step_cord)
        else:
            inp_rabits_cords[before_step_cord].pop(key)

        if len(parther_rabit) == 1:
            inp_rabits_cords.pop(target_point)
        else:
            inp_rabits_cords[target_point].pop(random_parther)

        return inp_rabits_cords, delit_key


# rabits_cords, delit_key_get = update_cord_rabit(rabits, rabits_cords, cords, 2, target_point=point, can_remove=can_redact, remove=True)
# rabits_cords, delit_key

rabits, list_of_cords = generate_rabbits(200)

paring = []
hospital = {}

dirt_id = list(range(8, 20)) + [0]
grass_id = list(range(60, 80))
water_id = [20]
delit_key = []

heal_time_seconds = 30
damage_time_seconds = 20
attraction_time_seconds = 2

grass_heal_per_tick = 30
damage_per_tick = 1
attraction_per_tick = 3

start = time.time()
start_damage = start
start_growth = start
start_attraction = start

iters = 0
restart_timer = False

drop_keys = []
delit_key = []
rabits_cords = {}
state_paring = False


def find_de_way(vision, cordinates, input_radius, speed, dirt_id=list(), elemnt_to_find=list(), is_dirt=False):
    # Вернет кординату куда походить и нашел ли он находимую корданиту(True/False)
    """

    :param vision:  матрица вижина
    :param cordinates: матрица такого же как вижин
    :param input_radius: vision_radius -->
    :param speed: фактическая скорость e.g (5)
    :param dirt_id: список айдишников всей земли
    :param elemnt_to_find: тот элемент, что нам нужно найти ( ДЛЯ ЛОБОГО ОБЬЕКТА)  ( если кролик отображается в vision )
    :param is_dirt: ход пойдёт на рандомную землю (state 0)
    :return:
    (
    1 param - точку в которую он походит
    2 param - нашёл ли он элемент, который надо было найти( подошёл ли он в плотную к нему )
    3 param - элемент, к которому он подошёл, его координаты

    """
    def find_real_cords(input_points=[], input_cordinates=list()):
        output = []

        for cord in input_points:
            output.append(tuple(input_cordinates[cord]))

        return output

    def get_random_point(list_of_cords, radius=0):

        length = len(list_of_cords)
        random_index = np.random.randint(length)
        return_cord = list_of_cords[random_index]
        return return_cord

    def merge_dirt_points(all_dirt, dirt_near_point):
        # all_dirt, dirt_near_point - все точки земли и самые ближайшие
        """Нашёл точку в которую хочет походить -> и на в"""
        can_to_move = []
        for cord in dirt_near_point:
            if cord in all_dirt:
                can_to_move.append(cord)

        return can_to_move

    all_dirt_cels = find_all_dirt_speed(vision, cordinates, speed, dirt_id, input_radius) # получаем список всех координат
    # print('all', all_dirt_cels, end=' ')
    if not is_dirt:
        maximum_dirt_cels = find_all_dirt_speed(vision, cordinates, speed, dirt_id, input_radius, maximum=True)
        # print('MAX',maximum_dirt_cels, end=' ')

    if is_dirt:
        return get_random_point(all_dirt_cels)

    for inner_speed in range(0, speed + 2):

        step_vision = find_object(vision, input_radius=input_radius, speed=inner_speed)
        cord_step_vision = find_target_cord(step_vision, elemnt_to_find)
        element_real_cords = find_real_cords(input_points=cord_step_vision, input_cordinates=cordinates)

        if len(element_real_cords) > 0:
            random_point = get_random_point(element_real_cords, input_radius)  # выбираем рандомный искомый элемент

            elemnt_x, elemnt_z = random_point

            vision_elemnt, cordinates_elemnt, radius_elemnt = vision_obl(elemnt_x, elemnt_z, radius=1)
            elemnt_step_vision = find_object(vision_elemnt, input_radius=radius_elemnt,
                                             speed=1)  # расчиьываем облость видимости от элемента
            elemnt_cord_step_vision = find_target_cord(elemnt_step_vision, dirt_id)  # ищем землю вокруг этого элемента
            dirt_near_elemnt = find_real_cords(input_points=elemnt_cord_step_vision,
                                               input_cordinates=cordinates_elemnt)  # переводим кординаты земли на реальной карте
            possible_to_move = merge_dirt_points(all_dirt_cels,
                                                 dirt_near_elemnt)  # находим общие точки между всеми точками куда мы можем походить и точками земли выбраного элемента

        # фактически ищем ближайшую точку травы на карте
            if len(possible_to_move) != 0:
                return get_random_point(
                    possible_to_move), True, random_point  # выбираем рандомную точку земли, после соеденения
            else:
                get_random_point(
                    maximum_dirt_cels), False, ()  # выбираем рандомную точку земли если при соеденение не было найдено ни одной общей точки.
    return get_random_point(maximum_dirt_cels), False, ()   #

"""TESTING FOR DAMN PAIRING!"""
# def search_rabbit_vision(vision_inp, inp_cordinates, rabits_cords, rabit_cord, input_rabit_key):
#     to_cordinates = []
#     vision_key = []
#
#     work_rabit_cord = rabit_cord
#     atraction1 = rabits_cords[work_rabit_cord][input_rabit_key]
#     for first in range(len(inp_cordinates)):
#         for second in range(len(inp_cordinates)):
#
#             work_cord = tuple(inp_cordinates[first][second])
#             if work_cord in rabits_cords.keys():
#                 atraction_calc = rabits_cords[work_cord]
#
#                 for key in atraction_calc:
#                     if key != input_rabit_key:
#                         atraction2 = rabits_cords[work_cord][key]
#                         if abs(atraction1 - atraction2) < 50:
#                             to_cordinates.append((first, second))
#                             vision_key.append(key)
#     vision_edit = vision_inp.copy()
#     for cord in to_cordinates:
#         vision_edit[cord] = 1000
#
#     return vision_edit, vision_key


def make_rabits_cords(rabits, exception=[]):
    """

    :param rabits: словарь кроликов         ( generate rabbits )
    :param exception: ключи, которые не добавляем сюда
    :return: словарь {координаты: список словарей id кролика
    """
    rabits_cords_calc = {}
    for key in rabits:
        if key not in exception:
            rabbit_cord = rabits[key]['coord_x'], rabits[key]['coord_z']
            if rabbit_cord not in rabits_cords_calc:
                rabits_cords_calc[rabbit_cord] = {key: rabits[key]['attraction']}
            else:
                rabits_cords_calc[rabbit_cord][key] = rabits[key]['attraction']
    return rabits_cords_calc


# fuck_тически запускаем тут мир!
while wait(start, 0.02) and len(rabits) != 0:

    start = time.time()

    rabits_cords = make_rabits_cords(rabits, exception=delit_key)
    # print(rabits_cords)
    for key in rabits:

        if len(rabits) == 0:
            break

        if rabits[key]['health'] <= 0:  # убираем кролика в больницу
            hospital[key] = rabits[key]
            rabits[key]['move_status'] = 4

        if len(rabits) == 0:
            break

        if key not in delit_key:  # проверяем что кролики не находятся в спаривании.

            rabbit_state = rabits[key]['state']
            coord_x, coord_z = rabits[key]['coord_x'], rabits[key]['coord_z']
            vision_radius = rabits[key]['vision_radius']
            speed = rabits[key]['speed']
            health = rabits[key]['health']
            saturation = rabits[key]['saturation']
            hydration = rabits[key]['hydration']

            vision, cordinates, radius = vision_obl(coord_x, coord_z, radius=vision_radius)

            if rabbit_state == 0:  # random move
                coord_x, coord_z = find_de_way(vision, cordinates, radius, speed, dirt_id=dirt_id)[0]  # ________
                cords = coord_x, coord_z

            # elif rabbit_state == 4 and key not in delit_key:  # PARTNER_SEARCH
            #     # print(key)
            #     # print((coord_x, coord_z))
            #     vision_with_rabits, can_redact = search_rabbit_vision(vision, cordinates, rabits_cords,
            #                                                           (coord_x, coord_z), key)
            #     # print(vision_with_rabits)
            #     cords, state_paring, point = find_de_way(vision_with_rabits, cordinates, radius, speed=1,
            #                                              elemnt_to_find=[1000], dirt_id=dirt_id)

                # print('PARTNER_SEARCH', cords, state_paring, point, end=' ')

            elif rabbit_state == 3:  # EAT_SEARCH
                cords, state, point = find_de_way(vision, cordinates, radius, speed, elemnt_to_find=grass_id,
                                                  dirt_id=dirt_id)  # ________
                if state:
                    rabits[key]['state'] = 6  # ставим статуc, чтобы кролик поел.
                coord_x, coord_z = cords  # распаковываем кординаты для записи.
                rabits[key]['target_point'] = point
                # print('EAT_SEARCH', cords, state, point)

            elif rabbit_state == 2:  # WATER_SEARCH
                cords, state, point = find_de_way(vision, cordinates, radius, speed, elemnt_to_find=water_id,
                                                  dirt_id=dirt_id)  # ________
                if state:
                    rabits[key]['state'] = 5  # ставим статуc, чтобы кролик попил.

                coord_x, coord_z = cords  # распаковываем кординаты для записи.
                # print('WATER_SEARCH', cords, state, point)

            if rabbit_state == 6:  # EATING
                index_grass_element = find_grass_by_coord(
                    rabits[key]['target_point'])  # получаем индекс травы в grass_cords по кординате на карте
                grass_health = grass_cords[index_grass_element][1]  # запоминаем здоровье травы
                need_to_fill = rabits[key]['max_saturation'] - rabits[key][
                    'saturation']  # посттили сколько надо заполнить до max_saturation

                can_to_fill = grass_health - need_to_fill
                if can_to_fill < 0:
                    need_to_fill = grass_health
                    grass_health = 0
                else:
                    grass_health -= need_to_fill

                grass_cords[index_grass_element][1] = grass_health  # обновление здоровья травы

                rabits[key]['saturation'] += need_to_fill
                rabits[key]['state'] = 0
                rabits[key]['action_log'].append('EATING')

            if rabbit_state == 5:  # DRINKING
                rabits[key]['hydration'] = rabits[key]['max_hydration']
                rabits[key]['state'] = 0
                rabits[key]['action_log'].append('DRINKING')
            #
            # if state_paring:
            #     # print('\ncordinates', rabits_cords, end=' ')
            #
            #     rabits_cords, delit_key_get = update_cord_rabit(rabits, rabits_cords, cords, key, target_point=point,
            #                                                     can_remove=can_redact, remove=True)
            #
            #     key1, key2 = delit_key_get
            #     print(delit_key_get)
            #     if rabits[key1]['action_log'].count('REPRODUCTION') == 0 and rabits[key2]['action_log'].count(
            #             'REPRODUCTION') == 0:
            #         rabits[key1]['action_log'].append('REPRODUCTION')
            #         rabits[key2]['action_log'].append('REPRODUCTION')
            #
            #         rabits[key1]['state'] = 7
            #         rabits[key1]['state'] = 7
            #
            #         paring.append([{key1: rabits[key1]}, {key2: rabits[key2]}])
            #
            #     for key in delit_key_get:
            #         delit_key.append(key)

            # else:

# {
#     (1,2): 120
# }
            rabits_cords, delit_key_get = update_cord_rabit(rabits, rabits_cords, cords, key, remove=False)

            coord_x, coord_z = cords
            log_cords = float_cords(coord_x, coord_z)
            rabits[key]['coord_x'], rabits[key]['coord_z'] = coord_x, coord_z
            rabits[key]['move_log'].append(log_cords)
            rabits[key]['move_log'] = rabits[key]['move_log'][-50:]

            end = time.time()

        if saturation <= 0 or hydration <= 0:
            rabits[key]['health'] -= 1

        if rabits[key]['state'] not in [5, 6, 7, 4]:  # меняем стейты на поиск еды или воды
            if rabits[key]['saturation'] <= 50:
                rabits[key]['state'] = 3
            elif rabits[key]['hydration'] <= 50:
                rabits[key]['state'] = 2

        # if rabits[key]['attraction'] >= 80 and rabits[key]['state'] != 7:  # меняем стейт на поиск партнера
        #     rabits[key]['state'] = 4

        if rabits[key]['health'] < 0:  # зануление здоровья
            rabits[key]['health'] = 0
        # if iters%1 == 0:
        #     print(iters)
        # iters += 1
    # _________________________________________________________________________________________________________________________________
    # ________________Выход из озновного цикла и начало удаления ключей, нанесения урона, увелечение всех параметров завязаных на времени_____________

    for key in delit_key:  # удаляем кролей из списка всех кроликов после спаривания.
        print('del', key)
        rabits.pop(key)
    # print('_______________________')
    delit_key = []

    drop_keys = []
    for key in rabits:
        if rabits[key]['health'] <= 0:
            drop_keys.append(key)

    for key in drop_keys:  # удаляем ключи где health меньши или равен 0
        rabits.pop(key)

    # ___________TIME SECTION______________
    # THIS IS GRASS GROWTH
    if end - start_growth >= heal_time_seconds:  # хилим траву каждые heal_time_seconds
        grass_cords = heal_grass(grass_cords, grass_heal_per_tick)  # хилим на grass_heal_per_time
        start_growth = time.time()

    # THIS IS DAMAGE
    if end - start_damage >= damage_time_seconds:  # наносим урон рандомнуму параметру
        for key in rabits:
            if rabits[key]['state'] not in [7,
                                            4]:  # чтобы при задаче по поиску партнера, не дамажить параметры кролика.
                all_params = ['saturation', 'health', 'hydration']
                random_params = []
                for param in all_params:
                    if rabits[key][param] > 0:
                        random_params.append(param)

                rabits[key][choose_random_parametr(random_params)] -= damage_per_tick
                # print(rabits[key]['health'], rabits[key]['saturation'], rabits[key]['hydration'])
        start_damage = time.time()

    # THIS IS attraction
    if end - start_attraction >= attraction_time_seconds:
        for key in rabits:
            if rabits[key]['attraction'] < 100:
                rabits[key]['attraction'] += attraction_per_tick

        start_attraction = time.time()
    print(rabits[0])
    #print(len(hospital), len(rabits), len(paring), sep='\n')
    # if iters%100 == 0:
    #     print(iters)
    # iters += 1

    # print(time.time() - start)
