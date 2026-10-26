import pygame
from pygame.sprite import Sprite

from settings import Settings
from ship import Ship


# Conceito de HERANÇA: Bullet herda atributos e métodos de Sprite, classe do Pygame para objetos visuais.
# A classe Bullet gerencia os projéteis disparados pela nave: posição, movimento e aparência.
class Bullet(Sprite):
    """Gerencia os projéteis disparados pela nave."""

    def __init__(
        self, alien_invasion_screen: pygame.Surface, alien_invasion_settings: Settings, alien_invasion_ship: Ship
    ) -> None:
        """Cria um objeto para o projétil na posição atual da nave."""
        super().__init__()  # Inicializa corretamente a classe como um sprite do Pygame
        self.screen = alien_invasion_screen
        self.settings = alien_invasion_settings
        self.ship = alien_invasion_ship
        self.color = self.settings.bullet_color
        # Cria um rect para o projétil em (0, 0) e depois define a posição correta
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.image = pygame.Surface((self.settings.bullet_width, self.settings.bullet_height))  # Exigido por Sprite
        self.image.fill(self.color)
        self.rect.midtop = self.ship.rect.midtop  # Posiciona o projétil na parte superior da nave
        self.y = float(self.rect.y)  # Posição vertical em ponto flutuante para movimentos suaves

    def update(self) -> None:
        """Move o projétil para cima na tela."""
        self.y -= self.settings.bullet_speed  # Diminui a coordenada y
        self.rect.y = int(self.y)  # Atualiza o rect com a nova coordenada y

    def draw_bullet(self) -> None:
        """Desenha o projétil na tela."""
        pygame.draw.rect(self.screen, self.color, self.rect)
