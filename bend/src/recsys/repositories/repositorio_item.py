from abc import ABC, abstractmethod

from recsys.domain.item import Item
from recsys.repositories.excecoes import EntidadeJaExiste


class RepositorioItem(ABC):
    @abstractmethod
    def salvar(self, item: Item) -> None:
        """Persiste um item novo. Levanta EntidadeJaExiste se o ID já existir."""

    @abstractmethod
    def buscar_por_id(self, item_id: str) -> Item | None:
        ...

    @abstractmethod
    def listar(self) -> list[Item]:
        ...


class RepositorioItemMemoria(RepositorioItem):
    def __init__(self) -> None:
        self._itens: dict[str, Item] = {}

    def salvar(self, item: Item) -> None:
        if item.id in self._itens:
            raise EntidadeJaExiste("Item", item.id)
        self._itens[item.id] = item

    def buscar_por_id(self, item_id: str) -> Item | None:
        return self._itens.get(item_id)

    def listar(self) -> list[Item]:
        return list(self._itens.values())
