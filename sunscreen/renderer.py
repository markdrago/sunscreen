import asyncio
import datetime
import pygame
import time

TARGET_FPS = 10
MIN_DELAY = 0.01
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class Renderer:
    def __init__(self, fullscreen):
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption("Sunscreen")
        pygame.mouse.set_visible(False)
        self.status_font = pygame.font.Font(None, size=24)

    async def loop(self):
        current_time = time.time()
        while True:
            last_time, current_time = current_time, time.time()
            target_delay = 1 / TARGET_FPS
            time_over_target = max(0, last_time - current_time - target_delay)
            delay = max(MIN_DELAY, target_delay - time_over_target)
            await asyncio.sleep(delay)
            try:
                self.render()
            except Exception as e:
                print("Render Exception", repr(e))

    def render(self):
        self.screen.fill("black")
        player_pos = pygame.Vector2(
            self.screen.get_width() / 2, self.screen.get_height() / 2
        )
        pygame.draw.circle(self.screen, "red", player_pos, 40)

        self.frame()
        self.status_time()

        pygame.display.flip()

    def frame(self):
        buffer = 16
        width = 2
        pygame.draw.rect(
            self.screen,
            "white",
            pygame.Rect(
                buffer,
                buffer,
                SCREEN_WIDTH - (buffer * 2),
                SCREEN_HEIGHT - (buffer * 2),
            ),
            width,
        )

    def status_time(self):
        now = datetime.datetime.now()
        now_str = now.strftime("%b %d %H:%M:%S")
        (text_width, text_height) = self.status_font.size(now_str)
        text_surface = self.status_font.render(now_str, True, "gray50", "black")
        self.screen.blit(
            text_surface, (SCREEN_WIDTH - 15 - text_width, SCREEN_HEIGHT - text_height)
        )
