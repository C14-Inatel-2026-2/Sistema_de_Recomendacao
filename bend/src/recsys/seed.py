"""Dados iniciais para desenvolver a Home sem depender do cadastro."""
from datetime import datetime, timezone

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracao

JOGOS = [
    ("witcher3", "The Witcher 3", "rpg"),
    ("eldenring", "Elden Ring", "rpg"),
    ("bg3", "Baldur's Gate 3", "rpg"),
    ("skyrim", "Skyrim", "rpg"),
    ("hades", "Hades", "acao"),
    ("doom", "Doom Eternal", "acao"),
    ("gow", "God of War", "acao"),
    ("celeste", "Celeste", "plataforma"),
    ("hollow", "Hollow Knight", "plataforma"),
    ("mario", "Super Mario Odyssey", "plataforma"),
    ("civ6", "Civilization VI", "estrategia"),
    ("xcom", "XCOM 2", "estrategia"),
    ("aoe2", "Age of Empires II", "estrategia"),
    ("stardew", "Stardew Valley", "simulacao"),
    ("cities", "Cities: Skylines", "simulacao"),
    ("ets2", "Euro Truck Simulator 2", "simulacao"),
    ("rocket", "Rocket League", "esporte"),
    ("forza", "Forza Horizon 5", "corrida"),
]

USUARIOS = [
    ("alice", "Alice"),
    ("bruno", "Bruno"),
    ("carla", "Carla"),
    ("diego", "Diego"),
    ("bia", "Bia"),
]

AVALIACOES = {
    "alice": {"witcher3": 5.0, "eldenring": 4.5, "hades": 4.0, "civ6": 2.0},
    "bruno": {"witcher3": 5.0, "bg3": 4.5, "skyrim": 4.0, "stardew": 3.0},
    "carla": {"celeste": 5.0, "hollow": 4.5, "hades": 4.5, "stardew": 4.0},
    "diego": {"civ6": 5.0, "xcom": 4.5, "aoe2": 4.0, "cities": 4.0, "doom": 3.0},
    "bia": {"stardew": 5.0, "cities": 4.5, "celeste": 4.0, "mario": 4.5, "rocket": 3.0},
}


def popular(
    usuarios: dict[str, Usuario],
    catalogo: dict[str, Item],
    repositorio: RepositorioInteracao,
) -> None:
    for id_, titulo, categoria in JOGOS:
        catalogo[id_] = Item(id=id_, titulo=titulo, categoria=categoria)
    for id_, nome in USUARIOS:
        usuarios[id_] = Usuario(id=id_, nome=nome)
    agora = datetime.now(timezone.utc)
    for usuario_id, notas in AVALIACOES.items():
        for item_id, nota in notas.items():
            repositorio.salvar(
                Interacao(usuario_id=usuario_id, item_id=item_id, nota=nota, timestamp=agora)
            )
