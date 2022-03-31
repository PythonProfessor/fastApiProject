import time

from main import database
from models.create_script import token_table

"""
Этот модуль используется фактически для CRUD операций над базой данных используя модель юзеров и токенов 
"""


class Token:

    def __init__(self, hard_token, soft_token, user_id, created):
        self.hard_token = hard_token
        self.soft_token = soft_token
        self.user_id = user_id
        self.created = created


    @classmethod
    async def get_tokens(cls, user_id: int):
        """
        The function literally gets all hard and soft tokens according to user_id
        :param user_id: int user_id
        :return: {"hard_token": "hard??1648646636.7908003", "soft_token": "soft??1648646636.7908092"}
        """
        q = token_table.select().where(token_table.c.user_id == user_id)
        tokens = dict(await database.fetch_one(q))
        token_dict = {"hard_token": tokens["hard_token"],
                      "soft_token": tokens["soft_token"]}
        return token_dict

    @classmethod
    def gen_hard_token(cls):
        return f'hard??{time.time()}'

    @classmethod
    def gen_soft_token(cls):
        return f'soft??{time.time()}'
