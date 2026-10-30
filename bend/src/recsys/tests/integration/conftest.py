import pytest

from recsys.repositories.repositorios import (
    Repositorios,
    criar_repositorios_memoria,
    criar_repositorios_sqlite,
)


@pytest.fixture(params=["memoria", "sqlite"])
def repositorios(request: pytest.FixtureRequest) -> Repositorios:
    """Cada teste que usa esta fixture roda contra as DUAS implementações."""
    repos = criar_repositorios_memoria() if request.param == "memoria" else criar_repositorios_sqlite()
    yield repos
    repos.fechar()
