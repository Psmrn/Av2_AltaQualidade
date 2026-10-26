import pygame
from pygame.sprite import Sprite

from src.settings import Settings


class Alien(Sprite):
    """Gerencia os alienígenas."""

    def __init__(self, alien_invasion_screen: pygame.Surface, alien_invasion_settings: Settings) -> None:
        """Inicializa o alienígena e define sua posição inicial."""
        super().__init__()  # Inicializa corretamente a classe como um sprite do Pygame
        self.screen = alien_invasion_screen
        self.settings = alien_invasion_settings

        # Carrega a imagem do alienígena e obtém seu rect
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Inicia cada novo alienígena próximo à parte superior esquerda da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)  # Posição horizontal em ponto flutuante para movimentos suaves
        self.y = float(self.rect.y)  # Posição vertical (antes era criada fora do __init__)

    def update(self) -> None:
        """Move o alienígena para a direita ou para a esquerda, conforme a direção da frota."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = int(self.x)

    def check_edges(self) -> bool:
        """Retorna True se o alienígena estiver na borda da tela."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0