import math
from typing import Optional

import pygame

from ..state.reading_span_group import ReadingSpanGroup
from ..state.recent_state import RecentState

SURFACE_HEIGHT = 380
SURFACE_WIDTH = 608
LEFT_AXIS_BAR_X = 30


class RecentStateRenderer:
    def __init__(self, recent_state_provider: RecentState):
        self.recent_state_provider = recent_state_provider
        self.state: Optional[ReadingSpanGroup] = None
        self.surface: Optional[pygame.Surface] = None
        self.axis_font = pygame.font.Font(None, size=20)

    def render(self) -> pygame.Surface:
        state = self.recent_state_provider.get_state()
        if self.state == state and self.surface:
            return self.surface

        surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        render_frame(surface)
        render_bars(surface, state)
        render_axis(surface, self.axis_font, state)

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
        (LEFT_AXIS_BAR_X, mid_height),
        (SURFACE_WIDTH - buffer, mid_height),
    )


def render_axis(
    surface: pygame.Surface, font: pygame.font.Font, state: ReadingSpanGroup
) -> None:
    label_right_gap = 2
    mid_height = get_mid_height(state)
    pixel_value = get_pixel_value(state) / 1_000_000  # milliwatts -> kilowatts

    # border bar
    pygame.draw.line(
        surface,
        "darkgray",
        (LEFT_AXIS_BAR_X, 0),
        (LEFT_AXIS_BAR_X, SURFACE_HEIGHT),
    )

    item_vspace = 20
    axis_value = get_axis_value(pixel_value, item_vspace)

    start_neg = -int((state.max_consumption() / 1_000_000) / axis_value)
    end_pos = math.ceil((state.max_production() / 1_000_000) / axis_value)
    for i in range(start_neg, end_pos):
        render_axis_item(
            surface, font, label_right_gap, mid_height, pixel_value, i * axis_value
        )


def render_axis_item(
    surface: pygame.Surface,
    font: pygame.font.Font,
    label_right_gap: int,
    mid_height: int,
    pixel_value: float,
    axis_item: float,
) -> None:
    axis_item_str = '{:0.3g}'.format(abs(axis_item))
    (text_width, text_height) = font.size(axis_item_str)

    # refuse to render partially out of vertical bounds
    text_top = mid_height - (axis_item // pixel_value) - (text_height // 2)
    if text_top <= 0:
        return
    text_bottom = text_top + text_height
    if text_bottom >= SURFACE_HEIGHT:
        return

    # render axis item
    text_surface = font.render(axis_item_str, True, "white", "black")
    surface.blit(
        text_surface,
        (
            LEFT_AXIS_BAR_X - text_width - label_right_gap,
            text_top,
        ),
    )


def get_axis_value(pixel_value: float, item_vspace: int) -> float:
    item_value = pixel_value * item_vspace
    prev = 0.0
    for exp in range(-1, 2):
        for mult in [1, 2.5, 5]:
            curr = mult * float(pow(10, exp))
            if item_value > prev and item_value < curr:
                return curr
            prev = curr
    return 0.0


def get_mid_height(state: ReadingSpanGroup) -> int:
    max_prod = state.max_production()
    max_cons = state.max_consumption()
    ratio = max_prod / (max_prod + max_cons)
    return round(SURFACE_HEIGHT * ratio)


def get_pixel_value(state: ReadingSpanGroup) -> float:
    sum_of_max = state.max_consumption() + state.max_production()
    buffer = 3  # space for top/bottom edge and mid-line
    return sum_of_max / (SURFACE_HEIGHT - 3)
