from os import environ
from typing import Any, Optional

from asyncpg import create_pool
from sqlalchemy import ClauseElement
from sqlalchemy.dialects.postgresql import asyncpg as pg_dialect


class AsyncPostgresClientSingleton:
    _instance: Optional['AsyncPostgresClientSingleton'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *, min_size: int = 1, max_size: int = 10) -> None:
        if not hasattr(self, '_initialized'):
            self.min_size = min_size
            self.max_size = max_size
            self.pool = None
            self._initialized = True

    async def connect(self) -> None:
        self.pool = await create_pool(dsn=self._get_dsn(), min_size=self.min_size, max_size=self.max_size)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

    async def execute(self, statement: ClauseElement) -> str:
        assert self.pool is not None, "Database connection pool is not initialized."

        async with self.pool.acquire() as conn:
            query, params = self._compile_statement(statement)
            return await conn.execute(query, *params)

    async def executemany(self, statement: ClauseElement) -> None:
        assert self.pool is not None, "Database connection pool is not initialized."

        async with self.pool.acquire() as conn:
            query, params = self._compile_statement(statement)
            await conn.executemany(query, params)

    async def fetch(self, statement: ClauseElement) -> list[dict]:
        assert self.pool is not None, "Database connection pool is not initialized."

        async with self.pool.acquire() as conn:
            query, params = self._compile_statement(statement)
            rows = await conn.fetch(query, *params)
            return [dict(row) for row in rows]

    async def fetchrow(self, statement: ClauseElement) -> Optional[dict]:
        assert self.pool is not None, "Database connection pool is not initialized."

        async with self.pool.acquire() as conn:
            query, params = self._compile_statement(statement)
            row = await conn.fetchrow(query, *params)
            return dict(row) if row else None

    async def fetchval(self, statement: ClauseElement) -> Any:
        assert self.pool is not None, "Database connection pool is not initialized."

        async with self.pool.acquire() as conn:
            query, params = self._compile_statement(statement)
            return await conn.fetchval(query, *params)


    def _compile_statement(self, statement: ClauseElement) -> tuple[str, list[Any]]:
        compiled = statement.compile(dialect=pg_dialect.dialect(), compile_kwargs={"literal_binds": False})
        query = str(compiled)
        params = compiled.params
        return query, list(params.values())

    def _get_dsn(self) -> str:
        host, port, password, user, dbname = (
            environ.get('POSTGRES_HOST'),
            environ.get('POSTGRES_PORT'),
            environ.get('POSTGRES_PASSWORD'),
            environ.get('POSTGRES_USER'),
            environ.get('POSTGRES_DB'),
        )
        return f'postgresql://{user}:{password}@{host}:{port}/{dbname}'


db_client = AsyncPostgresClientSingleton()