import aiohttp
import asyncio

from .envoy import Envoy

FETCH_FREQUENCY_SECONDS = 60


class EnvoyFetcher:
    def __init__(self, host, access_token, data_handler):
        self.envoy = Envoy(host, access_token)
        self.data_handler = data_handler

    async def loop(self):
        async with aiohttp.ClientSession(
            headers=self.envoy.headers(), timeout=aiohttp.ClientTimeout(total=60)
        ) as session:
            while True:
                try:
                    res = await self.envoy.getReading(session)
                    await self.data_handler(res)
                except (asyncio.TimeoutError, aiohttp.ClientConnectionError) as e:
                    print("Error retrieving reading:", repr(e))
                finally:
                    await asyncio.sleep(FETCH_FREQUENCY_SECONDS)
