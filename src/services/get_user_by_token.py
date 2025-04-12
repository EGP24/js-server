from src.entities.user import User
from src.exceptions import CohortIsRequired, TokenIsRequired, UserNotFound
from src.helpers.get_or_raise import get_or_raise
from src.repositories.postgres.users_repo import \
    get_user_by_token_and_cohort as pg_get_user_by_token_and_cohort


async def get_user_by_token_and_cohort(*, token: str, cohort: str) -> User:
    if not token:
        raise TokenIsRequired
    if not cohort:
        raise CohortIsRequired

    print('user has token and cohort')
    user = await get_or_raise(
        coroutine=pg_get_user_by_token_and_cohort(token=token, cohort=cohort),
        raise_on_none=UserNotFound,
    )
    return user