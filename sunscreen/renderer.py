import pygame


class Renderer:
    def __init__(self, fullscreen):
        pygame.init()
        flags = 0
        if fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((640, 480), flags)
        self.clock = pygame.time.Clock()

    def render(self):
        self.screen.fill("blue")

        player_pos = pygame.Vector2(
            self.screen.get_width() / 2, self.screen.get_height() / 2
        )
        pygame.draw.circle(self.screen, "red", player_pos, 40)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.render()
            self.clock.tick(60)  # limit FPS to 60
        self.quit()

    def quit(self):
        pygame.quit()
