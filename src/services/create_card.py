from src.entities.card import Card, InsertCard
from src.repositories.postgres.cards_repo import insert_card


async def create_card(*, owner_id: int, cohort: str, name: str, link: str) -> Card:
    return await insert_card(InsertCard(owner_id=owner_id, cohort=cohort, name=name, link=link, is_active=True))
