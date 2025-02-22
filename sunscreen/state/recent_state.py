import datetime
import itertools
import math
import time

from .reading import Reading
from .reading_span import ReadingSpan
from .reading_span_group import ReadingSpanGroup

from .db import Db

from typing import Callable, Iterable, Sequence, Tuple

BUCKET_MINS = 15


class RecentState:
    def __init__(self, db: Db):
        self.db = db
        self.state = ReadingSpanGroup([])

    def get_state(self) -> ReadingSpanGroup:
        return self.state

    async def new_reading_notice(self, reading_time: int) -> None:
        if time.time() - (24 * 60) <= reading_time:
            await self.refresh()

    async def refresh(self) -> None:
        start_sec = int(state_start().timestamp())
        end_sec = int(time.time())
        readings = await self.db.get_readings(start_sec, end_sec)
        grouped = group_by_period(readings)
        self.state = ReadingSpanGroup(
            [reading_span(dt, list(readings)) for dt, readings in grouped]
        )


def reading_span(dt: datetime.datetime, readings: Sequence[Reading]) -> ReadingSpan:
    return ReadingSpan(
        dt,
        datetime.timedelta(minutes=BUCKET_MINS),
        len(readings),
        mean_property(lambda r: r.production, readings),
        mean_property(lambda r: r.consumption, readings),
    )


def mean_property(func: Callable[[Reading], int], readings: Sequence[Reading]) -> int:
    if len(readings) == 0:
        return 0
    total = sum(map(func, readings))
    mean = total / len(readings)
    return int(mean / (60 // BUCKET_MINS))


# takes readings, returns grouped by BUCKET_MIN-sized intervals
# key is interval start
def group_by_period(
    readings: Iterable[Reading],
) -> Iterable[Tuple[datetime.datetime, Iterable[Reading]]]:
    return itertools.groupby(readings, lambda r: period_start(r.time))


def period_start(epoch: float) -> datetime.datetime:
    dt = datetime.datetime.fromtimestamp(epoch)
    minute_group_index = min(math.floor(dt.minute / BUCKET_MINS), (59 // BUCKET_MINS))
    start_min = minute_group_index * BUCKET_MINS
    return dt.replace(minute=start_min, second=0, microsecond=0)


def state_start() -> datetime.datetime:
    # start of current period
    current_start = period_start(time.time())

    # subtract nearly 24 hours to get start of 24-hour period
    return current_start - datetime.timedelta(minutes=(24 * 60) - BUCKET_MINS)
