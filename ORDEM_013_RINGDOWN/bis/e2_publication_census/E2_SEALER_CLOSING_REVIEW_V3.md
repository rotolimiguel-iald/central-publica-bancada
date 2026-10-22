# E2 — fechamento independente v3, helper nativo Win32

[REAL] **Papel ACTIVATION: BLOCKERS_CLOSED. blocking_findings: [].** Helper nativo, integração V2 e candidato003 conferidos nos bytes abaixo. O GO existente rege a execução pelo principal após revisão; nenhuma nova confirmação humana é exigida. Este parecer não relata selagem/seed/campanha real executada pelo revisor.

[REAL] Candidato `bis/E2_REVIEW_CANDIDATE_003.json`, SHA256 **172811a2fe94f8db540459d782e24517df9b672b21b6b6a3b6dd8759ee4234e5**, 183159 bytes. Conferência 2026-09-22T21:42:18.776951+00:00: 14/14 pins own_code conferem; 68 entradas extras declaradas, sem repetir sua revisão científica; guarda e helper nativo têm pins iguais aos arquivos examinados. Nada foi alterado em produtores, registro, aplicação V1, seed ou política de execução.

## O que foi executado, com limite explícito

[REAL] **23/23 controles passaram:** 4 de ACL real em fixture, 14 de ACL/descritores/reparse e 5 de integração simulada. Conferências independentes adicionais: SID obtido pelo helper igual ao token do processo; volume NTFS com suporte a ACL persistente.

[REAL] Fixture exclusiva:
`C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\NATIVE_ACL_FIXTURE_20260922T213829`.

O helper foi carregado somente após conferir seu hash, com nome de módulo diferente de __main__; **B foi redefinido em memória para essa fixture** antes de operar. Criaram-se diretórios de teste e um arquivo de **34 bytes constantes fictícios**, identificado como teste. O nome BLIND_SEED_V1.bin.pending aparece exclusivamente dentro da fixture porque é o contrato de VerifySeed; seu conteúdo não é seed, não vem de RNG e não foi lido. Nenhum caminho privado E2 real foi acessado, sondado ou criado pelo revisor.

[REAL] A fixture foi mantida para auditoria, inclusive junction com destino inteiramente dentro dela. Não houve deleção recursiva, alteração de ExecutionPolicy, redução de proteções de pastas reais, leitura de HDF/posterior/strain, PE, waveform, MC ou repetição científica. O selador/assembler/writer/checked_registration de produção não foram executados.

## ACL, SID e descritores

[REAL] CreateDirectoryW recebe SECURITY_ATTRIBUTES com descritor DACL protegido e ACE de FullControl exclusiva para o SID atual, com OI/CI e bInheritHandle=False. A restrição é fornecida **na criação do diretório**, antes do descritor do arquivo fictício. Prepare, Verify e VerifySeed passaram em NTFS; segunda criação do diretório existente foi recusada. O arquivo fictício foi aberto em modo binário exclusivo e herdou a ACL esperada.

[REAL] A declaração SID por whoami.exe do System32 foi cruzada independentemente com OpenProcessToken/GetTokenInformation(TokenUser)/ConvertSidToStringSidW. Houve igualdade. O handle de token da checagem independente foi fechado e a string SID liberada. Só um digest de SID entra na evidência, não a identidade textual do usuário.

[REAL] Negativos recusados: ACE adicional, SID errado, DACL sem proteção, falta de herança, ACE herdada indevida no diretório, direitos insuficientes, DACL nula, ACE de negação em vez do contrato de Allow e flags inválidas no arquivo. Verificação do descritor real contra SID deliberadamente errado também recusou.

[REAL] Foi criada uma junction NTFS **apenas na fixture**, apontando para outro diretório da mesma fixture. A inspeção dos pais recusou esse reparse point antes de prosseguir. Atributos inexistentes/redirecionados são falhas visíveis no código. Não testei nem afirmei proteção contra um adversário privilegiado capaz de trocar objetos concorrentemente.

[REAL] Instrumentação das chamadas Win32 nos caminhos de criação/verificação e falhas: **7 alocações de buffers nativos rastreadas, 7 LocalFree bem-sucedidos, zero saldo pendente**. Foram incluídas falha simulada de CreateDirectoryW, falha de conversão para SDDL e rejeição após conversão. Isto evidencia liberação dos buffers nesses caminhos, não uma prova universal de ausência de leaks. O helper não abre handle de token; ele consulta whoami por subprocess.run. A checagem independente que abriu token o fechou explicitamente.

[INPUT — alcance de segurança] DACL exclusiva significa proteção procedural no mesmo usuário/host. Processos do mesmo usuário, WSL com esse acesso e acesso privilegiado do SO continuam fora da promessa de separação. Não é custódia humana independente, segredo inacessível ao administrador ou cegueira absoluta. O retorno do helper declara esse limite.

## Integração revista

[REAL] Diff contra bis/e2_sealer_snapshot_failed_policy confirma a substituição de PowerShell -File por **sys.executable -B e2_private_directory_native.py --action**, atualização dos pins/cobertura para o helper Python, aplicação V2 e nota de preservação da tentativa anterior. O writer referencia este parecer V3. O assembler fixa o helper nos inputs; selador e writer exigem pin/cobertura correspondente antes da operação; snapshot/stable permanecem ativos.

[REAL] Mocks focados verificaram argumentos do subprocess e opções check/timeout/captura; status inesperado do helper e erro de processo recusam. Nenhum processo do helper de produção foi iniciado por esse teste de integração: as chamadas reais ao helper ocorreram somente com B da fixture. Não há fallback para uma guarda mais fraca ou mudança de ExecutionPolicy.

[REAL] Guarda atual `3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7`: comparação de bytes confirmou que o delta sobre d957… é exclusivamente o caminho da aplicação V1→V2. O mock recusa V1 e admite V2; C1/C3/R1/R2 anteriores permanecem com seu fechamento no alcance já revisado. Não repeti os 39 controles gerais nem a matemática.

[REAL] Li ACTIVATION_APP_V2_PATH_RECEIPT.json, cujo pin está abaixo. [DECLARADO] Seus 40 controles pertencem ao autor; não são os meus 23. Meu teste independente da mudança de caminho está na evidência.

## Tentativa anterior preservada

[DECLARADO — recibo do principal] E2_SEAL_ATTEMPT_001_FAILED_SCRIPT_EXECUTION_POLICY.json registra falha em PowerShell -File antes de pasta privada/seed/registro, sem ciência ou mudança de política. Li o recibo e conferi seu hash; não repeti sondagens de paths privados E2 para reconstituir a tentativa. A aplicação V1 e o candidato002 permanecem como história segundo a custódia informada; este revisor não os alterou.

[REAL] A nota gerada pelo selador agora menciona a tentativa e a transição para API nativa. O cabeçalho de exposição segue remetendo à declaração vinculada; não transforma ausência de leitura em fato absoluto.

## Cobertura para a aplicação técnica do GO

```json
{
  "role": "ACTIVATION",
  "status": "BLOCKERS_CLOSED",
  "blocking_findings": [],
  "candidate_sha256": "172811a2fe94f8db540459d782e24517df9b672b21b6b6a3b6dd8759ee4234e5",
  "covered_source_sha256": {
    "bis/e2_code/registration_guard.py": "3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7"
  },
  "covered_security_input_sha256": {
    "ORDEM_013_RINGDOWN/refeito/e2_private_directory_native.py": "5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
  },
  "reviewed_sealer_sha256": "ca121c6863007f1940611cd2af4ab294d424375037935946c587717b73cc5f85",
  "scope": "Native ACL helper fixture; current SID, descriptors, reparse refusal and V2 application path; previous scientific/review closure retained"
}
```

## Pins finais medidos

| Artefato | SHA256 |
|---|---|
| `bis/E2_REVIEW_CANDIDATE_003.json` | `172811a2fe94f8db540459d782e24517df9b672b21b6b6a3b6dd8759ee4234e5` |
| `refeito/e2_private_directory_native.py` | `5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0` |
| `refeito/seal_e2_013bis.py` | `ca121c6863007f1940611cd2af4ab294d424375037935946c587717b73cc5f85` |
| `refeito/assemble_e2_review_candidate_013bis.py` | `770a5c5f362a360a52b35c8c9f1615d8be3b11ea1283e7edd1ea6f94cc71fbc5` |
| `refeito/write_e2_review_application_013bis.py` | `3a48cfd55cbad98f3c6621cbf8e612636cedee718c3d81607811d2d7d1a964cc` |
| `bis/e2_code/registration_guard.py` | `3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7` |
| `bis/e2_review/ACTIVATION_APP_V2_PATH_RECEIPT.json` | `c44da66dc2d57a7f9357b77a312bb3c3334ef2421c9e58b0ea076172947aeb55` |
| `bis/E2_SEAL_ATTEMPT_001_FAILED_SCRIPT_EXECUTION_POLICY.json` | `ad8d73bb0244588c97594587e6f652d4a4d2715e034dbbc524688d5023ca3a33` |

[REAL] Rastreabilidade científico-matemática E7 v4 permanece no parecer E7_INDEPENDENT_REVIEW_V4.md. [OPEN] PE, calibração, seleção, normalização, convergência e significado físico não são pagos por uma fixture ACL. NOT_FALSIFIED nunca CONFIRMED. Os pins delimitam este fechamento; bytes futuros exigem conferência correspondente.

## Resultados independentes

```json
{
  "initial_real_ACL_fixture": {
    "helper_sha256": "5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0",
    "fixture": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\NATIVE_ACL_FIXTURE_20260922T213829",
    "dummy_path": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\NATIVE_ACL_FIXTURE_20260922T213829\\cache\\E2_PRIVATE\\BLIND_SEED_V1.bin.pending",
    "dummy_bytes": 34,
    "tests": [
      {
        "name": "prepare_restrictive_directory",
        "passed": true,
        "result": "CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED"
      },
      {
        "name": "verify_directory_before_dummy_descriptor",
        "passed": true,
        "result": "CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED"
      },
      {
        "name": "verify_dummy_inherited_DACL",
        "passed": true,
        "result": "CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED"
      },
      {
        "name": "retry_prepare_refused",
        "passed": true,
        "error": "FileExistsError: Private directory exists; explicit audit required"
      }
    ],
    "passed": 4,
    "total": 4,
    "real_E2_path_touched": false,
    "helper_B_rebound_only_in_memory": true
  },
  "negative_ACL_descriptor_reparse": {
    "fixture": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\NATIVE_ACL_FIXTURE_20260922T213829",
    "helper_sha256": "5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0",
    "current_sid_sha256": "fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88",
    "tests": [
      {
        "name": "SDDL extra_allow",
        "passed": true,
        "error": "ValueError: DACL must have one explicit identity"
      },
      {
        "name": "SDDL wrong_SID",
        "passed": true,
        "error": "ValueError: DACL is not current-user FullControl only"
      },
      {
        "name": "SDDL unprotected",
        "passed": true,
        "error": "ValueError: Directory must be protected and inheritable"
      },
      {
        "name": "SDDL missing_inheritance",
        "passed": true,
        "error": "ValueError: Directory must be protected and inheritable"
      },
      {
        "name": "SDDL inherited_directory_ACE",
        "passed": true,
        "error": "ValueError: Directory must be protected and inheritable"
      },
      {
        "name": "SDDL read_only_rights",
        "passed": true,
        "error": "ValueError: DACL is not current-user FullControl only"
      },
      {
        "name": "SDDL null_DACL",
        "passed": true,
        "error": "ValueError: DACL must have one explicit identity"
      },
      {
        "name": "SDDL deny_only",
        "passed": true,
        "error": "ValueError: DACL is not current-user FullControl only"
      },
      {
        "name": "SDDL invalid_file_ACE_flags",
        "passed": true,
        "error": "ValueError: Unexpected seed ACE flags"
      },
      {
        "name": "tracked actual CreateDirectory with protected descriptor",
        "passed": true,
        "detail": "CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED"
      },
      {
        "name": "wrong actual ACL current-SID expectation frees buffers",
        "passed": true,
        "error": "ValueError: DACL is not current-user FullControl only"
      },
      {
        "name": "conversion failure frees security descriptor",
        "passed": true,
        "error": "OSError: [WinError 87] Parâmetro incorreto."
      },
      {
        "name": "CreateDirectory failure frees descriptor",
        "passed": true,
        "error": "PermissionError: [WinError 5] Acesso negado."
      },
      {
        "name": "actual junction parent refused",
        "passed": true,
        "error": "ValueError: Missing or redirected parent"
      }
    ],
    "passed": 14,
    "total": 14,
    "native_allocations": 7,
    "successful_LocalFree": 7,
    "outstanding_allocations": 0,
    "junction_target_within_fixture": true,
    "seed_bytes_read": false,
    "real_E2_touched": false,
    "production_main_called": false
  },
  "integration_mocks": {
    "tests": [
      {
        "name": "native subprocess argv pinned interpreter -B",
        "passed": true
      },
      {
        "name": "wrong helper status refused",
        "passed": true,
        "error": "ValueError"
      },
      {
        "name": "helper process failure propagated",
        "passed": true,
        "error": "CalledProcessError"
      },
      {
        "name": "V1 application path refused",
        "passed": true,
        "error": "ValueError"
      },
      {
        "name": "V2 application path admitted",
        "passed": true
      }
    ],
    "passed": 5,
    "total": 5,
    "real_subprocess_launched": false,
    "real_activation_called": false
  },
  "independent_SID_and_filesystem": {
    "current_sid_matches_process_token": true,
    "token_handle_closed": true,
    "SID_string_LocalFree": true,
    "filesystem": "NTFS",
    "persistent_ACLs_supported": true,
    "real_E2_touched": false
  },
  "candidate003": {
    "utc": "2026-09-22T21:42:18.776951+00:00",
    "candidate_sha256": "172811a2fe94f8db540459d782e24517df9b672b21b6b6a3b6dd8759ee4234e5",
    "candidate_bytes": 183159,
    "helper_pin": "5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0",
    "guard_pin": "3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7",
    "own_pins_match": true,
    "own_count": 14,
    "extra_count": 68,
    "pins": {
      "refeito/e2_private_directory_native.py": "5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0",
      "refeito/seal_e2_013bis.py": "ca121c6863007f1940611cd2af4ab294d424375037935946c587717b73cc5f85",
      "refeito/assemble_e2_review_candidate_013bis.py": "770a5c5f362a360a52b35c8c9f1615d8be3b11ea1283e7edd1ea6f94cc71fbc5",
      "refeito/write_e2_review_application_013bis.py": "3a48cfd55cbad98f3c6621cbf8e612636cedee718c3d81607811d2d7d1a964cc",
      "bis/e2_code/registration_guard.py": "3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7",
      "bis/e2_review/ACTIVATION_APP_V2_PATH_RECEIPT.json": "c44da66dc2d57a7f9357b77a312bb3c3334ef2421c9e58b0ea076172947aeb55",
      "bis/E2_SEAL_ATTEMPT_001_FAILED_SCRIPT_EXECUTION_POLICY.json": "ad8d73bb0244588c97594587e6f652d4a4d2715e034dbbc524688d5023ca3a33"
    },
    "A_receipt": {
      "status": "PATH_V2_ONLY_GUARD_FROZEN_FOR_REVIEW",
      "created_utc": "2026-09-22T21:40:12.741672+00:00",
      "modified_source": "ORDEM_013_RINGDOWN/bis/e2_code/registration_guard.py",
      "old_sha256": "d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9",
      "new_sha256": "3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7",
      "fixed_application_path": "ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V2.json",
      "exact_single_byte_string_replacement": true,
      "finite_checks": 40,
      "prior_cases": 38,
      "focused_new_cases": 2,
      "test_receipt_sha256": "3fa6f34fa77e81d4058bc145c0bc4466330dd13ef4b2e29c817a044f0f930dca",
      "old_receipts_modified": false,
      "other_production_sources_modified": false,
      "execution_policy_modified_or_bypassed": false,
      "real_sealer_executed": false,
      "science_executed": false,
      "files_created_sha256": {
        "ORDEM_013_RINGDOWN/bis/e2_review/ACTIVATION_APP_V2_PATH_TESTS.json": "3fa6f34fa77e81d4058bc145c0bc4466330dd13ef4b2e29c817a044f0f930dca",
        "ORDEM_013_RINGDOWN/bis/e2_review/activation_app_v2_path_mock/R/ORDEM_013_RINGDOWN/bis/E2_REGISTRATION_RECEIPT.json": "4417f0b5a654ab468eeb33cb48d2b6b760703b975c6b850770f3575e85e91b31",
        "ORDEM_013_RINGDOWN/bis/e2_review/activation_app_v2_path_mock/R/ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_V2.json": "cef4969997b09da3e7f35cb44078de132f31c903590eb99c382c8a4a6b3aa8dc",
        "ORDEM_013_RINGDOWN/bis/e2_review/activation_app_v2_path_mock/R/ORDEM_013_RINGDOWN/bis/MOCK_REVIEW.txt": "bbd3d32ac2c0eae92113ca0eb7f026a1021a0dfd641db28996f7112f162d67be",
        "ORDEM_013_RINGDOWN/bis/e2_review/activation_app_v2_path_mock/R/ORDEM_013_RINGDOWN/bis/MOCK_WITNESS.txt": "3e8c5fef44045d341d3cdf9e95adc209837a897921162492556deb0bab9c56e2",
        "ORDEM_013_RINGDOWN/bis/e2_review/activation_app_v2_path_mock/R/ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py": "df144af1a2ca7d3472ce157dcb6f71a305fac3c214eec3e9103940b8e3bfba50",
        "ORDEM_013_RINGDOWN/bis/e2_review/activation_app_v2_path_snapshot/registration_guard.py": "d9577982731a69c2837d729a129cdc278c06da8a2bd854b0d526d1ceb971f4e9",
        "ORDEM_013_RINGDOWN/bis/e2_review/prepare_activation_app_v2_path_tests.py": "63f9f548d877237af862d8086f856520aca3c2383d8a26a20b70b0aaaa606685",
        "ORDEM_013_RINGDOWN/bis/e2_review/record_activation_app_v2_and_kerr_repin.py": "d7bff07d652e16fa103fcf416aabf85fb2824567644be979bdab0117c7d5d541",
        "ORDEM_013_RINGDOWN/bis/e2_review/test_activation_app_v2_path.py": "3a7221f420c1bafc89eeabdefc60940e13c91e74aca0ba2121973c05508152c7"
      },
      "receipt_itself": "ORDEM_013_RINGDOWN/bis/e2_review/ACTIVATION_APP_V2_PATH_RECEIPT.json"
    }
  }
}
```

## Harnesses executados

[REAL] Scripts por stdin/Python -B, preservados como evidência. A fixture é separada; não se deve trocar seu B pelo diretório real E2. Reprodução exige fixture nova para as etapas que recusam arquivos existentes.

### Fixture inicial

```python
from pathlib import Path
from datetime import datetime,timezone
import ctypes,hashlib,json,os,types
source=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\refeito\e2_private_directory_native.py")
raw=source.read_bytes();pin=hashlib.sha256(raw).hexdigest()
assert pin=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
root=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census")
fixture=root/("NATIVE_ACL_FIXTURE_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"))
fixture.mkdir();(fixture/"cache").mkdir()
m=types.ModuleType("independent_native_acl");m.__file__=str(source)
exec(compile(raw,str(source),"exec"),m.__dict__)
m.B=fixture
records=[]
def check(name,fn,reject=False):
 try:
  value=fn();records.append({"name":name,"passed":not reject,"result":value})
 except (ValueError,OSError,FileExistsError) as e:
  records.append({"name":name,"passed":reject,"error":type(e).__name__+": "+str(e)})
check("prepare_restrictive_directory",lambda:m.operate("Prepare")["status"])
check("verify_directory_before_dummy_descriptor",lambda:m.operate("Verify")["status"])
dummy=fixture/"cache/E2_PRIVATE/BLIND_SEED_V1.bin.pending"
fd=os.open(dummy,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_BINARY,0o600)
with os.fdopen(fd,"wb") as f:
 f.write(b"INDEPENDENT_DUMMY_BYTES_NOT_A_SEED");f.flush();os.fsync(f.fileno())
check("verify_dummy_inherited_DACL",lambda:m.operate("VerifySeed")["status"])
check("retry_prepare_refused",lambda:m.operate("Prepare"),True)
print(json.dumps({"helper_sha256":pin,"fixture":str(fixture),"dummy_path":str(dummy),"dummy_bytes":dummy.stat().st_size,"tests":records,"passed":sum(x["passed"] for x in records),"total":len(records),"real_E2_path_touched":False,"helper_B_rebound_only_in_memory":True}))

```

### ACL, descritores e reparse

```python
from pathlib import Path
import ctypes,hashlib,json,os,subprocess,types
source=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\refeito\e2_private_directory_native.py")
raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
m=types.ModuleType("independent_native_acl");m.__file__=str(source);exec(compile(raw,str(source),"exec"),m.__dict__)
fixture=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\NATIVE_ACL_FIXTURE_20260922T213829");m.B=fixture
sid=m.current_sid();records=[]
def check(name,fn,reject=False):
 try:
  d=fn();records.append({"name":name,"passed":not reject,"detail":d})
 except (ValueError,OSError,FileExistsError) as e:
  records.append({"name":name,"passed":reject,"error":type(e).__name__+": "+str(e)})
for name,text,directory in [
 ("extra_allow","D:P(A;OICI;FA;;;"+sid+")(A;OICI;FR;;;WD)",True),
 ("wrong_SID","D:P(A;OICI;FA;;;S-1-1-0)",True),
 ("unprotected","D:(A;OICI;FA;;;"+sid+")",True),
 ("missing_inheritance","D:P(A;;FA;;;"+sid+")",True),
 ("inherited_directory_ACE","D:P(A;OICIID;FA;;;"+sid+")",True),
 ("read_only_rights","D:P(A;OICI;FR;;;"+sid+")",True),
 ("null_DACL","D:NO_ACCESS_CONTROL",True),
 ("deny_only","D:P(D;OICI;FA;;;"+sid+")",True),
 ("invalid_file_ACE_flags","D:(A;OICI;FA;;;"+sid+")",False)]:
 check("SDDL "+name,lambda t=text,d=directory:m.check_sddl(t,sid,d),True)
# Trace all successful LocalAlloc-returning APIs through the actual Win32 calls.
adv,kernel=m.native();active=set();allocations=0;frees=0;fail_convert=False;fail_create=False
def address(out):return ctypes.cast(out,ctypes.POINTER(ctypes.c_void_p))[0]
def add(out):
 global allocations
 ptr=address(out);assert ptr and ptr not in active;active.add(ptr);allocations+=1
class Adv:
 def ConvertStringSecurityDescriptorToSecurityDescriptorW(self,*a):
  ok=adv.ConvertStringSecurityDescriptorToSecurityDescriptorW(*a)
  if ok:add(a[2])
  return ok
 def GetNamedSecurityInfoW(self,*a):
  err=adv.GetNamedSecurityInfoW(*a)
  if not err:add(a[7])
  return err
 def ConvertSecurityDescriptorToStringSecurityDescriptorW(self,*a):
  if fail_convert:ctypes.set_last_error(87);return False
  ok=adv.ConvertSecurityDescriptorToStringSecurityDescriptorW(*a)
  if ok:add(a[3])
  return ok
class Kernel:
 def __getattr__(self,n):return getattr(kernel,n)
 def CreateDirectoryW(self,*a):
  if fail_create:ctypes.set_last_error(5);return False
  return kernel.CreateDirectoryW(*a)
 def LocalFree(self,p):
  global frees
  ptr=p.value if isinstance(p,ctypes.c_void_p) else p
  assert ptr in active
  result=kernel.LocalFree(p);assert not result
  active.remove(ptr);frees+=1
ta,tk=Adv(),Kernel();m.native=lambda:(ta,tk)
tracked=fixture/"allocation_case";tracked.mkdir();(tracked/"cache").mkdir();m.B=tracked
check("tracked actual CreateDirectory with protected descriptor",lambda:m.operate("Prepare")["status"])
check("wrong actual ACL current-SID expectation frees buffers",lambda:m.verify_acl(tracked/"cache/E2_PRIVATE","S-1-1-0",True,ta,tk),True)
fail_convert=True
check("conversion failure frees security descriptor",lambda:m.operate("Verify"),True)
fail_convert=False
failure=fixture/"creation_failure_case";failure.mkdir();(failure/"cache").mkdir();m.B=failure;fail_create=True
check("CreateDirectory failure frees descriptor",lambda:m.operate("Prepare"),True)
fail_create=False
assert not active and allocations==frees
# Actual NTFS junction wholly inside fixture, no deletion or external target.
target=fixture/"reparse_target";target.mkdir();(target/"cache").mkdir()
alias=fixture/"junction_alias"
r=subprocess.run([str(Path(os.environ["SystemRoot"])/"System32/cmd.exe"),"/d","/c","mklink","/J",str(alias),str(target)],capture_output=True)
assert r.returncode==0,"Fixture junction creation failed: "+str(r.returncode)
m.B=alias
check("actual junction parent refused",lambda:m.operate("Verify"),True)
print(json.dumps({"fixture":str(fixture),"helper_sha256":hashlib.sha256(raw).hexdigest(),"current_sid_sha256":hashlib.sha256(sid.encode()).hexdigest(),"tests":records,"passed":sum(t["passed"] for t in records),"total":len(records),"native_allocations":allocations,"successful_LocalFree":frees,"outstanding_allocations":len(active),"junction_target_within_fixture":True,"seed_bytes_read":False,"real_E2_touched":False,"production_main_called":False}))

```

### Integração simulada

```python
from pathlib import Path
import ast,hashlib,json,types,subprocess
b=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
raw=(b/"refeito/seal_e2_013bis.py").read_bytes();assert hashlib.sha256(raw).hexdigest()=="ca121c6863007f1940611cd2af4ab294d424375037935946c587717b73cc5f85"
tree=ast.parse(raw);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="private_directory")
calls=[]
def runner(command,**kw):
 calls.append((command,kw))
 assert command==["FIXTURE_PYTHON","-B",str(b/"refeito/e2_private_directory_native.py"),"--action","Prepare"]
 assert kw==dict(capture_output=True,text=True,check=True,timeout=30)
 return types.SimpleNamespace(stdout=json.dumps({"status":"CURRENT_WINDOWS_USER_ONLY_DACL_VERIFIED"}))
env={"B":b,"os":types.SimpleNamespace(name="nt"),"sys":types.SimpleNamespace(executable="FIXTURE_PYTHON"),"subprocess":types.SimpleNamespace(run=runner),"json":json}
exec(compile(ast.Module(body=[fn],type_ignores=[]),"wrapper_AST_only","exec"),env)
results=[]
def case(name,fn,reject=False):
 try:fn();results.append({"name":name,"passed":not reject})
 except (ValueError,subprocess.CalledProcessError) as e:results.append({"name":name,"passed":reject,"error":type(e).__name__})
case("native subprocess argv pinned interpreter -B",lambda:env["private_directory"]("Prepare"))
env["subprocess"].run=lambda *a,**k:types.SimpleNamespace(stdout='{"status":"WRONG"}')
case("wrong helper status refused",lambda:env["private_directory"]("Prepare"),True)
def fail(*a,**k):raise subprocess.CalledProcessError(1,["MOCK"])
env["subprocess"].run=fail
case("helper process failure propagated",lambda:env["private_directory"]("Prepare"),True)
guard=(b/"bis/e2_code/registration_guard.py").read_bytes();assert hashlib.sha256(guard).hexdigest()=="3cb2d9ef0672ccdf9bbca8547102b9a1323ea9d51bbc780732bb78bad99b40d7"
gf=next(n for n in ast.parse(guard).body if isinstance(n,ast.FunctionDef) and n.name=="check_activation")
prefix=gf.body[1:4]
assert isinstance(prefix[-1],ast.If)
def route(version):
 e={"reg":{"activation":{"receipt_relative_to_Chatgpt":"ORDEM_013_RINGDOWN/bis/E2_REGISTRATION_RECEIPT.json","review_application_relative_to_Chatgpt":"ORDEM_013_RINGDOWN/bis/E2_REVIEW_APPLICATION_"+version+".json","sealer_relative_to_Chatgpt":"ORDEM_013_RINGDOWN/refeito/seal_e2_013bis.py"}}}
 exec(compile(ast.Module(body=prefix,type_ignores=[]),"activation_path_AST_only","exec"),e)
case("V1 application path refused",lambda:route("V1"),True)
case("V2 application path admitted",lambda:route("V2"))
print(json.dumps({"tests":results,"passed":sum(x["passed"] for x in results),"total":len(results),"real_subprocess_launched":False,"real_activation_called":False}))

```

### SID e volume independentes

```python
from pathlib import Path
import ctypes,ctypes.wintypes as w,hashlib,json,types
source=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\refeito\e2_private_directory_native.py")
raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
m=types.ModuleType("independent_sid");m.__file__=str(source);exec(compile(raw,str(source),"exec"),m.__dict__)
k=ctypes.WinDLL("kernel32",use_last_error=True);a=ctypes.WinDLL("advapi32",use_last_error=True)
k.GetCurrentProcess.restype=w.HANDLE
a.OpenProcessToken.argtypes=[w.HANDLE,w.DWORD,ctypes.POINTER(w.HANDLE)];a.OpenProcessToken.restype=w.BOOL
a.GetTokenInformation.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD,ctypes.POINTER(w.DWORD)];a.GetTokenInformation.restype=w.BOOL
a.ConvertSidToStringSidW.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)];a.ConvertSidToStringSidW.restype=w.BOOL
k.CloseHandle.argtypes=[w.HANDLE];k.CloseHandle.restype=w.BOOL
k.LocalFree.argtypes=[ctypes.c_void_p];k.LocalFree.restype=ctypes.c_void_p
token=w.HANDLE();text=ctypes.c_void_p();token_closed=False;sid_freed=False
if not a.OpenProcessToken(k.GetCurrentProcess(),8,ctypes.byref(token)):raise ctypes.WinError(ctypes.get_last_error())
try:
 size=w.DWORD()
 a.GetTokenInformation(token,1,None,0,ctypes.byref(size))
 if not size.value:raise ctypes.WinError(ctypes.get_last_error())
 buf=ctypes.create_string_buffer(size.value)
 if not a.GetTokenInformation(token,1,buf,size,ctypes.byref(size)):raise ctypes.WinError(ctypes.get_last_error())
 sidptr=ctypes.cast(buf,ctypes.POINTER(ctypes.c_void_p))[0]
 if not a.ConvertSidToStringSidW(sidptr,ctypes.byref(text)):raise ctypes.WinError(ctypes.get_last_error())
 try:
  native_sid=ctypes.wstring_at(text);matches=native_sid==m.current_sid()
 finally:
  assert not k.LocalFree(text);sid_freed=True
finally:
 token_closed=bool(k.CloseHandle(token));assert token_closed
volume=ctypes.create_unicode_buffer(512);fs=ctypes.create_unicode_buffer(512)
k.GetVolumePathNameW.argtypes=[w.LPCWSTR,w.LPWSTR,w.DWORD];k.GetVolumePathNameW.restype=w.BOOL
k.GetVolumeInformationW.argtypes=[w.LPCWSTR,w.LPWSTR,w.DWORD,ctypes.POINTER(w.DWORD),ctypes.POINTER(w.DWORD),ctypes.POINTER(w.DWORD),w.LPWSTR,w.DWORD];k.GetVolumeInformationW.restype=w.BOOL
if not k.GetVolumePathNameW(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\NATIVE_ACL_FIXTURE_20260922T213829",volume,512):raise ctypes.WinError(ctypes.get_last_error())
flags=w.DWORD()
if not k.GetVolumeInformationW(volume,None,0,None,None,ctypes.byref(flags),fs,512):raise ctypes.WinError(ctypes.get_last_error())
assert matches and fs.value=="NTFS" and flags.value&8
print(json.dumps({"current_sid_matches_process_token":matches,"token_handle_closed":token_closed,"SID_string_LocalFree":sid_freed,"filesystem":fs.value,"persistent_ACLs_supported":bool(flags.value&8),"real_E2_touched":False}))

```

