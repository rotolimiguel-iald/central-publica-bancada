# E2 — fechamento independente de custódia runtime

[REAL] **Papel CUSTODY: BLOCKERS_CLOSED no contrato de transferência exclusiva de DACL pelo reparador pinado.** O fluxo completo funcionou na fixture entre as duas identidades Windows medidas, com commitment fictício preservado e posterior acesso WSL à fixture. Não é confirmação de que o reparo E2 real já ocorreu; o principal ainda deve executar e registrar target → transfer → verify → smoke real conforme sua autorização.

[INPUT] Esta revisão não altera fontes E2, registro, testemunha, aplicação de ativação ou parecer V3 imutável. Seu escopo é o novo reparador de custódia. Nenhuma seed/offset real, posterior ou strain foi lido; nenhuma ciência, PE ou campanha foi executada.

## Pins examinados

| Fonte | SHA256 |
|---|---|
| `refeito/repair_e2_runtime_custody_013bis.py` | `ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb` |
| `refeito/e2_private_directory_native.py` | `5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0` |
| `bis/E2_SMOKE_ATTEMPT_001_FAILED_PRIVATE_ACCESS.json` | `03676479d22c9036249df2ac180759362b3ddead85249e2305d797780f23fbd4` |

[REAL] Hashes medidos por script e reconferidos ao final. O reparador e helper mantiveram seus bytes durante os ensaios. A leitura do recibo de falha é documental; não reproduzi acesso à seed E2 real.

[DECLARADO — diagnóstico preservado no recibo do principal] A smoke real anterior falhou em seed.stat, após checks de contexto, com SID de criação diferente do SID Windows host e sem ciência. Essa história permanece preservada; esta revisão adiciona evidência de fixture, não reescreve o recibo ou o registro original.

## Fixture e identidade

[REAL] Fixture principal isolada:
`C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\CUSTODY_TRANSFER_FIXTURE_20260922T214951`.

Helper e reparador foram carregados após conferência de hash, com nomes de módulo que não disparam __main__. No harness, **B, TARGET, FOLDER e SEED do reparador, além de B do helper, foram redefinidos exclusivamente para essa fixture**. Assert de containment precedeu cada ação. Todos os nomes semelhantes a registro/seed/recibo nesta fixture referem-se a objetos fictícios.

[REAL] Arquivo fictício de 32 bytes constantes identificados como teste, não aleatórios. Registro fictício com status FIXTURE_ONLY_NOT_A_REGISTRATION. Hash dos dados fictícios: `4e7b1b70451d6fe0fb35709137bf12f777bd5105abbf79564841aae62329b097`; hash do registro fictício: `b051c29542deffb192770266d6fdbc205c12d4681f27cff920a2c20ce4fc90a6`. Esses valores não têm relação com a seed ou o commitment E2 reais.

[REAL] Identidade de criação, medida no processo default:
`fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88`.

Identidade destino, medida no processo Windows host escalado:
`4a6b9a70b410d658acf941f1d42fa6aa031566e3f53e3d7a05a48417caa6f9ae`.

São distintos e coincidem com os hashes do diagnóstico informado. O SID textual foi usado somente na fixture/metadados de identidade; o parecer exibe seus hashes. Nenhuma regra Everyone/grupo foi adicionada.

## Resultado de ponta a ponta na fixture

1. [REAL] **record-target no host:** gravou apenas metadados no TARGET fictício. Antes da transferência, tentativa normal de ler o arquivo fictício pelo host recebeu PermissionError.
2. [REAL] **transfer sob identidade criadora:** verificou DACL inicial, tamanho e commitment fictício; publicou recibo BEFORE antes de mutar; aplicou a ACL protegida do host primeiro ao arquivo e depois ao diretório. Recibo final: DACL_TRANSFERRED_AWAITING_HOST_VERIFICATION.
3. [REAL] **verify no host:** confirmou identidade destino, DACL, 32 bytes e o mesmo commitment; registro fictício permaneceu byte a byte igual. Recibo HOST_EXCLUSIVE_DACL_AND_UNCHANGED_SEED_COMMITMENT_VERIFIED.
4. [REAL] **WSL via host, somente fixture:** uid0 conseguiu stat e hash do arquivo fictício; 32 bytes e commitment idênticos. Isso resolve o cenário de integração na fixture, não certifica a futura smoke real.
5. [REAL] **retorno à identidade criadora:** leitura dos dados fictícios passou a ser recusada. A evidência de mudança de acesso foi obtida sem ler dados E2 reais.

[REAL] Nenhuma alteração de ExecutionPolicy, código E2 ou registro real. As permissões mutadas pertencem somente à fixture. As ações reais do reparador não foram executadas fora dela.

## Herança, duplicação e ctypes

[REAL] O reparador cria descritor SDDL D:P com ACE única para o target SID e extrai a DACL com GetSecurityDescriptorDacl. O argumento de SetNamedSecurityInfoW é **0x80000004**, combinando DACL_SECURITY_INFORMATION e PROTECTED_DACL_SECURITY_INFORMATION. Isso fixa a proteção no objeto, não apenas na representação textual.

[REAL] **Após a primeira mutação:** arquivo fictício com DACL protegida, uma ACE, flags vazias, SID do host. **Após mudar o diretório:** o arquivo continuou protegido com exatamente uma ACE explícita do host; não recebeu ACE herdada duplicada. O diretório apresentou uma ACE do host com flags OICI e DACL protegida. Este era o ponto principal de herança solicitado e foi medido após ambos os estágios.

[REAL] Prototipagem revisada: DWORD/BOOL Windows, ponteiros para PBOOL/PACL, retorno DWORD de SetNamedSecurityInfoW, SECURITY_DESCRIPTOR como ponteiro e LocalFree do descritor proprietário. O ponteiro DACL retornado é parte do descritor e não recebe liberação independente. Falhas de API retornam exceção; DACL ausente/nula é recusada.

[REAL] Instrumentação durante a transferência e leitura de metadados da fixture: **14 alocações rastreadas, 14 LocalFree, zero pendentes**. O finally de assign libera o descritor mesmo se uma operação interna falhar; os casos de sucesso exercitaram as duas atribuições. Não extrapolo esse rastreamento finito para prova universal de ausência de leaks.

[REAL] O código verifica reparse points/atributos ausentes nos alvos e pais antes de mutar. A primitive nativa e sua recusa de reparse real já foram ensaiadas na revisão V3. Não repeti toda a bateria anterior, nem alego isolamento contra troca concorrente de objetos por processo privilegiado.

## Falha parcial e preservação de história

[REAL] Três mocks do **bloco try/except exato** da mutação confirmaram: falha no arquivo não chama atribuição do diretório e registra zero estágios; falha no diretório conserva apenas o estágio do arquivo; sucesso registra os dois em ordem. Em falha, o estado não é promovido a verificado.

[REAL — leitura estática] O reparador escreve BEFORE antes das mutações e um recibo com status parcial/erro se a atribuição falhar; não regrava dados da seed nem registro. Receipt existente impede repetição silenciosa, e o BEFORE é publicado sem sobrescrita. Verify requer status de transferência concluída, identidade host, DACL final, tamanho e commitment; o smoke real continua etapa separada. Falhas ao publicar recibos podem exigir auditoria de estado parcial; não há promessa de transação ou rollback atômico de duas ACLs.

[REAL] O SHA da seed é lido **programaticamente pelo reparador** no fluxo pretendido para conferir o commitment. Nos meus testes, essas leituras recaíram somente sobre o arquivo fictício. Não se expõem bytes/offsets. Não se deve confundir essa verificação programática autorizada do principal com autorização ao revisor para ler a seed real.

## Limite de segurança: DACL exclusiva não muda o proprietário

[REAL] O OWNER SID do arquivo e do diretório fictícios **permaneceu o da identidade criadora**, medido após a transferência. O reparador só usa flags de DACL; não solicita troca de proprietário.

[INPUT — alcance aprovado] O contrato aqui fechado é **ACL de acesso do host exclusiva, protegida e sem ACE de grupo**, conservando bytes/commitment. Não é transferência de proprietário, custódia humana independente ou exclusão absoluta do criador/administrador com poderes de gestão de ACL. A identidade criadora perdeu leitura normal dos dados na fixture, mas conservar o owner não equivale a torná-la incapaz de administrar permissões. Esse limite deve acompanhar a descrição “host exclusivo”.

[OPEN] A execução E2 real e sua smoke de integração são responsabilidade do principal, com os pins/recibos esperados e história preservada. Se uma fase real falhar, não repetir silenciosamente nem ampliar permissões. O fechamento de custódia não move gate científico; NOT_FALSIFIED nunca CONFIRMED.

## Evidência independente completa

```json
{
  "fixture": {
    "fixture": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\CUSTODY_TRANSFER_FIXTURE_20260922T214951",
    "helper_sha256": "5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0",
    "repair_sha256": "ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb",
    "dummy_bytes": 32,
    "dummy_commitment_sha256": "4e7b1b70451d6fe0fb35709137bf12f777bd5105abbf79564841aae62329b097",
    "fixture_registration_sha256": "b051c29542deffb192770266d6fdbc205c12d4681f27cff920a2c20ce4fc90a6",
    "creation_sid_sha256": "fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88",
    "real_E2_accessed": false
  },
  "target": {
    "fixture": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\CUSTODY_TRANSFER_FIXTURE_20260922T214951",
    "target_metadata": {
      "status": "WINDOWS_RUNTIME_HOST_IDENTITY_ONLY",
      "sha256": "dc72fec72fa2d17f79e74d5e38beea556b68fc8fc370282db2a3fedc6fd282da",
      "sid_sha256": "4a6b9a70b410d658acf941f1d42fa6aa031566e3f53e3d7a05a48417caa6f9ae"
    },
    "pretransfer_dummy_read_denied_to_target": true,
    "real_E2_touched": false
  },
  "transfer": {
    "fixture": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\CUSTODY_TRANSFER_FIXTURE_20260922T214951",
    "receipt": {
      "registration_sha256": "b051c29542deffb192770266d6fdbc205c12d4681f27cff920a2c20ce4fc90a6",
      "target_identity_sha256": "dc72fec72fa2d17f79e74d5e38beea556b68fc8fc370282db2a3fedc6fd282da",
      "seed_commitment_sha256": "4e7b1b70451d6fe0fb35709137bf12f777bd5105abbf79564841aae62329b097",
      "script_sha256": "ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb",
      "utc": "2026-09-22T21:51:33.198018+00:00",
      "seed_bytes_disclosed": false,
      "registration_modified": false,
      "execution_policy_changed": false,
      "status": "DACL_TRANSFERRED_AWAITING_HOST_VERIFICATION",
      "stages": [
        "seed_exclusive_target_DACL",
        "directory_exclusive_target_DACL"
      ],
      "error": null,
      "seed_bytes_rewritten": false
    },
    "mutation_order": [
      {
        "object": "dummy_file",
        "ACL": {
          "protected": true,
          "ace_count": 1,
          "ace_flags": [
            ""
          ],
          "sid_hashes": [
            "4a6b9a70b410d658acf941f1d42fa6aa031566e3f53e3d7a05a48417caa6f9ae"
          ]
        }
      },
      {
        "object": "directory",
        "ACL": {
          "protected": true,
          "ace_count": 1,
          "ace_flags": [
            "OICI"
          ],
          "sid_hashes": [
            "4a6b9a70b410d658acf941f1d42fa6aa031566e3f53e3d7a05a48417caa6f9ae"
          ]
        }
      }
    ],
    "after_parent_mutation_dummy_ACL": {
      "protected": true,
      "ace_count": 1,
      "ace_flags": [
        ""
      ],
      "sid_hashes": [
        "4a6b9a70b410d658acf941f1d42fa6aa031566e3f53e3d7a05a48417caa6f9ae"
      ]
    },
    "after_parent_mutation_directory_ACL": {
      "protected": true,
      "ace_count": 1,
      "ace_flags": [
        "OICI"
      ],
      "sid_hashes": [
        "4a6b9a70b410d658acf941f1d42fa6aa031566e3f53e3d7a05a48417caa6f9ae"
      ]
    },
    "native_allocations": {
      "allocated": 14,
      "freed": 14
    },
    "outstanding": 0,
    "fixture_registration_unchanged": true,
    "real_E2_touched": false
  },
  "host_verification": {
    "fixture": "C:\\IALD\\Central de Patentes\\Chatgpt\\ORDEM_013_RINGDOWN\\bis\\e2_publication_census\\CUSTODY_TRANSFER_FIXTURE_20260922T214951",
    "verify": {
      "status": "HOST_EXCLUSIVE_DACL_AND_UNCHANGED_SEED_COMMITMENT_VERIFIED",
      "sha256": "05f0fcb901814e9af21e8f164ce72f04d6e1edd2ae1f75352b4c69ceead55d50"
    },
    "dummy_size": 32,
    "dummy_commitment_unchanged": true,
    "registration_unchanged": true,
    "real_E2_touched": false
  },
  "WSL_fixture": {
    "fixture_only": true,
    "WSL_uid": 0,
    "dummy_size": 32,
    "dummy_commitment_unchanged": true,
    "real_E2_touched": false
  },
  "scope_and_failure_mocks": {
    "old_identity_dummy_data_read_denied": true,
    "owner_sid_hashes_after_DACL_transfer": {
      "dummy_file": "fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88",
      "fixture_directory": "fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88"
    },
    "creation_sid_hash": "fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88",
    "original_owner_retained": true,
    "partial_failure_mocks": [
      {
        "failure_at": "file",
        "passed": true,
        "calls": [
          "file"
        ],
        "recorded_stages": [],
        "error_recorded": true
      },
      {
        "failure_at": "directory",
        "passed": true,
        "calls": [
          "file",
          "directory"
        ],
        "recorded_stages": [
          "seed_exclusive_target_DACL"
        ],
        "error_recorded": true
      },
      {
        "failure_at": null,
        "passed": true,
        "calls": [
          "file",
          "directory"
        ],
        "recorded_stages": [
          "seed_exclusive_target_DACL",
          "directory_exclusive_target_DACL"
        ],
        "error_recorded": false
      }
    ],
    "real_E2_touched": false
  }
}
```

## Harnesses preservados

[REAL] Estes scripts documentam somente ensaios em fixture. O bootstrap redefine todos os globais críticos antes de chamar main. Etapas de criação não são idempotentes; reprodução deve usar outra fixture. Não substituir os caminhos por E2 real.

### Preparação da fixture

```python
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,types,sys,os
b=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
helper=b/"refeito/e2_private_directory_native.py";repair=b/"refeito/repair_e2_runtime_custody_013bis.py"
hb=helper.read_bytes();rb=repair.read_bytes()
assert hashlib.sha256(hb).hexdigest()=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
assert hashlib.sha256(rb).hexdigest()=="ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb"
m=types.ModuleType("e2_private_directory_native");m.__file__=str(helper);exec(compile(hb,str(helper),"exec"),m.__dict__);sys.modules[m.__name__]=m
root=b/"bis/e2_publication_census";fixture=root/("CUSTODY_TRANSFER_FIXTURE_"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"))
fixture.mkdir();(fixture/"cache").mkdir();(fixture/"bis").mkdir();m.B=fixture
m.operate("Prepare")
dummy=fixture/"cache/E2_PRIVATE/BLIND_SEED_V1.bin"
data=b"FICTITIOUS_CUSTODY_DATA".ljust(32,b".")
assert len(data)==32
fd=os.open(dummy,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_BINARY,0o600)
with os.fdopen(fd,"wb") as f:f.write(data);f.flush();os.fsync(f.fileno())
reg={"status":"FIXTURE_ONLY_NOT_A_REGISTRATION","blinding":{"seed_commitment_sha256":hashlib.sha256(data).hexdigest()}}
regraw=(json.dumps(reg,sort_keys=True)+"\n").encode()
with (fixture/"RINGDOWN_5SIGMA_V1.json").open("xb") as f:f.write(regraw)
print(json.dumps({"fixture":str(fixture),"helper_sha256":hashlib.sha256(hb).hexdigest(),"repair_sha256":hashlib.sha256(rb).hexdigest(),"dummy_bytes":len(data),"dummy_commitment_sha256":hashlib.sha256(data).hexdigest(),"fixture_registration_sha256":hashlib.sha256(regraw).hexdigest(),"creation_sid_sha256":hashlib.sha256(m.current_sid().encode()).hexdigest(),"real_E2_accessed":False}))

```

### Identidade destino — processo host

```python
from pathlib import Path
import ast,ctypes,hashlib,json,types,sys,os,io,contextlib
production=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
fixture=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\CUSTODY_TRANSFER_FIXTURE_20260922T214951")
assert fixture.is_relative_to(production/"bis/e2_publication_census") and fixture!=production
hp=production/"refeito/e2_private_directory_native.py";rp=production/"refeito/repair_e2_runtime_custody_013bis.py"
hb=hp.read_bytes();rb=rp.read_bytes()
assert hashlib.sha256(hb).hexdigest()=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
assert hashlib.sha256(rb).hexdigest()=="ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb"
acl=types.ModuleType("e2_private_directory_native");acl.__file__=str(hp);exec(compile(hb,str(hp),"exec"),acl.__dict__);sys.modules[acl.__name__]=acl
repair=types.ModuleType("fixture_repair");repair.__file__=str(rp);exec(compile(rb,str(rp),"exec"),repair.__dict__)
acl.B=fixture;repair.B=fixture;repair.TARGET=fixture/"bis/E2_RUNTIME_WINDOWS_IDENTITY_V1.json";repair.FOLDER=fixture/"cache/E2_PRIVATE";repair.SEED=repair.FOLDER/"BLIND_SEED_V1.bin"
assert all(p.is_relative_to(fixture) for p in (repair.TARGET,repair.FOLDER,repair.SEED))

sys.argv=["fixture_repair","--action","record-target"]
out=io.StringIO()
with contextlib.redirect_stdout(out):repair.main()
target=json.loads(out.getvalue())
denied=False
try:
 with repair.SEED.open("rb") as stream:data=stream.read()
except PermissionError:denied=True
print(json.dumps({"fixture":str(fixture),"target_metadata":target,"pretransfer_dummy_read_denied_to_target":denied,"real_E2_touched":False}))

```

### Transferência — processo criador

```python
from pathlib import Path
import ast,ctypes,hashlib,json,types,sys,os,io,contextlib
production=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
fixture=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\CUSTODY_TRANSFER_FIXTURE_20260922T214951")
assert fixture.is_relative_to(production/"bis/e2_publication_census") and fixture!=production
hp=production/"refeito/e2_private_directory_native.py";rp=production/"refeito/repair_e2_runtime_custody_013bis.py"
hb=hp.read_bytes();rb=rp.read_bytes()
assert hashlib.sha256(hb).hexdigest()=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
assert hashlib.sha256(rb).hexdigest()=="ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb"
acl=types.ModuleType("e2_private_directory_native");acl.__file__=str(hp);exec(compile(hb,str(hp),"exec"),acl.__dict__);sys.modules[acl.__name__]=acl
repair=types.ModuleType("fixture_repair");repair.__file__=str(rp);exec(compile(rb,str(rp),"exec"),repair.__dict__)
acl.B=fixture;repair.B=fixture;repair.TARGET=fixture/"bis/E2_RUNTIME_WINDOWS_IDENTITY_V1.json";repair.FOLDER=fixture/"cache/E2_PRIVATE";repair.SEED=repair.FOLDER/"BLIND_SEED_V1.bin"
assert all(p.is_relative_to(fixture) for p in (repair.TARGET,repair.FOLDER,repair.SEED))

adv,kernel=acl.native()
original_native=acl.native
allocs=set();counts={"allocated":0,"freed":0};stages=[]
def ptr(out):return ctypes.cast(out,ctypes.POINTER(ctypes.c_void_p))[0]
def tracked(fn,index,success):
 def call(*args):
  result=fn(*args)
  if success(result):
   address=ptr(args[index]);assert address and address not in allocs
   allocs.add(address);counts["allocated"]+=1
  return result
 return call
adv.ConvertStringSecurityDescriptorToSecurityDescriptorW=tracked(adv.ConvertStringSecurityDescriptorToSecurityDescriptorW,2,bool)
adv.GetNamedSecurityInfoW=tracked(adv.GetNamedSecurityInfoW,7,lambda r:r==0)
adv.ConvertSecurityDescriptorToStringSecurityDescriptorW=tracked(adv.ConvertSecurityDescriptorToStringSecurityDescriptorW,3,bool)
real_free=kernel.LocalFree
def free(p):
 address=p.value if isinstance(p,ctypes.c_void_p) else p
 assert address in allocs
 result=real_free(p);assert not result
 allocs.remove(address);counts["freed"]+=1
 return result
kernel.LocalFree=free
acl.native=lambda:(adv,kernel)
def metadata(path):
 descriptor=ctypes.c_void_p();text=ctypes.c_void_p()
 code=adv.GetNamedSecurityInfoW(str(path),1,4,None,None,None,None,ctypes.byref(descriptor))
 if code:raise ctypes.WinError(code)
 try:
  if not adv.ConvertSecurityDescriptorToStringSecurityDescriptorW(descriptor,1,4,ctypes.byref(text),None):raise ctypes.WinError(ctypes.get_last_error())
  try:
   sddl=ctypes.wstring_at(text);aces=acl.re.findall(r"\(([^()]*)\)",sddl)
   return {"protected":"P" in sddl.split("(",1)[0][2:],"ace_count":len(aces),"ace_flags":[x.split(";")[1] for x in aces],"sid_hashes":[hashlib.sha256(x.split(";")[5].encode()).hexdigest() for x in aces]}
  finally:kernel.LocalFree(text)
 finally:kernel.LocalFree(descriptor)
original_assign=repair.assign
def assign(path,sid,directory,*args):
 original_assign(path,sid,directory,*args)
 evidence=metadata(path)
 assert evidence["protected"] and evidence["ace_count"]==1
 stages.append({"object":"directory" if directory else "dummy_file","ACL":evidence})
repair.assign=assign
sys.argv=["fixture_repair","--action","transfer","--expected-target-sha256","dc72fec72fa2d17f79e74d5e38beea556b68fc8fc370282db2a3fedc6fd282da","--expected-registration-sha256","b051c29542deffb192770266d6fdbc205c12d4681f27cff920a2c20ce4fc90a6"]
out=io.StringIO()
with contextlib.redirect_stdout(out):repair.main()
after_file=metadata(repair.SEED);after_folder=metadata(repair.FOLDER)
assert after_file["ace_count"]==after_folder["ace_count"]==1
assert after_file["protected"] and after_file["ace_flags"]==[""]
assert not allocs and counts["allocated"]==counts["freed"]
print(json.dumps({"fixture":str(fixture),"receipt":json.loads(out.getvalue()),"mutation_order":stages,"after_parent_mutation_dummy_ACL":after_file,"after_parent_mutation_directory_ACL":after_folder,"native_allocations":counts,"outstanding":len(allocs),"fixture_registration_unchanged":repair.sha(fixture/"RINGDOWN_5SIGMA_V1.json")=="b051c29542deffb192770266d6fdbc205c12d4681f27cff920a2c20ce4fc90a6","real_E2_touched":False}))

```

### Verificação — processo host

```python
from pathlib import Path
import ast,ctypes,hashlib,json,types,sys,os,io,contextlib
production=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
fixture=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\CUSTODY_TRANSFER_FIXTURE_20260922T214951")
assert fixture.is_relative_to(production/"bis/e2_publication_census") and fixture!=production
hp=production/"refeito/e2_private_directory_native.py";rp=production/"refeito/repair_e2_runtime_custody_013bis.py"
hb=hp.read_bytes();rb=rp.read_bytes()
assert hashlib.sha256(hb).hexdigest()=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
assert hashlib.sha256(rb).hexdigest()=="ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb"
acl=types.ModuleType("e2_private_directory_native");acl.__file__=str(hp);exec(compile(hb,str(hp),"exec"),acl.__dict__);sys.modules[acl.__name__]=acl
repair=types.ModuleType("fixture_repair");repair.__file__=str(rp);exec(compile(rb,str(rp),"exec"),repair.__dict__)
acl.B=fixture;repair.B=fixture;repair.TARGET=fixture/"bis/E2_RUNTIME_WINDOWS_IDENTITY_V1.json";repair.FOLDER=fixture/"cache/E2_PRIVATE";repair.SEED=repair.FOLDER/"BLIND_SEED_V1.bin"
assert all(p.is_relative_to(fixture) for p in (repair.TARGET,repair.FOLDER,repair.SEED))

sys.argv=["fixture_repair","--action","verify","--expected-target-sha256","dc72fec72fa2d17f79e74d5e38beea556b68fc8fc370282db2a3fedc6fd282da","--expected-registration-sha256","b051c29542deffb192770266d6fdbc205c12d4681f27cff920a2c20ce4fc90a6"]
out=io.StringIO()
with contextlib.redirect_stdout(out):repair.main()
assert repair.SEED.stat().st_size==32
assert repair.sha(repair.SEED)=="4e7b1b70451d6fe0fb35709137bf12f777bd5105abbf79564841aae62329b097"
assert repair.sha(fixture/"RINGDOWN_5SIGMA_V1.json")=="b051c29542deffb192770266d6fdbc205c12d4681f27cff920a2c20ce4fc90a6"
print(json.dumps({"fixture":str(fixture),"verify":json.loads(out.getvalue()),"dummy_size":32,"dummy_commitment_unchanged":True,"registration_unchanged":True,"real_E2_touched":False}))

```

### WSL — somente arquivo fictício

```python
from pathlib import Path
import os,hashlib,json
p=Path("/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e2_publication_census/CUSTODY_TRANSFER_FIXTURE_20260922T214951/cache/E2_PRIVATE/BLIND_SEED_V1.bin")
assert "bis/e2_publication_census/CUSTODY_TRANSFER_FIXTURE_" in str(p)
n=p.stat().st_size;h=hashlib.sha256(p.read_bytes()).hexdigest()
assert n==32 and h=="4e7b1b70451d6fe0fb35709137bf12f777bd5105abbf79564841aae62329b097"
print(json.dumps({"fixture_only":True,"WSL_uid":os.getuid(),"dummy_size":n,"dummy_commitment_unchanged":True,"real_E2_touched":False}))

```

### OWNER, recusa ao criador e falhas parciais

```python
from pathlib import Path
import ast,ctypes,hashlib,json,types,sys,os,io,contextlib
production=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN")
fixture=Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\bis\e2_publication_census\CUSTODY_TRANSFER_FIXTURE_20260922T214951")
assert fixture.is_relative_to(production/"bis/e2_publication_census") and fixture!=production
hp=production/"refeito/e2_private_directory_native.py";rp=production/"refeito/repair_e2_runtime_custody_013bis.py"
hb=hp.read_bytes();rb=rp.read_bytes()
assert hashlib.sha256(hb).hexdigest()=="5827a3a7a55b499ee44db3df34c8a60563ac5910f281065f554bccf7c02a54f0"
assert hashlib.sha256(rb).hexdigest()=="ebac65df2ff47369e61cc69c3b6a7e49894d2280beb6d9a8ece7766cfef95cfb"
acl=types.ModuleType("e2_private_directory_native");acl.__file__=str(hp);exec(compile(hb,str(hp),"exec"),acl.__dict__);sys.modules[acl.__name__]=acl
repair=types.ModuleType("fixture_repair");repair.__file__=str(rp);exec(compile(rb,str(rp),"exec"),repair.__dict__)
acl.B=fixture;repair.B=fixture;repair.TARGET=fixture/"bis/E2_RUNTIME_WINDOWS_IDENTITY_V1.json";repair.FOLDER=fixture/"cache/E2_PRIVATE";repair.SEED=repair.FOLDER/"BLIND_SEED_V1.bin"
assert all(p.is_relative_to(fixture) for p in (repair.TARGET,repair.FOLDER,repair.SEED))

adv,kernel=acl.native()
adv.ConvertSidToStringSidW.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p)]
adv.ConvertSidToStringSidW.restype=acl.wt.BOOL
def owner_hash(path):
 owner=ctypes.c_void_p();descriptor=ctypes.c_void_p();text=ctypes.c_void_p()
 err=adv.GetNamedSecurityInfoW(str(path),1,1,ctypes.byref(owner),None,None,None,ctypes.byref(descriptor))
 if err:raise ctypes.WinError(err)
 try:
  if not adv.ConvertSidToStringSidW(owner,ctypes.byref(text)):raise ctypes.WinError(ctypes.get_last_error())
  try:return hashlib.sha256(ctypes.wstring_at(text).encode()).hexdigest()
  finally:kernel.LocalFree(text)
 finally:kernel.LocalFree(descriptor)
denied=False
try:
 with repair.SEED.open("rb") as stream:stream.read()
except PermissionError:denied=True
owners={"dummy_file":owner_hash(repair.SEED),"fixture_directory":owner_hash(repair.FOLDER)}
assert denied
# Test only the exact mutation try/except from the pinned repair source.
tree=ast.parse(rb);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="main")
attempt=next(n for n in ast.walk(fn) if isinstance(n,ast.Try) and any(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=="assign" for x in ast.walk(n)))
records=[]
for failure in ("file","directory",None):
 calls=[]
 def mocked_assign(path,*args):
  calls.append(path)
  if path==failure:raise OSError("INDEPENDENT_INJECTED_FAILURE")
 env={"stages":[],"error":None,"assign":mocked_assign,"SEED":"file","FOLDER":"directory","target_sid":"FAKE","adv":None,"kernel":None}
 exec(compile(ast.Module(body=[attempt],type_ignores=[]),"custody_stage_AST_only","exec"),env)
 expected=[] if failure=="file" else ["seed_exclusive_target_DACL"] if failure=="directory" else ["seed_exclusive_target_DACL","directory_exclusive_target_DACL"]
 assert env["stages"]==expected and (env["error"] is not None)==(failure is not None)
 assert calls==(["file"] if failure=="file" else ["file","directory"])
 records.append({"failure_at":failure,"passed":True,"calls":calls,"recorded_stages":env["stages"],"error_recorded":env["error"] is not None})
print(json.dumps({"old_identity_dummy_data_read_denied":denied,"owner_sid_hashes_after_DACL_transfer":owners,"creation_sid_hash":"fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88","original_owner_retained":all(x=="fc30a0e0edfeef5a7734a3edbdf616e0bdc4895e13c2c1a66530a0714ee04e88" for x in owners.values()),"partial_failure_mocks":records,"real_E2_touched":False}))

```

