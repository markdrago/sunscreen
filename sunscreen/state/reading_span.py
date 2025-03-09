import dataclasses
import datetime

# Data used during rendering for a period of time


@dataclasses.dataclass
class ReadingSpan:
    start: datetime.datetime
    duration: datetime.timedelta
    reading_count: int

    # Power in milliwatt hours / (durations in hour)
    production: int
    consumption: int
    imported: int
    exported: int
