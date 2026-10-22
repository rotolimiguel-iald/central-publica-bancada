# -*- coding: utf-8 -*-
"""
auditar_axiomas.py (v2) — audita uma compilacao isolada `lake env lean <arquivo>` pelo LOG e pela FONTE.

Uso:  python auditar_axiomas.py <fonte.lean> <log> [<fonte.lean> <log> ...]   (pares; JSON no stdout)

Regra (fail-closed), a auditoria so da PASSA se TODAS valem:
  (1) LOG: ha >= 1 linha de `#print axioms` lida; toda declaracao impressa tem axiomas contidos no
      trio da casa {propext, Classical.choice, Quot.sound}; 0 linhas de erro; sem `sorryAx` e sem
      "declaration uses 'sorry'".
  (2) COBERTURA: todo `theorem`/`lemma` da FONTE (fora de comentario e de string), com o nome
      qualificado pelo `namespace` corrente, tem o seu `#print axioms` lido no LOG. Declaracao sem
      `#print` = FALHA por cobertura (era o furo da v1: ela so lia as linhas impressas).
  (3) FONTE: nenhum dos tokens `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`,
      `extern`, `unsafe`, `opaque` fora de comentario/string. `private theorem` tambem e FALHA
      (o nome e mangled e escapa da cobertura).
Nao executa Lean; so le os dois arquivos. v1 (so log) foi medida fail-open para declaracao nova sem
`#print` (mutante M7b); v2 fecha esse furo. Redator do ADENDO 001 (gerencia), 23/09/2026.
"""
import hashlib
import json
import re
import sys

TRIO = {"propext", "Classical.choice", "Quot.sound"}
RX = re.compile(r"'([^']+)' depends on axioms: \[([^\]]*)\]", re.S)
RX_NONE = re.compile(r"'([^']+)' does not depend on any axioms")
PROIBIDOS = ["axiom", "sorry", "admit", "native_decide", "implemented_by", "extern", "unsafe", "opaque"]
RX_PROIB = re.compile(r"(?<![\w.'])(" + "|".join(PROIBIDOS) + r")(?![\w'])")
RX_DECL = re.compile(r"(?<![\w.'])(private\s+|protected\s+)?(theorem|lemma)\s+(«[^»]+»|[^\s:({\[⦃]+)")
RX_NS = re.compile(r"(?<![\w.'])(namespace|section|end)(?:[ \t]+([^\s]+))?")


def sem_comentarios(src):
    """Remove comentarios (--, /- -/ aninhados, docstrings) e literais de string; preserva quebras de linha."""
    out, i, n, depth = [], 0, len(src), 0
    while i < n:
        c2 = src[i:i + 2]
        if depth:
            if c2 == "/-":
                depth += 1; i += 2; continue
            if c2 == "-/":
                depth -= 1; i += 2; continue
            out.append("\n" if src[i] == "\n" else " "); i += 1; continue
        if c2 == "/-":
            depth = 1; i += 2; continue
        if c2 == "--":
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if src[i] == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append(" "); i = j + 1; continue
        out.append(src[i]); i += 1
    return "".join(out)


def decls_da_fonte(codigo):
    """Nomes qualificados dos theorem/lemma, seguindo namespace/section/end."""
    pilha, nomes, decl_private = [], [], []
    eventos = [(m.start(), "ns", m) for m in RX_NS.finditer(codigo)] + \
              [(m.start(), "decl", m) for m in RX_DECL.finditer(codigo)]
    for _, tipo, m in sorted(eventos, key=lambda e: e[0]):
        if tipo == "ns":
            kw, nome = m.group(1), m.group(2)
            if kw == "namespace":
                pilha.append(("ns", nome.split(".") if nome else []))
            elif kw == "section":
                pilha.append(("sec", []))
            elif pilha:
                pilha.pop()
            continue
        nome = m.group(3).strip("«»")
        if m.group(1) and m.group(1).strip() == "private":
            decl_private.append(nome)
        if nome.startswith("_root_."):
            q = nome[len("_root_."):]
        else:
            q = ".".join([p for kind, parts in pilha if kind == "ns" for p in parts] + [nome])
        nomes.append(q)
    return nomes, decl_private


def audita(fonte, log):
    raw = open(log, "rb").read()
    txt = raw.decode("utf-8", errors="replace")
    fraw = open(fonte, "rb").read()
    codigo = sem_comentarios(fraw.decode("utf-8", errors="replace"))
    decl = {}
    for nome, lista in RX.findall(txt):
        decl[nome] = sorted(x.strip() for x in lista.split(",") if x.strip())
    for nome in RX_NONE.findall(txt):
        decl[nome] = []
    fora = {n: a for n, a in decl.items() if not set(a) <= TRIO}
    erros = len(re.findall(r":\d+:\d+: error", txt))
    sorry = ("sorryAx" in txt) or ("declaration uses 'sorry'" in txt)
    nomes, decl_private = decls_da_fonte(codigo)
    sem_print = sorted(set(nomes) - set(decl))
    proib = sorted({m.group(1) for m in RX_PROIB.finditer(codigo)})
    motivos = []
    if not decl: motivos.append("nenhum #print axioms lido no log")
    if fora: motivos.append("fora do trio")
    if erros: motivos.append("erro de compilacao")
    if sorry: motivos.append("sorry")
    if sem_print: motivos.append("cobertura: theorem/lemma sem #print axioms")
    if proib: motivos.append("token proibido na fonte")
    if decl_private: motivos.append("private theorem/lemma")
    return {
        "fonte": fonte, "fonte_sha16": hashlib.sha256(fraw).hexdigest()[:16],
        "log": log, "log_sha16": hashlib.sha256(raw).hexdigest()[:16],
        "n_theorem_lemma_na_fonte": len(nomes),
        "n_declaracoes_auditadas": len(decl),
        "sem_print_axioms": sem_print,
        "tokens_proibidos_na_fonte": proib,
        "decl_private": decl_private,
        "fora_do_trio": fora,
        "n_erros": erros,
        "sorry": sorry,
        "n_warnings": len(re.findall(r": warning:", txt)),
        "auditoria": "FALHA" if motivos else "PASSA",
        "motivos": motivos,
        "axiomas": decl,
    }


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or len(a) % 2:
        sys.stderr.write("uso: auditar_axiomas.py <fonte.lean> <log> [<fonte.lean> <log> ...]\n")
        sys.exit(2)
    out = [audita(a[i], a[i + 1]) for i in range(0, len(a), 2)]
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")
    sys.exit(0 if all(r["auditoria"] == "PASSA" for r in out) else 1)
