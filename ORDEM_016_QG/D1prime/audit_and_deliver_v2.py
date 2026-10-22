# predecessor_sha256: 0b0a9a4e507d21a477bba527b06a484a0255258433f679e17f5029329535568c
"""Audit local photon characters; record global representation debts explicitly."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,re
from fractions import Fraction as F
from math import isqrt
from itertools import permutations
R=Path(__file__).resolve().parents[1];D=R/'D1prime';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import sha,save,write
now=datetime.now(timezone.utc);proofs=[]
for fn,label,n in [('PhotonScreenCharacters_v3.lean','photon_03',10),('PhotonCharacterCocycle.lean','character_01',4)]:
 p=D/fn;log=D/(label+'.log');receipt=D/(label+'.json');x=json.loads(receipt.read_bytes())
 assert x['rc']==0 and x['source_sha256']==sha(p) and x['log_sha256']==sha(log)
 assert not x['newer_kernel_files'] and not x['scan_errors']
 assert not re.search(r'\b(sorry|axiom)\b',p.read_text('utf-8'))
 ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log.read_text('utf-8-sig'))
 assert len(ax)==n and all(set(v.split(', '))<={'propext','Classical.choice','Quot.sound'} for _,v in ax)
 proofs.append(dict(source=str(p),source_sha256=sha(p),receipt_sha256=sha(receipt),log_sha256=sha(log),declarations=dict(ax)))
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def diag(*v):return [[F(v[i]) if i==j else F(0) for j in range(len(v))] for i in range(len(v))]
def tr(a):return list(map(list,zip(*a)))
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def scale(a,c):return [[c*x for x in row] for row in a]
def det(a):
 n=len(a);total=F(0)
 for q in permutations(range(n)):
  v=F((-1)**sum(q[i]>q[j] for i in range(n) for j in range(i+1,n)))
  for i,j in enumerate(q):v*=a[i][j]
  total+=v
 return total
eta=diag(1,-1,-1,-1);p=[[F(x)] for x in [5,3,4,0]];checks=[]
def check(name,ok):
 assert ok,name
 checks.append(dict(name=name,passed=True))
def frame(p):
 v=[x[0] for x in p];q=v[2]**2+v[3]**2
 r=F(isqrt(q.numerator),isqrt(q.denominator));assert r*r==q and r>0
 return [[v[1]/r,0],[v[0]/r,0],[0,-v[3]/r],[0,v[2]/r]]
def C(g,p):return scale(mm(mm(mm(tr(frame(mm(g,p))),eta),g),frame(p)),-1)
boost=[[F(5,4),F(3,4),0,0],[F(3,4),F(5,4),0,0],[0,0,1,0],[0,0,0,1]]
inv=[[F(5,4),-F(3,4),0,0],[-F(3,4),F(5,4),0,0],[0,0,1,0],[0,0,0,1]]
def little(a,b):return mm(mm(boost,[[1,0,0,0],[0,a,0,-b],[0,0,1,0],[0,b,0,a]]),inv)
g=little(F(3,5),F(4,5));h=little(F(5,13),F(12,13));gh=mm(g,h)
for name,T in [('g',g),('h',h),('gh',gh)]:
 check(name+'_Lorentz',mm(mm(tr(T),eta),T)==eta);check(name+'_det1',det(T)==1)
 c=C(T,p);check(name+'_quotient_orthogonal',mm(tr(c),c)==eye(2));check(name+'_quotient_det1',det(c)==1)
check('actual_screen_composition',C(gh,p)==mm(C(g,mm(h,p)),C(h,p)))
def phase(c):return c[0][0],c[0][1]
def cmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
check('actual_photon_phase_composition',phase(C(gh,p))==cmul(phase(C(g,mm(h,p))),phase(C(h,p))))
reflection=diag(1,1,1,-1);ref=C(reflection,p)
check('improper_metric_preservation',mm(mm(tr(reflection),eta),reflection)==eta)
check('improper_orientation_rejected',det(ref)==-1)
check('improper_not_same_complex_phase',(ref[1][0],ref[1][1])!=cmul(phase(ref),(0,1)))
save(D/'CONTROLS.json',dict(status='REAL_EXACT_RATIONAL_NOT_LEAN_GLOBAL_REPRESENTATION',tests=checks,script_sha256=sha(Path(__file__))))
old=json.loads((R/'C4/RESULTS.json').read_bytes())
attempts=[json.loads((D/(k+'.json')).read_bytes()) for k in ['photon_01','photon_02','photon_03','character_01']]
result=dict(at=now.isoformat(),status='PARTIAL_REAL_WITH_NAMED_GLOBAL_DEBT',proofs=proofs,declarations=14,controls=len(checks),inherited_named_lemma=old['named_remaining'],inherited_specification=old['specification'],new_result='O(2) quotient derived from actual metric-preserving screen transport; orientation +1 implies U(1) character and composition; conjugation switches character and circular wave sections',remaining=['ScreenOrientationMeasured derived for all proper orthochronous Lorentz maps with the chosen orientation conventions','Measurable patch changes and exceptional null sets under all Lorentz transformations','Strongly continuous unitary induced representation on cone L2, tied to already implemented boosts','Physical photon PCT/net identification, not just complex conjugation of sections'],cpu_seconds=sum(t['cpu_user_seconds']+t['cpu_kernel_seconds'] for t in attempts),wall_seconds=sum(t['wall_seconds'] for t in attempts),bench_hours=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600,opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),new_remote_calls=0,gate_changed=False)
save(D/'RESULTS.json',result)
text=f'''[REAL — 14 declarações no trio; OPEN — representação global de fóton e identificação PCT]

Abertura016SHA256: {result['opening_sha256']}

D1′ reaproveitou a C4. A conservação métrica do transporte real agora implica CᵀC=I na tela transversal. Acrescentar orientação det C=+1 determina C=[[a,b],[-b,a]], a²+b²=1; daí sai o caractere a+ib e sua composição, ligada ao cociclo concreto de C4. A conjugação troca o caractere e as seções circulares ±1. Não se usou um argumento real global da fase.

Duas fontes Lean aprovadas, 14 declarações auditadas, rc0, somente propext/Classical.choice/Quot.sound. Provas/logs/hashes em D1prime/RESULTS.json. Três ciclos no primeiro arquivo, um no segundo. Os dois erros iniciais eram normalizações explícitas do pareamento e comutação do produto complexo; preservados. CPU {result['cpu_seconds']:.6f}s; parede {result['wall_seconds']:.6f}s; bancada {result['bench_hours']:.6f}h, teto16h.

Controle complementar: {len(checks)} verificações racionais exatas. Uma reflexão preserva a métrica mas dá det C=-1 e falha como multiplicação pela mesma fase complexa. Logo a orientação não pode ser suprimida. O controle finito não é prova Lean do grupo inteiro.

GlobalHelicityInducedRepresentationMeasured continua NÃO PAGO, agora com a etapa O(2) e extração/composição do caractere pagas. Faltam: orientação induzida para todo Lorentz próprio ortócrono; cartas mensuráveis e exceções transportadas; ação Lorentz unitária fortemente contínua no L² do cone e restrição ao boost existente; identificação da conjugação/PCT física na rede. Não se inferiu a última da conjugação finita. A aceitação alternativa «teoremas ou lema nomeado» é atendida como MEDIDA parcial; nenhuma hipótese foi inserida como novo axioma.

As três chamadas remotas novas continuam aguardando resposta à autorização específica anteriormente solicitada. Nenhuma chamada falha/incerta foi repetida. Próximo D2′: tensor de Maxwell e controle forjado, com localidade operacional explicitada se aberta. Gate e originais intactos.
'''
write(OUT/'ENTREGA_016_D1prime_foton.md',text.encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now.isoformat()} — D1′ MEDIDA parcial:14 declarações, {len(checks)} controles racionais; representação global nomeada. Bancada{result["bench_hours"]:.6f}h, CPU{result["cpu_seconds"]:.6f}s. PróximoD2′. AberturaSHA256 {result["opening_sha256"]}.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now.isoformat(),own_live_process=None,own_live_processes=[],D1prime_delivery=str(D/'RESULTS.json'),next='D2prime Maxwell StressTensorDataLocal_v2. D1prime local characters proved; global photon representation remains named. Three remote payloads still pending explicit egress approval, do not dispatch. B stays after Part D.');save(q,c,True)
print(json.dumps({k:result[k] for k in ['status','declarations','controls','bench_hours','cpu_seconds','wall_seconds']},ensure_ascii=False))
