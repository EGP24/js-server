import sqlalchemy as sa

from src.entities.user import User
from src.mappers.users import users_mapper
from src.repositories.postgres.base import db_client
from src.repositories.postgres.tables import users_table


async def update_user_info(
    *,
    user_id: int,
    about: str | None,
    name: str | None,
    avatar: str | None,
) -> User | None:
    assert about or name or avatar, 'about or name or avatar must be provided'

    query = (
        sa.update(users_table)
        .where(users_table.c.id == user_id, users_table.c.is_active == sa.true())
        .returning(users_table)
    )
    if about:
        query = query.values(about=about)
    if name:
        query = query.values(name=name)
    if avatar:
        query = query.values(avatar=avatar)

    row = await db_client.fetchrow(query)
    return users_mapper.map_from(row) if row else None


async def get_user_by_token_and_cohort(*, token: str, cohort: str) -> User | None:
    query = sa.select(users_table).where(
        users_table.c.token == token,
        users_table.c.cohort == cohort,
        users_table.c.is_active == sa.true(),
    )
    row = await db_client.fetchrow(query)
    return users_mapper.map_from(row) if row else None
