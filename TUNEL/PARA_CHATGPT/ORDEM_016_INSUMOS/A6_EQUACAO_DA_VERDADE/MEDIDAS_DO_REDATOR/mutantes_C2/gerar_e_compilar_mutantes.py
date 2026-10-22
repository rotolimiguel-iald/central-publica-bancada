# -*- coding: utf-8 -*-
r"""
gerar_e_compilar_mutantes.py — pre-resolucao do ramo C2 do ADENDO 001 (redator, gerencia, 23/09/2026).
Gera POR SCRIPT, a partir da pedra V3 (sha16 conferido), as mutacoes M1..M6, M7a, M7b, cada uma por
substituicao exata com assert count == 1; compila cada uma ISOLADA contra o kernel (so leitura),
UMA DE CADA VEZ; roda o auditor v2 sobre (fonte, log); confere find -newer no kernel = 0.
A pedra V3 e CRLF (medido: 610 CRLF): as ancoras usam o fim de linha do arquivo (NL).
Nao escreve fora desta pasta. Nao executa um.py. Nao roda lake build.
Uso: python gerar_e_compilar_mutantes.py [--so-gerar]
"""
import hashlib
import json
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.join(AQUI, "..", "..", "..", "V3", "TheEquationOfTruth.lean")
AUD = os.path.join(AQUI, "..", "auditar_axiomas.py")
KER = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"

src = open(V3, "rb").read()
assert hashlib.sha256(src).hexdigest()[:16] == "35b91f86b88b8e6c", "pedra V3 divergente"
s = src.decode("utf-8")
CRLF = chr(13) + chr(10)
NL = CRLF if CRLF in s else chr(10)


def L(*linhas):
    """junta linhas com o fim de linha do arquivo"""
    return NL.join(linhas)


MUT = [
    ("M1", "retirar o binder (hH : IsSelfAdjoint H) de proj_mul_H",
     L("theorem proj_mul_H (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)", ""),
     L("theorem proj_mul_H (H : E →L[𝕜] E)", ""), "rc!=0"),
    ("M2", "retirar hpos de flowTendsToFamily_of_finiteDimensional",
     L("theorem flowTendsToFamily_of_finiteDimensional (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)",
       "    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x, H x⟫_𝕜) :", ""),
     L("theorem flowTendsToFamily_of_finiteDimensional (H : E →L[𝕜] E) (hH : IsSelfAdjoint H) :", ""), "rc!=0"),
    ("M3", "retirar (hl : Continuous l) de conserved_iff_factors",
     "(hlim : FlowTendsToFamily Tf P) (l : X → Y) (hl : Continuous l) :",
     "(hlim : FlowTendsToFamily Tf P) (l : X → Y) :", "rc!=0"),
    ("M4", "trocar -(1 / 4) por -(1 / 2) em profA_second_deriv_zero",
     "theorem profA_second_deriv_zero : deriv (deriv profA) 0 = -(1 / 4) := by",
     "theorem profA_second_deriv_zero : deriv (deriv profA) 0 = -(1 / 2) := by", "rc!=0"),
    ("M5", "trocar truthValue 1 0 = 0 por truthValue 1 0 = 1 em truthValue_table",
     "truthValue 1 1 = 1 ∧ truthValue 0 0 = 1 ∧ truthValue 1 0 = 0 ∧ truthValue 0 1 = 0 := by",
     "truthValue 1 1 = 1 ∧ truthValue 0 0 = 1 ∧ truthValue 1 0 = 1 ∧ truthValue 0 1 = 0 := by", "rc!=0"),
]
# M6: o corpo de ker_penalty sai inteiro, por recorte exato entre duas ancoras unicas
KP_INI = L("    (penalty D).ker = ⨅ j, (D j).ker := by", "")
KP_FIM = L("    simp [penalty, h]", "")
FIM_PRINT = "#print axioms TGLExt.EquationOfTruth.profQ_zero" + chr(10)  # a ultima linha da pedra termina em LF (medido)
FAKE = L("", "axiom eot_fake : False", "theorem eot_uses_fake : (1 : Nat) = 2 := eot_fake.elim", "")


def gera():
    out = {}
    for mid, desc, a, b, esp in MUT:
        assert s.count(a) == 1, (mid, s.count(a))
        out[mid] = (desc, s.replace(a, b), esp)
    assert s.count(KP_INI) == 1 and s.count(KP_FIM) == 1, "M6"
    i = s.index(KP_INI) + len(KP_INI)
    j = s.index(KP_FIM, i) + len(KP_FIM)
    out["M6"] = ("trocar a prova inteira de ker_penalty por sorry", s[:i] + "  sorry" + NL + s[j:],
                 "rc0 + auditor FALHA (sorry)")
    assert s.count(FIM_PRINT) == 1 and s.endswith(FIM_PRINT), "fim da pedra inesperado"
    out["M7a"] = ("acrescentar axiom eot_fake : False e um teorema que o use, COM o seu #print axioms",
                  s + FAKE + "#print axioms eot_uses_fake" + NL, "auditor FALHA (fora do trio)")
    out["M7b"] = ("acrescentar axiom eot_fake : False e um teorema que o use, SEM #print axioms",
                  s + FAKE, "auditor FALHA (cobertura; token proibido na fonte)")
    return out


def compila(mid, texto):
    d = os.path.join(AQUI, mid)
    os.makedirs(os.path.join(d, "out"), exist_ok=True)
    f = os.path.join(d, "TheEquationOfTruth%s.lean" % mid)
    open(f, "wb").write(texto.encode("utf-8"))
    marca = os.path.join(d, ".marco_kernel")
    open(marca, "wb").write(b"")
    time.sleep(1.1)
    t0 = time.time()
    p = subprocess.run(["lake", "env", "lean", f, "-R", d, "-o", os.path.join(d, "out", "M.olean")],
                       cwd=KER, capture_output=True)
    wall = time.time() - t0
    log = os.path.join(d, "out", "compile.log")
    open(log, "wb").write(p.stdout + p.stderr)
    mt = os.path.getmtime(marca)
    mudou = [os.path.join(r, x) for r, _, fs in os.walk(KER) for x in fs
             if os.path.getmtime(os.path.join(r, x)) > mt]
    a = subprocess.run([sys.executable, AUD, f, log], capture_output=True)
    aud = json.loads(a.stdout.decode("utf-8"))[0]
    return {"fonte": os.path.relpath(f, AQUI).replace("\\", "/"),
            "fonte_sha16": hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16],
            "rc": p.returncode, "wall_s": round(wall, 1), "kernel_find_newer": len(mudou),
            "log_sha16": hashlib.sha256(open(log, "rb").read()).hexdigest()[:16],
            "n_erros": aud["n_erros"], "auditoria": aud["auditoria"], "motivos": aud["motivos"],
            "sem_print_axioms": aud["sem_print_axioms"], "tokens_proibidos": aud["tokens_proibidos_na_fonte"],
            "fora_do_trio": aud["fora_do_trio"]}


if __name__ == "__main__":
    ms = gera()
    res = {}
    so = "--so-gerar" in sys.argv
    for mid, (desc, t, esp) in ms.items():
        if so:
            res[mid] = {"descricao": desc, "esperado": esp,
                        "sha16": hashlib.sha256(t.encode("utf-8")).hexdigest()[:16], "bytes": len(t.encode("utf-8"))}
            continue
        r = compila(mid, t)
        r["descricao"] = desc
        r["esperado"] = esp
        r["detectada"] = (r["rc"] != 0) if esp == "rc!=0" else (r["auditoria"] == "FALHA")
        res[mid] = r
        print(mid, "rc", r["rc"], "wall", r["wall_s"], "aud", r["auditoria"], r["motivos"],
              "find_newer", r["kernel_find_newer"], "detectada", r["detectada"], flush=True)
    nome = "GERADOS.json" if so else "RESULTADO_C2.json"
    open(os.path.join(AQUI, nome), "wb").write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
    if not so:
        print("detectadas", sum(r["detectada"] for r in res.values()), "de", len(res))
