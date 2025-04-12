from dataclasses import dataclass
from datetime import timedelta, datetime


@dataclass
class InsertLike:
    user_id: int
    """Идентификатор пользователя"""
    card_id: int
    """Идентификатор карточки"""
    is_active: bool
    """Статус активности"""


@dataclass
class Like(InsertLike):
    created_at: datetime
    """Дата создания лайка"""
    updated_at: datetime
    """Дата обновления лайка"""

    @property
    def created_at_msc(self) -> datetime:
        return self.created_at + timedelta(hours=3)

    @property
    def updated_at_msc(self) -> datetime:
        return self.updated_at + timedelta(hours=3)
