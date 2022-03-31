import datetime
import sqlalchemy

metadata = sqlalchemy.MetaData()

world_table = sqlalchemy.Table(
    "game_world",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("world_name", sqlalchemy.String()),
    sqlalchemy.Column("running", sqlalchemy.Boolean()),
    sqlalchemy.Column("visible", sqlalchemy.Boolean()),
    sqlalchemy.Column("world_map", sqlalchemy.JSON()),
    sqlalchemy.Column("grass_map", sqlalchemy.JSON())
)
