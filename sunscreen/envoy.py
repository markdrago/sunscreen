import aiohttp


class Envoy:
    def __init__(self, host, access_token):
        self.host = host
        self.access_token = access_token

    async def fetch(self, path):
        url = f"https://{self.host}{path}"
        async with aiohttp.ClientSession(headers=self.headers()) as session:
            async with session.get(url, ssl=False) as response:
                return await response.text()

    async def getReading(self):
        return await self.fetch("/ivp/meters/reports/consumption")

    def headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
