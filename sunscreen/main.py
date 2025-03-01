import argparse
import asyncio

import pygame

from .config import Config
from .envoy.envoy_fetcher import EnvoyFetcher
from .loop.loop import Loop
from .loop.pygame_event_loop import PygameEventLoop
from .render.recent_state_render_cache import RecentStateRenderCache
from .render.renderer import Renderer
from .state.db import Db
from .state.recent_state import RecentState
from .state.state_refresher import StateRefresher


def main() -> None:
    args = parse_args()
    config = Config("sunscreen.cfg")
    pygame.display.init()
    pygame.font.init()

    loop = Loop()

    db = Db(config.getDbPath())
    loop.add_future(db.init())

    recent_state = RecentState(db)
    state_refresher = StateRefresher(recent_state)
    loop.add_future(state_refresher.loop())
    db.set_listener(state_refresher.handle_new_reading)

    recent_state_renderer = RecentStateRenderCache(recent_state)

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
