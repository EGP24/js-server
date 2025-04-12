import sqlalchemy as sa

metadata = sa.MetaData()


users_table = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.BIGINT, primary_key=True),
    sa.Column('name', sa.VARCHAR, nullable=False),
    sa.Column('about', sa.TEXT, nullable=False),
    sa.Column('avatar', sa.VARCHAR, nullable=True),
    sa.Column('cohort', sa.VARCHAR, nullable=False),
    sa.Column('token', sa.VARCHAR, nullable=False),
    sa.Column('is_active', sa.BOOLEAN, nullable=False),
)

cards_table = sa.Table(
    'cards',
    metadata,
    sa.Column('id', sa.BIGINT, primary_key=True),
    sa.Column('name', sa.VARCHAR, nullable=False),
    sa.Column('cohort', sa.VARCHAR, nullable=False),
    sa.Column('link', sa.VARCHAR, nullable=False),
    sa.Column('owner_id', sa.BIGINT, nullable=False),
    sa.Column('is_active', sa.BOOLEAN, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
)

likes_table = sa.Table(
    'likes',
    metadata,
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('card_id', sa.BIGINT, nullable=False),
    sa.Column('is_active', sa.BOOLEAN, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True)),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True)),
)
