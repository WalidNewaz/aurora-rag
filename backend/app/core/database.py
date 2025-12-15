from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

class Database:
    """
    Database access built around:
      - a connection pool (safe under concurrency)
      - transaction-scoped connections (atomic units of work)

    Repositories should execute queries using the connection passed
    by `transaction()` to ensure consistent commit/rollback behavior.
    """

    def __init__(self, dsn: str):
        self.dsn = dsn
        self._conn: psycopg.AsyncConnection | None = None
        self._pool: Optional[AsyncConnectionPool] = None

    async def connect(self):
        if self._pool is None:
            # open=False so we can explicitly open on startup
            self._pool = AsyncConnectionPool(
                conninfo=self.dsn,
                open=False,
                kwargs={"row_factory": dict_row},
            )
            await self._pool.open()

    async def close(self):
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncIterator[psycopg.AsyncConnection]:
        await self.connect()
        assert self._pool is not None
        async with self._pool.connection() as conn:
            yield conn

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[psycopg.AsyncConnection]:
        """
        Acquire a dedicated connection from the pool for the duration of the transaction.
        All queries that must be atomic must run using this `conn`.
        """
        async with self.connection() as conn:
            async with conn.transaction():
                yield conn

    # ---------------------------------------
    # Convenience methods (non-transactional)
    # Use only for read-only queries, or simple writes where
    # atomicity doesn't matter.
    # ---------------------------------------

    async def fetchone(self, query: str, params: dict[str, Any] | None = None) -> Any:
        async with self.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or {})
                return await cur.fetchone()

    async def fetchall(self, query: str, params: dict[str, Any] | None = None) -> list[Any]:
        async with self.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or {})
                return await cur.fetchall()

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> None:
        async with self.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params or {})
            await conn.commit()

