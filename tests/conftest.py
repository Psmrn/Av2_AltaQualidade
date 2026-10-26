"""Configurações compartilhadas pelos testes.

- Usa o driver de vídeo "dummy" do SDL: o pygame funciona sem abrir janela real.
- Executa cada teste a partir da raiz do projeto, para que 'images/...' seja encontrado.
"""

import os
from collections.abc import Iterator
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402  (precisa vir depois das variáveis de ambiente)
import pytest  # noqa: E402

from src.settings import Settings  # noqa: E402

RAIZ_DO_PROJETO = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def executar_na_raiz(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(RAIZ_DO_PROJETO)


@pytest.fixture
def settings() -> Settings:
    """Um Settings novo para cada teste (fleet_direction muda durante o jogo)."""
    return Settings()


@pytest.fixture
def screen(settings: Settings) -> Iterator[pygame.Surface]:
    """Tela de testes (invisível, por causa do driver dummy)."""
    pygame.init()
    tela = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    yield tela
    pygame.quit()