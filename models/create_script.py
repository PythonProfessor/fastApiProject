import datetime
import sqlalchemy

# metadata = sqlalchemy.MetaData()


import datetime
from sqlalchemy import types as types
import sqlalchemy

metadata = sqlalchemy.MetaData()

pet_type_choices = {
    "rabbit": "rabbit",
    "fox": "fox",
    "bear": "bear"}

state_choices = {
    "DO_NOTHING": 0,
    "RUNNING_AWAY": 1,
    "WATER_SEARCH": 2,
    "EAT_SEARCH": 3,
    "PARTNER_SEARCH": 4,
    "DRINKING": 5,
    "EATING": 6,
    "REPRODUCTION": 7,
    "MOVING_TO_TARGET": 8}

move_status_choises = {
    "in_pocket": 0,
    "on_island": 1,
    "in_wait_trow_to_island": 2,
    "in_wait_pick_up_from_island": 3,
    "in_hospital": 4,
    "wait_auction": 5
}


class ChoiceType(types.TypeDecorator):  # add ABC
    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


entity_table = sqlalchemy.Table(
    'entity',
    metadata,

    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("coord_x", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("coord_z", sqlalchemy.Float, nullable=True),

    sqlalchemy.Column("health", sqlalchemy.Float, default=100),
    sqlalchemy.Column("saturation", sqlalchemy.Float, default=100),
    sqlalchemy.Column("hydration", sqlalchemy.Float, default=100),
    sqlalchemy.Column("speed", sqlalchemy.Float, default=5),
    sqlalchemy.Column("vision_radius", sqlalchemy.Float, default=5),
    sqlalchemy.Column("hearing_radius", sqlalchemy.Float, default=10),
    sqlalchemy.Column("prettiness", sqlalchemy.Float, default=70),
    sqlalchemy.Column("attraction", sqlalchemy.Float, default=70),
    sqlalchemy.Column("stealth", sqlalchemy.Integer, default=20),

    sqlalchemy.Column("max_health", sqlalchemy.Integer, default=100),
    sqlalchemy.Column("max_saturation", sqlalchemy.Integer, default=100),
    sqlalchemy.Column("max_hydration", sqlalchemy.Integer, default=100),
    sqlalchemy.Column("level", sqlalchemy.Integer, default=1),

    sqlalchemy.Column('state', sqlalchemy.Integer, default=state_choices['DO_NOTHING']),
    sqlalchemy.Column('move_status', sqlalchemy.Integer, default=move_status_choises['in_pocket']),
    sqlalchemy.Column('pet_type', sqlalchemy.String, default='rabbit'),

    sqlalchemy.Column('race', sqlalchemy.JSON, default=[{"race": "forest", "value": 100}]),
    sqlalchemy.Column('name', sqlalchemy.String, default='It\'s a cat'),
    sqlalchemy.Column('skin', sqlalchemy.JSON, default={'skin': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}),
    sqlalchemy.Column('data', sqlalchemy.String, default='It`s a cat'),
    sqlalchemy.Column('move_log', sqlalchemy.JSON, default={'log': []}),
    sqlalchemy.Column('change_move_status_timestamp', sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column('generation', sqlalchemy.Integer, nullable=True, default=1),

    sqlalchemy.Column('owner_id', sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('world_id', sqlalchemy.ForeignKey('game_world.id'), nullable=True),

)

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
    sqlalchemy.Column("selected_island", sqlalchemy.ForeignKey("game_world.id" , ondelete="RESTRICT"))
    # world_id, chosen_world relations
)
"""
ondelete¶ – Optional string. If
set, emit ON DELETE <value> when issuing DDL for this constraint. 
Typical values include CASCADE, DELETE and RESTRICT.
"""

wallet_table = sqlalchemy.Table(
    "wallet",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("soft_1", sqlalchemy.Float, default=10),
    sqlalchemy.Column("soft_2", sqlalchemy.Float, default=10),
    sqlalchemy.Column("pop_up_timestamp", sqlalchemy.Integer),
    sqlalchemy.Column("owner_id", sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"))
)

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

token_table = sqlalchemy.Table(
    'token',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("hard_token", sqlalchemy.String()),
    sqlalchemy.Column("soft_token", sqlalchemy.String()),
    sqlalchemy.Column('created', sqlalchemy.Integer),  # везде где ток можно, нужно делать таймстэмп
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id', ondelete="CASCADE"))
)

# here has to be imported all databases world_table --> td tp
