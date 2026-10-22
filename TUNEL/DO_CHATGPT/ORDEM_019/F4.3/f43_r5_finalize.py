"""Write new R5 receipt, explanation and map entry; no source modification."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p)}
def freeze(p,raw):
    with p.open("xb") as f: f.write(raw)
    assert sha(p)==hashlib.sha256(raw).hexdigest()
def jbytes(v): return (json.dumps(v,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
spec=ROOT/"PREREGISTRO_F4_3_V4_R5_20261008.json"
verdict=ROOT/"f43_r5_verdict.py"
test=ROOT/"F43_R5_SYNTHETIC_SELFTEST_20261008.json"
builder=ROOT/"f43_r5_build.py"
selftest=ROOT/"f43_r5_selftest.py"
inventory=ROOT/"f43_r4_inventory.py"
s=json.loads(spec.read_text(encoding="utf-8"))
t=json.loads(test.read_text(encoding="utf-8"))
assert len(s["fields_13"])==13 and t["cases"]==2240
assert s["sources"]["R4_inventory_generator"]["sha256"]==sha(inventory)
note=f"""# F4.3 — R5 documental ao lado da V3 (08/10/2026)

Em nome de codex-gerente-tgl, sob a reivindicação F4.3. [REAL documental] O Nós Vivo localizou a rota ringdown.modo_unico.degenerescencia, o V1 do ramo B, C7, QNM_GRID e a F4.3 R4. O V1 permanece primário, IMR completo; F4.3 é diagnóstico 220+440. Nenhum hdf5, strain, posterior, PE ou conjunto D foi aberto. Nenhuma injeção exata foi rodada.

## Treze campos

[INPUT pinado] O novo pré-registro PREREGISTRO_F4_3_V4_R5_20261008.json tem 13 campos não nulos. A coorte sintética contém os 10 elegíveis sem os quatro data_quality_hold do V1; qualquer mudança da lista real do D exige novo registro antes de poder ou abertura. A PSD de projeto C7 é a curva ASD O4 aLIGO_O4_high_asd.txt (SHA-256 {s["fields_13"]["psd_hashes"]["curve"]}), elevada ao quadrado para a PSD de H1 e L1 em cada evento; não é PSD fora da fonte por evento. Janelas, priors, covariância, semente e contagens estão em arquivos próprios. f43_r4_inventory.py também está pinado: SHA-256 {sha(inventory)}.

[OPEN] O campo waveform_hash fixa o CONTRATO de forma de onda de fonte comum (SHA-256 {s["fields_13"]["waveform_hash"]}), não um executável pSEOB 220+440. O adaptador full IMR, a injeção exata e a calibração da cauda seguem trabalho de construção da gerência. Os 13 campos de desenho não constituem poder medido. O resultado vigente é AWAITING_POWER; o pedido ao operador continua SUSPENSO.

## Função de veredito

[REAL — execução sintética] f43_r5_verdict.py (SHA-256 {sha(verdict)}) recebe o token oficial V1 e o preserva em v1_official_token_public_unchanged; devolve o token secundário em diagnostic_token_local. Valida os sufixos AWAITING_DATA__INSUFFICIENT_SAMPLE e NOT_FALSIFIED_UNDERPOWERED__POWER_x_OF_5_SIGMA (x<5). A leitura conjunta é descritiva, sem substituir a palavra do V1.

A precedência é a PRIMEIRA LINHA QUE CASAR: AWAITING_POWER → UNDERPOWERED/NONIDENTIFIABLE → INCONCLUSIVE_SYSTEMATICS → BOTH_MODELS_REJECTED → CONFLICTS_V1 → CORROBORATES_V1 → NEITHER_REJECTED → NO_V1_DIRECTION. Em {t["overlap_cases"]} de {t["cases"]} combinações sintéticas, mais de uma linha casou; nenhuma ficou sem token. UNDERPOWERED vem antes de INCONCLUSIVE apenas na função local porque a potência exata é pré-requisito do diagnóstico; causas sistêmicas continuam em matched_rows, e a ordem oficial do V1 não muda.

«Aponta oposto» significa: exatamente uma nula F4.3 rejeitada com p unilateral ≤ 2,8665×10⁻⁷, diferente da nula nomeada como rejeitada no V1. Se as duas caem, vale BOTH_MODELS_REJECTED; se o V1 não nomeia direção, vale NO_V1_DIRECTION com revisão cética quando pertinente. NOT_FALSIFIED_POWERED nunca sai da F4.3. O campo público oficial é o token V1 preservado; diagnostic_token_local é interno.

## Poder e próximo passo

[DERIVED condicional] η=25 é precisamente a regra do V1 |δ_pred|/σ_usado≥5 elevada ao quadrado. Num deslocamento gaussiano simples rende cerca de 50% de chance de cruzar 5σ; cobrar recuperação ≥90% na F4.3 é mais duro que o V1. η_440≥1 é só relevância mínima do segundo modo. A campanha exata com C3, fonte comum e nulos calibrados é cálculo novo: espera o levantamento do ADENDO 001. Falha de cauda, cobertura, viés, rcond ou família produz diagnóstico inconclusivo, sem abrir D. A PSD de projeto foi escolhida pela c1; nenhum ato do operador é exigido para medir o poder sintético. Abrir D continua ato específico posterior.
"""
note_path=ROOT/"ADENDO_F43_R5_20261008.md"
freeze(note_path,note.encode("utf-8"))
artifacts=[spec,verdict,test,builder,selftest,inventory,note_path]
artifacts += [Path(v["path"]) for v in s["artifacts"].values() if Path(v["path"]) not in artifacts]
result={
 "unit":"F4.3","layer":"R5","status":"ENTREGUE_PARA_AUDITORIA__AWAITING_POWER",
 "author":"codex-gerente-tgl","created_utc":datetime.now(timezone.utc).isoformat(),
 "consultar_nos_vivo":["ringdown.modo_unico.degenerescencia","V1 Ramo B","C7","QNM_GRID","F4.3 R4"],
 "sources":s["sources"],"artifacts":[pin(p) for p in artifacts],
 "fields_nonnull":13,"synthetic_selftest_cases":t["cases"],"synthetic_overlap_cases":t["overlap_cases"],
 "exact_power_measured":False,"waveform_adapter_executable":False,
 "PSD_regime":"C7 project ASD for H1/L1, V1 blind medians",
 "operator_request":"SUSPENDED","observational_data_opened":False,"gate_moved":False,
 "memory_surfaces_touched":[]}
result_path=ROOT/"RESULTADO_F43_R5_20261008.json"
freeze(result_path,jbytes(result))
route={
 "tipo":"RESULTADO","rota_id":"ringdown.modo_unico.degenerescencia","dominio":"RINGDOWN",
 "titulo":"F4.3 R5: manifesto documental e função de veredito",
 "pergunta":"A F4.3 pode fixar os 13 campos e a precedência do diagnóstico antes do poder sintético?",
 "dados":[],"metodo":"Nós Vivo; V1/C7/V3 pinados; PSD de projeto e medianas cegas; 2240 combinações sintéticas, sem dado D",
 "resultado":"Treze campos de desenho pinados, inclusive inventário R4. Função executável fixa precedência e limiar de oposição; 2240 casos sintéticos, zero sem token. Hash de forma de onda é contrato, implementação IMR conjunta aberta. Poder exato não medido.",
 "veredito":"F43_R5_DOCUMENTED__AWAITING_POWER__OPERATOR_REQUEST_SUSPENDED__NO_DATA_OPENED__GATE_NONE",
 "estatuto":"DERIVED","status":"EXAMINADA_COM_DEFEITO","olhou_dados":False,
 "defeito":"Adaptador full IMR 220+440 e campanha exata ainda não construídos/rodados",
 "nao_refazer":"V1, C7, F4.3 V2/V3/R4 e inventário continuam íntegros; não transportar Fisher k=1",
 "proximo_passo":"Levantamento ADENDO 001, construção do adaptador, poder exato, reauditoria c1; só depois pedido específico de abertura",
 "onde":str(ROOT),"artefatos":[pin(result_path),pin(spec),pin(verdict),pin(test),pin(note_path)],
 "refs":["ringdown.ramo_b_preregistro_v386"]}
map_path=ROOT/"MAPA_F43_R5_20261008.json"
freeze(map_path,jbytes(route))
print(json.dumps({"result":pin(result_path),"map":pin(map_path),"note":pin(note_path)},ensure_ascii=False))