import datetime
import itertools
import math
import time

import sunscreen.reading_span

BUCKET_MINS = 15


class RecentState:
    def __init__(self, db):
        self.db = db
        self.state = []

    async def new_reading_notice(self, reading_time):
        if time.time() - (24 * 60) <= reading_time:
            await self.refresh()

    async def refresh(self):
        start_sec = int(state_start().timestamp())
        end_sec = int(time.time())
        readings = await self.db.get_readings(start_sec, end_sec)
        grouped = group_by_period(readings)
        self.state = [reading_span(dt, list(readings)) for dt, readings in grouped]
        print()
        for span in self.state:
            print(span)


def reading_span(dt, readings):
    return sunscreen.reading_span.ReadingSpan(
        dt,
        datetime.timedelta(minutes=BUCKET_MINS),
        len(readings),
        mean_property(lambda r: r.production, readings),
        mean_property(lambda r: r.consumption, readings),
    )


def mean_property(func, readings):
    if len(readings) == 0:
        return 0
    total = sum(map(func, readings))
    mean = total / len(readings)
    return int(mean / (60 // BUCKET_MINS))


# takes readings, returns grouped by BUCKET_MIN-sized intervals
# key is interval start
def group_by_period(readings):
    return itertools.groupby(readings, lambda r: period_start(r.time))


def period_start(epoch):
    dt = datetime.datetime.fromtimestamp(epoch)
    minute_group_index = min(math.floor(dt.minute / BUCKET_MINS), (59 // BUCKET_MINS))
    start_min = minute_group_index * BUCKET_MINS
    return dt.replace(minute=start_min, second=0, microsecond=0)


def state_start():
    # start of current period
    current_start = period_start(time.time())

    # subtract nearly 24 hours to get start of 24-hour period
    return current_start - datetime.timedelta(minutes=(24 * 60) - BUCKET_MINS)
