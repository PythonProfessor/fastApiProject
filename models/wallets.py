import datetime
import sqlalchemy

metadata = sqlalchemy.MetaData()

wallet_table = sqlalchemy.Table(
    "wallet",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("soft_1", sqlalchemy.Float, default=10),
    sqlalchemy.Column("soft_2", sqlalchemy.Float, default=10),
    sqlalchemy.Column("pop_up_timestamp", sqlalchemy.Integer),
    sqlalchemy.Column("owner_id", sqlalchemy.ForeignKey("users.id"))
)
