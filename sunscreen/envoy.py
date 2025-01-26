import aiohttp
import asyncio


class Envoy:
    def __init__(self, host, access_token):
        self.host = host
        self.access_token = access_token

    async def fetch(self, session, path):
        url = f"https://{self.host}{path}"
        try:
            async with session.get(url, ssl=False) as response:
                return await response.text()
        except asyncio.TimeoutError as e:
            print("Envoy request timed out:", repr(e))
        except aiohttp.ClientConnectionError as e:
            print("Envoy connection failed:", repr(e))

    async def getReading(self, session):
        return await self.fetch(session, "/ivp/meters/reports/consumption")

    def headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
