from dataclasses import dataclass


@dataclass
class InsertUser:
    name: str
    """Имя пользователя"""
    about: str
    """Описание"""
    avatar: str | None
    """Ссылка на аватар"""
    is_active: bool
    """Статус активности"""
    cohort: str
    """Группа"""
    token: str
    """Токен авторизации"""


@dataclass
class User(InsertUser):
    id: int
    """Идентификатор пользователя"""


@dataclass
class PresentedUser:
    id: int
    """Идентификатор пользователя"""
    name: str
    """Имя пользователя"""
    about: str
    """Описание"""
    avatar: str | None
    """Ссылка на аватар"""
    cohort: str
    """Группа"""
