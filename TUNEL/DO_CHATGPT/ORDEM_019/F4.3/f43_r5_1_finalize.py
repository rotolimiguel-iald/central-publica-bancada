"""Finalize the additive R5.1 contract correction in new files only."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p)}
def put(p,value):
    raw=value.encode("utf-8") if isinstance(value,str) else (json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    with p.open("xb") as f: f.write(raw)
    assert sha(p)==hashlib.sha256(raw).hexdigest()
wrapper=root/"f43_r5_1_calibrated_gate.py"
test=root/"F43_R5_1_SYNTHETIC_SELFTEST_20261008.json"
testcode=root/"f43_r5_1_selftest.py"
r5=root/"RESULTADO_F43_R5_20261008.json"
v1=root/"PREREGISTRO_F4_3_V4_R5_20261008.json"
t=json.loads(test.read_text(encoding="utf-8"))
assert t["wrapper_sha256"]==sha(wrapper)
note=f"""# F4.3 — correção R5.1 ao lado, contrato de calibração (08/10/2026)

Em nome de codex-gerente-tgl, sob a reivindicação F4.3 do quadro. O Nós Vivo foi consultado antes desta camada: rota ringdown.modo_unico.degenerescencia, V1 Ramo B, C7/QNM_GRID e R4/R5 já existem. A R5 permanece íntegra (RESULTADO SHA-256 {sha(r5)}; função SHA-256 {t["r5_function_sha256"]}). Esta camada não reescreve nenhum arquivo da R5.

## Defeito e correção

[REAL — leitura de código] A função R5 aceitava p_reject_B, p_reject_GR e systematics_ok como valores simples. O texto da R5 dizia p unilateral e FWER, mas a assinatura não exigia origem, calibração sob a nula nomeada nem cobertura. Portanto uma entrada arbitrária poderia aparentar 5σ.

[REAL — implementação] O wrapper f43_r5_1_calibrated_gate.py (SHA-256 {sha(wrapper)}) é a porta para qualquer uso da função R5. Em produção ele exige SETE recibos com caminho e SHA-256 verificados: poder exato, controles sistemáticos, cauda sob B, cauda sob GR, token oficial V1, forma de onda executável full IMR de fonte comum e auditoria c1. Exige evento de auditoria, hashes de V1, especificação F4.3, coorte e PSD de projeto. O hash do contrato de forma de onda da R5 não vale como hash de executável.

Cada cauda deve declarar nula B ou GR, p unilateral calibrado sob essa nula, alpha=2,8665×10⁻⁷, cobertura do nulo PASS e vínculo ao mesmo resultado de poder. O wrapper DERIVA p_B e p_GR dos recibos, sem aceitar os números da pessoa chamadora. Os controles PSD, família, início, cobertura, viés e estabilidade rcond também são DERIVADOS de recibo vinculado ao poder. Um token V1 direcional exige recibo de sua própria cauda unilateral calibrada sob a mesma nula, com p≤alpha. A regra de FWER é a interseção dos dois testes sobre a MESMA nula nomeada: nenhum produto, soma de p ou independência é presumido. A função oficial do V1 permanece em campo separado. A validação de formato/hash pelo wrapper não substitui a auditoria científica c1 dos cálculos.

[REAL — teste sintético, sem valor probatório físico] O modo de teste exige a chave SYNTHETIC_TEST_ONLY e retorna SYNTHETIC_ONLY_NOT_EVIDENCE. O modo de produção recusa esse recibo. Houve {t["malformed_contracts_refused"]} contratos malformados recusados, além dos limiares exatamente em alpha, acima dele, concordância na mesma nula e falha PSD. O recibo de teste é {test.name}, SHA-256 {sha(test)}. Nenhum dado D, hdf5, strain, posterior, PE ou campanha de injeções foi aberto/rodado.

[OPEN] Não há hoje os sete recibos de produção: poder exato, forma de onda executável e auditoria c1 seguem ausentes. Assim o portão permanece AWAITING_POWER, o pedido ao operador SUSPENSO e o gate intocado. A campanha exata é cálculo novo e aguarda o levantamento do ADENDO 001.
"""
note_path=root/"ADENDO_F43_R5_1_CALIBRACAO_20261008.md"
put(note_path,note)
result={
 "unit":"F4.3","layer":"R5.1","status":"ENTREGUE_PARA_AUDITORIA__AWAITING_POWER",
 "author":"codex-gerente-tgl","created_utc":datetime.now(timezone.utc).isoformat(),
 "sources":[pin(r5),pin(v1)],
 "artifacts":[pin(wrapper),pin(testcode),pin(test),pin(note_path)],
 "risk_fixed":"raw numeric p values and systematics Boolean accepted by R5 without calibration attestation",
 "production_receipts_required":7,"production_receipts_available":0,
 "operator_request":"SUSPENDED","observational_data_opened":False,
 "exact_injections_run":False,"gate_moved":False,"memory_touched":False}
result_path=root/"RESULTADO_F43_R5_1_20261008.json"
put(result_path,result)
route={
 "tipo":"ERRATA","rota_id":"ringdown.modo_unico.degenerescencia","dominio":"RINGDOWN",
 "titulo":"F4.3 R5.1: porta de calibração para as duas caudas",
 "pergunta":"Como recusar p unilateral ou systematics_ok sem recibos de calibração sob cada nula e FWER V1?",
 "dados":[],"metodo":"QA de assinatura R5/V1, wrapper fail-closed e testes 100% sintéticos",
 "resultado":"Wrapper deriva p_B, p_GR e sistemáticas só de sete recibos pinados; produção recusa recibo sintético. Nenhum recibo real disponível; AWAITING_POWER preservado.",
 "veredito":"F43_R5_1_CALIBRATION_CONTRACT__AWAITING_POWER__NO_DATA_OPENED__GATE_NONE",
 "estatuto":"REAL","status":"EXAMINADA_COM_DEFEITO","olhou_dados":False,
 "defeito":"Poder exato e adaptação IMR não executados; nenhum recibo científico de produção",
 "nao_refazer":"R5 pinada íntegra; V1 e C7 sem alteração",
 "proximo_passo":"Levantamento ADENDO 001, campanha exata, auditoria c1, só depois ato do operador para D",
 "onde":str(root),"artefatos":[
  {"caminho":str(result_path),"bytes":result_path.stat().st_size,"sha256":sha(result_path)},
  {"caminho":str(wrapper),"bytes":wrapper.stat().st_size,"sha256":sha(wrapper)},
  {"caminho":str(test),"bytes":test.stat().st_size,"sha256":sha(test)},
  {"caminho":str(note_path),"bytes":note_path.stat().st_size,"sha256":sha(note_path)}],
 "refs":["ringdown.ramo_b_preregistro_v386"],
 "corrige":928,
}
map_path=root/"MAPA_F43_R5_1_20261008.json"
put(map_path,route)
print(json.dumps({"result":pin(result_path),"map":pin(map_path),"note":pin(note_path)},ensure_ascii=False))