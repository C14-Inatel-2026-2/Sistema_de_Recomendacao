from recsys.domain.item import Item
from recsys.domain.usuario import Usuario
from recsys.repositories.repositorio_interacao import RepositorioInteracaoMemoria
from recsys.strategies.filtragem_colaborativa import FiltragemColaborativa


class TestFiltragemColaborativa:
    def test_similaridade_cosseno_vetores_identicos_e_um(self) -> None:
        vetor = {"a": 5.0, "b": 3.0}
        sim = FiltragemColaborativa._similaridade_cosseno(vetor, vetor)
        assert sim == 1.0

    def test_similaridade_cosseno_sem_itens_em_comum_e_zero(self) -> None:
        sim = FiltragemColaborativa._similaridade_cosseno({"a": 5.0}, {"b": 5.0})
        assert sim == 0.0

    def test_recomenda_item_bem_avaliado_por_usuario_similar(
        self,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item],
        alice: Usuario,
    ) -> None:
        # Bruno tem gosto parecido com Alice e avaliou bem o "livro-2"
        # que Alice ainda nao avaliou -> deve aparecer na recomendacao
        recomendador = FiltragemColaborativa(repositorio_populado, catalogo)

        recomendacoes = recomendador.recomendar(alice, n=3)

        ids_recomendados = {item.id for item in recomendacoes}
        assert "livro-2" in ids_recomendados

    def test_nao_recomenda_item_ja_avaliado_pelo_usuario(
        self,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item],
        alice: Usuario,
    ) -> None:
        recomendador = FiltragemColaborativa(repositorio_populado, catalogo)

        recomendacoes = recomendador.recomendar(alice, n=5)

        ids_recomendados = {item.id for item in recomendacoes}
        assert "livro-1" not in ids_recomendados  # Alice ja avaliou livro-1

    def test_usuario_sem_interacoes_recebe_fallback_de_populares(
        self,
        repositorio_populado: RepositorioInteracaoMemoria,
        catalogo: dict[str, Item]
    ) -> None:
        # usuario novo, sem nenhuma interacao registrada
        usuario_novo = Usuario(id="novo-usuario", nome="Carla")
        recomendador = FiltragemColaborativa(repositorio_populado, catalogo)

        recomendacoes = recomendador.recomendar(usuario_novo, n=3)

        # Nao deve levantar excecao e deve retornar itens (os mais populares)
        assert "livro-1" in {item.id for item in recomendacoes}  # livro 1 foi avaliado por 2 usuarios

    def test_repositorio_vazio_nao_levanta_excecao(self, catalogo: dict[str, Item]) -> None:
        repositorio_vazio = RepositorioInteracaoMemoria()
        usuario = Usuario(id="u1", nome="Alice")
        recomendador = FiltragemColaborativa(repositorio_vazio, catalogo)

        recomendacoes = recomendador.recomendar(usuario, n=3)

        assert recomendacoes == []
