from abc import ABC, abstractmethod

from recsys.domain.usuario import Usuario
from recsys.repositories.excecoes import EntidadeJaExiste


class RepositorioUsuario(ABC):
    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        """Persiste um usuário novo. Levanta EntidadeJaExiste se o ID já existir."""

    @abstractmethod
    def buscar_por_id(self, usuario_id: str) -> Usuario | None:
        ...

    @abstractmethod
    def listar(self) -> list[Usuario]:
        ...


class RepositorioUsuarioMemoria(RepositorioUsuario):
    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}

    def salvar(self, usuario: Usuario) -> None:
        if usuario.id in self._usuarios:
            raise EntidadeJaExiste("Usuário", usuario.id)
        self._usuarios[usuario.id] = usuario

    def buscar_por_id(self, usuario_id: str) -> Usuario | None:
        return self._usuarios.get(usuario_id)

    def listar(self) -> list[Usuario]:
        return list(self._usuarios.values())
