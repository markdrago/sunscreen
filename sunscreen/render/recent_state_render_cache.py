from typing import Optional

import pygame

from ..state.reading_span_group import ReadingSpanGroup
from ..state.recent_state import RecentState
from .recent_state_renderer import RecentStateRenderer


class RecentStateRenderCache:
    def __init__(self, recent_state_provider: RecentState):
        self.recent_state_provider = recent_state_provider
        self.state: Optional[ReadingSpanGroup] = None
        self.surface: Optional[pygame.Surface] = None

    def render(self) -> pygame.Surface:
        state = self.recent_state_provider.get_state()
        if self.state == state and self.surface:
            return self.surface

        self.state = state
        renderer = RecentStateRenderer(self.state)
        self.surface = renderer.render()
        return self.surface
