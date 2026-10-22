# -*- coding: utf-8 -*-
r"""
reauditar_C2.py — reaudita as 8 mutacoes do C2 (fonte + log JA gravados; nao compila nada) com o
auditor v2 vigente, e confere que auditoria e motivos sao IDENTICOS aos do RESULTADO_C2.json.
Motivo: o auditor v2 teve so um nome de variavel trocado depois da compilacao (sha16 antes
db5a0874087bdf62; a logica nao mudou). Grava REAUDITORIA_C2.json.
"""
import hashlib
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(os.path.dirname(AQUI), "auditar_axiomas.py")
c2 = json.load(open(os.path.join(AQUI, "RESULTADO_C2.json"), encoding="utf-8"))
out, iguais = {}, 0
for mid, r in c2.items():
    f = os.path.join(AQUI, r["fonte"])
    log = os.path.join(AQUI, mid, "out", "compile.log")
    assert hashlib.sha256(open(log, "rb").read()).hexdigest()[:16] == r["log_sha16"], mid
    a = json.loads(subprocess.run([sys.executable, AUD, f, log], capture_output=True).stdout.decode("utf-8"))[0]
    igual = (a["auditoria"] == r["auditoria"]) and (a["motivos"] == r["motivos"])
    iguais += igual
    out[mid] = {"auditoria": a["auditoria"], "motivos": a["motivos"], "log_sha16": a["log_sha16"],
                "fonte_sha16": a["fonte_sha16"], "igual_ao_RESULTADO_C2": igual}
    print(mid, a["auditoria"], a["motivos"], "igual" if igual else "DIFERENTE")
res = {"auditor_sha16": hashlib.sha256(open(AUD, "rb").read()).hexdigest()[:16], "n": len(out),
       "n_iguais": iguais, "mutacoes": out}
open(os.path.join(AQUI, "REAUDITORIA_C2.json"), "wb").write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
print("iguais", iguais, "de", len(out), "auditor", res["auditor_sha16"])
sys.exit(0 if iguais == len(out) else 1)
