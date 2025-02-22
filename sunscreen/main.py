import argparse
import asyncio
import pygame

from .config import Config
from .state.db import Db
from .envoy.envoy_fetcher import EnvoyFetcher
from .loop.loop import Loop
from .loop.pygame_event_loop import PygameEventLoop
from .state.recent_state import RecentState
from .render.recent_state_renderer import RecentStateRenderer
from .render.renderer import Renderer


def main() -> None:
    args = parse_args()
    config = Config("sunscreen.cfg")
    pygame.display.init()
    pygame.font.init()

    loop = Loop()

    db = Db(config.getDbPath())
    loop.add_future(db.init())

    recent_state = RecentState(db)
    loop.add_future(recent_state.refresh())
    db.set_listener(recent_state.new_reading_notice)

    recent_state_renderer = RecentStateRenderer(recent_state)

    renderer = Renderer(args.fullscreen, recent_state_renderer)
    loop.add_future(renderer.loop())

    envoy_fetcher = EnvoyFetcher(
        config.getEnvoyHost(), config.getEnvoyAccessToken(), db.record_reading
    )
    loop.add_future(envoy_fetcher.loop())

    loop.set_event_handler(event_handler)
    pygame_event_loop = PygameEventLoop(loop.queue_add_event)
    loop.add_external_loop(pygame_event_loop.run)

    try:
        loop.run()
    finally:
        print("Quitting")
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        pygame.quit()


def event_handler(event: pygame.event.Event) -> None:
    print("event", event)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sunscreen", description="Displays stats from an enphase solar system."
    )
    parser.add_argument("-f", "--fullscreen", action="store_true")
    return parser.parse_args()
