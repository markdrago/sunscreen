import asyncio
import pygame
import time

TARGET_FPS = 10
MIN_DELAY = 0.01


class Renderer:
    def __init__(self, fullscreen):
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((640, 480), flags)
        pygame.display.set_caption("Sunscreen")

    async def loop(self):
        current_time = time.time()
        while True:
            last_time, current_time = current_time, time.time()
            target_delay = 1 / TARGET_FPS
            time_over_target = max(0, last_time - current_time - target_delay)
            delay = max(MIN_DELAY, target_delay - time_over_target)
            await asyncio.sleep(delay)
            self.render()

    def render(self):
        self.screen.fill("blue")

        player_pos = pygame.Vector2(
            self.screen.get_width() / 2, self.screen.get_height() / 2
        )
        pygame.draw.circle(self.screen, "red", player_pos, 40)

        pygame.display.flip()
