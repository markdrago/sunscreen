import dataclasses


@dataclasses.dataclass
class Reading:
    # time in seconds since epoch
    time: int

    # power in milliwatts per hour
    production: int
    consumption: int
