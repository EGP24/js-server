from src.entities.card import PresentedCard
from src.entities.user import PresentedUser
from src.mappers.custom import map_user_to_presented_user
from src.repositories.postgres.cards_repo import get_cards_with_owners
from src.repositories.postgres.likes_repo import get_likes_users


async def get_presented_cards(*, cohort: str) -> list[PresentedCard]:
    cards_with_owners = await get_cards_with_owners(cohort=cohort)
    presented_cards = []
    for card, owner in cards_with_owners:
        likes_users = await get_likes_users(card_id=card.id, cohort=cohort)
        presented_card = PresentedCard(
            id=card.id,
            name=card.name,
            link=card.link,
            owner=map_user_to_presented_user(owner),
            likes=[map_user_to_presented_user(user) for user in likes_users],
            created_at=card.created_at_msc,
        )
        presented_cards.append(presented_card)
    return presented_cards
