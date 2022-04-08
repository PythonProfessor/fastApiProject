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


pairing_bid_table = sqlalchemy.Table(
    'pairing_bid',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("bid_time", sqlalchemy.Integer),
    sqlalchemy.Column('bid_count', sqlalchemy.Integer),
    sqlalchemy.Column('owner_id', sqlalchemy.ForeignKey('entity.id', ondelete='DELETE')),
    sqlalchemy.Column('pairing', sqlalchemy.ForeignKey('pairing.id', ondelete='DELETE')),
)
