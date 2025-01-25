import pygame


class PygameEventLoop:
    def __init__(self, event_handler):
        self.event_handler = event_handler

    def run(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.event_handler(event)
