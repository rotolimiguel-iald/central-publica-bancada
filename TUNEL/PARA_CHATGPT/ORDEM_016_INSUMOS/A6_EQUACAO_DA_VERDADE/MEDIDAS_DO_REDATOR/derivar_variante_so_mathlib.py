# -*- coding: utf-8 -*-
"""
derivar_variante_so_mathlib.py — deriva, por script, a variante SO-MATHLIB da pedra da gerencia.
Uso: python derivar_variante_so_mathlib.py <TheEquationOfTruth.lean> <saida.lean>
O que remove (e so isto): a linha `import TGLExt.TheNameIsTheInstrument`, a secao
`section NameBridge ... end NameBridge` e as duas linhas `#print axioms ...name_verifies_T*`.
Tudo o mais fica byte a byte. A variante perde so a ponte com a folha v336 (`Verifies`);
`verdict_T`, `verdict_eq_one_iff` e `hasDerivAt_reading_T` permanecem.
Medido pelo redator em 23/09/2026: entrada sha16 35b91f86b88b8e6c -> saida sha16 9808cfc523dbdd57
(27.100 B, 44 teoremas), compilada isolada com rc 0.
"""
import hashlib
import sys

src = open(sys.argv[1], "rb").read()
assert hashlib.sha256(src).hexdigest()[:16] == "35b91f86b88b8e6c", "fonte nao e a pedra da gerencia"
linhas = src.decode("utf-8").split("\n")
out, pular = [], False
for l in linhas:
    if l.strip() == "import TGLExt.TheNameIsTheInstrument":
        continue
    if l.startswith("section NameBridge"):
        pular = True
    if pular:
        if l.startswith("end NameBridge"):
            pular = False
        continue
    if l.startswith("#print axioms") and "name_verifies_T" in l:
        continue
    out.append(l)
b = "\n".join(out).encode("utf-8")
open(sys.argv[2], "wb").write(b)
print("saida", hashlib.sha256(b).hexdigest()[:16], len(b), "B", sum(1 for l in out if l.startswith("theorem")), "teoremas")
