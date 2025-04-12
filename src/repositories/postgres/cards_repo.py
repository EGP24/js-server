import sqlalchemy as sa

from src.entities.card import Card, InsertCard
from src.entities.user import User
from src.helpers.pg import add_created_and_updated_value, add_updated_value, filter_dict
from src.mappers.cards import cards_mapper, insert_cards_mapper
from src.mappers.users import users_mapper
from src.repositories.postgres.base import db_client
from src.repositories.postgres.tables import cards_table, users_table


async def insert_card(card: InsertCard) -> Card:
    values = insert_cards_mapper.map_to(card)
    query = sa.insert(cards_table).values(**values).returning(cards_table)
    with add_created_and_updated_value(query) as query:
        row = await db_client.fetchrow(query)
    return cards_mapper.map_from(row)


async def get_card_by_id(*, card_id: int, cohort: str) -> Card | None:
    query = sa.select(cards_table).where(
        cards_table.c.id == card_id,
        cards_table.c.cohort == cohort,
        cards_table.c.is_active == sa.true(),
    )
    row = await db_client.fetchrow(query)
    return cards_mapper.map_from(row) if row else None


async def update_card(
    *,
    card_id: int,
    cohort: str,
    name: str | None,
    link: str | None,
    is_active: bool | None,
) -> Card | None:
    assert name or link or is_active is not None, 'name or link or is_active must be provided'

    query = (
        sa.update(cards_table)
        .where(cards_table.c.id == card_id, cards_table.c.cohort == cohort)
        .returning(cards_table)
    )
    if name:
        query = query.values(name=name)
        query &= cards_table.c.is_active == sa.true()
    if link:
        query = query.values(link=link)
        query &= cards_table.c.is_active == sa.true()
    if is_active is not None:
        query = query.values(is_active=is_active)

    with add_updated_value(query) as query:
        row = await db_client.fetchrow(query)
    return cards_mapper.map_from(row) if row else None


async def get_cards_with_owners(cohort: str) -> list[tuple[Card, User]]:
    card_prefix, user_prefix = 'card_', 'user_'
    card_fields = [
        cards_table.columns[field_name].label(f'{card_prefix}{field_name}')
        for field_name in cards_table.columns.keys()
    ]
    user_fields = [
        users_table.columns[field_name].label(f'{user_prefix}{field_name}')
        for field_name in users_table.columns.keys()
    ]

    query = sa.select(*card_fields, *user_fields).select_from(
        cards_table.join(users_table, cards_table.c.owner_id == users_table.c.id)
    ).where(
        cards_table.c.is_active == sa.true(),
        cards_table.c.cohort == cohort,
        users_table.c.is_active == sa.true(),
        users_table.c.cohort == cohort,
    )

    rows = await db_client.fetch(query)
    return [
        (
            cards_mapper.map_from(filter_dict(data=row, prefix=card_prefix)),
            users_mapper.map_from(filter_dict(data=row, prefix=user_prefix))
        )
        for row in rows
    ]