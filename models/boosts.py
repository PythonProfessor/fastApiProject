import sqlalchemy

metadata = sqlalchemy.MetaData()

boost_table = sqlalchemy.Table(
    'boost',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("boost_name", sqlalchemy.String()),
    sqlalchemy.Column("running", sqlalchemy.Boolean),
    sqlalchemy.Column("pet_id", sqlalchemy.ForeignKey('entity.id', ondelete="DO NOTHING")),
)
