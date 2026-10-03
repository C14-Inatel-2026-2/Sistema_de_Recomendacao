from collections import Counter

from recsys.strategies.recomendador_strategy import RecomendadorStrategy
from recsys.domain.usuario import Usuario
from recsys.domain.item import Item
from recsys.repositories.repositorio_interacao import RepositorioInteracao

class FiltragemConteudo(RecomendadorStrategy):
    """Recomenda itens parecidos com os que o usuário já avaliou bem,
    usando a categoria do item como principal atributo de similaridade.

    Não depende de outros usuários, então funciona bem para usuários novos,
    desde que já tenham feito ao menos uma avaliação positiva.
    """

    NOTA_MINIMA = 3.5

    def __init__(
        self,
        repositorio: RepositorioInteracao,
        catalogo: dict[str, Item]
    ) -> None:
        self._repositorio = repositorio
        self._catalogo = catalogo

    def recomendar(self, usuario: Usuario, n: int = 5) -> list[Item]:
        interacoes_usuario = self._repositorio.buscar_por_usuario(usuario.id)
        avaliados = {i.item_id for i in interacoes_usuario}

        categorias_preferida = Counter(
            self._catalogo[i.item_id].categoria
            for i in interacoes_usuario
            if i.nota >= self.NOTA_MINIMA and i.item_id in self._catalogo
        )

        if not categorias_preferida:
            return []

        candidatos = [
            item
            for item_id, item in self._catalogo.items()
            if item_id not in avaliados and item.categoria in categorias_preferida
        ]

        candidatos.sort(key=lambda item: categorias_preferida[item.categoria], reverse=True)

        return candidatos[:n]
