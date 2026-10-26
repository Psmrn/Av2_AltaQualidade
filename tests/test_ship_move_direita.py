import pygame

from src.settings import Settings
from src.ship import Ship


def test_ship_move_direita() -> None:
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    settings = Settings()

    ship = Ship(screen, settings)

    x_inicial = ship.x

    # ação
    ship.moving_right = True
    ship.update()

    # verificação
    assert ship.x > x_inicial