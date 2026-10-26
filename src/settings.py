class Settings:
    """Classe que armazena todas as configurações do jogo."""

    def __init__(self) -> None:
        # Configurações da tela
        self.screen_width: int = 1366
        self.screen_height: int = 768
        self.bg_color: tuple[int, int, int] = (230, 230, 230)  # Cor de fundo (cinza claro)
        self.ship_speed: float = 1.5  # Velocidade da nave

        # Configurações dos projéteis
        self.bullet_speed: float = 1.0  # Velocidade dos projéteis
        self.bullet_width: int = 3  # Largura dos projéteis
        self.bullet_height: int = 15  # Altura dos projéteis
        self.bullet_color: tuple[int, int, int] = (60, 60, 60)  # Cor dos projéteis
        self.bullet_allowed: int = 1  # Número máximo de projéteis na tela ao mesmo tempo

        # Configurações do alien
        self.alien_speed: float = 0.3  # Velocidade dos alienígenas
        self.fleet_drop_speed: int = 10  # Quanto a frota desce ao atingir uma borda
        self.fleet_direction: int = 1  # Direção da frota: 1 = direita; -1 = esquerda
