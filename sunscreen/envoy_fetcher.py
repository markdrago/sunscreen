import aiohttp
import asyncio

import sunscreen.envoy

FETCH_FREQUENCY_SECONDS = 60


class EnvoyFetcher:
    def __init__(self, host, access_token, data_handler):
        self.envoy = sunscreen.envoy.Envoy(host, access_token)
        self.data_handler = data_handler

    async def loop(self):
        async with aiohttp.ClientSession(
            headers=self.envoy.headers(), timeout=aiohttp.ClientTimeout(total=60)
        ) as session:
            while True:
                res = await self.envoy.getReading(session)
                await self.data_handler(res)
                await asyncio.sleep(FETCH_FREQUENCY_SECONDS)
