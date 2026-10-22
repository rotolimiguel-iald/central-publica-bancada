"""Prepare immutable, provider-specific ORDEM_018 requests without sending them."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from iald_orchestrator import canonical_memory
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.safe_files import save_json, utc_now


BASE = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE / "campaign.json"
CHATGPT = BASE.parent
SOURCES = {
    "resident_plan": CHATGPT / "TGL_BANCADA_OFICIAL" / "PLANO_UNIVERSO_RESIDENTE.md",
    "time_audit": CHATGPT / "TGL_BANCADA_OFICIAL" / "TIME_SOURCE_AUDIT.md",
    "c0_adendum": CHATGPT / "ORDEM_013_RINGDOWN" / "C0_ADENDO_FRASES_PUBLICAS.md",
    "c7_status": CHATGPT / "ORDEM_013_RINGDOWN" / "C7_GWTC3_REPRODUCTION_v3_2" / "README.md",
    "o15_audit": CHATGPT / "ORDEM_013_RINGDOWN" / "bis" / "015" / "closing_audit" / "T01_T13_CLOSING_AUDIT.md",
    "data_catalog": CHATGPT / "TGL_BANCADA_OFICIAL" / "data_lab.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    campaign = json.loads(CAMPAIGN.read_bytes())
    manifest, freshness = canonical_memory.load(refresh=False)
    um = next(doc for doc in manifest["documents"] if doc["name"] == "um.py")
    if (manifest["generation"] != campaign["canonical_memory"]["generation"]
            or um["sha256"] != campaign["um_py"]["sha256"]):
        raise ValueError("Canonical memory or v375 source changed; no request prepared")

    source_receipt = {
        key: {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}
        for key, path in SOURCES.items()
    }
    save_json(HERE / "local_sources.json", {
        "checked_at": utc_now(),
        "canonical_generation": manifest["generation"],
        "canonical_freshness": freshness,
        "sources": source_receipt,
        "scope": "Local scientific references; not automatically transported in full",
    })

    shared = f"""ORDEM_018, campanha de sensibilidade científica TGL, proposta independente da rodada 1.
[REAL local] um.py v375: {um['bytes']} bytes; SHA-256 {um['sha256']}. Índice comum: geração {manifest['generation']}, {len(manifest['documents'])} documentos e {manifest['chunks']} trechos. O pacote efetivamente anexado pelo adaptador é recuperação PARCIAL, com referências e linhas no recibo. Não declare ter lido integralmente v375 ou toda a TGL; liste lacunas importantes.

Evidência local medida ou documentada, que deve ser confrontada com o contexto fornecido:
- Universo GW residente U1: 180 arquivos strain GWOSC, 900 arrays, 22,50550 GiB em RAM; 173 hashes de strain distintos. Sete cópias não são observações independentes. U3 (PSD/DQ, projeção do detector e posterior por evento), U4 (likelihood/controles) e U6 (busca conjunta) ainda são etapas dependentes no plano.
- O ringdown existente distingue R-A Planck, R-B massa e R-MOD condicional, ensemble versus realização estocástica; τ*, τ_GR e o relógio modular têm estatutos/hipóteses diferentes. Não escolher leitura silenciosamente.
- Auditoria C0: GW V2 razão efeito/erro 0,177851σ; R-B ensemble correção/σ 0,343377425. D1 V3 encontrou tensão de 3,0124975σ do beta livre contra α√e, não confirmação TGL. βτ* é degenerado sem relógio externo.
- Auditoria ORDEM_015: T03 teve 0/30 células aceitas, nulos/sistemáticas não pagos; T04 sem posterior físico aceito, ramo F ESS 3051,78 mas sigma inelegível; T05 N90 O5/R-B 2289,94 condicional e sem sistemática; T11 2,952854σ contra a escala declarada de neutrino, sem nova determinação; T12 0 eventos cegos. C7 é reprodução não cega condicional, com calibração de fonte livre e mapeamento da realização ainda abertos.
- data_lab.py cataloga fontes instaladas, não valida automaticamente a física: no contexto sandbox foram vistos 856 arquivos elegíveis, inclusive 610 do snapshot v350, 176 strain 013BIS, 4 strain GWOSC O4b, 65 posteriores públicos e 1 tabela GWTC-3. A raiz BAO externa não ficou acessível nessa leitura; não inferir que esteja ausente. KiDS e outros catálogos existem no snapshot, mas relevância/colunas/covariância exigem confirmação.

Âncoras locais com hash calculado (as referências não concedem acesso a caminhos do meu disco): {json.dumps({k: {'sha256': v['sha256'], 'bytes': v['bytes']} for k, v in source_receipt.items()}, ensure_ascii=False)}.

Objetivo: propor teste que, com dados ATUAIS efetivamente instalados, tenha melhor poder discriminante TGL versus rival especificado e estimar se >=5σ de significância global seria alcançável. Separe poder prospectivo, estimativa condicional, significância observada e confirmação física. Não some sigmas, não fabrique medidas, não trate catálogo não cego como descoberta virgem, não mova gate. Se as entradas não sustentarem cálculo quantitativo, entregue fórmula, parâmetros ausentes e medição local necessária. Não execute código, não peça credenciais, não use acervo jurídico. Preserve [REAL]/[DERIVED]/[INPUT]/[CONJECTURE]/[OPEN]/[DECLARADO].
"""

    specifics = {
        "kimi": "Mapeie rotas físicas independentes (GW ringdown/eco, cosmologia, neutrino e outras sustentadas), compare poder discriminante TGL versus GR/ΛCDM/hipótese nula, selecione uma rota prioritária e uma reserva. Identifique previsão fixa, modelo rival, escala de efeito, sensibilidade atual e maior obstáculo quantitativo. Não use nomes de lemas como previsão empírica.",
        "mimo": "Audite observáveis, dados realmente instalados, unidade, ruído, PSD, DQ, calibração, seleção, covariâncias e reproduzibilidade. Calcule apenas limites/poder numéricos autorizados pelas entradas; diga por que dados faltantes ou degenerações impedem estimativa de 5σ. Proponha controles nulos e injeção-recuperação concretos para a melhor rota.",
        "deepseek": "Faça análise cética da estatística conjunta: defina hipótese nula/alternativa, teste e calibração global, parâmetros nuisance, correlações, trials/look-elsewhere, seleção pós-observação e vieses. Procure falsas rotas para >=5σ nos resultados C0/C7/015 e proponha regra adversarial de parada. Não combine eventos ou domínios sem modelo conjunto e covariância.",
    }
    roles = {"kimi": "draft", "mimo": "draft", "deepseek": "skeptic"}
    runtime = Runtime(recover=False)
    previews = {}
    for provider, detail in specifics.items():
        prompt = shared + "\nTAREFA ESPECÍFICA PARA " + provider.upper() + ": " + detail
        request_id = campaign["wave_1"][provider]["request_id"]
        constraints = {
            "mission_id": "TGL_BANCADA_OFICIAL",
            "branch_id": "ORDEM_018_SENSITIVITY",
            "lemma_id": "wave1_" + provider + "_v375",
            "role": roles[provider],
            "required_provider": provider,
            "max_calls": 1,
            "memory_generation": manifest["generation"],
            "allowed_sources": ["um.py"],
        }
        record = {
            "operation": "submit",
            "prompt": prompt,
            "request_id": request_id,
            "execution_constraints": constraints,
        }
        path = HERE / "wave1" / (provider + "_submit.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if json.loads(path.read_bytes()) != record:
                if campaign["state"] != "wave_1_prepared_not_dispatched":
                    raise ValueError("Request may have been submitted; do not change it")
                save_json(path, record)
        else:
            save_json(path, record)
        preview = runtime.preview(prompt, constraints)
        if preview.get("selected") != provider:
            raise ValueError("Mandatory provider not selected for " + provider)
        previews[provider] = {
            "selected": preview["selected"],
            "request_id": request_id,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "prompt_bytes": len(prompt.encode("utf-8")),
            "preview": preview,
        }
    save_json(HERE / "wave1" / "previews.json", previews)
    campaign["wave_1_prepared_at"] = utc_now()
    campaign["state"] = "wave_1_prepared_not_dispatched"
    campaign["source_receipt"] = str(HERE / "local_sources.json")
    save_json(CAMPAIGN, campaign)
    print(json.dumps({name: {k: value[k] for k in ("selected", "request_id", "prompt_sha256", "prompt_bytes")}
                      for name, value in previews.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
