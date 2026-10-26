"""Dublês de teste (stubs) usados nos testes."""

import pygame

from src.desconto import IDesconto


class StubSemDesconto(IDesconto):
    """Stub: simula um desconto que sempre retorna 0."""

    def calcular(self, valor: float) -> float:
        return 0


class StubShip:
    """Stub da nave: só tem o que o Bullet precisa (um rect em posição fixa)."""

    def __init__(self) -> None:
        self.rect = pygame.Rect(100, 500, 60, 48)
