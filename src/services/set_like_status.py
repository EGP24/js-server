from src.entities.like import InsertLike, Like
from src.repositories.postgres.likes_repo import upsert_like


async def set_like_status(
    *,
    user_id: int,
    card_id: int,
    is_like: bool,
) -> Like:
    return await upsert_like(InsertLike(user_id=user_id, card_id=card_id, is_active=is_like))
