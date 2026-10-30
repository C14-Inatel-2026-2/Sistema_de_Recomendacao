from recsys.domain.usuario import Usuario
from recsys.repositories.repositorios import criar_repositorios_memoria, criar_repositorios_sqlite
from recsys.seed import popular_se_vazio


class TestPersistencia:
    def test_dados_sobrevivem_a_reabrir_o_arquivo(self, tmp_path) -> None:
        caminho = str(tmp_path / "recsys.db")
        primeiro = criar_repositorios_sqlite(caminho)
        primeiro.usuarios.salvar(Usuario(id="u1", nome="Alice"))
        primeiro.fechar()

        segundo = criar_repositorios_sqlite(caminho)

        assert segundo.usuarios.buscar_por_id("u1") == Usuario(id="u1", nome="Alice")
        segundo.fechar()


class TestSeed:
    def test_popula_banco_vazio(self) -> None:
        repos = criar_repositorios_memoria()

        assert popular_se_vazio(repos) is True
        assert len(repos.usuarios.listar()) > 0
        assert len(repos.interacoes.buscar_todas()) > 0

    def test_e_idempotente(self) -> None:
        repos = criar_repositorios_memoria()
        popular_se_vazio(repos)
        total = len(repos.interacoes.buscar_todas())

        assert popular_se_vazio(repos) is False
        assert len(repos.interacoes.buscar_todas()) == total
