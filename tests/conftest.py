import pytest

from ingest import amostra
from ingest.carregar import carregar


@pytest.fixture(scope="session")
def db_amostra(tmp_path_factory):
    """DuckDB com a amostra sintética carregada em raw."""
    pasta = tmp_path_factory.mktemp("amostra")
    amostra.escrever(pasta / "csv")
    db = pasta / "olist.duckdb"
    carregar(pasta / "csv", db)
    return db
