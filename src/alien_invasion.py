import sys

import pygame

from alien import Alien
from bullet import Bullet
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Gerencia o jogo e seus comportamentos."""

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

        self.bullets: pygame.sprite.Group[Bullet] = pygame.sprite.Group()  # Projéteis disparados pela nave
        self.aliens: pygame.sprite.Group[Alien] = pygame.sprite.Group()  # Alienígenas presentes no jogo

    def create_fleet(self) -> None:
        """Cria uma frota de alienígenas."""
        # Cria um alienígena e calcula o número de alienígenas em uma linha
        # O espaçamento entre os alienígenas é igual a um alienígena
        alien = Alien(self.screen, self.settings)
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
                alien = Alien(self.screen, self.settings)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = int(alien.x)
                alien.y = alien_height + 2 * alien_height * row_number
                alien.rect.y = int(alien.y)
                self.aliens.add(alien)

    def run_game(self) -> None:
        """Cria um laço de repetição para a tela sempre ficar visível até
        que o usuário decida fechar a janela."""

        self.create_fleet()  # Cria a frota de alienígenas para ser desenhada na tela

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # Uma tecla foi pressionada
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = True
                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = True
                    elif event.key == pygame.K_SPACE and len(self.bullets) < self.settings.bullet_allowed:
                        # Só dispara se o limite de projéteis na tela ainda não foi atingido
                        new_bullet = Bullet(self.screen, self.settings, self.ship)
                        self.bullets.add(new_bullet)  # Adiciona o novo projétil ao grupo de projéteis

                elif event.type == pygame.KEYUP:  # Uma tecla foi liberada
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False
                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = False

            # Redesenha a tela a cada passagem pelo laço
            self.screen.fill(self.bg_color)

            # Redesenha a nave em sua posição atual
            self.ship.blitme()

            # Desenha os alienígenas do grupo na tela
            self.aliens.draw(self.screen)

            # Atualiza a posição da nave com base nas variáveis de controle
            self.ship.update()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()  # Desenha cada projétil na tela

            self.bullets.update()  # Atualiza a posição de cada projétil
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:  # O projétil saiu pela parte de cima da tela
                    self.bullets.remove(bullet)

            # Se um projétil atingir um alienígena, remove os dois
            pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

            for alien in self.aliens.sprites():
                if alien.check_edges():  # Algum alienígena atingiu a borda da tela
                    for fleet_alien in self.aliens.sprites():
                        fleet_alien.rect.y += self.settings.fleet_drop_speed  # Desce a frota
                    self.settings.fleet_direction *= -1  # Inverte a direção da frota
                    break  # Basta um alienígena na borda para mudar a direção

            # Torna visível a tela mais recente
            pygame.display.flip()

            self.bullets.update()  # Atualiza a posição de cada projétil

            self.aliens.update()  # Atualiza a posição de cada alienígena

            if pygame.sprite.spritecollideany(self.ship, self.aliens):  # A nave colidiu com algum alienígena
                print("A nave foi atingida!")
                sys.exit()  # Encerra o jogo


if __name__ == "__main__":
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()