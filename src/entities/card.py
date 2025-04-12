from dataclasses import dataclass
from datetime import datetime, timedelta

from src.entities.user import PresentedUser


@dataclass
class InsertCard:
    name: str
    """Название карточки"""
    cohort: str
    """Группа"""
    link: str
    """Ссылка на фото"""
    owner_id: int
    """Идентификатор владельца карточки"""
    is_active: bool
    """Статус активности"""


@dataclass
class Card(InsertCard):
    id: int
    """Идентификатор карточки"""
    created_at: datetime
    """Дата создания карточки"""
    updated_at: datetime
    """Дата обновления карточки"""

    @property
    def created_at_msc(self) -> datetime:
        return self.created_at + timedelta(hours=3)

    @property
    def updated_at_msc(self) -> datetime:
        return self.updated_at + timedelta(hours=3)


@dataclass
class PresentedCard:
    likes: list[PresentedUser]
    """Лайки карточки"""
    id: int
    """Идентификатор карточки"""
    name: str
    """Название карточки"""
    link: str
    """Ссылка на фото"""
    owner: PresentedUser
    """Владелец карточки"""
    created_at: datetime
    """Дата создания карточки"""
