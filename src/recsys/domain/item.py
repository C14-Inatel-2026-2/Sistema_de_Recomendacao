from dataclasses import dataclass, field

@dataclass(frozen=True)
class Item:
    id: str
    titulo: str
    categoria: str
    atributos: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("O item precisa de um ID.")
        if not self.titulo:
            raise ValueError("O item precisa de um título.")
