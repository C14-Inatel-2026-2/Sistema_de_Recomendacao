from recsys.domain.item import Item
from recsys.metrics.avaliador_metrica import AvaliadorMetrica


def _item(item_id: str) -> Item:
    return Item(id=item_id, titulo=f"Item {item_id}", categoria="qualquer")


class TestAvaliadorMetrica:
    def test_precisao_com_todos_relevantes_e_um(self) -> None:
        recomendados = [_item("a"), _item("b")]
        relevantes = {"a", "b"}
        assert AvaliadorMetrica.precisao(recomendados, relevantes) == 1.0

    def test_precisao_com_nenhum_relevante_e_zero(self) -> None:
        recomendados = [_item("a"), _item("b")]
        relevantes = {"c", "d"}
        assert AvaliadorMetrica.precisao(recomendados, relevantes) == 0.0

    def test_precisao_parcial(self) -> None:
        recomendados = [_item("a"), _item("b"), _item("c"), _item("d")]
        relevantes = {"a", "c"}
        assert AvaliadorMetrica.precisao(recomendados, relevantes) == 0.5

    def test_precisao_lista_vazia_e_zero(self) -> None:
        assert AvaliadorMetrica.precisao([], {"a"}) == 0.0

    def test_recall_com_todos_relevantes_recuperados(self) -> None:
        recomendados = [_item("a"), _item("b"), _item("c")]
        relevantes = {"a", "b"}
        assert AvaliadorMetrica.recall(recomendados, relevantes) == 1.0

    def test_recall_parcial(self) -> None:
        recomendados = [_item("a")]
        relevantes = {"a", "b", "c", "d"}
        assert AvaliadorMetrica.recall(recomendados, relevantes) == 0.25

    def test_recall_sem_relevantes_e_zero(self) -> None:
        assert AvaliadorMetrica.recall([_item("a")], set()) == 0.0
