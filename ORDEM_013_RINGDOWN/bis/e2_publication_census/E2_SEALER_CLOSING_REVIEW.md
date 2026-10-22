# E2 — fechamento independente crítico do selador

[REAL] **Candidato 001: conferido para preparação/revisão; selagem ainda pendente de dois ajustes localizados.** C1 CLOSED; C3 CLOSED nos bytes atuais; C2/C4 PARTIAL, com os resíduos R1/R2 abaixo. Não registrar este parecer global como BLOCKERS_CLOSED enquanto R1/R2 permanecerem abertos.

[INPUT] O GO existente autoriza execução pelo principal após revisão. Não se pede nova autorização humana. Nenhuma produção foi modificada ou executada por este revisor. Este parecer não demonstra campanha executada, cegueira absoluta, custódia humana independente ou confirmação física.

[REAL] Conferência do candidato em 2026-09-22T21:20:41.540740+00:00: `bis/E2_REVIEW_CANDIDATE_001.json`, SHA256 **d4d91d925e449441bc726d7313f247fca11a72726b3473c65bf901f4328e0161**, lido dos bytes por script. Own code: 14 arquivos, todos com pin conferido; extra code: 68 entradas declaradas; 48 identidades de calibração/exclusão e 14 elegíveis ausentes no escopo. Nesta etapa não reauditei cientificamente as 68 entradas extras. Caminho declarado da seed é o subdiretório privado contratado; nenhum arquivo de seed foi sondado/lido/criado.

[REAL] Evidência independente: **39/39 controles finitos**, mais **5/5** focados nos 16 pins exigidos pelo candidato concreto (14 own + 2 E7). Somente funções extraídas da AST, mocks de IO/OS/ACL, mapa de bytes fictícios e sentinelas. Nenhum main de selador/assembler/writer/guarda foi executado; nenhuma chamada PowerShell de produção, descritor real de seed ou diretório privado real foi criado. No mock, os 32 bytes são constantes fictícias em memória; a função os.urandom real não é chamada. Não houve HDF, posterior, strain, PE, waveform, MC ou repetição matemática.

[REAL] Helper PowerShell: leitura estática e parsing pelo parser PowerShell, zero erros sintáticos; não executado. Portanto a ordem dos checks está avaliada, mas não afirmo ter medido ACL efetiva de um diretório privado real.

## C1 — CLOSED no contrato de aplicação declarado

[REAL] O selador exige candidato SHA da CLI, sealer SHA e aplicação com hash esperado; papéis exatos PE/MAIN/E7/ACTIVATION; BLOCKERS_CLOSED e blocking_findings=[] por papel; identidade distinta declarada entre construtor/revisor; arquivos de parecer pinados; cobertura que coincide com a união das árvores exigidas, com os pins presentes nos textos; GO existente pinado sob PARA_CHATGPT; exposição tipada como declaração.

[REAL] Os mocks recusaram papéis faltantes/extras, achados abertos, status inadequado, identidade igual, candidato/selador divergentes, cobertura incompleta/obsoleta, pin de parecer/GO errado, GO fora do diretório e aplicação futura. Os cinco casos concretos conferiram especificamente a cobertura dos pins do candidato 001.

[DECLARADO] O writer novo é ato técnico do principal após ler os pareceres. Ele declara fechamento/independência, não faz análise semântica dos textos nem autentica humanos. A ocorrência de um hash num parecer negativo não significa aprovação. Essa limitação está explícita e o principal não deve marcar BLOCKERS_CLOSED contra as conclusões efetivas deste parecer.

## C2 — ordem de proteção corrigida; vínculo de helper ainda OPEN (R1)

[REAL] Paths críticos agora são fixos, resolvidos, sem symlinks/reparse points observados na cadeia de teste, com destinos e temporários distintos; tentativa anterior impede retry silencioso. Prepare/Verify de ACL precedem o primeiro descritor; abertura exclusiva inclui O_BINARY; VerifySeed precede o hard link final. Os mocks demonstraram recusa de traversal/absoluto/redirecionamento e ausência de descritor quando Prepare/Verify falham; tamanho inválido/VerifySeed falho não publica link.

[REAL] O PS monta DACL protegida, um único Allow FullControl para o SID atual, com herança aos objetos/containers; verifica diretório e temporário. Same-user/WSL continuam no alcance procedural declarado. Não executei esses comandos; não converti leitura estática em prova de ACL implantada.

**R1 — P2, bloqueante antes da selagem: pin aprovado do helper ACL não está vinculado ao candidato/aplicação.**

[REAL] O candidato 001 não contém `ORDEM_013_RINGDOWN/refeito/e2_private_directory.ps1` em input_pins nem nas raízes extras. O selador captura esse arquivo no início (linha 113) e o revalida com stable(), mas não compara a captura com pin previamente aprovado. O writer também não inclui o helper entre os pins que vincula ao GO. O hash lido nesta revisão está na tabela abaixo.

[DERIVED] Alteração do helper **antes** da captura inicial pode ser absorvida como nova base estável, sem mudar o sealer pin, o candidato ou o conjunto de fontes exigidas na aplicação. Snapshot estável não substitui vínculo com os bytes revisados de um componente que controla privacidade.

Correção mínima: acrescentar o pin do helper à entrada congelada do candidato ou a um campo explícito da aplicação, conferir contra os bytes aprovados antes de chamar Prepare e mantê-lo na rechecagem; registrar a cobertura correspondente na revisão ACTIVATION. Pode ser resolvido por nova montagem com pin de input, aproveitando a checagem de input já existente. Não é necessário mudar ciência, executar ACL real ou gerar seed para verificar esse vínculo.

## C3 — CLOSED na guarda atual e no marcador final

[REAL] Guarda **d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9** exige recibo E2_ACTIVATION_COMPLETE antes de seguir à verificação integral de runtime/código. Confere paths fixos; pins de aplicação e selador; registro/witness; timestamps; candidato da proveniência; aplicação emitida no máximo no registro; quatro papéis; achados vazios; arquivos de revisão pinados. A divergência inicial de três/quatro papéis foi corrigida pelo responsável durante esta revisão; não a atribuo à fonte final.

[REAL] Mocks recusaram ausência do marcador, status parcial, registro/witness/selador divergentes, recibo futuro, candidato errado, aplicação posterior ao registro, papel faltante e finding aberto. O caso positivo terminou em True somente com marcador completo. Isto testa a função isolada; não chama checked_registration real nem runtime científico.

[REAL] No selador, o recibo final é publicado depois de witness, stable() e nova conferência de prazo. A nota isolada agora diz que não ativa o registro. Falha antes do marcador deixa tentativa parcial preservada e não concede ativação pela guarda. O recibo liga artefatos locais; não vira custódia externa.

[DECLARADO] Li integralmente ACTIVATION_V2_CLOSING_RECEIPT.json: o autor registra 38 mocks. Não os contabilizo como meus. Seu pin de guarda/selador confere com os bytes usados aqui. Pin do recibo: `b3df1827d4387de3e4584a93fa739774c87bd64a2a35af7b2fc6970bd948f7e3`. Pin medido de ACTIVATION_MARKER_MOCKS_V2.json: `88419225e5dc51ce63289e416238ac29723bfe9fe8008af1e214b3e408a84b6b`, igual ao apontado no recibo. O recibo ainda informa repin de dependência Kerr antes de execução; não certifico esse repin nesta revisão.

## C4 — snapshots/declaração corrigidos; cabeçalho ainda OPEN (R2)

[REAL] O conteúdo JSON do candidato e seu digest vêm dos mesmos bytes; fonte Python é parseada dos bytes capturados. Hashes capturados são reutilizados na proveniência. stable() recusa mudança em nova captura e antes da ativação; o assembler também revalida antes de publicar. Os mocks cobriram mudança A→B na segunda leitura e na conferência final. Estatísticas do censo, holds, leituras e duração do piloto agora vêm do candidato.

[REAL] A proveniência usa executed_science_by_this_sealing_step=False e exposure_history da aplicação; o writer preserva exposição incidental e UNKNOWN fora do trabalho registrado. Essa tipagem é apropriada. Os controles não demonstram história universal de acesso.

**R2 — P2, bloqueante documental antes da ficha final: afirmação absoluta no cabeçalho.**

[REAL] A linha 161 do selador ainda gera `[REAL — reaproveitamento E2; desenho NÃO-CEGO, dados novos de teste ainda não lidos]`. A sentença atribui a REAL a ausência de leitura, enquanto o corpo passa corretamente a tratar exposição como declaração do principal. A alteração do corpo não corrige o estatuto do cabeçalho.

Correção mínima: cabeçalho “desenho NÃO-CEGO; exposição conforme declaração vinculada”, ou separação explícita REAL para artefatos e DECLARADO para exposição no escopo. Preservar UNKNOWN fora do trabalho e o incidente do censo. Nenhuma nova busca de posterior ou prova de cegueira é solicitada.

## E7 v4 e ciência

[REAL] F3 da E7 v4 está **CLOSED** em E7_INDEPENDENT_REVIEW_V4.md: 10/10 controles focados, só checked_authorization alterada, sem repetir matemática. F1/F2 permanecem fechados pela v3. A fonte atual e os dois pins E7 estão naquele parecer. Este documento não reabre fórmulas, nuisance, forecasts, prior handling ou pairing já revisados. Estatutos e limites físicos continuam os da fonte. NOT_FALSIFIED nunca CONFIRMED.

## Pins operacionais desta revisão

| Fonte | SHA256 |
|---|---|
| `refeito/seal_e2_013bis.py` | `ce99da4a9e16405c5f469d8a7cfa956ffcdf044d4fbce99d731e3a226e90cdc6` |
| `refeito/e2_private_directory.ps1` | `73247d9846b18b9464355aaf9667b7abaf0f8b8013ea8378034f7fea765761e5` |
| `refeito/assemble_e2_review_candidate_013bis.py` | `b87a3008c39ccb6887c21fe816ac48c14567827da30f6bf5904d5f8e358365e9` |
| `refeito/write_e2_review_application_013bis.py` | `d7e534e206278b888063dd5f545dcb8774aeaf604de64155896b4a68c0365553` |
| `bis/e2_code/registration_guard.py` | `d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9` |

[REAL] Pins inteiros lidos por script. O pin da guarda no candidato 001 confere. O fragmento v4 no candidato tem SHA256 `5d351ffb05dada66f890b1d13812c28fd2bb4b321f772c80ae29d1d9fe3a8d76`. Não confundir pins de revisões parciais anteriores com aprovação destes bytes.

## Resultado para o principal

[OPEN] Preparar candidato é admissível. Para marcar fechamento global de selagem: resolver R1/R2, emitir os novos pins/candidato quando necessário e fazer fechamento somente dessas diferenças. C1 e C3 não exigem repetição ampla; ciência E7 está fechada no alcance declarado. A execução pelo principal seguirá o GO já existente e a guarda final; este revisor não executa selagem.

## Apêndice — resultados finitos independentes

[REAL] “ACCEPT” em testes de falha de ACL significa que o teste observou a recusa esperada dentro do mock e aprovou a propriedade de segurança, não que a ACL defeituosa foi aceita em produção.

```json
{
  "captured_pins": {
    "sealer": "ce99da4a9e16405c5f469d8a7cfa956ffcdf044d4fbce99d731e3a226e90cdc6",
    "guard": "d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9",
    "assembler": "b87a3008c39ccb6887c21fe816ac48c14567827da30f6bf5904d5f8e358365e9",
    "acl": "73247d9846b18b9464355aaf9667b7abaf0f8b8013ea8378034f7fea765761e5",
    "writer": "d7e534e206278b888063dd5f545dcb8774aeaf604de64155896b4a68c0365553"
  },
  "results": [
    {
      "name": "C1 valid exact 16-source application",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": 4
    },
    {
      "name": "C1 missing_role",
      "passed": true,
      "outcome": "REJECT",
      "error": "Four distinct review roles required"
    },
    {
      "name": "C1 extra_role",
      "passed": true,
      "outcome": "REJECT",
      "error": "Four distinct review roles required"
    },
    {
      "name": "C1 open_status",
      "passed": true,
      "outcome": "REJECT",
      "error": "Unclosed review E7"
    },
    {
      "name": "C1 blocking_findings",
      "passed": true,
      "outcome": "REJECT",
      "error": "Unclosed review PE"
    },
    {
      "name": "C1 same_builder",
      "passed": true,
      "outcome": "REJECT",
      "error": "Distinct reviewer declaration required"
    },
    {
      "name": "C1 candidate",
      "passed": true,
      "outcome": "REJECT",
      "error": "GO/review applies to other bytes"
    },
    {
      "name": "C1 sealer",
      "passed": true,
      "outcome": "REJECT",
      "error": "GO/review applies to other bytes"
    },
    {
      "name": "C1 missing_coverage",
      "passed": true,
      "outcome": "REJECT",
      "error": "Incomplete current-source review coverage"
    },
    {
      "name": "C1 bad_coverage",
      "passed": true,
      "outcome": "REJECT",
      "error": "Review coverage does not match source bis/e2_code/code0.py"
    },
    {
      "name": "C1 bad_review_pin",
      "passed": true,
      "outcome": "REJECT",
      "error": "Review evidence changed"
    },
    {
      "name": "C1 GO_pin",
      "passed": true,
      "outcome": "REJECT",
      "error": "Existing GO source differs"
    },
    {
      "name": "C1 GO_outside",
      "passed": true,
      "outcome": "REJECT",
      "error": "Existing GO source differs"
    },
    {
      "name": "C1 absolute_exposure",
      "passed": true,
      "outcome": "REJECT",
      "error": "Exposure history must remain a declaration"
    },
    {
      "name": "C1 future_application",
      "passed": true,
      "outcome": "REJECT",
      "error": "Review application chronology invalid"
    },
    {
      "name": "C2 fixed path valid",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": "C:\\REVIEW_MEMORY\\ORDEM\\cache\\E2_PRIVATE\\BLIND_SEED_V1.bin"
    },
    {
      "name": "C2 fixed path refuses ../escape",
      "passed": true,
      "outcome": "REJECT",
      "error": "Critical path differs from fixed contract"
    },
    {
      "name": "C2 fixed path refuses C:/outside",
      "passed": true,
      "outcome": "REJECT",
      "error": "Critical path differs from fixed contract"
    },
    {
      "name": "C2 fixed path refuses TUNEL/DO_CHATGPT/note.md",
      "passed": true,
      "outcome": "REJECT",
      "error": "Critical path differs from fixed contract"
    },
    {
      "name": "C2 reparse refused",
      "passed": true,
      "outcome": "REJECT",
      "error": "Redirected path refused: <__main__.FakeRedirect object at 0x000002252E368590>"
    },
    {
      "name": "C2 seed order None",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": {
        "log": [
          "Prepare",
          "Verify",
          "descriptor",
          "dummy_bytes",
          "write_dummy",
          "flush",
          "VerifySeed",
          "link",
          "unlink"
        ],
        "failure": null,
        "no_os_calls": true
      }
    },
    {
      "name": "C2 seed order Prepare",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": {
        "log": [
          "Prepare"
        ],
        "failure": "MOCK_ACL_FAILURE",
        "no_os_calls": true
      }
    },
    {
      "name": "C2 seed order Verify",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": {
        "log": [
          "Prepare",
          "Verify"
        ],
        "failure": "MOCK_ACL_FAILURE",
        "no_os_calls": true
      }
    },
    {
      "name": "C2 seed order VerifySeed",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": {
        "log": [
          "Prepare",
          "Verify",
          "descriptor",
          "dummy_bytes",
          "write_dummy",
          "flush",
          "VerifySeed"
        ],
        "failure": "MOCK_ACL_FAILURE",
        "no_os_calls": true
      }
    },
    {
      "name": "C2 seed order size",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": {
        "log": [
          "Prepare",
          "Verify",
          "descriptor",
          "dummy_bytes",
          "write_dummy",
          "flush"
        ],
        "failure": "Incomplete private seed retained",
        "no_os_calls": true
      }
    },
    {
      "name": "C4 same bytes snapshot",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": "99a1c79ade06b931b42d4e8d8db265a046c9a17117fbd2babf60cdc7dfafb017"
    },
    {
      "name": "C4 changed during capture",
      "passed": true,
      "outcome": "REJECT",
      "error": "Input changed during snapshot: C:\\REVIEW_MEMORY\\snapshot.txt"
    },
    {
      "name": "C4 changed before activation",
      "passed": true,
      "outcome": "REJECT",
      "error": "Captured input changed: C:\\REVIEW_MEMORY\\snapshot.txt"
    },
    {
      "name": "C3 final activation valid",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": true
    },
    {
      "name": "C3 no receipt",
      "passed": true,
      "outcome": "REJECT",
      "error": "MOCK_MISSING"
    },
    {
      "name": "C3 receipt wrong status",
      "passed": true,
      "outcome": "REJECT",
      "error": "Activation incomplete or registration/witness differs"
    },
    {
      "name": "C3 receipt wrong registration_sha256",
      "passed": true,
      "outcome": "REJECT",
      "error": "Activation incomplete or registration/witness differs"
    },
    {
      "name": "C3 receipt wrong witness_sha256",
      "passed": true,
      "outcome": "REJECT",
      "error": "Activation incomplete or registration/witness differs"
    },
    {
      "name": "C3 receipt wrong sealer_sha256",
      "passed": true,
      "outcome": "REJECT",
      "error": "Activation receipt pins differ"
    },
    {
      "name": "C3 future receipt",
      "passed": true,
      "outcome": "REJECT",
      "error": "Activation chronology invalid"
    },
    {
      "name": "C3 application other candidate",
      "passed": true,
      "outcome": "REJECT",
      "error": "Reviewed GO application differs from registered candidate"
    },
    {
      "name": "C3 application postdates registration",
      "passed": true,
      "outcome": "REJECT",
      "error": "Review application postdates registration"
    },
    {
      "name": "C3 role missing",
      "passed": true,
      "outcome": "REJECT",
      "error": "Four required review roles"
    },
    {
      "name": "C3 findings open",
      "passed": true,
      "outcome": "REJECT",
      "error": "Review blockers not closed: MAIN"
    }
  ],
  "passed": 39,
  "total": 39,
  "no_production_main_called": true,
  "no_real_seed_generation": true,
  "no_os_mutation_or_HDF_or_PE": true,
  "script_helpers_only": "AST-selected functions, fake byte store, no PowerShell execution"
}
```

### Aplicação sobre o contrato do candidato 001

```json
{
  "candidate_sha256": "d4d91d925e449441bc726d7313f247fca11a72726b3473c65bf901f4328e0161",
  "source_count": 16,
  "tests": [
    {
      "name": "C1 valid exact 16-source application",
      "passed": true,
      "outcome": "ACCEPT",
      "detail": 4
    },
    {
      "name": "candidate001 stale expected candidate",
      "passed": true,
      "outcome": "REJECT",
      "error": "GO/review applies to other bytes"
    },
    {
      "name": "candidate001 incomplete source coverage",
      "passed": true,
      "outcome": "REJECT",
      "error": "Incomplete current-source review coverage"
    },
    {
      "name": "candidate001 old guard coverage",
      "passed": true,
      "outcome": "REJECT",
      "error": "Review coverage does not match source bis/e2_code/registration_guard.py"
    },
    {
      "name": "candidate001 old E7 coverage",
      "passed": true,
      "outcome": "REJECT",
      "error": "Review coverage does not match source bis/e7_prepare/producer/tgl_ringdown_ampliacao.py"
    }
  ],
  "passed": 5,
  "total": 5,
  "main_not_called": true,
  "dummy_reviews_only": true
}
```

### Script dos 39 controles em memória

```python
from pathlib import Path
from datetime import datetime,timezone
from unittest.mock import patch
import ast,copy,hashlib,json,types,os,stat,re
B=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
paths={"sealer":B/"refeito/seal_e2_013bis.py","guard":B/"bis/e2_code/registration_guard.py","assembler":B/"refeito/assemble_e2_review_candidate_013bis.py","acl":B/"refeito/e2_private_directory.ps1","writer":B/"refeito/write_e2_review_application_013bis.py"}
raws={k:p.read_bytes() for k,p in paths.items()}
pins={k:hashlib.sha256(v).hexdigest() for k,v in raws.items()}
assert pins["sealer"]=="ce99da4a9e16405c5f469d8a7cfa956ffcdf044d4fbce99d731e3a226e90cdc6"
def select(raw,names,env):
 t=ast.parse(raw);nodes=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in names]
 exec(compile(ast.Module(body=nodes,type_ignores=[]),"review_selected_functions","exec"),env)
fakeB=Path("C:/REVIEW_MEMORY/ORDEM");fakeR=fakeB.parent
def hp(data):return hashlib.sha256(data).hexdigest()
mem={};env={"Path":Path,"datetime":datetime,"timezone":timezone,"hashlib":hashlib,"stat":stat,"B":fakeB,"R":fakeR,"SNAPSHOTS":{}}
select(raws["sealer"],{"snapshot","stable","fixed_path","unredirected","check_review_application","create_seed"},env)
unredirected=env["unredirected"]
env["unredirected"]=lambda p:Path(p).resolve()
def snap(p):raw=mem[Path(p).resolve()];return raw,hp(raw)
env["snapshot"]=snap
cp,sp=hp(b"candidate"),hp(b"sealer")
required={"bis/e2_code/code"+str(i)+".py":hp(("code"+str(i)).encode()) for i in range(14)}
required.update({"bis/e7_prepare/producer/"+n:hp(n.encode()) for n in ("consumer.py","extractor.py")})
reg={"own_code_tree_sha256":{k.split("/")[-1]:v for k,v in required.items() if "/e2_code/" in k},"e7":{"producer_tree_sha256":{k.split("/")[-1]:v for k,v in required.items() if "/producer/" in k}}}
app={"status":"APPLY_EXISTING_GO_TO_REVIEWED_CANDIDATE","candidate_sha256":cp,"sealer_sha256":sp,"created_utc":"2026-01-01T00:00:00+00:00","reviews":{},"exposure_declaration":{"statute":"DECLARADO_PRINCIPAL_WITH_SCOPED_CENSUS"}}
for role in ("PE","MAIN","E7","ACTIVATION"):
 n="bis/review_"+role+".md";raw=("\n".join(required.values())).encode();mem[(fakeB/n).resolve()]=raw
 app["reviews"][role]={"status":"BLOCKERS_CLOSED","blocking_findings":[],"reviewer_agent_id":"reviewer","builder_identity":"builder","files":{n:hp(raw)},"covered_source_sha256":required.copy() if role=="MAIN" else {}}
go="TUNEL/PARA_CHATGPT/go.md";mem[(fakeR/go).resolve()]=b"existing GO dummy"
app["existing_go"]={"relative_to_Chatgpt":go,"sha256":hp(b"existing GO dummy")}
tests=[]
def record(name,fn,expect_reject=False):
 try:
  detail=fn();tests.append({"name":name,"passed":not expect_reject,"outcome":"ACCEPT","detail":detail})
 except (ValueError,KeyError,TypeError,FileNotFoundError,RuntimeError,OSError) as e:
  tests.append({"name":name,"passed":expect_reject,"outcome":"REJECT","error":str(e)})
def review(mut=lambda a:None):
 a=copy.deepcopy(app);mut(a);return len(env["check_review_application"](a,reg,cp,sp))
record("C1 valid exact 16-source application",review)
mutations=[
 ("missing_role",lambda a:a["reviews"].pop("ACTIVATION")),
 ("extra_role",lambda a:a["reviews"].update(EXTRA=copy.deepcopy(a["reviews"]["PE"]))),
 ("open_status",lambda a:a["reviews"]["E7"].update(status="OPEN")),
 ("blocking_findings",lambda a:a["reviews"]["PE"].update(blocking_findings=["F0"])),
 ("same_builder",lambda a:a["reviews"]["MAIN"].update(reviewer_agent_id="builder")),
 ("candidate",lambda a:a.update(candidate_sha256="0"*64)),
 ("sealer",lambda a:a.update(sealer_sha256="0"*64)),
 ("missing_coverage",lambda a:a["reviews"]["MAIN"]["covered_source_sha256"].pop(next(iter(required)))),
 ("bad_coverage",lambda a:a["reviews"]["MAIN"]["covered_source_sha256"].update({next(iter(required)):"0"*64})),
 ("bad_review_pin",lambda a:a["reviews"]["PE"]["files"].update({"bis/review_PE.md":"0"*64})),
 ("GO_pin",lambda a:a["existing_go"].update(sha256="0"*64)),
 ("GO_outside",lambda a:a["existing_go"].update(relative_to_Chatgpt="outside.md")),
 ("absolute_exposure",lambda a:a["exposure_declaration"].update(statute="REAL_NO_EXPOSURE")),
 ("future_application",lambda a:a.update(created_utc="2999-01-01T00:00:00+00:00"))]
for n,mut in mutations:record("C1 "+n,lambda mut=mut:review(mut),True)
expected="ORDEM/cache/E2_PRIVATE/BLIND_SEED_V1.bin"
record("C2 fixed path valid",lambda:str(env["fixed_path"](expected,expected)))
for value in ("../escape","C:/outside","TUNEL/DO_CHATGPT/note.md"):
 record("C2 fixed path refuses "+value,lambda v=value:env["fixed_path"](v,expected),True)
class FakeRedirect:
 def absolute(self):return self
 @property
 def parents(self):return ()
 def exists(self):return True
 def lstat(self):return types.SimpleNamespace(st_file_attributes=1024)
 def is_symlink(self):return False
 def resolve(self):raise AssertionError("reparse must reject first")
env["Path"]=lambda p:p
record("C2 reparse refused",lambda:unredirected(FakeRedirect()),True)
env["Path"]=Path
# No OS calls: full seed orchestration against a sink and dummy fixed bytes.
def seed_case(fail=None):
 log=[]
 class Node:
  name="DUMMY.bin"
  def with_name(self,n):return self
  def stat(self):return types.SimpleNamespace(st_size=31 if fail=="size" else 32)
  def unlink(self):log.append("unlink")
 class Sink:
  def __enter__(self):return self
  def __exit__(self,*a):return False
  def write(self,raw):assert raw==b"X"*32;log.append("write_dummy")
  def flush(self):log.append("flush")
  def fileno(self):return 987
 def acl(action):
  log.append(action)
  if fail==action:raise ValueError("MOCK_ACL_FAILURE")
  return {"status":"MOCK_ONLY"}
 def opening(*a):
  log.append("descriptor")
  assert a[1]&8 and log[:2]==["Prepare","Verify"]
  return 987
 def dummy(n):assert n==32;log.append("dummy_bytes");return b"X"*32
 fakeos=types.SimpleNamespace(O_WRONLY=1,O_CREAT=2,O_EXCL=4,O_BINARY=8,open=opening,fdopen=lambda *a:Sink(),urandom=dummy,fsync=lambda *a:None,link=lambda *a:log.append("link"))
 env.update(os=fakeos,private_directory=acl)
 error=None
 try:env["create_seed"](Node())
 except (ValueError,OSError) as e:error=str(e)
 if fail in ("Prepare","Verify"):assert "descriptor" not in log
 if fail is not None:assert "link" not in log and error
 else:assert log.index("VerifySeed")<log.index("link")
 return {"log":log,"failure":error,"no_os_calls":True}
for fail in (None,"Prepare","Verify","VerifySeed","size"):
 record("C2 seed order "+str(fail),lambda f=fail:seed_case(f))
# Restore snapshot implementation; fake read_bytes and sha only.
select(raws["sealer"],{"snapshot","stable"},env)
key=Path("C:/REVIEW_MEMORY/snapshot.txt").resolve();mem[key]=b"version-A"
env["sha"]=lambda p:hp(mem[Path(p).resolve()])
with patch.object(Path,"read_bytes",lambda p:mem[p.resolve()]):
 record("C4 same bytes snapshot",lambda:env["snapshot"](key)[1])
 mem[key]=b"version-B"
 record("C4 changed during capture",lambda:env["snapshot"](key),True)
 record("C4 changed before activation",env["stable"],True)
# C3 latest guard against fake bytes/paths only.
g={"Path":Path,"ROOT":fakeR,"BASE":fakeB,"datetime":datetime,"timezone":timezone,"json":json,"re":re}
select(raws["guard"],{"check_activation","strict_json","utc","contained"},g)
g["sha"]=lambda p:hp(mem[Path(p).resolve()])
act={"receipt_relative_to_Chatgpt":"ORDEM_013_RINGDOWN/bis/E2_REGISTRATION_RECEIPT.json","review_application_relative_to_Chatgpt":"ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V1.json","sealer_relative_to_Chatgpt":"ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py"}
note=(fakeR/"TUNEL/DO_CHATGPT/note.md").resolve();mem[note]=b"dummy witness"
ap=(fakeR/act["review_application_relative_to_Chatgpt"]).resolve();ss=(fakeR/act["sealer_relative_to_Chatgpt"]).resolve();rp=(fakeR/act["receipt_relative_to_Chatgpt"]).resolve()
mem[ss]=b"sealer"
aa=copy.deepcopy(app);aa["sealer_sha256"]=hp(mem[ss]);mem[ap]=json.dumps(aa).encode()
act.update(review_application_sha256=hp(mem[ap]),sealer_sha256=hp(mem[ss]))
gg={"activation":act,"registered_utc":"2026-01-02T00:00:00+00:00","registration_provenance":{"candidate_sha256":cp}}
rr={"status":"E2_ACTIVATION_COMPLETE","registration_sha256":"d"*64,"witness_sha256":hp(mem[note]),"review_application_sha256":act["review_application_sha256"],"sealer_sha256":act["sealer_sha256"],"finished_utc":"2026-01-03T00:00:00+00:00"}
def activation(mut=None,missing=False,appmut=None):
 r=copy.deepcopy(rr);a=copy.deepcopy(aa);reg2=copy.deepcopy(gg)
 if mut:mut(r)
 if appmut:appmut(a)
 mem[ap]=json.dumps(a).encode();reg2["activation"]["review_application_sha256"]=hp(mem[ap]);r["review_application_sha256"]=hp(mem[ap])
 if missing:mem.pop(rp,None)
 else:mem[rp]=json.dumps(r).encode()
 def reader(p):
  if p.resolve() not in mem:raise FileNotFoundError("MOCK_MISSING")
  return mem[p.resolve()]
 with patch.object(Path,"read_bytes",reader):return g["check_activation"](reg2,"d"*64,note)
record("C3 final activation valid",activation)
record("C3 no receipt",lambda:activation(missing=True),True)
for field in ("status","registration_sha256","witness_sha256","sealer_sha256"):
 record("C3 receipt wrong "+field,lambda f=field:activation(lambda r:r.update({f:"WRONG"})),True)
record("C3 future receipt",lambda:activation(lambda r:r.update(finished_utc="2999-01-01T00:00:00+00:00")),True)
record("C3 application other candidate",lambda:activation(appmut=lambda a:a.update(candidate_sha256="0"*64)),True)
record("C3 application postdates registration",lambda:activation(appmut=lambda a:a.update(created_utc="2026-01-04T00:00:00+00:00")),True)
record("C3 role missing",lambda:activation(appmut=lambda a:a["reviews"].pop("ACTIVATION")),True)
record("C3 findings open",lambda:activation(appmut=lambda a:a["reviews"]["MAIN"].update(blocking_findings=["OPEN"])),True)
out={"captured_pins":pins,"results":tests,"passed":sum(t["passed"] for t in tests),"total":len(tests),"no_production_main_called":True,"no_real_seed_generation":True,"no_os_mutation_or_HDF_or_PE":True,"script_helpers_only":"AST-selected functions, fake byte store, no PowerShell execution"}
print(json.dumps(out))

```

