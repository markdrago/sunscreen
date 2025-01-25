import asyncio

import sunscreen.envoy

FETCH_FREQUENCY_SECONDS = 5


class EnvoyFetcher:
    def __init__(self, host, access_token):
        self.envoy = sunscreen.envoy.Envoy(host, access_token)

    async def loop(self):
        while True:
            res = await self.envoy.getReading()
            print(res)
            await asyncio.sleep(FETCH_FREQUENCY_SECONDS)
