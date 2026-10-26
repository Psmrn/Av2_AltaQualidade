from alien import Alien


class FastAlien(Alien):
    """Alienígena mais rápido: estende Alien sem modificar a classe original (OCP)."""

    def update(self) -> None:
        """Move o alienígena com o dobro da velocidade configurada."""
        self.x += (self.settings.alien_speed * 2) * self.settings.fleet_direction
        self.rect.x = int(self.x)