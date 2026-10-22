"""Custody a single T08 MiMo protocol unit before queue submission."""
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAT = HERE.parents[3]
BASE = CHAT / "ORDEM_013_RINGDOWN"
CENSUS = BASE / "bis" / "e1_selection" / "CALIBRATION_AND_CANDIDATE_CENSUS.json"
ORDER = CHAT / "TUNEL" / "PARA_CHATGPT" / "ORDEM_015_continuacao_do_ringdown_rumo_ao_5sigma.md"
OUT = HERE / "T08_MIMO_REQUEST.json"

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

census = json.loads(CENSUS.read_bytes())
rows = census["SNR_ge12_metadata_rows"]
assert len(rows) == 74
assert not OUT.exists()
prompt = (
    "ORDEM016 Parte B, T08/PASSO14. Uma questão de rascunho técnico: dê o protocolo mínimo "
    "e as equações para medir rho_inspiral e rho_pos-inspiral (critério LVK >=8 E >=8) "
    "no MAP GR público e PSD pública para os 74 eventos O4 SNR>=12; depois estimar "
    "epsilon(theta) com IC e alpha(Lambda) por leitura usando injeções baratas sem PE. "
    "Diga quais dados faltam, onde a condição [INPUT] da fronteira GWTC3 Tabela4 entra, "
    "como evitar confundir rho da potência F4 de 10tM com matched-filter SNR e "
    "como tratar evento sem PSD ou MAP. Entregue algoritmo curto, critérios falsificáveis "
    "e lista de campos para a tabela por evento. NÃO execute, NÃO infira 74 MAP/PSD disponíveis "
    "de um censo só de metadados, NÃO invente epsilon/alpha/sigma/gate. "
    f"Ordem015 SHA256={sha(ORDER)}; censo SHA256={sha(CENSUS)}. "
    f"Censo: 74 linhas, campos={list(rows[0])}; apenas SNR_network_GWOSC e "
    "GR_final_mass_detector_median/GR_final_spin_median como mediana, não MAP. "
    "O4a=28, O4b=45, O4c_discovery_only=1. Pasta pública local contém GWTC3 e GWTC5, "
    "mas sua cobertura não equivale a 74 posteriors GR. "
    "T07 anterior: 31/33 potências da janela calculadas; 17 excessos positivos, "
    "14 não positivos; a interpretação física segue aberta. "
    "Estatuto obrigatório: DECLARADO; uma proposta de protocolo não é prova nem medição."
)
req = {
    "operation": "submit",
    "request_id": str(uuid.uuid4()),
    "prompt": prompt,
    "execution_constraints": {
        "mission_id": "ORDEM_016", "branch_id": "B_T08",
        "lemma_id": "selection_protocol_draft",
        "role": "draft", "required_provider": "mimo", "max_calls": 1,
        "max_cost_usd": 0.5,
    },
}
record = {"created_utc": datetime.now(timezone.utc).isoformat(),
          "request_id": req["request_id"], "origin": "ORDEM_016/PART_B/T08",
          "census_sha256": sha(CENSUS), "order_sha256": sha(ORDER),
          "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
          "queue_payload": req, "status": "PREPARED_NOT_SUBMITTED"}
raw = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode()
with OUT.open("xb") as stream:
    stream.write(raw)
print(json.dumps({"request_id": req["request_id"], "request_sha256": sha(OUT),
                  "prompt_chars": len(prompt)}))
