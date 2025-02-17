import aiohttp
import asyncio

from ..state.reading import Reading


class Envoy:
    def __init__(self, host, access_token):
        self.host = host
        self.access_token = access_token

    # throws asyncio.TimeoutError & aiohttp.ClientConnectionError
    async def fetch(self, session, path):
        url = f"https://{self.host}{path}"
        async with session.get(url, ssl=False) as response:
            return await response.json(content_type=None)

    async def getReading(self, session):
        json = await self.fetch(session, "/ivp/meters/reports/consumption")

        time = None
        net_consumption = None
        total_consumption = None
        for stanza in json:
            time = int(stanza["createdAt"])
            if stanza["reportType"] == "total-consumption":
                total_consumption = stanza["cumulative"]["currW"]
            elif stanza["reportType"] == "net-consumption":
                net_consumption = stanza["cumulative"]["currW"]

        # convert from decimal watts to integer milliwatts & calc production
        consumption = int(total_consumption * 1000)
        production = consumption - int(net_consumption * 1000)

        return Reading(time, production, consumption)

    def headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
