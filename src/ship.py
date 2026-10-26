import pygame
from pygame.sprite import Sprite

from src.settings import Settings


class Ship(Sprite):
    """Gerencia a nave espacial."""

    def __init__(self, alien_invasion_screen: pygame.Surface, alien_invasion_settings: Settings) -> None:
        """Inicializa a nave e define sua posição inicial."""
        super().__init__()  # Ship passa a ser um Sprite, como Bullet e Alien (exigido pela tipagem do pygame)
        self.screen = alien_invasion_screen
        self.settings = alien_invasion_settings
        self.screen_rect = self.screen.get_rect()  # Rect representa posições e áreas retangulares

        # Carrega a imagem da nave e obtém seu rect
        self.image = pygame.image.load("images/ship.bmp")
        # O pygame trata os elementos como retângulos, tornando seu processamento eficiente
        self.rect = self.image.get_rect()
        # Posiciona a nave no centro inferior da tela
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False  # Controle do movimento da nave para a direita
        self.moving_left = False  # Controle do movimento da nave para a esquerda

        self.x = float(self.rect.x)  # Posição horizontal em ponto flutuante para movimentos suaves

    def blitme(self) -> None:
        """Desenha a nave em sua posição atual."""
        # O método blit desenha a imagem da nave na tela usando as coordenadas do rect
        self.screen.blit(self.image, self.rect)  # ('o que', 'onde')

    def update(self) -> None:
        """Atualiza a posição da nave com base nas variáveis de controle."""
        if self.moving_right and self.rect.right < self.screen_rect.right:  # Não deixa sair pela direita
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:  # Não deixa sair pela esquerda
            self.x -= self.settings.ship_speed

        # Atualiza o rect da nave
        self.rect.x = int(self.x)