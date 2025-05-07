from typing import Coroutine, TypeVar

from src.entities.card import Card
from src.exceptions import CardNotFound, ResourceNotFound
from src.repositories.postgres.cards_repo import get_card_by_id

T = TypeVar('T')


async def get_or_raise(
    *,
    coroutine: Coroutine[None, None, T | None],
    raise_on_none: type[Exception] | None = None,
) -> T:
    raise_on_none = (raise_on_none or ResourceNotFound)
    if not (result := await coroutine):
        raise raise_on_none()
    return result


async def get_card_or_raise(*, card_id: int, cohort: str) -> Card:
    return await get_or_raise(
        coroutine=get_card_by_id(card_id=card_id, cohort=cohort),
        raise_on_none=CardNotFound
    )
