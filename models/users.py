import datetime
from models.worlds import world_table
import sqlalchemy

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(40), unique=True, index=True, nullable=True),
    sqlalchemy.Column("username", sqlalchemy.String(40), unique=True, index=True, nullable=False),
    sqlalchemy.Column("hashed_password", sqlalchemy.String()),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean(), default=True, nullable=False),
    sqlalchemy.Column("is_staff", sqlalchemy.Boolean(), default=False),
    sqlalchemy.Column("date_joined", sqlalchemy.DateTime(), default=datetime.datetime.utcnow()),
    sqlalchemy.Column("avatar", sqlalchemy.String(), default="path_to_png", nullable=True),
    sqlalchemy.Column("settings", sqlalchemy.JSON(), default={"language": "English"}),
    sqlalchemy.Column("selected_island", sqlalchemy.ForeignKey("game_world.id"))
    # world_id, chosen_world relations
)




# here has to be imported all databases world_table --> td tp