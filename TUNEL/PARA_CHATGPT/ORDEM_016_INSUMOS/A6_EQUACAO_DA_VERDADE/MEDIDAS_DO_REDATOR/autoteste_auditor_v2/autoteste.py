# -*- coding: utf-8 -*-
r"""
autoteste.py — autoteste do auditar_axiomas.py v2 (redator do ADENDO 001, gerencia, 23/09/2026).
Negativos (TEM de dar FALHA) e positivos (TEM de dar PASSA), com o motivo esperado.
  REAL      = par (fonte, log) de compilacao isolada de verdade (medida);
  SINTETICO = fonte/log escritos aqui so para exercitar o parser (dito como tal).
Nao executa Lean. Grava RESULTADO.json nesta pasta.
"""
import hashlib
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MED = os.path.dirname(AQUI)
ROOT = os.path.dirname(os.path.dirname(MED))
AUD = os.path.join(MED, "auditar_axiomas.py")
V1AUT = os.path.join(MED, "autoteste_auditor")
C2 = os.path.join(MED, "mutantes_C2")
V3 = os.path.join(ROOT, "V3")


def w(nome, texto):
    p = os.path.join(AQUI, "sinteticos", nome)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(texto.encode("utf-8"))
    return p


V3SRC = os.path.join(V3, "TheEquationOfTruth.lean")
V3LOG = os.path.join(V3, "out", "compile_final.log")
v3 = open(V3SRC, "rb").read().decode("utf-8")

casos = [
    # ---- negativos ----
    ("N1_sorry", "SINTETICO", w("n1.lean", "namespace A\ntheorem t : 1 = 1 := by sorry\nend A\n#print axioms A.t\n"),
     os.path.join(V1AUT, "sorry.log"), "FALHA", ["sorry"]),
    ("N2_axioma_com_print", "SINTETICO", w("n2.lean", "namespace A\naxiom fake : False\ntheorem u : 1 = 2 := fake.elim\nend A\n#print axioms A.u\n"),
     os.path.join(V1AUT, "axioma_novo.log"), "FALHA", ["fora do trio", "token proibido na fonte"]),
    ("N3_erro", "SINTETICO", w("n3.lean", "namespace A\ntheorem v (x : Nat) : x = x := by exact hH\nend A\n"),
     os.path.join(V1AUT, "erro.log"), "FALHA", ["erro de compilacao"]),
    ("N4_M6_sorry_real", "REAL", os.path.join(C2, "M6", "TheEquationOfTruthM6.lean"),
     os.path.join(C2, "M6", "out", "compile.log"), "FALHA", ["sorry"]),
    ("N5_M7a_axioma_com_print_real", "REAL", os.path.join(C2, "M7a", "TheEquationOfTruthM7a.lean"),
     os.path.join(C2, "M7a", "out", "compile.log"), "FALHA", ["fora do trio", "token proibido na fonte"]),
    ("N6_M7b_axioma_sem_print_real", "REAL", os.path.join(C2, "M7b", "TheEquationOfTruthM7b.lean"),
     os.path.join(C2, "M7b", "out", "compile.log"), "FALHA", ["cobertura: theorem/lemma sem #print axioms", "token proibido na fonte"]),
    ("N7_so_cobertura", "SINTETICO (fonte = V3 + 1 teorema sem #print; log = o REAL da V3)",
     w("n7.lean", v3 + "\ntheorem extra_sem_print : (1 : Nat) = 1 := rfl\n"), V3LOG, "FALHA",
     ["cobertura: theorem/lemma sem #print axioms"]),
    ("N8_native_decide", "SINTETICO (fonte = V3 + native_decide; log = o REAL da V3)",
     w("n8.lean", v3 + "\nexample : (2 : Nat) + 2 = 4 := by native_decide\n"), V3LOG, "FALHA", ["token proibido na fonte"]),
    ("N9_private", "SINTETICO (fonte = V3 + private theorem; log = o REAL da V3)",
     w("n9.lean", v3 + "\nprivate theorem escondido : (1 : Nat) = 1 := rfl\n"), V3LOG, "FALHA",
     ["cobertura: theorem/lemma sem #print axioms", "private theorem/lemma"]),
    # ---- positivos ----
    ("P1_V3_real", "REAL", V3SRC, V3LOG, "PASSA", []),
    ("P2_V3_copia_do_redator_real", "REAL", os.path.join(MED, "lean_copia", "TheEquationOfTruth.lean"),
     os.path.join(MED, "lean_copia", "out", "compile.log"), "PASSA", []),
    ("P3_so_mathlib_real", "REAL", os.path.join(MED, "lean_so_mathlib", "TheEquationOfTruthMathlibOnly.lean"),
     os.path.join(MED, "lean_so_mathlib", "out", "compile.log"), "PASSA", []),
    ("P4_contorno_real", "REAL", os.path.join(MED, "lean_contorno", "AxiomasContorno.lean"),
     os.path.join(MED, "lean_contorno", "out", "compile.log"), "PASSA", []),
    ("P5_comentario_com_palavras_proibidas", "SINTETICO (as palavras so em comentario e string)",
     w("p5.lean", "/-- um axiom, um sorry, native_decide: so em docstring -/\nnamespace A\n-- sorry aqui e comentario\ntheorem t : \"axiom\" = \"axiom\" := rfl\nend A\n#print axioms A.t\n"),
     w("p5.log", "'A.t' does not depend on any axioms\n"), "PASSA", []),
]

res, ok = [], 0
for cid, tipo, fonte, log, esperado, motivos_esp in casos:
    p = subprocess.run([sys.executable, AUD, fonte, log], capture_output=True)
    r = json.loads(p.stdout.decode("utf-8"))[0]
    passou = (r["auditoria"] == esperado) and all(m in r["motivos"] for m in motivos_esp)
    ok += passou
    res.append({"caso": cid, "tipo": tipo, "fonte": os.path.relpath(fonte, MED).replace("\\", "/"),
                "fonte_sha16": r["fonte_sha16"], "log": os.path.relpath(log, MED).replace("\\", "/"),
                "log_sha16": r["log_sha16"], "esperado": esperado, "motivos_esperados": motivos_esp,
                "auditoria": r["auditoria"], "motivos": r["motivos"], "rc_auditor": p.returncode,
                "n_theorem_lemma_na_fonte": r["n_theorem_lemma_na_fonte"],
                "n_declaracoes_auditadas": r["n_declaracoes_auditadas"], "conforme": passou})
    print(cid, r["auditoria"], r["motivos"], "conforme" if passou else "NAO CONFORME")

# o auditor v1 (fail-open), sobre o mesmo M7b real: a medida do furo
v1 = os.path.join(MED, "auditor_v1_fail_open", "auditar_axiomas_v1_FAIL_OPEN.py")
p = subprocess.run([sys.executable, v1, os.path.join(C2, "M7b", "out", "compile.log")], capture_output=True)
v1r = json.loads(p.stdout.decode("utf-8"))[0]["auditoria"]
print("auditor v1 sobre M7b:", v1r, "(esperado PASSA = o furo medido)")
out = {"nota": "negativos TEM de dar FALHA; positivos TEM de dar PASSA; tipo REAL = compilacao isolada medida, SINTETICO = so parser",
       "n_casos": len(casos), "n_conformes": ok,
       "n_negativos": sum(1 for c in casos if c[4] == "FALHA"), "n_positivos": sum(1 for c in casos if c[4] == "PASSA"),
       "auditor_v2_sha16": hashlib.sha256(open(AUD, "rb").read()).hexdigest()[:16],
       "auditor_v1_sobre_M7b": v1r, "casos": res}
open(os.path.join(AQUI, "RESULTADO.json"), "wb").write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
print("conformes", ok, "de", len(casos))
sys.exit(0 if ok == len(casos) else 1)
