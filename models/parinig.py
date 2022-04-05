import sqlalchemy

metadata = sqlalchemy.MetaData()

pairing_table = sqlalchemy.Table(
    'pairing',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("start_time", sqlalchemy.Integer),
    sqlalchemy.Column("finish_time", sqlalchemy.Integer),
    sqlalchemy.Column('pet_type', sqlalchemy.String()),
    sqlalchemy.Column('pet_id_1', sqlalchemy.ForeignKey('entity.id', ondelete='DELETE')),
    sqlalchemy.Column('pet_id_2', sqlalchemy.ForeignKey('entity.id', ondelete='DELETE')),
    sqlalchemy.Column('child_data', sqlalchemy.JSON),
)

