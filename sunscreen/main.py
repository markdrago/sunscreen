import argparse
import pygame

import sunscreen.config
import sunscreen.envoy_fetcher
import sunscreen.loop
import sunscreen.pygame_event_loop
import sunscreen.renderer


def main():
    args = parse_args()
    config = sunscreen.config.Config("sunscreen.cfg")
    pygame.init()

    loop = sunscreen.loop.Loop()

    renderer = sunscreen.renderer.Renderer(args.fullscreen)
    loop.add_future(renderer.loop())

    envoy_fetcher = sunscreen.envoy_fetcher.EnvoyFetcher(
        config.getEnvoyHost(), config.getEnvoyAccessToken()
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
