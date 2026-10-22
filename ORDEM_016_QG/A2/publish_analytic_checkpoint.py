from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys

root=Path(__file__).resolve().parents[1]
folder=root/'A2'
out=root.parent/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
 assert not p.exists(),p
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b
 t.rename(p)
def append(p,b):
 old=p.read_bytes()
 new(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),old)
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(old+b)
 assert t.read_bytes()==old+b
 t.replace(p)

pairs=[('LightRayAnalyticCore_v3','analytic_core_03'),('LightRayGaussianL2_v4','gaussian_l2_04'),
       ('LightRayGaussianL1','gaussian_l1_01')]
args=[sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py')]
artifacts=[]
for src,tag in pairs:
 p,l,r=folder/(src+'.lean'),folder/(tag+'.log'),folder/(tag+'.json')
 d=json.loads(r.read_bytes())
 assert d['rc']==0 and d['source_sha256']==sha(p) and d['log_sha256']==sha(l)
 assert not d['newer_kernel_files'] and not d['scan_errors']
 args.extend([str(p),str(l)])
 artifacts.extend({'file':str(a),'sha256':sha(a)} for a in [p,l,r])
audit=subprocess.run(args,capture_output=True)
assert audit.returncode==0,audit.stdout+audit.stderr
new(folder/'analytic_core_axioms.json',audit.stdout)
tags=[f'analytic_core_{i:02}' for i in range(1,4)]+[f'gaussian_l2_{i:02}' for i in range(1,5)]+['gaussian_l1_01']
receipts=[json.loads((folder/(t+'.json')).read_bytes()) for t in tags]
wall=sum(r['wall_seconds'] for r in receipts)
cpu=sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in receipts)
manifest={'utc':now.isoformat(),'target':'A2.3.a','status':'IN_PROGRESS_PARTIAL_ANALYTIC_INGREDIENTS',
 'artifacts':artifacts,'attempts':[{'label':t,'rc':r['rc'],'sha256':sha(folder/(t+'.json'))} for t,r in zip(tags,receipts)],
 'wall_seconds_all_attempts':wall,'cpu_seconds_all_attempts':cpu,'audit_sha256':sha(folder/'analytic_core_axioms.json'),
 'not_yet_proved':['density of real Gaussian span in transported K','membership of product in closed K','halfline isotony','width uniqueness'],
 'mimo_request_id':'4b84b6c7-4167-4ebb-ab89-129e9e1fd4b3','job_id':None,'gate_moved':False}
new(folder/'analytic_checkpoint_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
text=f'''[REAL] A-2.3.a em curso — ingredientes analíticos e core gaussiano em L1/L2.

Abertura SHA256: {opening}

[DERIVED — Lean isolado] Para m_a(z)=exp(i a exp z), provados holomorfia e |m_a(x+iy)|=exp(-a exp(x) sin(y)); a>=0 e y em [0,π] implicam contração. Para f_(b,r)(z)=exp(-b(z-r-iπ/2)^2), b>0, provadas holomorfia, torção f(x+iπ)=conj f(x), fórmula da norma, integrabilidade L1 e L2 de cada seção horizontal e majorante uniforme pela norma do bordo real. O produto m_a f herda a torção, L1, L2 e a majorante na faixa. Os lemas gaussianos da Mathlib foram reutilizados.

Quinze teoremas novos auditados, todos no trio permitido. Código 0 nas três pedras finais. Oito compilações totais: 3 na pedra analítica, 4 em L2 e 1 em L1; as cinco falhas foram preservadas. Restou um warning de tática redundante no passe L2, sem efeito no termo nem no auditor. Recursos totais {wall:.6f}s parede e {cpu:.6f}s CPU; nenhum arquivo canônico alterado segundo os recibos.

[OPEN — este ramo ainda não foi entregue como PAGO] Ter torção e integrabilidade não foi promovido a pertencer ao K fechado. Faltam a correspondência Fourier/domínio no produto e a densidade do span REAL da família, para estender ao K inteiro. Tampouco foi provada unicidade de π ou meia-inclusão. Esses são passos separados; o alvo A2.3.a continua ativo, dentro de seu teto, sem recuo prematuro.

[INPUT/OPERAÇÃO] Pergunta específica ao MiMo preparada com request_id 4b84b6c7-4167-4ebb-ab89-129e9e1fd4b3, ainda não submetida, aguardando schema de executor obrigatório. Teto financeiro/tamanho artificial MiMo retirados do recibo após conferir as novas falas do operador na tarefa coordenadora (read_thread, mensagens 01a0d357-671a-7de1-ae66-192c6276126c e 01a0d357-672b-7562-9640-79d7796a4c7c). Nenhuma chamada remota científica feita nesta unidade. A resposta do modelo será rascunho, não prova nem execução local. Não move gate.

'''
text+='\n'.join(f"- {a['file']} — SHA256 {a['sha256']}" for a in artifacts)
text+=f"\nManifesto: {folder/'analytic_checkpoint_manifest.json'} — {sha(folder/'analytic_checkpoint_manifest.json')}\nAuditor: {folder/'analytic_core_axioms.json'} — {sha(folder/'analytic_core_axioms.json')}\n"
report=out/'ENTREGA_016_MEDIDA_A2_3a_ingredientes_analiticos.md'
new(report,text.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | A-2.3.a EM CURSO/MEDIDA PARCIAL | 15 teoremas de holomorfia, torção, L1/L2 e majorante; densidade/fecho pendentes | Lean {wall/3600:.9f}h parede, {cpu/3600:.9f}h CPU; B pesada 0h; nenhum executor remoto chamado.\n'.encode())
print(json.dumps({'report':str(report),'sha256':sha(report),'audit_rc':audit.returncode,'declarations':15}))
