"""Comando `nqb`: ponto de entrada único do projeto.

nqb tudo              # dado real da Olist (baixa do Kaggle, ~45 MB)
nqb --amostra tudo    # amostra sintética, sem rede, em segundos
"""

import os
from pathlib import Path

import typer
from rich.console import Console

from ingest.fontes import Caminhos, caminhos

app = typer.Typer(help="Os números não batem: pipeline da Olist.", no_args_is_help=True)
console = Console()

DBT_DIR = Path(__file__).resolve().parent.parent / "dbt"


def _n(x: int) -> str:
    return f"{x:,}".replace(",", ".")


@app.callback()
def main(
    ctx: typer.Context,
    amostra: bool = typer.Option(
        False, "--amostra", help="Usa a amostra sintética em data/amostra em vez do dado real."
    ),
) -> None:
    """Os números não batem."""
    ctx.obj = caminhos(amostra)


@app.command()
def baixar(ctx: typer.Context) -> None:
    """Baixa os CSVs da Olist do Kaggle (ou gera a amostra sintética)."""
    c: Caminhos = ctx.obj
    if c.amostra:
        from ingest.amostra import escrever

        arquivos = escrever(c.csv_dir)
    else:
        from ingest.baixar import baixar as _baixar

        arquivos = _baixar(c.csv_dir)
    console.print(f"[green]{len(arquivos)} CSVs em {c.csv_dir}[/]")


@app.command()
def carregar(ctx: typer.Context) -> None:
    """Carrega os CSVs no esquema raw do DuckDB, como texto."""
    from rich.table import Table

    from ingest.carregar import carregar as _carregar

    c: Caminhos = ctx.obj
    tabela = Table("tabela raw", "linhas", title=f"Carga em {c.db_path}")
    for carga in _carregar(c.csv_dir, c.db_path):
        tabela.add_row(carga.tabela, _n(carga.linhas))
    console.print(tabela)


@app.command()
def auditar(ctx: typer.Context) -> None:
    """Roda as checagens da camada raw e grava o relatório em markdown."""
    from ingest.auditoria import auditar as _auditar

    c: Caminhos = ctx.obj
    # O relatório do dado real é versionado em docs/; o da amostra fica em data/.
    saida = c.base / "auditoria.md" if c.amostra else Path("docs/auditoria.md")
    console.print(f"[green]Auditoria em {_auditar(c.db_path, saida)}[/]")


def _dbt(c: Caminhos, *args: str) -> None:
    from dbt.cli.main import dbtRunner

    os.environ["NQB_DB_PATH"] = str(c.db_path.resolve())
    comum = ["--project-dir", str(DBT_DIR), "--profiles-dir", str(DBT_DIR)]
    if not (DBT_DIR / "dbt_packages").exists():
        dbtRunner().invoke(["deps", *comum])
    resultado = dbtRunner().invoke([*args, *comum])
    if not resultado.success:
        console.print(f"[red]dbt {' '.join(args)} falhou[/]")
        raise typer.Exit(1)


@app.command()
def dbt(ctx: typer.Context) -> None:
    """Roda `dbt build`: modelos e testes de staging, intermediate e marts."""
    _dbt(ctx.obj, "build")


@app.command()
def tudo(ctx: typer.Context) -> None:
    """Baixa, carrega, audita e roda o dbt, nessa ordem."""
    for passo in (baixar, carregar, auditar, dbt):
        console.rule(passo.__name__)
        passo(ctx)
