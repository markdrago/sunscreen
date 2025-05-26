from typing import Protocol
from abc import abstractmethod

import pygame


class Renderable(Protocol):
    @abstractmethod
    def render(self) -> pygame.Surface:
        raise NotImplementedError
