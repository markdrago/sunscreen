import argparse
import asyncio
import pygame

import sunscreen.config
import sunscreen.db
import sunscreen.envoy_fetcher
import sunscreen.loop
import sunscreen.pygame_event_loop
import sunscreen.recent_state
import sunscreen.recent_state_renderer
import sunscreen.renderer


def main():
    args = parse_args()
    config = sunscreen.config.Config("sunscreen.cfg")
    pygame.display.init()
    pygame.font.init()

    loop = sunscreen.loop.Loop()

    db = sunscreen.db.Db(config.getDbPath())
    loop.add_future(db.init())

    recent_state = sunscreen.recent_state.RecentState(db)
    loop.add_future(recent_state.refresh())
    db.set_listener(recent_state.new_reading_notice)

    recent_state_renderer = sunscreen.recent_state_renderer.RecentStateRenderer(
        recent_state
    )

    renderer = sunscreen.renderer.Renderer(args.fullscreen, recent_state_renderer)
    loop.add_future(renderer.loop())

    envoy_fetcher = sunscreen.envoy_fetcher.EnvoyFetcher(
        config.getEnvoyHost(), config.getEnvoyAccessToken(), db.record_reading
    )
    loop.add_future(envoy_fetcher.loop())

    loop.set_event_handler(event_handler)
    pygame_event_loop = sunscreen.pygame_event_loop.PygameEventLoop(
        loop.queue_add_event
    )
    loop.add_external_loop(pygame_event_loop.run)

    try:
        loop.run()
    finally:
        print("Quitting")
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        pygame.quit()


def event_handler(event):
    print("event", event)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="sunscreen", description="Displays stats from an enphase solar system."
    )
    parser.add_argument("-f", "--fullscreen", action="store_true")
    return parser.parse_args()
