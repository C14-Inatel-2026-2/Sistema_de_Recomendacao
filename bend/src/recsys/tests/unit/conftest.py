from datetime import datetime

import pytest

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria


@pytest.fixture
def catalogo() -> dict[str, Item]:
    itens = [
        Item(id="livro-1", titulo="Duna", categoria="ficcao-cientifica"),
        Item(id="livro-2", titulo="Fundacao", categoria="ficcao-cientifica"),
        Item(id="livro-3", titulo="O Hobbit", categoria="fantasia"),
        Item(id="livro-4", titulo="O Senhor dos Aneis", categoria="fantasia"),
        Item(id="livro-5", titulo="1984", categoria="distopia"),
    ]
    return {item.id: item for item in itens}


@pytest.fixture
def alice() -> Usuario:
    return Usuario(id="alice", nome="Alice")


@pytest.fixture
def bruno() -> Usuario:
    return Usuario(id="bruno", nome="Bruno")


@pytest.fixture
def repositorio_populado(alice: Usuario, bruno: Usuario) -> RepositorioInteracaoMemoria:
    repo = RepositorioInteracaoMemoria()
    agora = datetime(2026, 1, 1)

    repo.salvar(Interacao(usuario_id=alice.id, item_id="livro-1", nota=5.0, timestamp=agora))
    repo.salvar(Interacao(usuario_id=alice.id, item_id="livro-3", nota=2.0, timestamp=agora))

    repo.salvar(Interacao(usuario_id=bruno.id, item_id="livro-1", nota=5.0, timestamp=agora))
    repo.salvar(Interacao(usuario_id=bruno.id, item_id="livro-2", nota=4.5, timestamp=agora))

    return repo
