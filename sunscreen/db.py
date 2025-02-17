import aiosqlite
import asyncio
import sqlite3
import textwrap

import sunscreen.reading


class Db:
    def __init__(self, path):
        self.path = path
        self.listener = None
        self.conn = asyncio.Future()

    def set_listener(self, listener):
        self.listener = listener

    async def init(self):
        # https://github.com/omnilib/aiosqlite/issues/290
        awaitable_conn = aiosqlite.connect(self.path)
        awaitable_conn.daemon = True
        self.conn.set_result(await awaitable_conn)
        await self.create_tables()

    async def record_reading(self, reading):
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
        row = await conn.execute_insert(insert_query, values)
        await conn.commit()
        await self.notify_listener(reading.time)

    async def notify_listener(self, readingTime):
        if self.listener:
            await self.listener(readingTime)

    async def get_readings(self, start, end):
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
            cursor.row_factory = reading_row_factory
            return await cursor.fetchall()

    async def create_tables(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS reading (
            time INT PRIMARY KEY,
            production INT,
            consumption INT
        )"""

        conn = await self.conn
        await conn.execute(create_query)


def reading_row_factory(cursor, row):
    sqlite_row = sqlite3.Row(cursor, row)
    return sunscreen.reading.Reading(
        sqlite_row["time"], sqlite_row["production"], sqlite_row["consumption"]
    )
