from enum import Enum

from recsys.strategies.recomendador_strategy import RecomendadorStrategy
from recsys.strategies.recomendador_hibrido import RecomendadorHibrido
from recsys.strategies.filtragem_colaborativa import FiltragemColaborativa
from recsys.strategies.filtragem_conteudo import FiltragemConteudo
from recsys.repositories.repositorio_interacao import RepositorioInteracao
from recsys.domain.item import Item


class TipoRecomendador(str, Enum):
    COLABORATIVA = "colaborativa"
    CONTEUDO = "conteudo"
    HIBRIDA = "hibrida"

class RecomendadorFactory:
    @staticmethod
    def criar(
        tipo: TipoRecomendador,
        repositorio: RepositorioInteracao,
        catalogo: dict[str, Item]
    ) -> RecomendadorStrategy:
        if tipo == TipoRecomendador.COLABORATIVA:
            return FiltragemColaborativa(repositorio, catalogo)
        if tipo == TipoRecomendador.CONTEUDO:
            return FiltragemConteudo(repositorio, catalogo)
        if tipo == TipoRecomendador.HIBRIDA:
            return  RecomendadorHibrido(
                colaborativa = FiltragemColaborativa(repositorio, catalogo),
                conteudo = FiltragemConteudo(repositorio, catalogo)
            )
        raise ValueError(f"Tipo de recomendador desconhecido: {tipo}")
