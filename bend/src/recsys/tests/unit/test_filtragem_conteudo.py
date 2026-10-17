from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria
from recsys.strategies.filtragem_conteudo import FiltragemConteudo


class TestFiltragemConteudo:
    def test_recomenda_itens_da_mesma_categoria_bem_avaliada(
        self,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item],
        alice: Usuario,
    ) -> None:
        # Alice avaliou "livro-1" (ficcao-cientifica) com nota 5.0
        # -> deve recomendar outros itens de ficcao-cientifica, como livro-2
        recomendador = FiltragemConteudo(repositorio_populado, catalogo)

        recomendacoes = recomendador.recomendar(alice, n=3)

        categorias_recomendadas = {item.categoria for item in recomendacoes}
        assert "ficcao-cientifica" in categorias_recomendadas

    def test_nao_recomenda_itens_de_categoria_mal_avaliada(
        self,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item],
        alice: Usuario,
    ) -> None:
        # Alice avaliou "livro-3" (fantasia) com nota baixa (2.0)
        # -> "fantasia" nao deve ser puxada como categoria preferida
        recomendador = FiltragemConteudo(repositorio_populado, catalogo)

        recomendacoes = recomendador.recomendar(alice, n=5)

        ids_recomendados = {item.id for item in recomendacoes}
        assert "livro-4" not in ids_recomendados  # livro-4 é tambem fantasia

    def test_usuario_sem_avaliacoes_positivas_recebe_lista_vazia(
        self, catalogo: dict[str, Item]
    ) -> None:
        repositorio_vazio = RepositorioInteracaoMemoria()
        usuario_novo = Usuario(id="novo", nome="Carla")
        recomendador = FiltragemConteudo(repositorio_vazio, catalogo)

        recomendacoes = recomendador.recomendar(usuario_novo, n=3)

        assert recomendacoes == []

    def test_nao_recomenda_item_ja_avaliado(
        self,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item],
        alice: Usuario,
    ) -> None:
        recomendador = FiltragemConteudo(repositorio_populado, catalogo)

        recomendacoes = recomendador.recomendar(alice, n=5)

        ids_recomendados = {item.id for item in recomendacoes}
        assert "livro-1" not in ids_recomendados
