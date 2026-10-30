class EntidadeJaExiste(Exception):
    """Tentativa de salvar uma entidade cujo ID já está em uso."""

    def __init__(self, entidade: str, id_: str) -> None:
        super().__init__(f"{entidade} '{id_}' já existe.")
        self.entidade = entidade
        self.id = id_
