import math
import pygame

from typing import Optional

from ..state.recent_state import RecentState
from ..state.reading_span_group import ReadingSpanGroup

SURFACE_HEIGHT = 380
SURFACE_WIDTH = 608


class RecentStateRenderer:
    def __init__(self, recent_state_provider: RecentState):
        self.recent_state_provider = recent_state_provider
        self.state: Optional[ReadingSpanGroup] = None
        self.surface: Optional[pygame.Surface] = None

    def render(self) -> pygame.Surface:
        state = self.recent_state_provider.get_state()
        if self.state == state and self.surface:
            return self.surface

        surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        render_frame(surface)
        render_bars(surface, state)

        self.state = state
        self.surface = surface
        return self.surface


def render_frame(surface: pygame.Surface) -> None:
    width = 1
    pygame.draw.rect(
        surface,
        "white",
        pygame.Rect(
            0,
            0,
            SURFACE_WIDTH,
            SURFACE_HEIGHT,
        ),
        width,
    )


def render_bars(surface: pygame.Surface, state: ReadingSpanGroup) -> None:
    right_buffer = 1
    width = 5
    buffer = 1
    # TODO: handle missing spans
    max_bar_count = min(len(state.spans), 24)

    pixel_value = get_pixel_value(state)
    mid_height = get_mid_height(state)

    next_x = SURFACE_WIDTH - right_buffer - width
    for i in range(len(state.spans) - 1, -1, -1):
        span = state.spans[i]
        cons_h = math.floor(span.consumption / pixel_value)
        prod_h = math.floor(span.production / pixel_value)

        surface.fill(
            "blue",
            pygame.Rect(next_x, mid_height - prod_h, width, prod_h),
        )
        surface.fill(
            "orange",
            pygame.Rect(next_x, mid_height + 1, width, cons_h),
        )

        next_x -= buffer + width

    # draw mid_height line
    pygame.draw.line(
        surface,
        "darkgray",
        (buffer, mid_height),
        (SURFACE_WIDTH - buffer, mid_height),
    )


def get_mid_height(state: ReadingSpanGroup) -> int:
    max_prod = state.max_production()
    max_cons = state.max_consumption()
    ratio = max_prod / (max_prod + max_cons)
    return round(SURFACE_HEIGHT * ratio)


def get_pixel_value(state: ReadingSpanGroup) -> float:
    sum_of_max = state.max_consumption() + state.max_production()
    buffer = 3  # space for top/bottom edge and mid-line
    return sum_of_max / (SURFACE_HEIGHT - 3)
