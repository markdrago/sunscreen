import datetime
import math
import time
from typing import Callable, Dict, Iterable, Mapping, Sequence

from .db import Db
from .reading import Reading
from .reading_span import ReadingSpan
from .reading_span_group import ReadingSpanGroup

BUCKET_MINS = 15


class RecentState:
    def __init__(self, db: Db):
        self.db = db
        self.state = ReadingSpanGroup([])

    def get_state(self) -> ReadingSpanGroup:
        return self.state

    async def refresh(self) -> None:
        start_sec = int(state_start().timestamp())
        end_sec = int(time.time())
        readings = await self.db.get_readings(start_sec, end_sec)
        grouped = group_by_period(readings)

        self.state = ReadingSpanGroup(
            [reading_span(dt, list(readings)) for dt, readings in grouped.items()]
        )


def reading_span(dt: datetime.datetime, readings: Sequence[Reading]) -> ReadingSpan:
    return ReadingSpan(
        dt,
        datetime.timedelta(minutes=BUCKET_MINS),
        len(readings),
        mean_property(lambda r: r.production, readings),
        mean_property(lambda r: r.consumption, readings),
        mean_property(lambda r: max(0, r.consumption - r.production), readings),
        mean_property(lambda r: max(0, r.production - r.consumption), readings),
    )


def mean_property(func: Callable[[Reading], int], readings: Sequence[Reading]) -> int:
    if len(readings) == 0:
        return 0
    total = sum(map(func, readings))
    mean = total / len(readings)
    return int(mean / (60 // BUCKET_MINS))


def group_by_period(
    readings: Iterable[Reading],
) -> Mapping[datetime.datetime, Iterable[Reading]]:
    result: Dict[datetime.datetime, list[Reading]] = {}
    for dt in all_period_starts():
        result[dt] = []
    for reading in readings:
        reading_period = period_start(reading.time)
        if reading_period in result:
            result[reading_period].append(reading)
    return result


def period_start(epoch: float) -> datetime.datetime:
    dt = datetime.datetime.fromtimestamp(epoch)
    minute_group_index = min(math.floor(dt.minute / BUCKET_MINS), (59 // BUCKET_MINS))
    start_min = minute_group_index * BUCKET_MINS
    return dt.replace(minute=start_min, second=0, microsecond=0)


def all_period_starts() -> Sequence[datetime.datetime]:
    current_start = period_start(time.time())
    results = []
    for i in range(24 * (60 // BUCKET_MINS), 0, -1):
        delta = datetime.timedelta(minutes=(i - 1) * BUCKET_MINS)
        results.append(current_start - delta)
    return results


def state_start() -> datetime.datetime:
    # start of current period
    current_start = period_start(time.time())

    # subtract nearly 24 hours to get start of 24-hour period
    return current_start - datetime.timedelta(minutes=(24 * 60) - BUCKET_MINS)
