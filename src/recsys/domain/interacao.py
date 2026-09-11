from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Interacao:
    usuario_id: str
    item_it: str
    nota: float
    timestamp: datetime

    NOTA_MAXIMA = 5.0
    NOTA_MINIMA = 0.0

    def __post_init__(self) -> None:
        if not (self.NOTA_MINIMA <= self.nota <= self.NOTA_MAXIMA):
            raise ValueError(f"A nota deve estar entre {self.NOTA_MINIMA} e {self.NOTA_MAXIMA}.")
