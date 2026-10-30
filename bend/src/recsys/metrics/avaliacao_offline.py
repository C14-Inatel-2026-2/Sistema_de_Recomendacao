from collections.abc import Callable
from dataclasses import dataclass

from recsys.domain.interacao import Interacao, ultimas_interacoes
from recsys.domain.usuario import Usuario
from recsys.metrics.avaliador_metrica import AvaliadorMetrica
from recsys.repositories.repositorio_interacao import (
    RepositorioInteracao,
    RepositorioInteracaoMemoria,
)
from recsys.strategies.recomendador_strategy import RecomendadorStrategy

ConstrutorRecomendador = Callable[[RepositorioInteracao], RecomendadorStrategy]


@dataclass(frozen=True)
class ResultadoAvaliacao:
    nome: str
    usuarios_avaliados: int
    precisao: float
    recall: float
    taxa_acerto: float


class AvaliadorOffline:
    """Avaliação leave-one-out.

    Para cada usuário, esconde a avaliação positiva mais recente, monta o
    recomendador só com o restante dos dados e verifica se o item escondido
    aparece nas N recomendações.

    Como há exatamente um item relevante por usuário, a precisão@N nunca passa
    de 1/N; o número mais informativo é a taxa de acerto (hit rate@N), que
    coincide com o recall@N neste desenho.
    """

    def __init__(self, usuarios: list[Usuario], n: int = 5, nota_relevante: float = 3.5) -> None:
        self._usuarios = usuarios
        self._n = n
        self._nota_relevante = nota_relevante

    def avaliar(
        self, nome: str, construir: ConstrutorRecomendador, interacoes: list[Interacao]
    ) -> ResultadoAvaliacao:
        vigentes = ultimas_interacoes(interacoes)
        precisoes: list[float] = []
        recalls: list[float] = []

        for usuario in self._usuarios:
            do_usuario = [i for i in vigentes if i.usuario_id == usuario.id]
            relevantes = [i for i in do_usuario if i.nota >= self._nota_relevante]
            # Sem ao menos uma avaliação restante, não há nada para o modelo aprender.
            if len(do_usuario) < 2 or not relevantes:
                continue

            escondida = sorted(relevantes, key=lambda i: i.timestamp)[-1]
            treino = RepositorioInteracaoMemoria()
            for interacao in vigentes:
                if interacao is not escondida:
                    treino.salvar(interacao)

            recomendados = construir(treino).recomendar(usuario, n=self._n)
            alvo = {escondida.item_id}
            precisoes.append(AvaliadorMetrica.precisao(recomendados, alvo))
            recalls.append(AvaliadorMetrica.recall(recomendados, alvo))

        total = len(recalls)
        return ResultadoAvaliacao(
            nome=nome,
            usuarios_avaliados=total,
            precisao=sum(precisoes) / total if total else 0.0,
            recall=sum(recalls) / total if total else 0.0,
            taxa_acerto=sum(1 for r in recalls if r > 0) / total if total else 0.0,
        )
