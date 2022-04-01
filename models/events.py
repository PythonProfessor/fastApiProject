import sqlalchemy

metadata = sqlalchemy.MetaData()

event_table = sqlalchemy.Table(
    'event',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("type", sqlalchemy.String()),
    sqlalchemy.Column("timestamp", sqlalchemy.Integer),
    sqlalchemy.Column('title', sqlalchemy.String()),
    sqlalchemy.Column('text', sqlalchemy.String()),
    sqlalchemy.Column('for_pet_type', sqlalchemy.String()),
    sqlalchemy.Column('for_pet_id', sqlalchemy.Integer),
    sqlalchemy.Column('sent', sqlalchemy.Boolean),
    sqlalchemy.Column('data', sqlalchemy.JSON),
    sqlalchemy.Column('owner_id', sqlalchemy.ForeignKey('users.id', ondelete="CASCADE"))

)
