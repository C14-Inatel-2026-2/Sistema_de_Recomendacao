import pytest

from recsys import avaliar


def test_script_imprime_uma_linha_por_estrategia(capsys: pytest.CaptureFixture[str]) -> None:
    avaliar.main(n=5)

    saida = capsys.readouterr().out
    for estrategia in ("colaborativa", "conteudo", "hibrida"):
        assert estrategia in saida
