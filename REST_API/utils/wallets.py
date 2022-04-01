import time

import sqlalchemy

# from models.create_script import metadata
#
# wallet_table = sqlalchemy.Table(
#     "wallet",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("soft_1", sqlalchemy.Float, default=10),
#     sqlalchemy.Column("soft_2", sqlalchemy.Float, default=10),
#     sqlalchemy.Column("pop_up_timestamp", sqlalchemy.DateTime()),
#     sqlalchemy.Column("owner_id", sqlalchemy.ForeignKey("users.id"))
# )
from REST_API.utils.users import User
from main import database
from models.wallets import wallet_table
from models.users import users_table


class Wallet:

    def __init__(self, soft_1, soft_2, pop_up_timestamp, owner_id):     # initializing a wallet table
        self.soft_1 = soft_1
        self.soft_2 = soft_2
        self.pop_up_timestamp = pop_up_timestamp
        self.owner_id = owner_id

    @staticmethod
    async def check_balance_to_update_level(money_to_pay, hard_token):
        """The function updates column soft1 in the database literally withdraw money from wallet"""
        user_id = dict(await User.get_user_by_token(hard_token=hard_token))['id']       # get the user by token
        print("User id: ", user_id)
        q = wallet_table.select().where(wallet_table.c.owner_id == user_id)     # get the wallet by user id
        wallet = dict(await database.fetch_one(q))       # getting a wallet in dict representation
        print(f"Wallet: {wallet}")
        soft1 = wallet['soft_1']
        if soft1 - money_to_pay < 0:
            return False
        else:
            q = wallet_table.update().where(wallet_table.c.owner_id == user_id).values(soft_1=soft1-money_to_pay)      # updating values of a level
            await database.fetch_one(q)

    @classmethod
    async def create_wallet(cls, owner_id):
        """The function creates a wallet object and saves data into db"""
        # owner_id --> user_id from users table
        q = wallet_table.insert().values(
            **cls(soft_1=10, soft_2=10, pop_up_timestamp=time.time(), owner_id=owner_id).__dict__
        )
        await database.fetch_one(q)

