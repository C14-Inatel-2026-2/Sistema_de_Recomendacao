from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Interacao:
    usuario_id: str
    item_id: str
    nota: float
    timestamp: datetime

    NOTA_MAXIMA = 5.0
    NOTA_MINIMA = 0.0

    def __post_init__(self) -> None:
        if not (self.NOTA_MINIMA <= self.nota <= self.NOTA_MAXIMA):
            raise ValueError(f"A nota deve estar entre {self.NOTA_MINIMA} e {self.NOTA_MAXIMA}.")


def ultimas_interacoes(interacoes: Iterable[Interacao]) -> list[Interacao]:
    vigentes: dict[tuple[str, str], Interacao] = {}
    for interacao in interacoes:
        chave = (interacao.usuario_id, interacao.item_id)
        atual = vigentes.get(chave)
        if atual is None or interacao.timestamp >= atual.timestamp:
            vigentes[chave] = interacao
    return list(vigentes.values())
