import datetime
from typing import Protocol


class BucketDuration(Protocol):
    @staticmethod
    def timedelta() -> datetime.timedelta:
        raise NotImplementedError()

    @staticmethod
    def bucket_start(dt: datetime.datetime) -> datetime.datetime:
        raise NotImplementedError()


class BucketDurationQuarterHourly(BucketDuration):
    @staticmethod
    def timedelta() -> datetime.timedelta:
        return datetime.timedelta(minutes=15)

    @staticmethod
    def bucket_start(dt: datetime.datetime) -> datetime.datetime:
        minute_group_index = min(dt.minute // 15, 3)
        start_min = minute_group_index * 15
        return dt.replace(minute=start_min, second=0, microsecond=0)


class BucketDurationDaily(BucketDuration):
    @staticmethod
    def timedelta() -> datetime.timedelta:
        return datetime.timedelta(days=1)

    @staticmethod
    def bucket_start(dt: datetime.datetime) -> datetime.datetime:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
