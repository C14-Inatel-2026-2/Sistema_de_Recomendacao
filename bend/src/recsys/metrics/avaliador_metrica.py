from recsys.domain.item import Item

class AvaliadorMetrica:
    @staticmethod
    def precisao(recomendados: list[Item], relevantes: set[str]) -> float:
        """
        Proporção de itens recomendados que foram relevantes.
        """
        if not recomendados:
            return 0.0
        acertos = sum(1 for i in recomendados if i.id in relevantes)
        return acertos / len(recomendados)

    def recall(recomendados: list[Item], relevantes: set[str]) -> float:
        """
        Proporção de itens relevantes que foram recomendados.
        """
        if not relevantes:
            return 0.0
        acertos = sum(1 for i in recomendados if i.id in relevantes)
        return acertos / len(relevantes)
