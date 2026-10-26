from __future__ import annotations

import sys

import pygame

from src.alien import Alien
from src.settings import Settings
from src.ship import Ship


class FleetManager:
    """Responsável por criar e gerenciar a frota de alienígenas."""

    def __init__(
        self, screen: pygame.Surface, settings: Settings, ship: Ship, alien_class: type[Alien] = Alien
    ) -> None:
        self.screen = screen
        self.settings = settings
        self.ship = ship
        self.aliens: pygame.sprite.Group[Alien] = pygame.sprite.Group()
        # OCP: o tipo de alienígena é recebido de fora. Novos tipos (FastAlien, BigBoss...)
        # são criados por herança, sem alterar esta classe.
        self.alien_class = alien_class

    def _create_alien(self, alien_number: int, row_number: int, alien_width: int, alien_height: int) -> None:
        """Cria um alienígena e o posiciona na linha."""
        alien = self.alien_class(self.screen, self.settings)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = int(alien.x)
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.y = int(alien.y)
        self.aliens.add(alien)

    def create_fleet(self) -> None:
        """Cria uma frota de alienígenas."""
        # Cria um alienígena e calcula o número de alienígenas em uma linha
        # O espaçamento entre os alienígenas é igual a um alienígena
        alien = self.alien_class(self.screen, self.settings)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            # Cria uma linha de alienígenas
            for alien_number in range(number_aliens_x):
                # Cria um alienígena e o posiciona na linha
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def update_aliens(self) -> None:
        """Verifica se a frota está em uma borda, atualiza as posições e checa colisão com a nave."""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_ship_collision()

    def _check_fleet_edges(self) -> None:
        """Responde apropriadamente se algum alienígena tiver alcançado uma borda."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """Desce a frota e muda sua direção."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_ship_collision(self) -> None:
        """Verifica se a nave colidiu com algum alienígena e encerra o jogo."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("A nave foi atingida!")
            sys.exit()