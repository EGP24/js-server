from sqlalchemy.dialects.postgresql import insert
import sqlalchemy as sa

from src.entities.like import InsertLike, Like
from src.entities.user import User
from src.helpers.pg import add_created_and_updated_value
from src.mappers.likes import insert_likes_mapper, likes_mapper
from src.mappers.users import users_mapper
from src.repositories.postgres.base import db_client
from src.repositories.postgres.tables import likes_table, users_table


async def upsert_like(like: InsertLike) -> Like:
    values = insert_likes_mapper.map_to(like)
    query = (
        insert(likes_table)
        .values(**values)
        .on_conflict_do_update(
            index_elements=['user_id', 'card_id'],
            set_=values,
        )
        .returning(likes_table)
    )
    with add_created_and_updated_value(query) as query:
        row = await db_client.fetchrow(query)
    return likes_mapper.map_from(row)


async def get_likes_users(*, card_id: int, cohort: str) -> list[User]:
    user_fields = [users_table.columns[field_name] for field_name in users_table.columns.keys()]
    query = (
        sa.select(*user_fields)
        .select_from(
            users_table.join(
                likes_table,
                sa.and_(
                    likes_table.c.user_id == users_table.c.id,
                    likes_table.c.card_id == card_id,
                ),
            ),
        )
        .where(
            users_table.c.is_active == sa.true(),
            likes_table.c.is_active == sa.true(),
            users_table.c.cohort == cohort,
        )
    )

    rows = await db_client.fetch(query)
    return [users_mapper.map_from(row) for row in rows] if rows else []