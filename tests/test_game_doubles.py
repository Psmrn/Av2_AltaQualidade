"""Stub e mock aplicados ao jogo Game2D_Alien (momento interativo da Aula 08)."""

import pygame
from pytest_mock import MockerFixture

from src.alien_invasion import AlienInvasion
from src.bullet import Bullet
from src.fleet_manager import FleetManager
from src.game_events import GameEventHandler
from src.settings import Settings
from src.ship import Ship
from tests.doubles import StubShip


# ----------------------------------------------------------------------
# STUB: o Bullet é testado sem depender da nave real (nem da imagem dela)
# ----------------------------------------------------------------------
def test_bullet_com_stub_da_nave(screen: pygame.Surface, settings: Settings) -> None:
    nave_falsa = StubShip()

    bullet = Bullet(screen, settings, nave_falsa)  # type: ignore[arg-type]

    assert bullet.rect.midtop == nave_falsa.rect.midtop


# ----------------------------------------------------------------------
# MOCK: verificamos as INTERAÇÕES do GameEventHandler
# ----------------------------------------------------------------------
def test_barra_de_espaco_dispara_projetil(mocker: MockerFixture) -> None:
    ship = mocker.Mock()
    bullet_manager = mocker.Mock()
    evento = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    mocker.patch("pygame.event.get", return_value=[evento])  # Teclado simulado

    handler = GameEventHandler(ship, bullet_manager)
    handler.check_events()

    bullet_manager.fire_bullet.assert_called_once()


def test_seta_direita_liga_movimento_da_nave(mocker: MockerFixture) -> None:
    ship = mocker.Mock()
    ship.moving_right = False
    bullet_manager = mocker.Mock()
    evento = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
    mocker.patch("pygame.event.get", return_value=[evento])

    GameEventHandler(ship, bullet_manager).check_events()

    assert ship.moving_right is True
    bullet_manager.fire_bullet.assert_not_called()


def test_fechar_janela_encerra_o_jogo(mocker: MockerFixture) -> None:
    mocker.patch("pygame.event.get", return_value=[pygame.event.Event(pygame.QUIT)])
    mock_exit = mocker.patch("sys.exit")  # Impede que o pytest seja encerrado de verdade

    GameEventHandler(mocker.Mock(), mocker.Mock()).check_events()

    mock_exit.assert_called_once()


def test_colisao_com_a_nave_encerra_o_jogo(mocker: MockerFixture, screen: pygame.Surface, settings: Settings) -> None:
    mock_exit = mocker.patch("sys.exit")
    ship = Ship(screen, settings)
    fleet = FleetManager(screen, settings, ship)
    fleet.create_fleet()
    alien = fleet.aliens.sprites()[0]
    alien.rect.center = ship.rect.center  # Coloca um alienígena em cima da nave
    alien.x = float(alien.rect.x)

    fleet.update_aliens()

    mock_exit.assert_called_once()


# ----------------------------------------------------------------------
# MOCK no laço principal: AlienInvasion delega o trabalho para cada classe
# ----------------------------------------------------------------------
def test_alien_invasion_delega_atualizacao_para_os_gerenciadores(mocker: MockerFixture) -> None:
    jogo = AlienInvasion()
    jogo.ship = mocker.Mock()
    jogo.bullet_manager = mocker.Mock()
    jogo.fleet_manager = mocker.Mock()

    jogo._update_game_state()

    jogo.ship.update.assert_called_once()
    jogo.bullet_manager.update_bullets.assert_called_once_with(jogo.fleet_manager.aliens)
    jogo.fleet_manager.update_aliens.assert_called_once()
    pygame.quit()
