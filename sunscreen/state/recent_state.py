import datetime
from typing import Callable, Dict, Iterable, Mapping, Sequence

from .db import Db
from .period import Period
from .reading import Reading
from .reading_span import ReadingSpan
from .reading_span_group import ReadingSpanGroup

BUCKET_MINS = 15


class RecentState:
    def __init__(self, db: Db, period: Period):
        self.db = db
        self.state = ReadingSpanGroup([])
        self.period = period

    def get_state(self) -> ReadingSpanGroup:
        return self.state

    async def refresh(self) -> None:
        start_sec = int(self.period.state_start().timestamp())
        end_sec = int(self.period.state_end().timestamp())
        readings = await self.db.get_readings(start_sec, end_sec)
        grouped = self.group_by_bucket(readings)

        self.state = ReadingSpanGroup(
            [reading_span(dt, list(readings)) for dt, readings in grouped.items()]
        )

    def group_by_bucket(
        self,
        readings: Iterable[Reading],
    ) -> Mapping[datetime.datetime, Iterable[Reading]]:
        result: Dict[datetime.datetime, list[Reading]] = {}
        for dt in self.period.all_bucket_starts():
            result[dt] = []
        for reading in readings:
            reading_bucket = self.period.bucket_start(
                datetime.datetime.fromtimestamp(reading.time)
            )
            if reading_bucket in result:
                result[reading_bucket].append(reading)
        return result


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
