import math
from collections import defaultdict

from recsys.strategies.recomendador_strategy import RecomendadorStrategy
from recsys.repositories.repositorio_interacao import RepositorioInteracao
from recsys.domain.interacao import Interacao, ultimas_interacoes
from recsys.domain.usuario import Usuario
from recsys.domain.item import Item

class FiltragemColaborativa(RecomendadorStrategy):
    """Recomenda itens com base em usuários com gosto parecido:
    'usuários que avaliaram bem itens parecidos com os seus também gostaram de...'

    Usa similaridade de cosseno entre os vetores de avaliação dos usuários.
    Só avaliações positivas (>= nota_minima) dos vizinhos viram recomendação:
    um item que o vizinho detestou não deve ser sugerido.
    Quando o usuário não tem nenhuma interação, entra no fallback de itens
    mais populares: os mais bem avaliados (>= nota_minima) por usuários distintos.
    """
    def __init__(
        self,
        repositorio: RepositorioInteracao,
        catalogo: dict[str, Item],
        min_similar: int = 1,
        nota_minima: float = 3.5,
    ) -> None:
        self._repositorio = repositorio
        self._catalogo = catalogo
        self._min_similar = min_similar
        self._nota_minima = nota_minima

    def recomendar(self, usuario: Usuario, n: int = 5) -> list[Item]:
        vigentes = ultimas_interacoes(self._repositorio.buscar_todas())

        notas_por_usuario: dict[str, dict[str, float]] = defaultdict(dict)
        for interacao in vigentes:
            notas_por_usuario[interacao.usuario_id][interacao.item_id] = interacao.nota

        notas_usuario = notas_por_usuario.get(usuario.id)
        if not notas_usuario:
            return self._itens_populares(vigentes, excluir=set(), n=n)

        similaridades = []
        for outro_id, outra_nota in notas_por_usuario.items():
            if usuario.id == outro_id:
                continue
            valor_similar = self._similaridade_cosseno(notas_usuario, outra_nota)
            if valor_similar > 0:
                similaridades.append((outro_id, valor_similar))

        if len(similaridades) < self._min_similar:
            return self._itens_populares(vigentes, excluir=set(notas_usuario), n=n)

        pontuacao_item: dict[str, float] = defaultdict(float)
        for outro_id, valor_similar in similaridades:
            for item_id, nota_item in notas_por_usuario[outro_id].items():
                if item_id in notas_usuario or nota_item < self._nota_minima:
                    continue
                pontuacao_item[item_id] += nota_item * valor_similar
        candidatos = sorted(pontuacao_item.items(), key=lambda par: par[1], reverse=True)

        recomendados = [
            self._catalogo[item_id]
            for item_id, _ in candidatos
            if item_id in self._catalogo
        ][:n]

        if len(recomendados) < n:
            falta = n - len(recomendados)
            excluir = set(notas_usuario) | {item.id for item in recomendados}
            recomendados += self._itens_populares(vigentes, excluir=excluir, n=falta)

        return recomendados

    def _itens_populares(
        self, vigentes: list[Interacao], excluir: set[str], n: int
    ) -> list[Item]:
        usuarios_por_item: dict[str, set[str]] = defaultdict(set)
        for interacao in vigentes:
            if interacao.nota >= self._nota_minima:
                usuarios_por_item[interacao.item_id].add(interacao.usuario_id)
        populares = sorted(
            usuarios_por_item.items(), key=lambda par: (-len(par[1]), par[0])
        )
        return [
            self._catalogo[item_id]
            for item_id, _ in populares
            if item_id not in excluir and item_id in self._catalogo
        ][:n]

    @staticmethod
    def _similaridade_cosseno(a: dict[str, float], b: dict[str, float]) -> float:
        chaves_comuns = set(a) & set(b)
        if not chaves_comuns:
            return 0.0

        produto_escalar = sum(a[k] * b[k] for k in chaves_comuns)
        normal_a = math.sqrt(sum(valor**2 for valor in a.values()))
        normal_b = math.sqrt(sum(valor**2 for valor in b.values()))

        if normal_a == 0 or normal_b == 0:
            return 0.0

        return produto_escalar / (normal_a * normal_b)
