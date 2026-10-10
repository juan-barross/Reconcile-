"""Comando `nqb`: ponto de entrada único do projeto."""

import typer

app = typer.Typer(help="Os números não batem: pipeline da Olist.", no_args_is_help=True)


@app.callback()
def main() -> None:
    """Os números não batem."""
