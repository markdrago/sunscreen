import aiosqlite
import textwrap


class Db:
    def __init__(self, path):
        self.path = path

    async def init(self):
        # https://github.com/omnilib/aiosqlite/issues/290
        awaitable_conn = aiosqlite.connect(self.path)
        awaitable_conn.daemon = True
        self.conn = await awaitable_conn
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

        row = await self.conn.execute_insert(insert_query, values)
        await self.conn.commit()

    async def create_tables(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS reading (
            time INT PRIMARY KEY,
            production INT,
            consumption INT
        )"""

        await self.conn.execute(create_query)
