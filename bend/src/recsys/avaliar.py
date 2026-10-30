"""Compara as três estratégias com leave-one-out.

Uso (a partir da raiz do repositório):
    PYTHONPATH=bend/src python -m recsys.avaliar [N]
"""
import sys

from recsys.metrics.avaliacao_offline import AvaliadorOffline
from recsys.repositories.repositorios import criar_repositorios_memoria
from recsys.seed import popular_se_vazio
from recsys.strategies.recomendador_factory import RecomendadorFactory, TipoRecomendador


def main(n: int = 5) -> None:
    repos = criar_repositorios_memoria()
    popular_se_vazio(repos)
    catalogo = {item.id: item for item in repos.itens.listar()}
    avaliador = AvaliadorOffline(repos.usuarios.listar(), n=n)
    interacoes = repos.interacoes.buscar_todas()

    print(f"Leave-one-out, N={n}")
    print(f"{'estratégia':<14}{'usuários':>9}{'precisão':>10}{'recall':>8}{'acerto':>8}")
    for tipo in TipoRecomendador:
        r = avaliador.avaliar(
            tipo.value,
            lambda repo, tipo=tipo: RecomendadorFactory.criar(tipo, repo, catalogo),
            interacoes,
        )
        print(f"{r.nome:<14}{r.usuarios_avaliados:>9}{r.precisao:>10.2f}{r.recall:>8.2f}{r.taxa_acerto:>8.2f}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
