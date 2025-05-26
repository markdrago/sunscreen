from abc import abstractmethod
from typing import Protocol

import pygame


class Renderable(Protocol):
    @abstractmethod
    def render(self) -> pygame.Surface:
        raise NotImplementedError()
