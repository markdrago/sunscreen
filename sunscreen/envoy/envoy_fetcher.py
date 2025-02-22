import asyncio
from typing import Awaitable, Callable

import aiohttp

from ..state.reading import Reading
from .envoy import Envoy, EnvoyError

FETCH_FREQUENCY_SECONDS = 60


class EnvoyFetcher:
    def __init__(
        self,
        host: str,
        access_token: str,
        data_handler: Callable[[Reading], Awaitable[None]],
    ):
        self.envoy = Envoy(host, access_token)
        self.data_handler = data_handler

    async def loop(self) -> None:
        async with aiohttp.ClientSession(
            headers=self.envoy.headers(), timeout=aiohttp.ClientTimeout(total=60)
        ) as session:
            while True:
                try:
                    res = await self.envoy.getReading(session)
                    await self.data_handler(res)
                except (
                    asyncio.TimeoutError,
                    aiohttp.ClientConnectionError,
                    EnvoyError,
                ) as e:
                    print("Error retrieving reading:", repr(e))
                finally:
                    await asyncio.sleep(FETCH_FREQUENCY_SECONDS)
