from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;CENTRAL=Path(r'C:\IALD\Central de Patentes')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def replace_backup(path,data):
 old=path.read_bytes();stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');bak=path.with_name(path.name+'.bak_'+stamp)
 with bak.open('xb') as f:f.write(old)
 assert bak.read_bytes()==old
 tmp=path.with_name(path.name+'.tmp_'+stamp)
 with tmp.open('xb') as f:f.write(data)
 assert tmp.stat().st_size==len(data) and path.read_bytes()==old;tmp.replace(path);return bak
helper=CENTRAL/'Chatgpt/TGL_BANCADA_OFICIAL/record_universe_delivery.py'
spec=importlib.util.spec_from_file_location('safe_memory',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
source=HERE.parent/'derivacoes/preflight_262/PREFLIGHT_262_RESULT.json';pre=json.loads(source.read_text());test=json.loads((HERE/'VALIDACAO_WORKER_CLAIM.json').read_text())
assert test['status']=='PASS' and test['engine_sha256']==sha(HERE/'background_controls.py')
body=f'''## 06/10/2026 — Correção ao lado: worker reservado antes do solver e escopo de runtime

[REAL — revisão incorporada] Request f132a1d5-7477-405d-963b-b1659db63328. A versão inicial avaliava prediction_worker antes de write_new recusar uma saída existente; portanto a promessa de não repetir não estava implementada integralmente na entrada direta --worker. Não houve execução cosmológica naquela entrega. Fonte/manifesto/recibos anteriores preservados; código corrigido SHA256 {sha(HERE/'background_controls.py')}.

[REAL — correção] Claim exclusivo e persistente por request+hashdoProtocolo+ponto+precisão, mais reserva exclusiva do caminho de saída, ambos antes do solver. Sucesso, falha, interrupção e claim parcial não permitem retry. Claim sem terminal é incerteza visível. Treze controles stand-in passaram, incluindo entrada CLI direta, arquivo parcial, repetição com outro nome, concorrência e falha; três chamadas simuladas, zeroCAMB. VALIDACAO_WORKER_CLAIM.json. Não constitui validação numérica cosmológica.

[ERRATA — runtime] A frase anterior “Python Windows atual sem as três bibliotecas” excedia a medição. No subprocesso sandbox desta sessão, importlib.util.find_spec/importlib.metadata retornaram ausência de numpy/scipy/camb; isto caracteriza somente a resolução de módulos sob aquele token/ambiente. O preflight262 executado no ambiente normal do usuário registrou Python3.14.3 em C:\\Python314\\python.exe e NumPy{pre['runtime']['numpy']}. SciPy não foi usado ali; isso não estabelece ausência nem disponibilidade de SciPy/CAMB no normal-user. Fonte lida: {source}, SHA256 {sha(source)}. A existência em WSL /opt/lal_env é outra consulta independente. Mesmo executável não garante o mesmo sys.path/user-site/token. Nenhuma instalação/desinstalação realizada.

[OPEN] Configuração cosmológica continua candidata. Cinco pontos teóricos não executados. Revisão deste ajuste não autoriza F9 observado, solver ou nova grade. Manter leitura dos recibos e não repetir unidade incerta.
'''
marker='F9_BACKGROUND_WORKER_FIX_f132a1d5_20261006'
for p in [HERE/'PARECER_MOTOR_DE_FUNDO.md',HERE/'MEMORIA_DA_UNIDADE.md']+[CENTRAL/'memory'/x for x in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]+[CENTRAL/'Chatgpt/TGL_BANCADA_OFICIAL'/x for x in ('MEMORIA_CENTRAL.md','REGISTRO_DAS_CONVERSAS.md')]:m.append(p,body,marker)
manifest=HERE/'MANIFESTO_ENTREGA.json';oldmanifest=sha(manifest)
files=[{'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(HERE.iterdir()) if p.is_file() and '.bak_' not in p.name and '.tmp_' not in p.name and p.name not in ('MANIFESTO_ENTREGA.json','FINAL_CHECK_WORKER_FIX.json')]
obj={'request_id':'f132a1d5-7477-405d-963b-b1659db63328','revision':2,'created_utc':datetime.now(timezone.utc).isoformat(),'previous_manifest_sha256':oldmanifest,'status':'WORKER_ADMISSION_FIXED_PREPARATION_ONLY','science_runs':0,'active_validation':'VALIDACAO_WORKER_CLAIM.json','historical_receipts_not_current_engine':['VALIDACAO_PREPARACAO.json','FINAL_CHECK.json','WORKER_FIX_RECEIPT.json'],'files':files}
bak=replace_backup(manifest,(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
for x in files:assert sha(HERE/x['name'])==x['sha256']
spec=importlib.util.spec_from_file_location('fixed',HERE/'background_controls.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.check_delivery();contract=b.validate(b.read('PROTOCOL.json'))
b.write_new(HERE/'FINAL_CHECK_WORKER_FIX.json',{'status':'PASS_NO_SOLVER','files_checked':len(files),'manifest_sha256':sha(manifest),'previous_manifest_backup':str(bak),'engine_sha256':sha(HERE/'background_controls.py'),'contract':contract,'stand_in_checks':13,'CAMB_calls':0,'runtime_erratum_source_sha256':sha(source)})
print(json.dumps({'files':len(files),'manifest_sha256':sha(manifest),'engine_sha256':sha(HERE/'background_controls.py'),'backup':str(bak)}))