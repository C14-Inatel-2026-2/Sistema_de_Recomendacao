from datetime import datetime

import pytest

from recsys.domain.interacao import Interacao
from recsys.domain.item import Item
from recsys.domain.usuario import Usuario


class TestUsuario:
    def test_cria_usuario_valido(self) -> None:
        usuario = Usuario(id="u1", nome="Alice")
        assert usuario.id == "u1"

    def test_usuario_sem_id_levanta_erro(self) -> None:
        with pytest.raises(ValueError):
            Usuario(id="", nome="Alice")

    def test_usuario_sem_nome_levanta_erro(self) -> None:
        with pytest.raises(ValueError):
            Usuario(id="u1", nome="")


class TestItem:
    def test_cria_item_valido(self) -> None:
        item = Item(id="i1", titulo="Duna", categoria="ficcao-cientifica")
        assert item.id == "i1"

    def test_item_sem_titulo_levanta_erro(self) -> None:
        with pytest.raises(ValueError):
            Item(id="i1", titulo="", categoria="ficcao-cientifica")


class TestInteracao:
    def test_cria_interacao_valida(self) -> None:
        interacao = Interacao(
            usuario_id="u1", item_id="i1", nota=4.5, timestamp=datetime(2026, 1, 1)
        )
        assert interacao.nota == 4.5

    @pytest.mark.parametrize("nota_invalida", [-1.0, 5.1, 10.0])
    def test_nota_fora_do_intervalo_levanta_erro(self, nota_invalida: float) -> None:
        with pytest.raises(ValueError):
            Interacao(
                usuario_id="u1", item_id="i1", nota=nota_invalida, timestamp=datetime(2026, 1, 1)
            )


class TestUltimasInteracoes:
    def test_reavaliacao_substitui_a_anterior(self) -> None:
        from recsys.domain.interacao import ultimas_interacoes

        antiga = Interacao("u1", "i1", 5.0, datetime(2026, 1, 1))
        nova = Interacao("u1", "i1", 1.0, datetime(2026, 1, 2))

        assert ultimas_interacoes([antiga, nova]) == [nova]

    def test_vale_o_timestamp_e_nao_a_ordem_de_chegada(self) -> None:
        from recsys.domain.interacao import ultimas_interacoes

        antiga = Interacao("u1", "i1", 5.0, datetime(2026, 1, 1))
        nova = Interacao("u1", "i1", 1.0, datetime(2026, 1, 2))

        assert ultimas_interacoes([nova, antiga]) == [nova]

    def test_empate_de_timestamp_vale_a_ultima_registrada(self) -> None:
        from recsys.domain.interacao import ultimas_interacoes

        agora = datetime(2026, 1, 1)
        primeira = Interacao("u1", "i1", 5.0, agora)
        segunda = Interacao("u1", "i1", 2.0, agora)

        assert ultimas_interacoes([primeira, segunda]) == [segunda]

    def test_usuarios_e_itens_diferentes_nao_se_misturam(self) -> None:
        from recsys.domain.interacao import ultimas_interacoes

        agora = datetime(2026, 1, 1)
        interacoes = [
            Interacao("u1", "i1", 5.0, agora),
            Interacao("u2", "i1", 3.0, agora),
            Interacao("u1", "i2", 4.0, agora),
        ]

        assert len(ultimas_interacoes(interacoes)) == 3
