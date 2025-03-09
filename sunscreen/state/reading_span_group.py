import dataclasses

from .reading_span import ReadingSpan


@dataclasses.dataclass
class ReadingSpanGroup:
    spans: list[ReadingSpan]

    def consumptions(self) -> list[int]:
        return [s.consumption for s in self.spans]

    def productions(self) -> list[int]:
        return [s.production for s in self.spans]

    def max_consumption(self) -> int:
        return max(self.consumptions())

    def max_production(self) -> int:
        return max(self.productions())

    def production_sum(self) -> int:
        return sum(self.productions())

    def consumption_sum(self) -> int:
        return sum(self.consumptions())

    def imported_sum(self) -> int:
        return sum([s.imported for s in self.spans])

    def exported_sum(self) -> int:
        return sum([s.exported for s in self.spans])
