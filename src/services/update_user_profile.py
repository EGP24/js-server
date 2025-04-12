from src.entities.user import User
from src.exceptions import UserNotFound
from src.helpers.get_or_raise import get_or_raise
from src.repositories.postgres.users_repo import update_user_info


async def update_user_profile(
    *,
    user_id: int,
    about: str | None = None,
    name: str | None = None,
    avatar: str | None = None,
) -> User:
    updated_user = await get_or_raise(
        coroutine=update_user_info(
            user_id=user_id,
            about=about,
            name=name,
            avatar=avatar,
        ),
        raise_on_none=UserNotFound,
    )
    return updated_user
