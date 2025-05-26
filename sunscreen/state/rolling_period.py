import dataclasses
import datetime
import time
from typing import Sequence

from .bucket_duration import BucketDuration
from .period import Period


@dataclasses.dataclass
class RollingPeriod(Period):
    bucket_duration: BucketDuration
    num_buckets: int
    offset: datetime.timedelta = datetime.timedelta(0)

    def start(self) -> datetime.datetime:
        return self.bucket_duration.bucket_start(
            datetime.datetime.fromtimestamp(time.time()) - self.offset
        )

    def all_bucket_starts(self) -> Sequence[datetime.datetime]:
        current_start = self.start()
        results = []
        for i in range(self.num_buckets, 0, -1):
            delta = self.bucket_duration.timedelta() * (i - 1)
            results.append(current_start - delta)
        return results

    def state_start(self) -> datetime.datetime:
        return self.start() - (
            (self.num_buckets - 1) * self.bucket_duration.timedelta()
        )

    def state_end(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(time.time()) - self.offset

    def bucket_start(self, time: datetime.datetime) -> datetime.datetime:
        return self.bucket_duration.bucket_start(time)
