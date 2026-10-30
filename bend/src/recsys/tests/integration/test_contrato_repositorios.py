"""Testes de contrato: memória e SQLite precisam se comportar de forma idêntica."""
from datetime import datetime, timezone

import pytest

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.excecoes import EntidadeJaExiste
from recsys.repositories.repositorios import Repositorios


class TestRepositorioUsuario:
    def test_salva_e_busca_por_id(self, repositorios: Repositorios) -> None:
        repositorios.usuarios.salvar(Usuario(id="u1", nome="Alice"))

        assert repositorios.usuarios.buscar_por_id("u1") == Usuario(id="u1", nome="Alice")

    def test_busca_inexistente_devolve_none(self, repositorios: Repositorios) -> None:
        assert repositorios.usuarios.buscar_por_id("fantasma") is None

    def test_id_duplicado_levanta_excecao(self, repositorios: Repositorios) -> None:
        repositorios.usuarios.salvar(Usuario(id="u1", nome="Alice"))

        with pytest.raises(EntidadeJaExiste):
            repositorios.usuarios.salvar(Usuario(id="u1", nome="Outra"))

    def test_lista_na_ordem_de_insercao(self, repositorios: Repositorios) -> None:
        for id_ in ("b", "a", "c"):
            repositorios.usuarios.salvar(Usuario(id=id_, nome=id_.upper()))

        assert [u.id for u in repositorios.usuarios.listar()] == ["b", "a", "c"]

    def test_preserva_preferencias(self, repositorios: Repositorios) -> None:
        usuario = Usuario(id="u1", nome="Alice", preferencias={"rpg": 0.9})
        repositorios.usuarios.salvar(usuario)

        assert repositorios.usuarios.buscar_por_id("u1") == usuario


class TestRepositorioItem:
    def test_salva_e_busca_por_id_preservando_atributos(self, repositorios: Repositorios) -> None:
        item = Item(id="i1", titulo="Hades", categoria="acao", atributos={"ano": "2020"})
        repositorios.itens.salvar(item)

        assert repositorios.itens.buscar_por_id("i1") == item

    def test_id_duplicado_levanta_excecao(self, repositorios: Repositorios) -> None:
        repositorios.itens.salvar(Item(id="i1", titulo="Hades", categoria="acao"))

        with pytest.raises(EntidadeJaExiste):
            repositorios.itens.salvar(Item(id="i1", titulo="Outro", categoria="rpg"))

    def test_lista_vazia_no_inicio(self, repositorios: Repositorios) -> None:
        assert repositorios.itens.listar() == []


class TestRepositorioInteracao:
    @pytest.fixture(autouse=True)
    def _entidades(self, repositorios: Repositorios) -> None:
        # o SQLite exige que usuário e item existam (chave estrangeira)
        for id_ in ("u1", "u2"):
            repositorios.usuarios.salvar(Usuario(id=id_, nome=id_))
        repositorios.itens.salvar(Item(id="i1", titulo="Hades", categoria="acao"))

    def test_salva_e_busca_por_usuario(self, repositorios: Repositorios) -> None:
        agora = datetime(2026, 1, 1, tzinfo=timezone.utc)
        interacao = Interacao("u1", "i1", 4.5, agora)
        repositorios.interacoes.salvar(interacao)
        repositorios.interacoes.salvar(Interacao("u2", "i1", 2.0, agora))

        assert repositorios.interacoes.buscar_por_usuario("u1") == [interacao]

    def test_timestamp_faz_o_caminho_de_ida_e_volta(self, repositorios: Repositorios) -> None:
        momento = datetime(2026, 3, 4, 5, 6, 7, tzinfo=timezone.utc)
        repositorios.interacoes.salvar(Interacao("u1", "i1", 3.0, momento))

        assert repositorios.interacoes.buscar_todas()[0].timestamp == momento

    def test_mantem_ordem_de_insercao_e_historico_de_reavaliacoes(
        self, repositorios: Repositorios
    ) -> None:
        agora = datetime(2026, 1, 1)
        repositorios.interacoes.salvar(Interacao("u1", "i1", 5.0, agora))
        repositorios.interacoes.salvar(Interacao("u1", "i1", 1.0, agora))

        assert [i.nota for i in repositorios.interacoes.buscar_todas()] == [5.0, 1.0]
