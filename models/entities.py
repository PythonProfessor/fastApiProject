import datetime
from abc import ABC

from sqlalchemy import types as types

from models import worlds
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

    sqlalchemy.Column('race', sqlalchemy.JSON, default= [{"race": "forest","value": 100}]),
    sqlalchemy.Column('name', sqlalchemy.String, default='It\'s a cat'),
    sqlalchemy.Column('skin', sqlalchemy.JSON, default={'skin': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}),
    sqlalchemy.Column('data', sqlalchemy.String, default='It`s a cat'),
    sqlalchemy.Column('move_log', sqlalchemy.JSON, default={'log': []}),
    sqlalchemy.Column('change_move_status_timestamp', sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column('generation', sqlalchemy.Integer, nullable=True, default=1),


    sqlalchemy.Column('owner_id', sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('world_id', sqlalchemy.ForeignKey('game_world.id'), nullable=True),

)
