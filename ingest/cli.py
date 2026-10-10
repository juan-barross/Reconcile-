"""Comando `nqb`: ponto de entrada único do projeto."""

import typer
from rich.console import Console

app = typer.Typer(help="Os números não batem: pipeline da Olist.", no_args_is_help=True)
console = Console()


@app.callback()
def main() -> None:
    """Os números não batem."""


@app.command()
def baixar() -> None:
    """Baixa os CSVs da Olist do Kaggle para data/csv."""
    from ingest.baixar import baixar as _baixar

    arquivos = _baixar()
    console.print(f"[green]{len(arquivos)} CSVs em {arquivos[0].parent}[/]")


@app.command()
def carregar() -> None:
    """Carrega os CSVs no esquema raw do DuckDB, como texto."""
    from rich.table import Table

    from ingest.carregar import carregar as _carregar

    tabela = Table("tabela raw", "linhas", title="Carga")
    for c in _carregar():
        tabela.add_row(c.tabela, f"{c.linhas:,}".replace(",", "."))
    console.print(tabela)


@app.command()
def auditar() -> None:
    """Roda as checagens da camada raw e grava docs/auditoria.md."""
    from ingest.auditoria import auditar as _auditar

    saida = _auditar()
    console.print(f"[green]Auditoria em {saida}[/]")
