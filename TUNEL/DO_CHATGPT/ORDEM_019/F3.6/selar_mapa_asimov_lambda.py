"""Create an additive route record for the measured F3.6 Lambda power gate."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile


UNIT = Path(__file__).resolve().parent
SANDBOX = UNIT / "ASIMOV_LAMBDA_SANDBOX"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def artifact(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"caminho": str(path), "sha256": sha(raw), "bytes": len(raw)}


def write_once(path: Path, value: dict) -> None:
    if path.exists():
        raise FileExistsError(path)
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False) as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
        temp = Path(stream.name)
    if temp.stat().st_size != len(raw):
        raise OSError("temporary truncated")
    os.replace(temp, path)
    if path.read_bytes() != raw:
        raise OSError("written bytes differ")


def main() -> None:
    pins = json.loads((SANDBOX / "HASHES_ASIMOV_LAMBDA.json").read_text(encoding="utf-8"))
    for pinned in pins["files"]:
        path = Path(pinned["path"])
        raw = path.read_bytes()
        if len(raw) != pinned["bytes"] or sha(raw) != pinned["sha256"]:
            raise ValueError(f"pin differs: {path}")
    gate = json.loads((SANDBOX / "VALIDACAO_GATE.json").read_text(encoding="utf-8"))
    result = json.loads((SANDBOX / "RESULTADO_ASIMOV_LAMBDA.json").read_text(encoding="utf-8"))
    primary = result["runs"][0]["cases"]["A_bare_corrected"]
    if (gate["status"] != "UNDERPOWERED_DO_NOT_OPEN_DATA__LOCAL_LAMBDA_FISHER__PRECISION_LIMITED"
            or primary["gate"] != "UNDERPOWERED_DO_NOT_OPEN_DATA"
            or gate["sigma_interval_from_steps"]["min"] <= gate["beta_runtime"]
            or gate["observed_means_processed_or_fitted"] is not False):
        raise ValueError("gate contract failed")
    evidence = [
        SANDBOX / "RESULTADO_ASIMOV_LAMBDA.json",
        SANDBOX / "VALIDACAO_GATE.json",
        SANDBOX / "RELATORIO_ASIMOV_LAMBDA.md",
        SANDBOX / "HASHES_ASIMOV_LAMBDA.json",
        SANDBOX / "FREEZE_PRE_RUN.json",
        SANDBOX / "BUILD_LOG.txt",
        UNIT / "PRE_REGISTRO_CONDICIONAL.md",
    ]
    entry = {
        "tipo": "RESULTADO",
        "rota_id": "d1.controle2_w0wa",
        "dominio": "D1_FUNDO_COSMOLOGICO",
        "titulo": "F3.6: portão C16 medido no tangente Λ com β,w0,wa livres; poder insuficiente",
        "pergunta": "No ponto Λ e com covariâncias corrigidas, o controle β livre com w0–wa livres tem σβ menor que β antes de abrir dado?",
        "dados": ["Fiducial sintético H0=67,5, ωb=0,02237, ωc=0,1200, β=0, w0=-1, wa=0",
                  "DESI DR1 com correlações DM–DH e Planck comprimido de Chen et al.; nenhum valor central observado usado",
                  "CAMB 2.0.4 WSL, quinze observáveis sintéticos, seis parâmetros livres"],
        "metodo": "Fisher local no tangente Λ, composições A e B′, fecho H(1)=H0, neutrino massivo lido de E_CAMB²; freeze pré-run, passos de derivada e revisão cética leve.",
        "resultado": "σβ principal=0,01804348 para β runtime=0,01203130 (1,4997β); intervalo dos passos=0,01790070–0,01836213, mínimo=1,4878β. A=B′ no tangente; posto 6. Portão UNDERPOWERED_DO_NOT_OPEN_DATA sob esta especificação.",
        "veredito": "UNDERPOWERED_DO_NOT_OPEN_DATA__LOCAL_LAMBDA_FISHER__PRECISION_LIMITED",
        "estatuto": "REAL numérico local; OPEN modelo CPL fora de Λ",
        "status": "EXAMINADA_COM_DEFEITO",
        "olhou_dados": False,
        "defeito": "Convergência a 0,5% falhou (variação até 1,77%); D1F-04 convenção l_A, likelihood CMB completo, CPL fora de Λ e injeção com ruído não aferidos. Médias publicadas ficaram incidentalmente visíveis na leitura de fonte, mas não entraram no cálculo.",
        "nao_refazer": "Não repetir ajuste V3 a dados, pedir de novo R1–R6 ou abrir dado depois de σβ≥β.",
        "proximo_passo": "Gerência c1 reaudita e decide FECHADA pelo critério local; qualquer controle fora de Λ requer especificação própria e novo pré-registro.",
        "onde": str(UNIT),
        "artefatos": [artifact(path) for path in evidence],
        "refs": ["d1.camb.v3_real"],
        "nota": "ADENDO 004 §4 e auditoria c1 evento 260: resultado negativo de poder não altera gate nem veredito físico V3. Fonte primária DESI https://arxiv.org/html/2404.03002v3 e Chen https://arxiv.org/html/1808.05724 ."
    }
    path = UNIT / "MAPA_ASIMOV_LAMBDA_INPUT.json"
    write_once(path, entry)
    print(json.dumps({"map_input": artifact(path), "beta": gate["beta_runtime"],
                      "sigma_min": gate["sigma_interval_from_steps"]["min"],
                      "sigma_primary": primary["sigma_beta"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
