from src.repositories.postgres.cards_repo import update_card


async def set_card_active_status(
    *,
    card_id: int,
    cohort: str,
    is_active: bool,
) -> None:
    await update_card(card_id=card_id, cohort=cohort, is_active=is_active, name=None, link=None)