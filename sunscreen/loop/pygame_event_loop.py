from typing import Callable

import pygame

EventHandler = Callable[[pygame.event.Event], None]
Event = pygame.event.Event


class PygameEventLoop:
    def __init__(self, event_handler: EventHandler):
        self.event_handler = event_handler

    def run(self) -> None:
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.event_handler(event)
