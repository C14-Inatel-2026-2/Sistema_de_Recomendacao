from datetime import datetime

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.metrics.avaliacao_offline import AvaliadorOffline
from recsys.repositories.repositorio_interacao import RepositorioInteracao
from recsys.strategies.filtragem_conteudo import FiltragemConteudo
from recsys.strategies.recomendador_strategy import RecomendadorStrategy


class _SempreVazio(RecomendadorStrategy):
    def recomendar(self, usuario: Usuario, n: int = 5) -> list[Item]:
        return []


def _interacoes() -> list[Interacao]:
    # Alice gosta de ficcao-cientifica: esconder livro-2 deve ser "adivinhável"
    return [
        Interacao("alice", "livro-1", 5.0, datetime(2026, 1, 1)),
        Interacao("alice", "livro-2", 5.0, datetime(2026, 1, 2)),
    ]


class TestAvaliadorOffline:
    def test_estrategia_que_acerta_tem_taxa_de_acerto_total(
        self, catalogo: dict[str, Item], alice: Usuario
    ) -> None:
        avaliador = AvaliadorOffline([alice], n=5)

        resultado = avaliador.avaliar(
            "conteudo", lambda repo: FiltragemConteudo(repo, catalogo), _interacoes()
        )

        assert resultado.usuarios_avaliados == 1
        assert resultado.taxa_acerto == 1.0
        assert resultado.recall == 1.0

    def test_estrategia_que_nao_recomenda_nada_tem_metricas_zero(self, alice: Usuario) -> None:
        avaliador = AvaliadorOffline([alice], n=5)

        resultado = avaliador.avaliar("vazio", lambda repo: _SempreVazio(), _interacoes())

        assert resultado.taxa_acerto == 0.0
        assert resultado.precisao == 0.0

    def test_item_escondido_nao_vai_para_o_treino(self, alice: Usuario) -> None:
        vistos: list[RepositorioInteracao] = []

        def construir(repo: RepositorioInteracao) -> RecomendadorStrategy:
            vistos.append(repo)
            return _SempreVazio()

        AvaliadorOffline([alice]).avaliar("x", construir, _interacoes())

        ids_no_treino = {i.item_id for i in vistos[0].buscar_todas()}
        assert ids_no_treino == {"livro-1"}  # livro-2, o mais recente, foi escondido

    def test_usuario_com_uma_unica_avaliacao_e_ignorado(self, alice: Usuario) -> None:
        unica = [Interacao("alice", "livro-1", 5.0, datetime(2026, 1, 1))]

        resultado = AvaliadorOffline([alice]).avaliar("x", lambda repo: _SempreVazio(), unica)

        assert resultado.usuarios_avaliados == 0
        assert resultado.recall == 0.0  # sem divisão por zero
