import sqlalchemy

metadata = sqlalchemy.MetaData()

token_table = sqlalchemy.Table(
    'token',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("hard_token", sqlalchemy.String()),
    sqlalchemy.Column("soft_token", sqlalchemy.String()),
    sqlalchemy.Column('created', sqlalchemy.Integer),  # везде где ток можно, нужно делать таймстэмп
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'))
)
