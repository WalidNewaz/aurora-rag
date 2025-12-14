from contextlib import asynccontextmanager
import psycopg
from psycopg.rows import dict_row

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._conn: psycopg.AsyncConnection | None = None

    async def connect(self):
        if self._conn is None:
            self._conn = await psycopg.AsyncConnection.connect(
                self.dsn,
                row_factory=dict_row,
            )

    @asynccontextmanager
    async def transaction(self):
        await self.connect()
        try:
            async with self._conn.transaction():
                yield
        except Exception:
            # psycopg automatically rolls back on exception
            raise

    async def fetchone(self, query: str, params=None):
        await self.connect()
        async with self._conn.cursor() as cur:
            await cur.execute(query, params or {})
            return await cur.fetchone()

    async def fetchall(self, query: str, params=None):
        await self.connect()
        async with self._conn.cursor() as cur:
            await cur.execute(query, params or {})
            return await cur.fetchall()

    async def execute(self, query: str, params=None):
        await self.connect()
        async with self._conn.cursor() as cur:
            await cur.execute(query, params or {})

    async def close(self):
        if self._conn:
            await self._conn.close()
