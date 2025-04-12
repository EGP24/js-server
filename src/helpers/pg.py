from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Iterator, TypeVar, Any

from asyncpg import Record
from sqlalchemy.sql.dml import ValuesBase

UpdateInsertQueryT = TypeVar('UpdateInsertQueryT', bound=ValuesBase)


@contextmanager
def add_created_value(query: UpdateInsertQueryT) -> Iterator[UpdateInsertQueryT]:
    now = datetime.now(tz=UTC)
    query = query.values(created_at=now)
    yield query


@contextmanager
def add_updated_value(query: UpdateInsertQueryT) -> Iterator[UpdateInsertQueryT]:
    now = datetime.now(tz=UTC)
    query = query.values(updated_at=now)
    yield query


@contextmanager
def add_created_and_updated_value(query: UpdateInsertQueryT) -> Iterator[UpdateInsertQueryT]:
    now = datetime.now(tz=UTC)
    query = query.values(created_at=now, updated_at=now)
    yield query


def filter_dict(*, data: dict[str, Any], prefix: str) -> dict[str, Any]:
    return {k.replace(prefix, ''): v for k, v in data.items() if k.startswith(prefix)}

