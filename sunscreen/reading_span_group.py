import dataclasses

import sunscreen.reading_span


@dataclasses.dataclass
class ReadingSpanGroup:
    spans: list[sunscreen.reading_span.ReadingSpan]

    def consumptions(self):
        return [s.consumption for s in self.spans]

    def productions(self):
        return [s.production for s in self.spans]

    def max_consumption(self):
        return max(self.consumptions())

    def max_production(self):
        return max(self.productions())
