from recsys.strategies.filtragem_colaborativa import FiltragemColaborativa
from recsys.strategies.filtragem_conteudo import FiltragemConteudo
from recsys.strategies.recomendador_strategy import RecomendadorStrategy
from recsys.domain.usuario import Usuario
from recsys.domain.item import Item

class RecomendadorHibrido(RecomendadorStrategy):
    """Combina filtragem baseada em conteúdo com filtragem colaborativa.

    Prioriza recomendações por conteúdo e completa o restante
    com filtragem colaborativa.
    """

    def __init__(
        self,
        colaborativa: FiltragemColaborativa,
        conteudo: FiltragemConteudo,
    ) -> None:
        self._colaborativa = colaborativa
        self._conteudo = conteudo

    def recomendar(self, usuario: Usuario, n: int = 5) -> list[Item]:
        recomendar_conteudo = self._conteudo.recomendar(usuario, n=n)
        if len(recomendar_conteudo) >= n:
            return recomendar_conteudo

        selecionados = [item.id for item in recomendar_conteudo]
        falta = n - len(recomendar_conteudo)

        recomendar_colaborativo = [
            item
            for item in self._colaborativa.recomendar(usuario, n=n + len(recomendar_conteudo))
            if item.id not in selecionados
        ][:falta]

        return recomendar_conteudo + recomendar_colaborativo
