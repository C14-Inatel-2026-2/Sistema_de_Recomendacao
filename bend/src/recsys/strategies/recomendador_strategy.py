from abc import ABC, abstractmethod

from recsys.domain.item import Item
from recsys.domain.usuario import Usuario

class RecomendadorStrategy(ABC):
    @abstractmethod
    def recomendar(self, usuario: Usuario, n: int) -> list[Item]:
        ...
