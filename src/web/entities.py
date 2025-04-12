from dataclasses import dataclass

from src.entities.card import PresentedCard
from src.entities.user import PresentedUser
from src.mappers.custom import ImageUrlEncoder


@dataclass
class GetUserProfileResponse(PresentedUser): ...


@dataclass
class UpdateUserProfileRequest:
    about: str | None
    """Описание"""
    name: str | None
    """Имя пользователя"""


@dataclass
class UpdateUserProfileResponse(PresentedUser): ...


@dataclass
class UpdateUserAvatarRequest:
    avatar: ImageUrlEncoder
    """Ссылка на аватар пользователя"""


@dataclass
class UpdateUserAvatarResponse(PresentedUser): ...


@dataclass
class CreateCardRequest:
    name: str
    """Название карточки"""
    link: ImageUrlEncoder
    """Ссылка на фото"""


@dataclass
class CreateCardResponse(PresentedCard): ...
