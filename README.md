# Game2D_Alien
Projeto realizado em aula durante a disciplina AQS (Acompanhamento da Qualidade de Software).

Jogo 2D em Pygame refatorado com análise estática, princípios SOLID e testes automatizados.

## Estrutura

```
Game2D_Alien/
├── images/            # ship.bmp e alien.bmp
├── src/               # código do jogo
│   ├── alien_invasion.py   # ponto de entrada
│   ├── settings.py, ship.py, bullet.py, alien.py, fast_alien.py
│   ├── bullet_manager.py, fleet_manager.py, game_events.py, game_renderer.py
│   └── desconto.py         # exemplo didático de SOLID (L, I, D)
├── tests/             # testes com pytest
├── pyproject.toml     # configuração do ruff e do mypy
├── pytest.ini
├── .coveragerc
└── requirements.txt
```

## Instalação (Windows / PowerShell)

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Executar o jogo (sempre a partir da raiz do projeto)

```
python src/alien_invasion.py
```

Setas esquerda/direita movem a nave e a barra de espaço dispara.

## Análise estática

```
ruff check src tests
mypy src
```

## Testes, relatório e cobertura

```
pytest -v
pytest --html=relatorio.html
coverage run -m pytest
coverage report
```