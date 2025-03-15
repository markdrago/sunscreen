import pygame

sun_img = pygame.image.load("icons/sun.svg")
plug_img = pygame.image.load("icons/plug.svg")
import_img = pygame.image.load("icons/import.svg")
export_img = pygame.image.load("icons/export.svg")


def sun() -> pygame.Surface:
    return sun_img


def plug() -> pygame.Surface:
    return plug_img


def import_icon() -> pygame.Surface:
    return import_img


def export() -> pygame.Surface:
    return export_img
