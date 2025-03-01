import asyncio
from datetime import datetime, timedelta
from typing import Awaitable, Callable

from .recent_state import RecentState

REFRESH_FREQUENCY_SECONDS = 60
REFRESH_LIMIT_SECONDS = 60


class StateRefresher:
    def __init__(self, recent_state: RecentState):
        self.recent_state = recent_state
        self.last_refresh = datetime.min

    async def loop(self) -> None:
        while True:
            # Refresh on a timer if we haven't refreshed due to new data for a bit
            if datetime.now() > self.last_refresh + timedelta(
                seconds=REFRESH_LIMIT_SECONDS
            ):
                await self.trigger_refresh()
            await asyncio.sleep(REFRESH_FREQUENCY_SECONDS)

    # Always refresh the state when we have new data
    async def handle_new_reading(self, reading_time: int) -> None:
        await self.trigger_refresh()

    async def trigger_refresh(self) -> None:
        self.last_refresh = datetime.now()
        await self.recent_state.refresh()
