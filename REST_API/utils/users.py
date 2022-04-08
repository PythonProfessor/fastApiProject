import hashlib
import random
import string
import time
from datetime import datetime, timedelta
from sqlalchemy import and_

from REST_API.utils.tokens import Token
from main import database
from models.tokens import token_table
from models.users import users_table

"""
Этот модуль используется фактически для CRUD операций над базой данных используя модель юзеров и токенов 
"""


def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


class User:
    """
    The class is used to proceed with operations on user into the database
    """

    @staticmethod
    async def get_user_by_email(email: str):
        """ Возвращает информацию о пользователе """
        query = users_table.select().where(users_table.c.email == email)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_username(username: str):
        """ Возвращает информацию о пользователе по юзернейму """
        query = users_table.select().where(users_table.c.username == username)
        # print(query.username)
        return await database.fetch_one(query)

    @staticmethod
    async def select_island(hard_token: str, island_id):
        # table.update().where(table.c.id==7).values(name='foo')
        user = await User.get_user_by_token(hard_token=hard_token)
        print(dict(user))
        q = users_table.update().where(users_table.c.id == user['id']).values(selected_island=island_id)
        await database.fetch_one(q)

    @staticmethod
    async def get_user_by_token(hard_token: str):
        """ Возвращает информацию о владельце указанного токена """
        token_query = token_table.select().where(  # token_table.join(users_table).select().where()
            token_table.c.hard_token == hard_token,  # тут надо уточнить хард или софт ..
            # token_table.c.expires > datetime.now()        > time.time()
        )
        user_id = dict(await database.fetch_one(token_query))['user_id']  # making dict
        user_query = users_table.select().where(
            users_table.c.id == user_id
        )
        return dict(await database.fetch_one(user_query))
        # print(dict(query))
        # return await database.fetch_one(query)

    @staticmethod
    async def create_user_token(user_id: int):
        """ Создает токен для пользователя с указанным user_id  """
        query = (
            token_table.insert()
                .values(**Token(hard_token=Token.gen_hard_token(), soft_token=Token.gen_soft_token(),
                                user_id=user_id, created=time.time()).__dict__)
                .returning(token_table.c.hard_token, token_table.c.soft_token)  # оно возвращает те поля шо мы указали
        )
        # print(await database.fetch_one(query))
        return await database.fetch_one(query)

