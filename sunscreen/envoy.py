import aiohttp
import asyncio

import sunscreen.reading


class Envoy:
    def __init__(self, host, access_token):
        self.host = host
        self.access_token = access_token

    async def fetch(self, session, path):
        url = f"https://{self.host}{path}"
        try:
            async with session.get(url, ssl=False) as response:
                return await response.json(content_type=None)
        except asyncio.TimeoutError as e:
            print("Envoy request timed out:", repr(e))
        except aiohttp.ClientConnectionError as e:
            print("Envoy connection failed:", repr(e))

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

        return sunscreen.reading.Reading(time, production, consumption)

    def headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
