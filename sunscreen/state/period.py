import datetime
from abc import abstractmethod
from typing import Protocol, Sequence


class Period(Protocol):
    @abstractmethod
    def all_bucket_starts(self) -> Sequence[datetime.datetime]:
        raise NotImplementedError()

    @abstractmethod
    def state_start(self) -> datetime.datetime:
        raise NotImplementedError()

    @abstractmethod
    def state_end(self) -> datetime.datetime:
        raise NotImplementedError()

    @abstractmethod
    def bucket_start(self, time: datetime.datetime) -> datetime.datetime:
        raise NotImplementedError()
