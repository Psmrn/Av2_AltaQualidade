from __future__ import annotations

import pygame

from alien import Alien
from bullet import Bullet
from ship import Ship


class GameRenderer:
    """Responsável apenas por desenhar os elementos do jogo na tela."""

    def __init__(
        self,
        screen: pygame.Surface,
        bg_color: tuple[int, int, int],
        ship: Ship,
        bullets: pygame.sprite.Group[Bullet],
        aliens: pygame.sprite.Group[Alien],
    ) -> None:
        self.screen = screen
        self.bg_color = bg_color
        self.ship = ship
        self.bullets = bullets
        self.aliens = aliens

    def render_screen(self) -> None:
        """Redesenha a tela a cada passagem pelo laço."""
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self._draw_bullets()
        pygame.display.flip()

    def _draw_bullets(self) -> None:
        """Desenha os projéteis na tela."""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()