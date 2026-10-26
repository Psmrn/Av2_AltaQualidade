"""Novos testes unitários para as classes do jogo Game2D_Alien."""

import pygame

from src.alien import Alien
from src.bullet import Bullet
from src.bullet_manager import BulletManager
from src.fast_alien import FastAlien
from src.fleet_manager import FleetManager
from src.settings import Settings
from src.ship import Ship


# ----------------------------------------------------------------------
# Ship
# ----------------------------------------------------------------------
def test_ship_comeca_no_centro_inferior(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    assert ship.rect.midbottom == screen.get_rect().midbottom


def test_ship_move_esquerda(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    x_inicial = ship.x

    ship.moving_left = True
    ship.update()

    assert ship.x < x_inicial


def test_ship_parada_nao_se_move(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    x_inicial = ship.x

    ship.update()

    assert ship.x == x_inicial


def test_ship_nao_sai_pela_direita(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    ship.rect.right = screen.get_rect().right
    ship.x = float(ship.rect.x)
    x_inicial = ship.x

    ship.moving_right = True
    ship.update()

    assert ship.x == x_inicial


# ----------------------------------------------------------------------
# Bullet / BulletManager
# ----------------------------------------------------------------------
def test_bullet_nasce_no_topo_da_nave(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    bullet = Bullet(screen, settings, ship)
    assert bullet.rect.midtop == ship.rect.midtop


def test_bullet_sobe_ao_atualizar(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    bullet = Bullet(screen, settings, ship)
    y_inicial = bullet.y

    bullet.update()

    assert bullet.y == y_inicial - settings.bullet_speed


def test_bullet_manager_respeita_limite_de_projeteis(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    manager = BulletManager(screen, settings, ship)

    for _ in range(settings.bullet_allowed + 3):
        manager.fire_bullet()

    assert len(manager.bullets) == settings.bullet_allowed


def test_bullet_manager_remove_projetil_fora_da_tela(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    manager = BulletManager(screen, settings, ship)
    manager.fire_bullet()
    bullet = manager.bullets.sprites()[0]
    bullet.y = -100.0  # Coloca o projétil acima da tela

    manager.update_bullets(pygame.sprite.Group())

    assert len(manager.bullets) == 0


# ----------------------------------------------------------------------
# Alien / FastAlien / FleetManager
# ----------------------------------------------------------------------
def test_alien_detecta_borda(screen: pygame.Surface, settings: Settings) -> None:
    alien = Alien(screen, settings)
    assert alien.check_edges() is False

    alien.rect.right = screen.get_rect().right
    assert alien.check_edges() is True


def test_fast_alien_e_mais_rapido_que_alien(screen: pygame.Surface, settings: Settings) -> None:
    alien = Alien(screen, settings)
    fast = FastAlien(screen, settings)
    x_alien, x_fast = alien.x, fast.x

    alien.update()
    fast.update()

    assert (fast.x - x_fast) > (alien.x - x_alien)


def test_fleet_manager_cria_frota(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    fleet = FleetManager(screen, settings, ship)

    fleet.create_fleet()

    assert len(fleet.aliens) > 0


def test_fleet_manager_usa_o_tipo_de_alien_recebido(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    fleet = FleetManager(screen, settings, ship, FastAlien)

    fleet.create_fleet()

    assert all(type(alien) is FastAlien for alien in fleet.aliens)


def test_frota_desce_e_inverte_direcao_na_borda(screen: pygame.Surface, settings: Settings) -> None:
    ship = Ship(screen, settings)
    fleet = FleetManager(screen, settings, ship)
    fleet.create_fleet()
    primeiro = fleet.aliens.sprites()[0]
    y_inicial = primeiro.rect.y
    primeiro.rect.right = screen.get_rect().right  # Força um alienígena na borda

    fleet.update_aliens()

    assert settings.fleet_direction == -1
    assert primeiro.rect.y == y_inicial + settings.fleet_drop_speed