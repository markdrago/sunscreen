import math
import pygame

SURFACE_HEIGHT = 380
SURFACE_WIDTH = 608


class RecentStateRenderer:
    def __init__(self, recent_state_provider):
        self.recent_state_provider = recent_state_provider
        self.state = None
        self.surface = None

    def render(self):
        state = self.recent_state_provider.get_state()
        if self.state == state and self.surface:
            return self.surface
        self.state = state
        self.surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        self.render_frame()
        self.render_bars()

        return self.surface

    def render_bars(self):
        right_buffer = 1
        width = 5
        buffer = 1
        # TODO: handle missing spans
        max_bar_count = min(len(self.state.spans), 24)

        pixel_value = self.pixel_value()
        mid_height = self.mid_height()

        next_x = SURFACE_WIDTH - right_buffer - width
        for i in range(len(self.state.spans) - 1, -1, -1):
            span = self.state.spans[i]
            cons_h = math.floor(span.consumption / pixel_value)
            prod_h = math.floor(span.production / pixel_value)

            self.surface.fill(
                "blue",
                pygame.Rect(next_x, mid_height - prod_h, width, prod_h),
            )
            self.surface.fill(
                "orange",
                pygame.Rect(next_x, mid_height + 1, width, cons_h),
            )

            next_x -= buffer + width

        # draw mid_height line
        pygame.draw.line(
            self.surface,
            "darkgray",
            (buffer, mid_height),
            (SURFACE_WIDTH - buffer, mid_height),
        )

    def render_frame(self):
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

    def mid_height(self):
        max_prod = self.state.max_production()
        max_cons = self.state.max_consumption()
        ratio = max_prod / (max_prod + max_cons)
        return round(SURFACE_HEIGHT * ratio)

    def pixel_value(self):
        sum_of_max = self.state.max_consumption() + self.state.max_production()
        buffer = 3  # space for top/bottom edge and mid-line
        return sum_of_max / (SURFACE_HEIGHT - 3)
