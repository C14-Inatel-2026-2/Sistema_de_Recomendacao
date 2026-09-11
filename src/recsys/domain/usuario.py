from dataclasses import dataclass, field

@dataclass(frozen=True)
class Usuario:
    id: str
    nome: str
    preferencias: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Usuário precisa de um ID.")
        if not self.nome:
            raise ValueError("Usuário precisa de um nome.")
