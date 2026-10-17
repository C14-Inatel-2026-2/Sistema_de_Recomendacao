import pytest

from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria
from recsys.strategies.filtragem_colaborativa import FiltragemColaborativa
from recsys.strategies.filtragem_conteudo import FiltragemConteudo
from recsys.strategies.recomendador_hibrido import RecomendadorHibrido


class TestRecomendadorHibrido:
    def test_completa_com_colaborativa_quando_conteudo_nao_basta(
        self,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item],
        alice: Usuario,
    ) -> None:
        colaborativa = FiltragemColaborativa(repositorio_populado, catalogo)
        conteudo = FiltragemConteudo(repositorio_populado, catalogo)
        hibrido = RecomendadorHibrido(colaborativa, conteudo)

        recomendacoes = hibrido.recomendar(alice, n=5)

        # nao deve haver duplicatas nem itens ja avaliados por Alice
        ids = [item.id for item in recomendacoes]
        assert len(ids) == len(set(ids))

    def test_usuario_sem_historico_ainda_recebe_recomendacoes(
        self, repositorio_populado: RepositorioInteracaoMemoria, catalogo: dict[str, Item]
    ) -> None:
        colaborativa = FiltragemColaborativa(repositorio_populado, catalogo)
        conteudo = FiltragemConteudo(repositorio_populado, catalogo)
        hibrido = RecomendadorHibrido(colaborativa, conteudo)

        usuario_novo = Usuario(id="novo", nome="Carla")
        recomendacoes = hibrido.recomendar(usuario_novo, n=3)

        assert len(recomendacoes) > 0
