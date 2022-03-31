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
from main import database
from models.wallets import wallet_table


class Wallet:

    def __init__(self, soft_1, soft_2, pop_up_timestamp, owner_id):
        self.soft_1 = soft_1
        self.soft_2 = soft_2
        self.pop_up_timestamp = pop_up_timestamp
        self.owner_id = owner_id

    @classmethod
    async def create_wallet(cls, owner_id):
        # owner_id --> user_id from users table
        q = wallet_table.insert().values(
            **cls(soft_1=10, soft_2=10, pop_up_timestamp=time.time(), owner_id=owner_id).__dict__
        )
        await database.fetch_one(q)

