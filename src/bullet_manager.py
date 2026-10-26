from __future__ import annotations

import pygame

from src.alien import Alien
from src.bullet import Bullet
from src.settings import Settings
from src.ship import Ship


class BulletManager:
    """Responsável apenas por criar, atualizar e remover os projéteis."""

    def __init__(self, screen: pygame.Surface, settings: Settings, ship: Ship) -> None:
        self.screen = screen
        self.settings = settings
        self.ship = ship
        self.bullets: pygame.sprite.Group[Bullet] = pygame.sprite.Group()

    def fire_bullet(self) -> None:
        """Dispara um projétil se o limite de projéteis ainda não tiver sido alcançado."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self.screen, self.settings, self.ship)
            self.bullets.add(new_bullet)

    def update_bullets(self, aliens: pygame.sprite.Group[Alien]) -> None:
        """Atualiza a posição dos projéteis e se livra dos projéteis antigos."""
        self.bullets.update()
        self._remove_offscreen_bullets()
        self._check_bullet_alien_collisions(aliens)

    def _remove_offscreen_bullets(self) -> None:
        """Remove os projéteis que desapareceram da tela."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_alien_collisions(self, aliens: pygame.sprite.Group[Alien]) -> None:
        """Verifica colisões entre projéteis e alienígenas, removendo ambos."""
        pygame.sprite.groupcollide(self.bullets, aliens, True, True)