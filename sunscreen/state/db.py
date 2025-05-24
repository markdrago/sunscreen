import asyncio
import sqlite3
from typing import Any, Awaitable, Callable, Iterable, Optional, cast

import aiosqlite

from .reading import Reading


class Db:
    def __init__(self, path: str):
        self.path = path
        self.listener: Optional[Callable[[int], Awaitable[None]]]
        self.conn: asyncio.Future[aiosqlite.Connection] = asyncio.Future()

    def set_listener(self, listener: Callable[[int], Awaitable[None]]) -> None:
        self.listener = listener

    async def init(self) -> None:
        # https://github.com/omnilib/aiosqlite/issues/290
        awaitable_conn = aiosqlite.connect(self.path)
        awaitable_conn.daemon = True
        self.conn.set_result(await awaitable_conn)
        await self.create_tables()

    async def record_reading(self, reading: Reading) -> None:
        insert_query = """
        INSERT INTO reading
            (time, production, consumption)
        VALUES
            (:time, :production, :consumption)"""

        values = {
            "time": reading.time,
            "production": reading.production,
            "consumption": reading.consumption,
        }

        conn = await self.conn
        await conn.execute_insert(insert_query, values)
        await conn.commit()
        await self.notify_listener(reading.time)

    async def notify_listener(self, readingTime: int) -> None:
        if self.listener:
            await self.listener(readingTime)

    async def get_readings(self, start: int, end: int) -> Iterable[Reading]:
        query = """
        SELECT time, production, consumption
        FROM reading
        WHERE time BETWEEN :start AND :end
        ORDER BY time ASC
        """

        params = {
            "start": start,
            "end": end,
        }

        conn = await self.conn
        async with conn.execute(query, params) as cursor:
            # Pretty sure the row_factory type is defined incorrectly in aiosqlite
            cursor.row_factory = reading_row_factory  # type: ignore
            # Type of cursor.fetchall specifies a sqlite3.Row despite row_factory
            return cast(Iterable[Reading], await cursor.fetchall())

    async def create_tables(self) -> None:
        create_query = """
        CREATE TABLE IF NOT EXISTS reading (
            time INT PRIMARY KEY,
            production INT,
            consumption INT
        )"""

        conn = await self.conn
        await conn.execute(create_query)


def reading_row_factory(cursor: sqlite3.Cursor, row: tuple[Any, ...]) -> Reading:
    sqlite_row = sqlite3.Row(cursor, row)
    return Reading(
        sqlite_row["time"], sqlite_row["production"], sqlite_row["consumption"]
    )
