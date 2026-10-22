# E2 — fechamento independente v2, deltas R1/R2

[REAL] **Papel ACTIVATION: BLOCKERS_CLOSED. blocking_findings: [].** R1 e R2 fechados para o candidato 002 e os bytes abaixo. C1/C3 permanecem fechados pelo parecer anterior; os 39 controles gerais e a ciência não foram repetidos. Este documento substitui somente as pendências R1/R2 do E2_SEALER_CLOSING_REVIEW.md, que permanece preservado.

[INPUT] O GO existente autoriza o principal a prosseguir após revisão, sem nova confirmação humana. Fechamento técnico não é relato de selagem, campanha ou teste físico executado. Não executei selador, assembler, writer, helper PS, guarda de produção ou extrator; não criei/li seed, diretório privado, HDF, posterior, strain ou PE.

## Resultado focado

[REAL] **3/3 grupos de controles passaram**, com quatro recusas negativas e um controle de cabeçalho, além da admissão de referência do helper correto. O candidato foi lido dos bytes e seu SHA256 medido: **d0e9c8fd9de7a1d6e77c10425a6af127625abeb3fa01117e54796f5ca7ca79d0**. Captura 2026-09-22T21:24:48.831223+00:00.

- **R1 CLOSED:** assembler põe o helper no input map; candidato 002 contém o pin medido. Selador compara o hash capturado com esse pin na linha 119, antes de create_seed na linha 151. ACTIVATION precisa conter covered_security_input_sha256 exato e o hash do helper presente no parecer; writer registra essa cobertura e a revalida. Helper ausente/divergente no candidato ou na cobertura é recusado nos blocos novos da AST.
- **R2 CLOSED:** a ficha passa a dizer “exposição conforme declaração vinculada”; o cabeçalho não afirma mais que dados de teste “ainda não lidos” sejam fato REAL. O corpo conserva exposição como declaração do principal e ausência global não demonstrada.

[REAL] Método: somente os condicionais novos extraídos da AST, namespace de teste e mapas em memória; não se chamou main ou create_seed. O estatuto foi conferido no literal AST destinado à ficha. Não houve execução PowerShell ou teste de ACL real. A garantia operacional de permissões continua no alcance da revisão estática e mocks anteriores, não em uma implantação executada por este revisor.

[REAL] Diff contra bis/e2_sealer_snapshot_v2 confirmou alterações focadas: vínculo do helper em assembler/selador/writer, cobertura de segurança de ACTIVATION, arquivo de parecer v2 no writer e cabeçalho da ficha. Os hashes dos três originais preservados conferiram com a rodada anterior. Helper PS e guarda mantêm os pins anteriores. Não reabri fórmulas, forecasts, priors ou ciência E7. NOT_FALSIFIED nunca CONFIRMED.

## Contrato de cobertura para o writer

[REAL] A cobertura abaixo vale exclusivamente para os bytes identificados. Identidade/independência de agentes continua declaração operacional, não assinatura humana ou custódia externa.

```json
{
  "role": "ACTIVATION",
  "status": "BLOCKERS_CLOSED",
  "blocking_findings": [],
  "candidate_sha256": "d0e9c8fd9de7a1d6e77c10425a6af127625abeb3fa01117e54796f5ca7ca79d0",
  "covered_source_sha256": {
    "bis/e2_code/registration_guard.py": "d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9"
  },
  "covered_security_input_sha256": {
    "ORDEM_013_RINGDOWN/refeito/e2_private_directory.ps1": "73247d9846b18b9464355aaf9667b7abaf0f8b8013ea8378034f7fea765761e5"
  },
  "reviewed_sealer_sha256": "ab4ed549b99a4b3ba7558dd20ab71a3034e1aadb8fb31fea1f1c0650ea8ec586",
  "scope": "R1/R2 delta closure plus unchanged C1/C3 closure from prior review; no science or real sealing executed"
}
```

## Pins atuais medidos

| Artefato | SHA256 |
|---|---|
| `bis/E2_REVIEW_CANDIDATE_002.json` | `d0e9c8fd9de7a1d6e77c10425a6af127625abeb3fa01117e54796f5ca7ca79d0` |
| `bis/e2_code/registration_guard.py` | `d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9` |
| `refeito/e2_private_directory.ps1` | `73247d9846b18b9464355aaf9667b7abaf0f8b8013ea8378034f7fea765761e5` |
| `refeito/seal_e2_013bis.py` | `ab4ed549b99a4b3ba7558dd20ab71a3034e1aadb8fb31fea1f1c0650ea8ec586` |
| `refeito/assemble_e2_review_candidate_013bis.py` | `479582e720fefb551b7b38db81169f29d90fbd79db7d0f52b2238ad6bd535a3c` |
| `refeito/write_e2_review_application_013bis.py` | `bc9680dc83627ea7312bf0d13cec761eebd316651cd0aa729b190c07d2ee58e6` |

[REAL] O candidato mantém own14 e guarda d957…; o helper tem exatamente o pin do arquivo consultado. E7 v4/F3 já fechado separadamente em E7_INDEPENDENT_REVIEW_V4.md. Os antigos candidatos/pareceres não foram modificados.

[OPEN — limites preservados] Física, convergência, calibração, normalização/seleção e execução real não são certificadas por este fechamento procedural. A aplicação concreta do GO, seu hash e o marcador final continuam sendo verificados pelas guardas no ato autorizado do principal. Alterações posteriores de fonte/candidato precisam manter a cadeia de revisão; este parecer não aprova bytes futuros.

## Evidência finita

```json
{
  "candidate_sha256": "d0e9c8fd9de7a1d6e77c10425a6af127625abeb3fa01117e54796f5ca7ca79d0",
  "baseline_approved_helper_accepted": true,
  "tests": [
    {
      "name": "R1 missing helper/coverage",
      "passed": true,
      "detail": {
        "candidate_missing_refused": true,
        "application_missing_refused": true
      }
    },
    {
      "name": "R1 changed helper/coverage",
      "passed": true,
      "detail": {
        "bytes_mismatch_refused": true,
        "review_pin_mismatch_refused": true
      }
    },
    {
      "name": "R2 header statute",
      "passed": true,
      "header": "[REAL — reaproveitamento E2; desenho NÃO-CEGO; exposição conforme declaração vinculada]"
    }
  ],
  "passed_groups": 3,
  "helper_check_line": 119,
  "seed_call_line": 151,
  "main_called": false,
  "seed_or_OS_or_production_called": false,
  "math_reexecuted": false
}
```

## Script focado executado em memória

[REAL] Python -B por stdin. Nenhum main de produção é chamado.

```python
from pathlib import Path
import ast,copy,hashlib,json
b=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
raw=(b/"refeito/seal_e2_013bis.py").read_bytes()
assert hashlib.sha256(raw).hexdigest()=="ab4ed549b99a4b3ba7558dd20ab71a3034e1aadb8fb31fea1f1c0650ea8ec586"
candidate_raw=(b/"bis/E2_REVIEW_CANDIDATE_002.json").read_bytes()
assert hashlib.sha256(candidate_raw).hexdigest()=="d0e9c8fd9de7a1d6e77c10425a6af127625abeb3fa01117e54796f5ca7ca79d0"
reg=json.loads(candidate_raw)
helper="ORDEM_013_RINGDOWN/refeito/e2_private_directory.ps1"
pin=hashlib.sha256((b/"refeito/e2_private_directory.ps1").read_bytes()).hexdigest()
tree=ast.parse(raw)
main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="main")
check=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="check_review_application")
early=next(n for n in ast.walk(main) if isinstance(n,ast.If) and any(isinstance(x,ast.Constant) and x.value=="Private ACL helper differs from approved candidate" for x in ast.walk(n)))
coverage=next(n for n in ast.walk(check) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and isinstance(n.test.left,ast.Name) and n.test.left.id=="role" and any(isinstance(x,ast.Constant) and x.value=="ACTIVATION" for x in ast.walk(n.test)))
seedline=min(n.lineno for n in ast.walk(main) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="create_seed")
assert early.lineno<seedline
def block(n,env):exec(compile(ast.Module(body=[n],type_ignores=[]),"review_R1_AST_only","exec"),env)
def env():
 return {"reg":copy.deepcopy(reg),"helper_pin":pin,"role":"ACTIVATION","review":{"covered_security_input_sha256":{helper:pin}},"texts":["reviewed helper "+pin]}
base=env();block(early,base);block(coverage,base)
def rejects(n,e):
 try:block(n,e)
 except (ValueError,KeyError):return True
 return False
e=env();e["reg"]["input_pins_relative_to_Chatgpt"].pop(helper)
f=env();f["review"].pop("covered_security_input_sha256")
missing={"candidate_missing_refused":rejects(early,e),"application_missing_refused":rejects(coverage,f)}
assert all(missing.values())
e=env();e["helper_pin"]="0"*64
f=env();f["review"]["covered_security_input_sha256"][helper]="0"*64
changed={"bytes_mismatch_refused":rejects(early,e),"review_pin_mismatch_refused":rejects(coverage,f)}
assert all(changed.values())
fiche=next(n for n in ast.walk(main) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="create" and isinstance(n.args[0],ast.Name) and n.args[0].id=="fiche")
texts=[n.value for n in ast.walk(fiche) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
header=next(t.split("\n")[0] for t in texts if t.startswith("[REAL"))
assert "exposi\u00e7\u00e3o conforme declara\u00e7\u00e3o vinculada" in header
assert "ainda n\u00e3o lidos" not in header
print(json.dumps({"candidate_sha256":hashlib.sha256(candidate_raw).hexdigest(),"baseline_approved_helper_accepted":True,"tests":[{"name":"R1 missing helper/coverage","passed":True,"detail":missing},{"name":"R1 changed helper/coverage","passed":True,"detail":changed},{"name":"R2 header statute","passed":True,"header":header}],"passed_groups":3,"helper_check_line":early.lineno,"seed_call_line":seedline,"main_called":False,"seed_or_OS_or_production_called":False,"math_reexecuted":False}))

```

