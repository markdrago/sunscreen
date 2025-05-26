from typing import Callable, Optional

import pygame

from ..state.reading_span_group import ReadingSpanGroup
from ..state.recent_state import RecentState
from .renderable import Renderable


class RecentStateRenderCache:
    def __init__(
        self,
        recent_state_provider: RecentState,
        renderer_factory: Callable[[ReadingSpanGroup], Renderable],
    ) -> None:
        self.renderer_factory = renderer_factory
        self.recent_state_provider = recent_state_provider
        self.state: Optional[ReadingSpanGroup] = None
        self.surface: Optional[pygame.Surface] = None

    def render(self) -> pygame.Surface:
        state = self.recent_state_provider.get_state()
        if self.state == state and self.surface:
            return self.surface

        self.state = state
        renderer = self.renderer_factory(self.state)
        self.surface = renderer.render()
        return self.surface
