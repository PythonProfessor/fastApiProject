from sqlalchemy import and_

from REST_API.utils.entities import Entity
from REST_API.utils.wallets import Wallet
from main import database
from models.users import users_table
from REST_API.schemas.users import UserCreate, UserLogin, UserSelectIsland
from REST_API.utils.users import get_random_string, hash_password, User, validate_password
from REST_API.utils.tokens import Token

"""
Этот модуль отвечает за логи  которая принимает Web-запрос и возвращает Web-ответы + взаимодействует с БД, игровым миром
"""


async def create_user(user: UserCreate):
    """ Создает нового пользователя в БД  UserCreate используется для ввода данных, тоесть фактически
    Fast Api юзает pydantic models для взаимодействия!"""
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    query = users_table.insert().values(
        username=user.username, hashed_password=f"{salt}${hashed_password}",
        is_active=True, is_staff=False)
    user_id = await database.execute(query)     # getting the specific user
    tokens = await User.create_user_token(user_id)      # creating tokens for specific user
    await Wallet.create_wallet(owner_id=user_id)       # creating a wallet for specific user
    token_dict = {"hard_token": tokens["hard_token"], "soft_token": tokens["soft_token"]}
    await Entity.generate_test_pets(user_id)
    response = {**user.dict(), "id": user_id, "is_active": True}
    response.update(token_dict)
    return response


async def select_island(model: UserSelectIsland):
    await User.select_island(hard_token=model.hard_token, island_id=model.island_id)
    return {"success":True}

async def login(user:UserLogin):
    """
    Значит кароче, шо я понял
    Прикол pydantic sql orm заключается с адекватной настройкой его взаимдоействия
    Суть такая, мы настраиваем тут модель, которая будет отображаться на вход ( при приёме аргументов ) вот она :

    user:UserLogin  --> schemas file

    дальше используя sql синтаксис и взаимодействуя конкретно с ОРМ мы получаем Record object -->

    q = users_table.select().where(users_table.c.username == user.username) # sql statement
    usr = await database.fetch_one(q) получаем обьект данных  что может быть конвертирован потом в словарь, для доступа к элементам  ecord object at 0x7f00c37fa360
    print(dict(**usr))   конвертируем этот словарь в такой вид:

    {'id': 5, 'email': None, 'username': 'yehor', 'hashed_password': '1c0fbe9e50fafeca703ab4a65e0028e21db8ca',
     'is_active': True, 'is_staff': False, 'date_joined': None, 'avatar': None, 'settings': None, 'selected_island': None}

    таким образом описывая модели в pydantic мы можем очень гибко управлять телом запросов и телом ответов,
    получать данные и сериализировать их, выбирать как надо, далее для получения конкретного поля просто обращаемся по ключу
    и в целом можем получать переменные туды
    :return:
    """
    q = await User.get_user_by_username(username=user.username)
    db_user = dict(q)
    tokens = await Token.get_tokens(db_user['id'])      # getting tokens
    db_user.update(tokens)
    if not validate_password(user.password, db_user['hashed_password']):        # checking hashed password
        return {"Incorrect password": False}
    return db_user

#update settings