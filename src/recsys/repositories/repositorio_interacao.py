from abc import ABC, abstract
from recsys.domain.interacao import Interacao

class RepositorioInteracao(ABC):
    @abstractmethod
    def buscar_por_usuario(self, usuario_id: str) -> list[Interacao]:
        pass

    @abstractmethod
    def buscar_todas(self) -> list[Interacao]:
        pass

    @abstractmethod
    def salvar(self, interacao: Interacao) -> None:
        pass

class RepositorioInteracaoMemoria(RepositorioInteracao) -> None:
    def __init__(self) -> None:
        self._interacoes: list[Interacao] = []

    def busca_por_usuario(self, usuario_id: str) -> list[Interacao]:
        return [i for i in self._interacoes if i.usuario_id == usuario_id]

    def buscar_todas(self) -> list[Interacao]:
        return list(self._interacoes)

    def salvar(self, interacao: Interacao) -> None:
        self._interacoes.append(interacao)
