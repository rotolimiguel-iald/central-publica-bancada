# E7 v4 — fechamento independente focado F3

[REAL] **Papel E7: BLOCKERS_CLOSED; blocking_findings: [].** F3 corrigido nos bytes abaixo. F1/F2 permanecem fechados pelo parecer v3. Isto é fechamento técnico do produtor E7, não execução, registro E2 ou autorização de extração. O GO existente do operador rege as etapas pelo principal após revisão; nenhuma nova confirmação humana é solicitada.

[REAL] Conferi HANDOFF_FINAL_v4, MANIFEST_FINAL_v4, UNIT_TESTS_F3_V4 e a alteração de código. Capturei os produtores em 2026-09-22T21:15:39.432569+00:00. Os **10/10 controles independentes** de cronologia passaram; **9/9 arquivos do manifesto** concordam em tamanho e SHA256. O fragmento e seu descritor concordam com os pins. Snapshot v3 tem o hash de manifesto esperado.

[REAL] Alteração AST de funções v3→v4: somente checked_authorization. Extrator byte a byte inalterado. Não reexecutei matemática, os 46 testes v3 ou as regressões anteriores. A adição de datetime é stdlib. Fórmulas, priors, pairing, fonte pinada e estatutos permanecem no alcance das revisões anteriores; NOT_FALSIFIED nunca CONFIRMED.

> [nota operacional do operador — omitida no retrato público]

[DECLARADO] O recibo do autor relata sete testes incrementais. A minha evidência é a execução independente de dez casos abaixo, não repetição ou apropriação da suíte do autor.

[REAL] Contrato atual: timestamp textual, fuso obrigatório e E2 <= autorização <= agora; prazo global continua responsabilidade distinta da guarda. O principal fornece caminho/hash do recibo independentemente do JSON posterior. Hash fixa bytes; não autentica pessoa.

[INPUT] Pin da guarda será recalculado no assembly final conforme ordem. O pin observado no fragmento não aprova futuras guardas. Integração de ativação/sealer é revisada separadamente em E2_SEALER_CLOSING_REVIEW.md.

## Pins de produtor cobertos por este fechamento

- `bis/e7_prepare/producer/tgl_ringdown_ampliacao.py`: `99a9ebc8e8a22c3a14f06b8f6dd465400beaf4d95cbef989d7d5652b5b4b8355`.
- `bis/e7_prepare/producer/extrai_posteriores_pseob.py`: `3e896bd014db610c9b83c6171de2b3b98db506e597b068da20617e189734e330`.
- MANIFEST_FINAL_v4.json: `229dc0a299098d1cd8ee97cb541e4ca42e084861a8c4f4131c9140989b31fbc2`.

## Evidência independente

```json
{
  "tests": [
    {
      "case": "future",
      "passed": true,
      "payload_sentinel_reached": false,
      "error": "Principal authorization is future-dated"
    },
    {
      "case": "naive",
      "passed": true,
      "payload_sentinel_reached": false,
      "error": "Timezone required"
    },
    {
      "case": "malformed",
      "passed": true,
      "payload_sentinel_reached": false,
      "error": "Invalid isoformat string: 'invalid'"
    },
    {
      "case": "nontext",
      "passed": true,
      "payload_sentinel_reached": false,
      "error": "Explicit authorization and E2 UTC timestamps required"
    },
    {
      "case": "missing",
      "passed": true,
      "payload_sentinel_reached": false,
      "error": "Explicit authorization and E2 UTC timestamps required"
    },
    {
      "case": "predates_E2",
      "passed": true,
      "payload_sentinel_reached": false,
      "error": "Principal authorization predates E2"
    },
    {
      "case": "UTC_valid",
      "passed": true,
      "payload_sentinel_reached": true,
      "error": null
    },
    {
      "case": "offset_valid",
      "passed": true,
      "payload_sentinel_reached": true,
      "error": null
    },
    {
      "case": "equal_now",
      "passed": true,
      "payload_sentinel_reached": true,
      "error": null
    },
    {
      "case": "equal_E2",
      "passed": true,
      "payload_sentinel_reached": true,
      "error": null
    }
  ],
  "passed": 10,
  "total": 10,
  "only_changed_functions": [
    "checked_authorization"
  ],
  "added_functions": [],
  "manifest_audit": {
    "producer/extrai_posteriores_pseob.py": {
      "sha256": "3e896bd014db610c9b83c6171de2b3b98db506e597b068da20617e189734e330",
      "bytes": 7673,
      "passed": true
    },
    "producer/tgl_ringdown_ampliacao.py": {
      "sha256": "99a9ebc8e8a22c3a14f06b8f6dd465400beaf4d95cbef989d7d5652b5b4b8355",
      "bytes": 29940,
      "passed": true
    },
    "E2_INCLUDE_FINAL_v4.json": {
      "sha256": "5d351ffb05dada66f890b1d13812c28fd2bb4b321f772c80ae29d1d9fe3a8d76",
      "bytes": 48532,
      "passed": true
    },
    "HANDOFF_FINAL_v4.md": {
      "sha256": "90c6abe7a6b0777c8fd10178277f63bf803eb886e642e52ed236c7b248253d86",
      "bytes": 2353,
      "passed": true
    },
    "EXTRACTION_PLAN.json": {
      "sha256": "7dc138a1690d45d381fc36d6e5cb54967b028741158f625ac814fb92159a7335",
      "bytes": 47760,
      "passed": true
    },
    "UNIT_TESTS_F3_V4.json": {
      "sha256": "9e3865500180e117237a970c5352412d532a7c3215e15c1f2df7b70f2ec25dcb",
      "bytes": 680,
      "passed": true
    },
    "UNIT_TESTS_F3_V4.log": {
      "sha256": "d45eac9ab79920551b8f39c7396746e23b8c8dd5a3f095ba3e09cd8fd66681d2",
      "bytes": 1003,
      "passed": true
    },
    "tests/test_authorization_v4.py": {
      "sha256": "6583917c5de711615fc458418f205df757482c4c313b0eaca88c3283207253e4",
      "bytes": 3147,
      "passed": true
    },
    "tests/finalize_F3_v4.py": {
      "sha256": "be62b295d6a5952a5346e91903c188a4e09f1d0249cba6d7433d332c2b8e9468",
      "bytes": 4391,
      "passed": true
    }
  },
  "snapshot_v3_manifest_hash_matches": true,
  "fragment_tree_matches": true,
  "assembly_fragment_pin_matches": true,
  "manifest_sha256": "229dc0a299098d1cd8ee97cb541e4ca42e084861a8c4f4131c9140989b31fbc2",
  "math_reexecuted": false,
  "extractor_imported": false,
  "files_written": false,
  "real_data_or_seed_accessed": false
}
```

## Script de controle em memória

[REAL] Executado por stdin com Python -B. Não há função de selagem nem leitura de seed/dados.

```python
from pathlib import Path
from datetime import datetime,timezone
import ast,json,hashlib,types,copy
b=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN");p=b/"bis/e7_prepare"
raw=(p/"producer/tgl_ringdown_ampliacao.py").read_bytes()
assert hashlib.sha256(raw).hexdigest()=="99a9ebc8e8a22c3a14f06b8f6dd465400beaf4d95cbef989d7d5652b5b4b8355"
tree=ast.parse(raw)
selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ("run","checked_authorization")]
fixed=datetime(2026,9,22,21,20,tzinfo=timezone.utc)
class Clock:
 @staticmethod
 def now(tz):return fixed
def utc(s):
 d=datetime.fromisoformat(s.replace("Z","+00:00"))
 if d.tzinfo is None:raise ValueError("Timezone required")
 return d.astimezone(timezone.utc)
env={"datetime":Clock,"timezone":timezone}
exec(compile(ast.Module(body=selected,type_ignores=[]),"pinned_F3_functions","exec"),env)
spec={"plan_path":"plan","nuisance_path":"nuisance","plan_sha256":"b"*64,"producer_tree_sha256":{"consumer.py":"c"*64}}
reg={"registered_utc":"2026-09-22T20:00:00+00:00","e7":spec}
baseauth={"status":"AUTHORIZED_BY_PRINCIPAL_AFTER_E2","registration_sha256":"a"*64,"plan_sha256":"b"*64,"producer_tree_sha256":spec["producer_tree_sha256"],"registered_utc":"2026-09-22T21:00:00+00:00"}
class Reached(Exception):pass
records=[]
for label,value,allow in [
 ("future","2026-09-22T21:20:00.000001+00:00",False),
 ("naive","2026-09-22T21:00:00",False),
 ("malformed","invalid",False),("nontext",7,False),("missing",None,False),
 ("predates_E2","2026-09-22T19:59:59+00:00",False),
 ("UTC_valid","2026-09-22T21:00:00+00:00",True),
 ("offset_valid","2026-09-22T18:00:00-03:00",True),
 ("equal_now",fixed.isoformat(),True),("equal_E2",reg["registered_utc"],True)]:
 reads=[];auth=copy.deepcopy(baseauth);auth["registered_utc"]=value
 def reader(path):
  reads.append(path)
  if path=="plan":return {"events":[{"role":"calibration"}]}
  if path=="nuisance":return {"gate":{}}
  if path=="auth":return auth
  if path=="payload":raise Reached()
  raise AssertionError(path)
 env.update(checked_context=lambda *a:(reg,types.SimpleNamespace(utc=utc)),contained=lambda root,path:path,require_pin=lambda *a:None,read_json=reader)
 reached=False;error=None
 try:env["run"]("root","reg","a"*64,"payload","d"*64,"auth","e"*64)
 except Reached:reached=True
 except (ValueError,TypeError) as e:error=str(e)
 records.append({"case":label,"passed":reached==allow and (allow or "payload" not in reads),"payload_sentinel_reached":reached,"error":error})
man=json.loads((p/"MANIFEST_FINAL_v4.json").read_bytes())
audit={}
for n,v in man["files"].items():
 data=(p/n).read_bytes();actual=hashlib.sha256(data).hexdigest()
 audit[n]={"sha256":actual,"bytes":len(data),"passed":actual==v["sha256"] and len(data)==v["bytes"]}
oldraw=(p/"snapshot_v3_before_F3_fix/producer/tgl_ringdown_ampliacao.py").read_bytes()
def funcs(r):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(r).body if isinstance(n,ast.FunctionDef)}
old,new=funcs(oldraw),funcs(raw)
inc=json.loads((p/"E2_INCLUDE_FINAL_v4.json").read_bytes())
assembly=json.loads((p/"E7_ASSEMBLY_V4.json").read_bytes())
snapman=(p/"snapshot_v3_before_F3_fix/MANIFEST_FINAL_v3.json").read_bytes()
out={"tests":records,"passed":sum(r["passed"] for r in records),"total":len(records),"only_changed_functions":sorted(k for k in old.keys()&new.keys() if old[k]!=new[k]),"added_functions":sorted(new.keys()-old.keys()),"manifest_audit":audit,"snapshot_v3_manifest_hash_matches":hashlib.sha256(snapman).hexdigest()==man["snapshot_v3_manifest_sha256"],"fragment_tree_matches":inc["e7"]["producer_tree_sha256"]==man["producer_tree_sha256"],"assembly_fragment_pin_matches":assembly["fragment_sha256"]==hashlib.sha256((p/"E2_INCLUDE_FINAL_v4.json").read_bytes()).hexdigest(),"manifest_sha256":hashlib.sha256((p/"MANIFEST_FINAL_v4.json").read_bytes()).hexdigest(),"math_reexecuted":False,"extractor_imported":False,"files_written":False,"real_data_or_seed_accessed":False}
print(json.dumps(out))

```

