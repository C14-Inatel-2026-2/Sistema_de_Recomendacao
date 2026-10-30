"""Um único lugar que escolhe a tecnologia."""
from collections.abc import Callable
from dataclasses import dataclass, field

from recsys.repositories.repositorio_interacao import (
    RepositorioInteracao,
    RepositorioInteracaoMemoria,
)
from recsys.repositories.repositorio_item import RepositorioItem, RepositorioItemMemoria
from recsys.repositories.repositorio_usuario import RepositorioUsuario, RepositorioUsuarioMemoria
from recsys.repositories.repositorios_sqlite import (
    ConexaoSQLite,
    RepositorioInteracaoSQLite,
    RepositorioItemSQLite,
    RepositorioUsuarioSQLite,
)


@dataclass(frozen=True)
class Repositorios:
    usuarios: RepositorioUsuario
    itens: RepositorioItem
    interacoes: RepositorioInteracao
    fechar: Callable[[], None] = field(default=lambda: None)


def criar_repositorios_memoria() -> Repositorios:
    return Repositorios(
        usuarios=RepositorioUsuarioMemoria(),
        itens=RepositorioItemMemoria(),
        interacoes=RepositorioInteracaoMemoria(),
    )


def criar_repositorios_sqlite(caminho: str = ":memory:") -> Repositorios:
    conexao = ConexaoSQLite(caminho)
    return Repositorios(
        usuarios=RepositorioUsuarioSQLite(conexao),
        itens=RepositorioItemSQLite(conexao),
        interacoes=RepositorioInteracaoSQLite(conexao),
        fechar=conexao.fechar,
    )
