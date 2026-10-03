import pytest

from recsys.domain.item import Item
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria
from recsys.strategies.filtragem_colaborativa import FiltragemColaborativa
from recsys.strategies.filtragem_conteudo import FiltragemConteudo
from recsys.strategies.recomendador_factory import RecomendadorFactory, TipoRecomendador
from recsys.strategies.recomendador_hibrido import RecomendadorHibrido


class TestRecomendadorFactory:
    @pytest.mark.parametrize(
        "tipo, classe_esperada",
        [
            (TipoRecomendador.COLABORATIVA, FiltragemColaborativa),
            (TipoRecomendador.CONTEUDO, FiltragemConteudo),
            (TipoRecomendador.HIBRIDA, RecomendadorHibrido),
        ],
    )
    def test_cria_estrategia_correta_para_cada_tipo(
        self,
        tipo: TipoRecomendador,
        classe_esperada: type,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item],
    ) -> None:
        estrategia = RecomendadorFactory.criar(tipo, repositorio_populado, catalogo)
        assert isinstance(estrategia, classe_esperada)
