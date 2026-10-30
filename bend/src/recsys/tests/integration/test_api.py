import pytest
from fastapi.testclient import TestClient

from recsys.api.app import criar_app
from recsys.repositories.repositorios import Repositorios, criar_repositorios_memoria
from recsys.seed import popular_se_vazio


@pytest.fixture
def repos() -> Repositorios:
    repositorios = criar_repositorios_memoria()
    popular_se_vazio(repositorios)
    return repositorios


@pytest.fixture
def client(repos: Repositorios) -> TestClient:
    return TestClient(criar_app(repos))


class TestUsuarios:
    def test_lista_usuarios_do_seed(self, client: TestClient) -> None:
        resposta = client.get("/usuarios")

        assert resposta.status_code == 200
        assert "alice" in {u["id"] for u in resposta.json()}

    def test_cria_usuario(self, client: TestClient) -> None:
        resposta = client.post("/usuarios", json={"id": "eva", "nome": "Eva"})

        assert resposta.status_code == 201
        assert resposta.json()["nome"] == "Eva"

    def test_usuario_duplicado_devolve_409(self, client: TestClient) -> None:
        resposta = client.post("/usuarios", json={"id": "alice", "nome": "Outra"})

        assert resposta.status_code == 409

    def test_usuario_sem_nome_devolve_422(self, client: TestClient) -> None:
        resposta = client.post("/usuarios", json={"id": "eva", "nome": ""})

        assert resposta.status_code == 422


class TestItens:
    def test_cria_e_lista_item(self, client: TestClient) -> None:
        criado = client.post("/itens", json={"id": "tetris", "titulo": "Tetris", "categoria": "puzzle"})

        assert criado.status_code == 201
        assert "tetris" in {i["id"] for i in client.get("/itens").json()}

    def test_item_duplicado_devolve_409(self, client: TestClient) -> None:
        resposta = client.post("/itens", json={"id": "hades", "titulo": "X", "categoria": "acao"})

        assert resposta.status_code == 409

    def test_item_sem_titulo_devolve_422(self, client: TestClient) -> None:
        resposta = client.post("/itens", json={"id": "x", "titulo": "", "categoria": "acao"})

        assert resposta.status_code == 422


class TestInteracoes:
    def test_registra_avaliacao(self, client: TestClient) -> None:
        resposta = client.post("/interacoes", json={"usuario_id": "alice", "item_id": "bg3", "nota": 4})

        assert resposta.status_code == 201
        assert client.get("/usuarios/alice/avaliacoes").json()["bg3"] == 4.0

    def test_reavaliacao_devolve_a_nota_vigente(self, client: TestClient) -> None:
        client.post("/interacoes", json={"usuario_id": "alice", "item_id": "bg3", "nota": 5})
        client.post("/interacoes", json={"usuario_id": "alice", "item_id": "bg3", "nota": 1})

        assert client.get("/usuarios/alice/avaliacoes").json()["bg3"] == 1.0

    @pytest.mark.parametrize(
        "corpo, status",
        [
            ({"usuario_id": "fantasma", "item_id": "bg3", "nota": 4}, 404),
            ({"usuario_id": "alice", "item_id": "fantasma", "nota": 4}, 404),
            ({"usuario_id": "alice", "item_id": "bg3", "nota": 9}, 422),
        ],
    )
    def test_erros(self, client: TestClient, corpo: dict, status: int) -> None:
        assert client.post("/interacoes", json=corpo).status_code == status

    def test_avaliacoes_de_usuario_inexistente_devolve_404(self, client: TestClient) -> None:
        assert client.get("/usuarios/fantasma/avaliacoes").status_code == 404


class TestRecomendacoes:
    @pytest.mark.parametrize("tipo", ["colaborativa", "conteudo", "hibrida"])
    def test_cada_estrategia_responde_ate_n_itens(self, client: TestClient, tipo: str) -> None:
        resposta = client.get("/recomendacoes/alice", params={"tipo": tipo, "n": 3})

        assert resposta.status_code == 200
        assert len(resposta.json()) <= 3

    def test_usuario_inexistente_devolve_404(self, client: TestClient) -> None:
        assert client.get("/recomendacoes/fantasma").status_code == 404

    def test_tipo_invalido_devolve_422(self, client: TestClient) -> None:
        assert client.get("/recomendacoes/alice", params={"tipo": "magica"}).status_code == 422

    @pytest.mark.parametrize("n", [0, -1, 51])
    def test_n_fora_do_intervalo_devolve_422(self, client: TestClient, n: int) -> None:
        assert client.get("/recomendacoes/alice", params={"n": n}).status_code == 422

    def test_nao_recomenda_o_que_o_usuario_ja_avaliou(self, client: TestClient) -> None:
        avaliados = set(client.get("/usuarios/alice/avaliacoes").json())

        ids = {i["id"] for i in client.get("/recomendacoes/alice", params={"n": 20}).json()}

        assert ids.isdisjoint(avaliados)

    def test_avaliacao_positiva_gera_recomendacao_da_mesma_categoria(self, client: TestClient) -> None:
        client.post("/usuarios", json={"id": "eva", "nome": "Eva"})
        assert client.get("/recomendacoes/eva", params={"tipo": "conteudo"}).json() == []

        client.post("/interacoes", json={"usuario_id": "eva", "item_id": "witcher3", "nota": 5})
        itens = client.get("/recomendacoes/eva", params={"tipo": "conteudo", "n": 20}).json()

        assert itens and {i["categoria"] for i in itens} == {"rpg"}
        assert "witcher3" not in {i["id"] for i in itens}


class TestCicloDeVida:
    def test_sem_injecao_abre_sqlite_e_popula(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "api.db"))

        with TestClient(criar_app()) as client:
            assert len(client.get("/usuarios").json()) > 0
            client.post("/usuarios", json={"id": "eva", "nome": "Eva"})

        with TestClient(criar_app()) as client:
            ids = [u["id"] for u in client.get("/usuarios").json()]
            assert "eva" in ids
            assert ids.count("alice") == 1
