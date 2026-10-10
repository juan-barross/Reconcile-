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
