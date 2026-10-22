# -*- coding: utf-8 -*-
"""
auditar_axiomas.py — le um log de `lake env lean <arquivo>` e audita as linhas `#print axioms`.
Uso: python auditar_axiomas.py <log> [<log> ...]   (imprime JSON no stdout)
Regra: toda declaracao auditada tem de ter axiomas contidos em {propext, Classical.choice, Quot.sound}
(o trio da casa); `sorryAx`, axioma novo ou linha de erro fazem a auditoria FALHAR (fail-closed).
Nao executa Lean; so le o log. Escrito pelo redator do ADENDO 001 (gerencia), 23/09/2026.
"""
import hashlib
import json
import re
import sys

TRIO = {"propext", "Classical.choice", "Quot.sound"}
RX = re.compile(r"'([^']+)' depends on axioms: \[([^\]]*)\]", re.S)
RX_NONE = re.compile(r"'([^']+)' does not depend on any axioms")


def audita(path):
    raw = open(path, "rb").read()
    txt = raw.decode("utf-8", errors="replace")
    decl = {}
    for nome, lista in RX.findall(txt):
        decl[nome] = sorted(x.strip() for x in lista.split(",") if x.strip())
    for nome in RX_NONE.findall(txt):
        decl[nome] = []
    fora = {n: a for n, a in decl.items() if not set(a) <= TRIO}
    erros = len(re.findall(r":\d+:\d+: error", txt))
    sorry = ("sorryAx" in txt) or ("declaration uses 'sorry'" in txt)
    return {
        "log": path,
        "log_sha16": hashlib.sha256(raw).hexdigest()[:16],
        "n_declaracoes_auditadas": len(decl),
        "fora_do_trio": fora,
        "n_erros": erros,
        "sorry": sorry,
        "n_warnings": len(re.findall(r": warning:", txt)),
        "auditoria": "PASSA" if (decl and not fora and erros == 0 and not sorry) else "FALHA",
        "axiomas": decl,
    }


if __name__ == "__main__":
    out = [audita(p) for p in sys.argv[1:]]
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")
