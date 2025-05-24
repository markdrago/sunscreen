from typing import Any, Dict, List, TypedDict, cast

import aiohttp

from ..state.reading import Reading


class Cumulative(TypedDict):
    currW: int


class Stanza(TypedDict):
    createdAt: str
    reportType: str
    cumulative: Cumulative


class Envoy:
    def __init__(self, host: str, access_token: str):
        self.host = host
        self.access_token = access_token

    # throws asyncio.TimeoutError & aiohttp.ClientConnectionError
    async def fetch(self, session: aiohttp.ClientSession, path: str) -> List[Any]:
        url = f"https://{self.host}{path}"
        async with session.get(url, ssl=False) as response:
            json = await response.json(content_type=None)
            if isinstance(json, list):
                return json
            raise EnvoyError(f"Invalid JSON: {json}")

    async def getReading(self, session: aiohttp.ClientSession) -> Reading:
        json = await self.fetch(session, "/ivp/meters/reports/consumption")
        json = cast(List[Stanza], json)

        time = None
        net_consumption = None
        total_consumption = None
        for stanza in json:
            time = int(stanza["createdAt"])
            if stanza["reportType"] == "total-consumption":
                total_consumption = stanza["cumulative"]["currW"]
            elif stanza["reportType"] == "net-consumption":
                net_consumption = stanza["cumulative"]["currW"]

        if total_consumption is None:
            raise EnvoyError("Missing total_consumption value")
        if net_consumption is None:
            raise EnvoyError("Missing net_consumption value")
        if time is None:
            raise EnvoyError("Missing time value")

        # convert from decimal watts to integer milliwatts & calc production
        consumption = int(total_consumption * 1000)
        production = consumption - int(net_consumption * 1000)

        return Reading(time, production, consumption)

    def headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }


class EnvoyError(Exception):
    pass
