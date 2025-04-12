from aiohttp import web

from src.entities.card import PresentedCard
from src.entities.user import PresentedUser
from src.helpers.get_or_raise import get_card_or_raise
from src.repositories.postgres.cards_repo import get_cards_with_owners
from src.services.create_card import create_card
from src.services.get_presented_cards import get_presented_cards
from src.services.get_user_by_token import get_user_by_token_and_cohort
from src.services.set_card_active_status import set_card_active_status
from src.services.set_like_status import set_like_status
from src.services.update_user_profile import update_user_profile
from src.web.base import (XAuthorizationRequired, XCardIdRequired,
                          XCohortRequired, with_typehinted_request)
from src.web.entities import (CreateCardRequest, CreateCardResponse,
                              GetUserProfileResponse, UpdateUserAvatarRequest,
                              UpdateUserAvatarResponse,
                              UpdateUserProfileRequest,
                              UpdateUserProfileResponse)


@with_typehinted_request
async def get_user_profile_handler(
    *,
    app: web.Application,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
) -> GetUserProfileResponse:
    user = await get_user_by_token_and_cohort(token=token, cohort=cohort)
    return GetUserProfileResponse(
        id=user.id,
        name=user.name,
        about=user.about,
        avatar=user.avatar,
        cohort=user.cohort,
    )


@with_typehinted_request
async def update_user_profile_handler(
    *,
    app: web.Application,
    request: UpdateUserProfileRequest,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
) -> UpdateUserProfileResponse:
    user = await get_user_by_token_and_cohort(token=token, cohort=cohort)
    updated_user = await update_user_profile(
        user_id=user.id,
        name=request.name,
        about=request.about,
    )
    return UpdateUserProfileResponse(
        id=updated_user.id,
        name=updated_user.name,
        about=updated_user.about,
        avatar=updated_user.avatar,
        cohort=updated_user.cohort,
    )


@with_typehinted_request
async def update_user_avatar_handler(
    *,
    app: web.Application,
    request: UpdateUserAvatarRequest,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
) -> UpdateUserAvatarResponse:
    user = await get_user_by_token_and_cohort(token=token, cohort=cohort)
    updated_user = await update_user_profile(user_id=user.id, avatar=request.avatar)
    return UpdateUserAvatarResponse(
        id=updated_user.id,
        name=updated_user.name,
        about=updated_user.about,
        avatar=updated_user.avatar,
        cohort=updated_user.cohort,
    )


@with_typehinted_request
async def create_card_handler(
    *,
    app: web.Application,
    request: CreateCardRequest,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
) -> CreateCardResponse:
    user = await get_user_by_token_and_cohort(token=token, cohort=cohort)
    card = await create_card(owner_id=user.id, cohort=cohort, name=request.name, link=request.link)
    return CreateCardResponse(
        id=card.id,
        name=card.name,
        link=card.link,
        owner=PresentedUser(
            id=user.id,
            name=user.name,
            about=user.about,
            avatar=user.avatar,
            cohort=user.cohort,
        ),
        likes=[],
        created_at=card.created_at_msc,
    )


@with_typehinted_request
async def delete_card_handler(
    *,
    app: web.Application,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
    card_id: XCardIdRequired,
) -> None:
    user = await get_user_by_token_and_cohort(token=token, cohort=cohort)
    card = await get_card_or_raise(card_id=card_id, cohort=cohort)
    if card.owner_id != user.id:
        raise web.HTTPBadRequest(text='You are not the owner of this card')
    await set_card_active_status(card_id=card.id, cohort=cohort, is_active=False)


@with_typehinted_request
async def get_cards_handler(
    *,
    app: web.Application,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
) -> list[PresentedCard]:
    await get_user_by_token_and_cohort(token=token, cohort=cohort)
    cards = await get_presented_cards(cohort=cohort)
    return cards


@with_typehinted_request
async def set_card_like_handler(
    *,
    app: web.Application,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
    card_id: XCardIdRequired,
) -> None:
    user = await get_user_by_token_and_cohort(token=token, cohort=cohort)
    card = await get_card_or_raise(card_id=card_id, cohort=cohort)
    await set_like_status(
        user_id=user.id,
        card_id=card.id,
        is_like=True,
    )


@with_typehinted_request
async def remove_card_like_handler(
    *,
    app: web.Application,
    token: XAuthorizationRequired,
    cohort: XCohortRequired,
    card_id: XCardIdRequired,
) -> None:
    user = await get_user_by_token_and_cohort(token=token, cohort=cohort)
    card = await get_card_or_raise(card_id=card_id, cohort=cohort)
    await set_like_status(
        user_id=user.id,
        card_id=card.id,
        is_like=False,
    )
