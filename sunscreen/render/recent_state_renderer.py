import math

import pygame

from ..state.reading_span_group import ReadingSpanGroup
from ..state.recent_state import RecentState

SURFACE_HEIGHT = 380
SURFACE_WIDTH = 608
LEFT_AXIS_BAR_X = 30


class RecentStateRenderer:
    def __init__(self, state: ReadingSpanGroup):
        self.state = state
        self.surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        self.axis_font = pygame.font.Font(None, size=22)

    def render(self) -> pygame.Surface:
        # self.render_frame()
        if self.state.max_consumption() + self.state.max_production() > 0:
            self.mid_height = self.get_mid_height()
            self.pixel_value = self.get_pixel_value()
            self.render_bars()
            self.render_axis()

        return self.surface

    def render_frame(self) -> None:
        width = 1
        pygame.draw.rect(
            self.surface,
            "white",
            pygame.Rect(
                0,
                0,
                SURFACE_WIDTH,
                SURFACE_HEIGHT,
            ),
            width,
        )

    def render_bars(self) -> None:
        right_buffer = 1
        width = 5
        buffer = 1

        next_x = SURFACE_WIDTH - right_buffer - width
        for i in range(len(self.state.spans) - 1, -1, -1):
            span = self.state.spans[i]
            cons_h = math.floor(span.consumption / self.pixel_value)
            prod_h = math.floor(span.production / self.pixel_value)

            self.surface.fill(
                "blue",
                pygame.Rect(next_x, self.mid_height - prod_h, width, prod_h),
            )
            self.surface.fill(
                "orange",
                pygame.Rect(next_x, self.mid_height + 1, width, cons_h),
            )

            next_x -= buffer + width

        # draw mid_height line
        pygame.draw.line(
            self.surface,
            "darkgray",
            (LEFT_AXIS_BAR_X, self.mid_height),
            (SURFACE_WIDTH - buffer, self.mid_height),
        )

    def render_axis(self) -> None:
        label_right_gap = 2
        pixel_value_kw = self.pixel_value / 1_000_000  # milliwatts -> kilowatts

        # border bar
        pygame.draw.line(
            self.surface,
            "darkgray",
            (LEFT_AXIS_BAR_X, 0),
            (LEFT_AXIS_BAR_X, SURFACE_HEIGHT),
        )
        item_vspace = 28
        axis_value = get_axis_value(pixel_value_kw, item_vspace)

        start_neg = -int((self.state.max_consumption() / 1_000_000) / axis_value)
        end_pos = math.ceil((self.state.max_production() / 1_000_000) / axis_value)
        for i in range(start_neg, end_pos):
            self.render_axis_item(label_right_gap, pixel_value_kw, i * axis_value)

    def render_axis_item(
        self,
        label_right_gap: int,
        pixel_value_kw: float,
        axis_item: float,
    ) -> None:
        axis_item_str = "{:0.3g}".format(abs(axis_item))
        (text_width, text_height) = self.axis_font.size(axis_item_str)

        # refuse to render partially out of vertical bounds
        text_top = self.mid_height - (axis_item // pixel_value_kw) - (text_height // 2)
        if text_top <= 0:
            return
        text_bottom = text_top + text_height
        if text_bottom >= SURFACE_HEIGHT:
            return

        # render axis item
        text_surface = self.axis_font.render(axis_item_str, True, "white", "black")
        self.surface.blit(
            text_surface,
            (
                LEFT_AXIS_BAR_X - text_width - label_right_gap,
                text_top,
            ),
        )

    def get_mid_height(self) -> int:
        max_prod = self.state.max_production()
        max_cons = self.state.max_consumption()
        ratio = max_prod / (max_prod + max_cons)
        return round(SURFACE_HEIGHT * ratio)

    def get_pixel_value(self) -> float:
        sum_of_max = self.state.max_consumption() + self.state.max_production()
        buffer = 3  # space for top/bottom edge and mid-line
        return sum_of_max / (SURFACE_HEIGHT - 3)


def get_axis_value(pixel_value_kw: float, item_vspace: int) -> float:
    item_value = pixel_value_kw * item_vspace
    prev = 0.0
    # Goal of code below is to choose interesting / rounded axis tick marks
    # Should end up with steps like; .01, .25, 0.5, 1.0, 2.5, 10, 25, etc.
    for exp in range(-1, 2):
        for mult in [1, 2.5, 5]:
            curr = mult * float(pow(10, exp))
            if item_value > prev and item_value < curr:
                return curr
            prev = curr
    return 0.0
