"""Baixa os dois datasets da Olist do Kaggle e copia os CSVs para data/csv.

Os datasets são públicos: o kagglehub baixa sem credencial. Se houver
~/.kaggle/kaggle.json ou KAGGLE_USERNAME/KAGGLE_KEY, ele usa.
"""

import shutil
from pathlib import Path

from ingest.fontes import CSV_DIR, FONTES


def baixar(destino: Path = CSV_DIR) -> list[Path]:
    import kagglehub

    destino.mkdir(parents=True, exist_ok=True)
    pastas = {ds: Path(kagglehub.dataset_download(ds)) for ds in {f.dataset for f in FONTES}}

    copiados = []
    for fonte in FONTES:
        origem = pastas[fonte.dataset] / fonte.arquivo
        if not origem.exists():
            raise FileNotFoundError(
                f"{fonte.arquivo} não veio no download de {fonte.dataset}. "
                "O dataset mudou de versão? Confira ingest/fontes.py."
            )
        alvo = destino / fonte.arquivo
        shutil.copyfile(origem, alvo)
        copiados.append(alvo)
    return copiados
