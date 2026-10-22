"""Read-only source and pin audit of installed N_eff/neutrino channels.

Creates only new evidence beside this script. Does not import audited modules,
run a channel, execute um.py, fit data, modify Bancada, or modify memory.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
CENTRAL = Path(r"C:\IALD\Central de Patentes")
UNIT = CENTRAL / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019"
BENCH = Path(r"C:\IALD\Bancada_Um")
FILES = {
    "mcp_wrappers": BENCH / "mcp_um.py",
    "neff_installed": BENCH / "bancada/neff_canal.py",
    "neutrino_v1": BENCH / "bancada/neutrino_canal.py",
    "neutrino_v2": BENCH / "bancada/neutrino_canal_v2.py",
    "manifest_v1": BENCH / "bancada/neutrino_fontes_f72.json",
    "manifest_v2": BENCH / "bancada/neutrino_fontes_f72_v2.json",
    "neff_frozen": Path(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py"),
    "neff_candidate_r3": UNIT / "F5.2/CANDIDATO_R3_20261008/neff_canal.py",
    "neff_candidate_r2": UNIT / "F5.2/CANDIDATO_R2_20261008/neff_canal.py",
    "neff_errata": UNIT / "F5.2/ERRATA_C1_R2_R4_R5_20261008.md",
    "neff_extraction_r3": UNIT / "F5.2/EXTRACAO_TABELA5_R3_20261008.json",
    "neff_result_r3": UNIT / "F5.2/RESULTADO_F52_R3_20261008.json",
    "phase8_preregistration": BENCH / "investigacao/preregistro_fase8_primordial/PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json",
    "um_current_source": Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"),
}
OUTPUT_NAMES = ("CHANNEL_AUDIT_R1.json", "CHANNEL_AUDIT_R1.md", "CONSULTA_NOS_VIVO_R1.txt", "CHANNEL_AUDIT_RECEIPT_R1.json")
for name in OUTPUT_NAMES:
    if (OUT / name).exists():
        raise FileExistsError(OUT / name)

started = datetime.now(timezone.utc).isoformat()
cache: dict[Path, bytes] = {}

def get_bytes(path: Path) -> bytes:
    if path not in cache:
        cache[path] = path.read_bytes()
    return cache[path]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def describe(path: Path) -> dict:
    try:
        raw = get_bytes(path)
        return {"path": str(path), "sha256": sha(raw), "bytes": len(raw), "exists": True}
    except OSError as exc:
        return {"path": str(path), "exists": False, "error": str(exc)}

def constants(path: Path) -> dict:
    tree = ast.parse(get_bytes(path).decode("utf-8-sig"), filename=str(path))
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        result[target.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError, SyntaxError):
                        pass
    return result

def anchors(key: str, patterns: list[str]) -> list[dict]:
    lines = get_bytes(FILES[key]).decode("utf-8-sig").splitlines()
    return [{"line": i, "text": line} for i, line in enumerate(lines, 1)
            if any(pattern in line for pattern in patterns)]

consultations = []
for name in ("F0.3.B1", "F0.3"):
    command = [r"C:\Python314\python.exe", "-B", r"C:\IALD\NOS_VIVO\consultar.py", "--unidade", name]
    run = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    consultations.append({"command": command, "exit_code": run.returncode, "stdout": run.stdout, "stderr": run.stderr})
consultation_text = "\n\n".join("COMMAND " + json.dumps(x["command"], ensure_ascii=False) + "\nEXIT " + str(x["exit_code"]) + "\n" + x["stdout"] + "\nSTDERR\n" + x["stderr"] for x in consultations)

inventory = {key: describe(path) for key, path in FILES.items()}
manifest_results = {}
all_entries = []
for version in ("v1", "v2"):
    manifest_path = FILES["manifest_" + version]
    manifest = json.loads(get_bytes(manifest_path))
    expected_manifest = constants(FILES["neutrino_" + version])["MANIFEST_SHA256"]
    entries = []
    for group in ("scripts", "documents", "primary_pdfs"):
        group_entries = manifest.get(group, [])
        if isinstance(group_entries, dict):
            group_entries = [{"entry_key": key, **value} for key, value in group_entries.items()]
        for item in group_entries:
            path = Path(item["path"])
            measured = describe(path)
            row = {"group": group, "key": item.get("entry_key", item.get("name", path.name)),
                   "expected_sha256": item["sha256"], "expected_bytes": item.get("bytes"), **measured}
            row["matches_sha256"] = measured.get("sha256") == item["sha256"]
            row["matches_bytes"] = measured.get("bytes") == item.get("bytes")
            if group == "primary_pdfs" and measured["exists"]:
                row["pdf_header_valid"] = get_bytes(path).startswith(b"%PDF-")
            entries.append(row)
            all_entries.append(row)
    manifest_results[version] = {"schema": manifest["schema"], "expected_manifest_sha256": expected_manifest,
                                "actual_manifest_sha256": sha(get_bytes(manifest_path)),
                                "manifest_matches": sha(get_bytes(manifest_path)) == expected_manifest,
                                "entry_count": len(entries),
                                "all_entry_pins_match": all(e["matches_sha256"] and e["matches_bytes"] for e in entries),
                                "entries": entries}

copied_root = BENCH / "fontes_externas/F7.2"
copied = []
for path in sorted(copied_root.rglob("*")):
    if path.is_file():
        item = describe(path)
        item["same_bytes_as_manifest_entries"] = sorted({e["path"] for e in all_entries if e.get("sha256") == item.get("sha256")})
        copied.append(item)

frozen = constants(FILES["neff_frozen"])
source_anchors = {
    "mcp_wrappers": anchors("mcp_wrappers", ["def neff_canal", "def neutrino_canal", "import neff_canal", "import neutrino_canal", "return {\"erro\"", "mcp.run()"]),
    "neff_installed": anchors("neff_installed", ["FROZEN =", "UM =", "def beta_runtime", "re.search", "def ler_fonte", "return env", "_sha(p)", "sigmas_extra", "NEFF_SM", "def controle", "quando_declarado"]),
    "neff_frozen": anchors("neff_frozen", ["CMB-SPA", "CMB-S4", "SO-ASO", "Simons", "NEFF_SM", "MEDIDAS =", "PROJECOES ="]),
    "neutrino_v2": anchors("neutrino_v2", ["MANIFEST_SHA256", "DOC_PATHS", "channel_power_table", "clock_v369_result", "Sec. IV.B", "operator_mapping_to_TGL", "SEM_LIMITE_TGL", "raw_experimental_data_custodied", "READ_ONLY_SOURCE_PROVENANCE", "CONDITIONAL_5SIGMA_PROJECTION"]),
    "neff_candidate_r3": anchors("neff_candidate_r3", ["Uninstalled", "uninstalled", "pinned", "X16", "D8", "v1", "v2"]),
}

findings = [
 {"id":"N1", "status":"REAL — inspeção estática e bytes", "severity":"material", "title":"O canal N_eff conserva a linha CMB-SPA errada e os calendários antigos", "evidence":"neff_canal.py:23,38-47,63-71 lê as literais de 10_frozen_neff_v1.py:46,50-53. A linha CMB-SPA 2,97±0,12 é a mistura já corrigida na F5.2; R3 oferece v1/v2 e Yp separados, sem estar instalado. O rótulo DECLARADO não torna correto o centro misturado. Os calendários são devolvidos como quando_declarado, não como medição.", "action":"Preparar uma implantação explicitamente autorizada do candidato corrigido ou suspender a superfície incorreta até ela; não editar o congelado nem decidir X16/D8 nesta auditoria."},
 {"id":"N2", "status":"REAL — código; riscos DERIVED", "severity":"material", "title":"Hashes informados não são pins verificados em N_eff", "evidence":"neff_canal.py:28-47 calcula SHA do congelado e um.py, mas não compara com um manifesto esperado. ler_fonte extrai AST de uma leitura e _sha(p) relê o arquivo: o hash devolvido pode nomear bytes diferentes dos valores, se houver troca entre leituras. beta_runtime extrai ALPHA_FINE_CODATA_2018 por regex e calcula α√e; não executa um.py.", "action":"Uma futura camada deve ler bytes uma vez, verificar identidade contra manifesto/versionamento e explicitar a versão; nenhuma alteração feita."},
 {"id":"N3", "status":"DERIVED — inspeção de fluxo; não executado", "severity":"validation", "title":"Entradas sigma de N_eff não têm validação finita e positiva", "evidence":"neff_canal.py:54-77 converte sigmas_extra por float e divide sem rejeitar bool, NaN, infinito ou negativos. zero levanta erro. A assinatura MCP float pode validar parte do transporte, mas a função local não o faz; a configuração real do serializador não foi sondada. neff wrapper:247-248 retorna somente erro, enquanto neutrino inclui ok:false.", "action":"Rejeitar tipos/valores inválidos antes das contas e padronizar erro explícito em camada autorizada. A auditoria não invocou o MCP."},
 {"id":"V1", "status":"REAL — código e pins medidos", "severity":"capability", "title":"Neutrino v1/v2 verificam custódia; não realizam um teste espectral", "evidence":"Manifestos e todos os bytes vinculados foram relidos e comparados nesta evidência. O código valida caminhos, SHA, tamanhos, AST dos scripts e cabeçalho PDF. canal retorna números publicados hardcoded com fonte pinada; não extrai curvas de verossimilhança, matriz resposta ou eventos. Mantém operator_mapping_to_TGL OPEN, tau_star_limit_s null e SEM_LIMITE_TGL.", "action":"Reutilizar como proveniência. Um teste novo exige dissipador TGL, resposta, ruídos e verossimilhança próprios; n=-2 sozinho não identifica os operadores."},
 {"id":"V2", "status":"REAL — caminhos e bytes", "severity":"dependency", "title":"Cópia R8 da Bancada permanece sem consumidor nos dois canais", "evidence":"neutrino_canal_v2.py:18-38 e manifesto apontam para documentos/PDFs no túnel, seis scripts de junho na casa Física e JSON v369 no project_fisica. Nenhum aponta a fontes_externas/F7.2. A pasta foi inventariada por bytes. Sua presença não prova ativação ou autocontenção do canal.", "action":"Manter fontes intactas; eventual migração exige evento c1 nomeado. Estado de processo/MCP ativo é apurado pelo coordenador."},
 {"id":"V3", "status":"REAL — texto do código; errata c1 já existente", "severity":"documentary", "title":"Âncoras antigas ainda são emitidas", "evidence":"V2:296 conserva Sec. IV.B junto de Eq.(6) para JUNO; a correção c1 aponta §III.B. O v1 conserva âncoras De Romeri/ORCA antigas e não tem JUNO. Os documentos posteriores no túnel não mudaram os literais emitidos pelas funções instaladas.", "action":"Registrar camada corretiva, sem tocar fontes pinadas nem instalar sem ato c1."},
 {"id":"V4", "status":"REAL — contrato lido", "severity":"scope", "title":"A referência v369 é uma projeção histórica explícita", "evidence":"V2:189-214 verifica no JSON pinado five_sigma_requirement; :344-371 rotula CONDITIONAL_5SIGMA_PROJECTION e observed_measurement false. Não é leitura do resultado científico atual do um.py. Também não reivindica limite TGL nem resultado 5σ.", "action":"Preservar qualificação histórica e distinguir cálculo de poder condicional de teste com dados. Não transplantar a projeção ao um.py recente por nome."},
 {"id":"S1", "status":"REAL — âmbito desta auditoria", "severity":"scope", "title":"A auditoria cobre arquivo instalado, não prova carregamento de processo", "evidence":"Nenhum original foi importado; nenhuma ferramenta MCP/neff/neutrino foi chamada; nenhum provedor, dado observado, GPU ou um.py foi executado. Os únicos comandos executados, além deste leitor, foram consultas de índice e leitura de arquivos. pyc presente não foi usado como prova de módulo carregado.", "action":"Cruzar com a auditoria de processo/versão conduzida pela gerência desta unidade."},
]

audit = {"schema":"iald.f0_3_b1.channel_audit.v1", "unit":"F0.3.B1", "claim_event":621,
         "author":"codex subagent nu2_data_sources", "started_at_utc":started,
         "finished_at_utc":datetime.now(timezone.utc).isoformat(),
         "mode":"STATIC_READ_ONLY_NO_CHANNEL_EXECUTION", "files":inventory,
         "consultations":[{k:v for k,v in x.items() if k not in ("stdout","stderr")} for x in consultations],
         "reused":"Nós Vivo F0.3: rota AUDITADA e catálogo/geração v391; F0.3.B1 ainda ausente no grafo. Fontes F5.2/F7.2 abertas diretamente, sem inferir seu conteúdo do índice.",
         "manifest_integrity":manifest_results, "copied_r8_sources":copied,
         "frozen_literal_content":{"NEFF_SM":frozen["NEFF_SM"], "MEDIDAS":frozen["MEDIDAS"], "PROJECOES":frozen["PROJECOES"]},
         "source_anchors":source_anchors, "findings":findings,
         "writes":"Somente script e novos artefatos derivados em F0.3.B1/channels_inventory. Nenhum byte da Bancada, memória, kernel, congelado ou fonte alterado.",
         "gate_effect":"NONE", "source_bytes_custody":"Os hashes foram medidos nos bytes locais; originais não foram copiados para esta pasta."}
summary = ["# F0.3.B1 — auditoria dos canais N_eff e neutrino, R1", "",
           f"[REAL] Unidade reivindicada, evento 621. Início UTC: {started}. Auditoria de arquivos instalados; execução e versão ativa são apuradas em outra subtarefa.", "",
           "## Reaproveitamento e método", "",
           audit["reused"], "", "Foram lidos os módulos, manifestos, fontes pinadas e as correções F5.2 já existentes. Não foram executados canais, um.py, ajuste de dados, controle GPU ou fornecedores. Os PDFs foram somente verificados como bytes/cabeçalho; seu conteúdo não foi reextraído nesta auditoria.", "",
           "## Resultado", ""]
for f in findings:
    summary += [f"### {f['id']} — {f['title']}", "", f"[{f['status']}] {f['evidence']}", "", f"Encaminhamento: {f['action']}", ""]
summary += ["## Integridade medida", "", "| Canal | Pin do manifesto | Dependências |", "|---|---|---|"]
for version,result in manifest_results.items():
    summary.append(f"| {version} | {'CONFERE' if result['manifest_matches'] else 'DIVERGE'} | {result['entry_count']} entradas; {'todas conferem' if result['all_entry_pins_match'] else 'há divergência — ver JSON'} |")
summary += ["", f"A cópia R8 contém {len(copied)} arquivos medidos; os caminhos e equivalências por SHA estão no JSON.", "", "## Hashes dos módulos", ""]
for key in ("mcp_wrappers","neff_installed","neutrino_v1","neutrino_v2","manifest_v1","manifest_v2","neff_candidate_r3","neff_frozen","um_current_source"):
    item=inventory[key]
    summary += [f"- `{key}`: `{item.get('sha256', 'ERRO_DE_LEITURA')}` — `{item['path']}`"]
summary += ["", "O JSON inclui a lista completa de pins, âncoras com linha e os valores literais auditados. Esta camada não declara conteúdo científico validado por mera coincidência de hash.", "", audit["writes"], "Nada move o gate.", ""]

def write_new(name: str, raw: bytes) -> dict:
    path = OUT / name
    with path.open("xb") as stream:
        stream.write(raw)
    measured = path.read_bytes()
    if measured != raw:
        raise OSError("written bytes differ: " + str(path))
    return {"path":str(path), "sha256":sha(measured), "bytes":len(measured)}

outputs = [write_new("CONSULTA_NOS_VIVO_R1.txt", consultation_text.encode("utf-8")),
           write_new("CHANNEL_AUDIT_R1.json", (json.dumps(audit,ensure_ascii=False,indent=2)+"\n").encode("utf-8")),
           write_new("CHANNEL_AUDIT_R1.md", "\n".join(summary).encode("utf-8"))]
receipt={"unit":"F0.3.B1","claim_event":621,"generated_at_utc":datetime.now(timezone.utc).isoformat(),
         "mode":"new_files_exclusive_write","outputs":outputs,"script":describe(Path(__file__).resolve()),
         "bancada_write_performed":False,"memory_write_performed":False,"channel_execution_performed":False}
receipt_info=write_new("CHANNEL_AUDIT_RECEIPT_R1.json",(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"manifest_summary":{k:{q:v[q] for q in ("manifest_matches","entry_count","all_entry_pins_match")} for k,v in manifest_results.items()},"r8_files":len(copied),"outputs":outputs,"receipt":receipt_info},ensure_ascii=False,indent=2))
