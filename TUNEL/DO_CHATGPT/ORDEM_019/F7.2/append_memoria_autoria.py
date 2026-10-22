"""Append the source-author correction to Central memory with byte backups."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HELPER = Path(__file__).resolve().with_name("append_memoria_v2.py")
spec = importlib.util.spec_from_file_location("iald_memory_append_authors", HELPER)
assert spec and spec.loader
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
helper.MARKER = b"<!-- F72_JUNO_AUTHORS_CORRECTION_20261008 -->"
helper.ENTRY = """

### Correção ao lado — F7.2 autoria JUNO (08/10/2026)

<!-- F72_JUNO_AUTHORS_CORRECTION_20261008 -->

[REAL documental] No adendo F7.2 acima, «das autoras» deve ser lido «de Martina Beccaria e Christoph A. Ternes» ou «dos autores». A página primária https://arxiv.org/abs/2606.13362v1 lista ambos. Nota ao lado `F7.2/CORRECAO_AUTORIA_JUNO.md` SHA-256 645b5347e69e677481e7acc96d8e3a098f1293273eb920c86357125aed577c2b; Mapa seq 809, quadro anotação evento 269. Cota publicada, pin do PDF, τ★ nulo e gate NONE inalterados.
""".encode("utf-8")


if __name__ == "__main__":
    for target in helper.PATHS:
        print(helper.append_one(target))
