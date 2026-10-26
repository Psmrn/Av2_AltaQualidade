import pygame

from src.bullet_manager import BulletManager
from src.fast_alien import FastAlien
from src.fleet_manager import FleetManager
from src.game_events import GameEventHandler
from src.game_renderer import GameRenderer
from src.settings import Settings
from src.ship import Ship


class AlienInvasion:
    """Gerencia o jogo e seus comportamentos.

    Agora a classe apenas monta os objetos e coordena o laço principal;
    cada responsabilidade foi movida para uma classe própria (SRP).
    """

    def __init__(self) -> None:
        """Construtor da classe que inicializa o jogo e cria os recursos básicos."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Criando uma instância da classe Ship para representar a nave espacial
        self.ship = Ship(self.screen, self.settings)

        # Cor do plano de fundo em RGB
        self.bg_color = self.settings.bg_color

        self.bullet_manager = BulletManager(self.screen, self.settings, self.ship)
        # OCP: basta trocar FastAlien por Alien (ou outro tipo) sem alterar o FleetManager
        self.fleet_manager = FleetManager(self.screen, self.settings, self.ship, FastAlien)
        self.event_handler = GameEventHandler(self.ship, self.bullet_manager)
        self.renderer = GameRenderer(
            self.screen,
            self.bg_color,
            self.ship,
            self.bullet_manager.bullets,
            self.fleet_manager.aliens,
        )

    def _update_game_state(self) -> None:
        """Atualiza a posição da nave, dos projéteis e dos alienígenas."""
        self.ship.update()
        self.bullet_manager.update_bullets(self.fleet_manager.aliens)
        self.fleet_manager.update_aliens()

    def run_game(self) -> None:
        """Cria um laço de repetição para a tela sempre ficar visível até
        que o usuário decida fechar a janela."""
        self.fleet_manager.create_fleet()  # Cria a frota de alienígenas para ser desenhada na tela

        while True:
            self.event_handler.check_events()
            self._update_game_state()
            self.renderer.render_screen()


if __name__ == "__main__":  # pragma: no cover
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
