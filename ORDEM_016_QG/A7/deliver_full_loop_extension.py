"""Register exact flat localized pair contacts and current orchestration status."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import json, hashlib, uuid

H=Path(__file__).resolve().parent;D=H/'full_loop_extension_delivery';D.mkdir(exist_ok=False)
O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2).encode()
def append(p,t):write(p,p.read_bytes()+t.encode())
artifacts=[];results=[]
for name in ['full_loop_extension','full_loop_extension_basis']:
 m=H/name/'manifest.json'
 for row in json.loads(m.read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256'],row['path']
 results.append(json.loads((H/name/'results.json').read_bytes()))
 artifacts += [m,H/(name+'_run.log')]
checks=sum(r['checks'] for r in results);cpu=sum(r['cpu_seconds'] for r in results)
assert checks==262 and results[1]['components']==120
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
proof=r'''[DERIVED — contato de extensão dos pares planos localizados; Q2 OPEN]

Prescrição mantida: R=FP_a[(1-a)mu^(2a)z^a(.)], z=(X-Y)^2,
CE=-4pi². Q_i denota derivada de delta, não momento de Fourier.
Os kernels foram contraídos a partir dos vértices completos EH e ghost,
incluindo suas correntes de fronteira. Não se reconstruiu o par a partir
da identidade de Ward reduzida.

Para cada monômio x^p/z^n usa-se C_D=R D-D R e a regra de Leibniz:
C_D(x^p/z^n)=sum_{I subset D} (partial_I x^p) C_{D\I}(z^-n).
Multiplicar x_i sobre derivadas de delta equivale a -partial_{Q_i}.
O operador de adjunção tem, em Y, -(eta_a-d_a) para h e
(eta_a-d_a)(eta_j-d_j) para partial_j h. Em X, multiplica-se por
-(lambda_i+d_i) quando a perna externa é partial_i h.
O contato P-Q, com P=O R(F) e Q=R(O F), é -C_O(F).
Conserva-se a multiplicidade simétrica 2/m_ar e a orientação do laço
ghost (segundo vértice transposto), além da divisão16 do par métrico.
Por fim chiX é removido à diagonal pela substituição Q -> Q-lambda.
Conservar apenas chiX(Y) omitiria derivadas de delta já verificadas.

Foram usados jatos exponenciais locais: chiX=e^(lambda.X),chiY=e^(eta.Y).
Um cutoff compacto pode coincidir com esses jatos na região do teste.
Três configurações: (lambda,eta)=(0,0),(0,e0),(e0-e1,e0).
Isso não constitui verificação de lambda,eta arbitrários.

Primeira etapa:85 verificações, incluindo contrações cruas no ponto
(1,2,-1,1) contra os motores localizados numéricos existentes. Segunda:
177 verificações; todas as10 polarizações simétricas,4 componentes ghost,
3 configurações:120 polinômios. O reuso dos resultados11,0 anteriores
é explícito; não se conta reexecução que não ocorreu.

Para h11,c0, em Q=(2,1,0,0), (ghost-metric/2)/CE dá respectivamente
153/64,21259/1920,-7351/640. Polinômios completos nos JSONs.
No caso constante, a fonte previamente calculada tem coeficientes
(-3/32,0,3/32) na base invariante de posto3/grau5. Sua soma aos pares
reproduz (-139/1920,99/1280,217/960) em TODAS as40 componentes.
Essa recuperação verifica normalizações/sinais sem apagar os contatos.

Limite: são contatos de extensão dos pares singulares planos. Ainda
faltam na montagem atual os termos da fonte correspondentes à fronteira
ghost pré-integração, inserções da corrente clássica, partes suaves,
curvatura, aridades superiores e continuação causal. Um contato não
nulo do par não é, sozinho, uma anomalia obstrutiva. Q2 completo não foi
calculado. Os testes CAS não foram apresentados como compilação Lean.
'''
write(D/'DERIVACAO.md',proof.encode());artifacts += [D/'DERIVACAO.md',Path(__file__)]
approval=H/'orchestration_localized_boundary/EGRESS_APPROVAL.json'
ar=json.loads(approval.read_bytes());assert ar['request_id']=='70e9e188-471f-412d-848f-bf0ecc7d51c4'
artifacts.append(approval)
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,full_Q2=False,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts])
write(D/'manifest.json',dump(manifest))
ledger=O/'LEDGER_016.jsonl';append(ledger,json.dumps(dict(at=now.isoformat(),event='FULL_LOCALIZED_FLAT_PAIR_EXTENSION',target='A7.b',checks=checks,cpu_seconds=cpu,rc=0,manifest_sha256=sha(D/'manifest.json'),remote_call=False))+'\n')
total=Decimal(0);seen=set()
for line in ledger.read_text('utf-8-sig').splitlines():
 if not line.strip():continue
 e=json.loads(line);k=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is not None and (k is None or k not in seen):
  total+=Decimal(str(v))
  if k:seen.add(k)
start=datetime.fromisoformat(json.loads((H/'full_loop_extension/PRE_REGISTER.json').read_bytes())['at']);wall=(now-start).total_seconds()/3600
out=O/'ENTREGA_016_A7b_contato_lacos_localizados_base_completa.md';assert not out.exists()
write(out,f'''[DERIVED — pares singulares planos com fronteiras e dois cutoffs; Q2 OPEN]

{now.isoformat()}. Abertura SHA256 {opening}.

Calculado contato P-Q=-C_O(F) diretamente dos kernels não reduzidos,
incluindo vértices EH/ghost completos. {checks} verificações exatas
(85+177), {cpu}s de CPU, duas execuções rc0. As120 combinações cobrem
10 tensores simétricos x4 ghosts x3 jatos de cutoff declarados.
No cutoff constante, somar a fonte recupera os três coeficientes antigos
em todas as40 componentes. Jatos variáveis produzem contatos adicionais;
foram preservadas todas as derivadas de delta na multiplicação por chiX.

Manifesto {D/'manifest.json'}; SHA256 {sha(D/'manifest.json')}.
Comandos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/full_loop_extension_check.py e A7/full_loop_extension_basis_check.py.
Logs/hashes no manifesto. Bancada registrada{wall:.6f}h; custo externo
parcial conhecido US${total}, não equivale ao custo total de assinaturas.

Próximo: fronteira ghost da fonte na mesma densidade, e inserções da
corrente clássica. Curvatura, partes suaves, aridades e causalidade ainda
exigem montagem; não se anunciou Q2 completo nem alteração do gate.

Coordenação: prioridade conjunta Kimi/MiMo confirmada na tarefa oficial.
Próxima vaga MiMo4d500ad2, depois Kimi f3c34038. DeepSeek70e9 recebeu
autorização expressa do operador na tarefa coordenadora; o bloqueio
histórico está resolvido e o envio aguarda fila como apoio secundário.
Nenhuma chamada duplicada ou original modificado nesta entrega.
'''.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: contato pares planos completos,262checks,120componentes,CPU{cpu}s,bancada{wall:.6f}h; parcialUS${total}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['Raw full localized pair extension computed','Complete10x4 basis for3 cutoff jets; constant source+pair recovered'],
 full_loop_extension_manifest=str(D/'manifest.json'),own_live_processes=[],
 pending_orchestration='Five Kimi admitted,9c1 active; next vacancy MiMo4d,then Kimi f3; DeepSeek70e9 specifically authorized,secondary staging',
 next=['Complete ghost-boundary source at same prescription','Assemble classical-current insertions; curvature, smooth pieces and arities remain',
 'Audit Kimi/MiMo through coordinator; keep current IDs','A7b deadline20:32Z; A7c/d,A8,PartB and final audit remain'])
c['pending_specific_egress_approval'].update(status='RESOLVED_BY_EXPLICIT_USER_APPROVAL_IN_COORDINATOR',approval_receipt=str(approval),remote_sent=False)
write(p,dump(c));print(json.dumps(dict(delivery=str(out),checks=checks,cpu_seconds=cpu,partial_cost=str(total))))
