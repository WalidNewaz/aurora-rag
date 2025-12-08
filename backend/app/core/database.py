# app/core/database.py
import psycopg
from psycopg.rows import dict_row

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._pool = None

    async def connect(self):
        if self._pool is None:
            self._pool = await psycopg.AsyncConnection.connect(
                self.dsn, row_factory=dict_row
            )

    async def fetchone(self, query: str, params=None):
        await self.connect()
        async with self._pool.cursor() as cur:
            await cur.execute(query, params or {})
            return await cur.fetchone()

    async def fetchall(self, query: str, params=None):
        await self.connect()
        async with self._pool.cursor() as cur:
            await cur.execute(query, params or {})
            return await cur.fetchall()

    async def execute(self, query: str, params=None):
        await self.connect()
        async with self._pool.cursor() as cur:
            await cur.execute(query, params or {})
            await self._pool.commit()

    async def close(self):
        if self._pool:
            await self._pool.close()
