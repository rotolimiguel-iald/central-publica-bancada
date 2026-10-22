"""Audit local photon characters; record global representation debts explicitly."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,re
import sympy as s
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
eta=s.diag(1,-1,-1,-1);p=s.Matrix([5,3,4,0]);checks=[]
def check(name,ok):
 assert ok,name
 checks.append(dict(name=name,passed=True))
def eq(a,b):return all(s.simplify(x)==0 for x in a-b)
def frame(p):
 r=s.sqrt(p[2]**2+p[3]**2)
 assert r!=0
 return s.Matrix.hstack(s.Matrix([p[1]/r,p[0]/r,0,0]),s.Matrix([0,0,-p[3]/r,p[2]/r]))
def C(g,p):return s.simplify(-frame(g*p).T*eta*g*frame(p))
g=s.Matrix([[s.Rational(5,4),0,0,s.Rational(3,4)],[0,1,0,0],[0,0,1,0],[s.Rational(3,4),0,0,s.Rational(5,4)]])
h=s.Matrix([[1,0,0,0],[0,s.Rational(3,5),0,-s.Rational(4,5)],[0,0,1,0],[0,s.Rational(4,5),0,s.Rational(3,5)]])
for name,T in [('g',g),('h',h),('gh',g*h)]:
 check(name+'_Lorentz',eq(T.T*eta*T,eta));check(name+'_det1',T.det()==1)
 c=C(T,p);check(name+'_quotient_orthogonal',eq(c.T*c,s.eye(2)));check(name+'_quotient_det1',s.simplify(c.det())==1)
check('actual_screen_composition',eq(C(g*h,p),C(g,h*p)*C(h,p)))
def phase(c):return c[0,0]+s.I*c[0,1]
check('actual_photon_phase_composition',s.simplify(phase(C(g*h,p))-phase(C(g,h*p))*phase(C(h,p)))==0)
reflection=s.diag(1,1,1,-1);ref=C(reflection,p)
check('improper_metric_preservation',eq(reflection.T*eta*reflection,eta))
check('improper_orientation_rejected',ref.det()==-1)
check('improper_not_same_complex_phase',not eq(ref*s.Matrix([1,s.I]),phase(ref)*s.Matrix([1,s.I])))
save(D/'CONTROLS.json',dict(status='REAL_EXACT_CAS_NOT_LEAN_GLOBAL_REPRESENTATION',tests=checks,script_sha256=sha(Path(__file__))))
old=json.loads((R/'C4/RESULTS.json').read_bytes())
attempts=[json.loads((D/(k+'.json')).read_bytes()) for k in ['photon_01','photon_02','photon_03','character_01']]
result=dict(at=now.isoformat(),status='PARTIAL_REAL_WITH_NAMED_GLOBAL_DEBT',proofs=proofs,declarations=14,controls=len(checks),inherited_named_lemma=old['named_remaining'],inherited_specification=old['specification'],new_result='O(2) quotient derived from actual metric-preserving screen transport; orientation +1 implies U(1) character and composition; conjugation switches character and circular wave sections',remaining=['ScreenOrientationMeasured derived for all proper orthochronous Lorentz maps with the chosen orientation conventions','Measurable patch changes and exceptional null sets under all Lorentz transformations','Strongly continuous unitary induced representation on cone L2, tied to already implemented boosts','Physical photon PCT/net identification, not just complex conjugation of sections'],cpu_seconds=sum(t['cpu_user_seconds']+t['cpu_kernel_seconds'] for t in attempts),wall_seconds=sum(t['wall_seconds'] for t in attempts),bench_hours=(now-datetime.fromisoformat(json.loads((D/'START.json').read_bytes())['at'])).total_seconds()/3600,opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),new_remote_calls=0,gate_changed=False)
save(D/'RESULTS.json',result)
text=f'''[REAL — 14 declarações no trio; OPEN — representação global de fóton e identificação PCT]

Abertura016SHA256: {result['opening_sha256']}

D1′ reaproveitou a C4. A conservação métrica do transporte real agora implica CᵀC=I na tela transversal. Acrescentar orientação det C=+1 determina C=[[a,b],[-b,a]], a²+b²=1; daí sai o caractere a+ib e sua composição, ligada ao cociclo concreto de C4. A conjugação troca o caractere e as seções circulares ±1. Não se usou um argumento real global da fase.

Duas fontes Lean aprovadas, 14 declarações auditadas, rc0, somente propext/Classical.choice/Quot.sound. Provas/logs/hashes em D1prime/RESULTS.json. Três ciclos no primeiro arquivo, um no segundo. Os dois erros iniciais eram normalizações explícitas do pareamento e comutação do produto complexo; preservados. CPU {result['cpu_seconds']:.6f}s; parede {result['wall_seconds']:.6f}s; bancada {result['bench_hours']:.6f}h, teto16h.

Controle complementar: {len(checks)} verificações CAS exatas. Uma reflexão preserva a métrica mas dá det C=-1 e falha como multiplicação pela mesma fase complexa. Logo a orientação não pode ser suprimida. CAS não é prova Lean do grupo inteiro.

GlobalHelicityInducedRepresentationMeasured continua NÃO PAGO, agora com a etapa O(2) e extração/composição do caractere pagas. Faltam: orientação induzida para todo Lorentz próprio ortócrono; cartas mensuráveis e exceções transportadas; ação Lorentz unitária fortemente contínua no L² do cone e restrição ao boost existente; identificação da conjugação/PCT física na rede. Não se inferiu a última da conjugação finita. A aceitação alternativa «teoremas ou lema nomeado» é atendida como MEDIDA parcial; nenhuma hipótese foi inserida como novo axioma.

As três chamadas remotas novas continuam aguardando resposta à autorização específica anteriormente solicitada. Nenhuma chamada falha/incerta foi repetida. Próximo D2′: tensor de Maxwell e controle forjado, com localidade operacional explicitada se aberta. Gate e originais intactos.
'''
write(OUT/'ENTREGA_016_D1prime_foton.md',text.encode())
q=OUT/'ENTREGA_016_PROGRESSO.md';write(q,q.read_bytes()+f'\n{now.isoformat()} — D1′ MEDIDA parcial:14 declarações, {len(checks)} controles CAS; representação global nomeada. Bancada{result["bench_hours"]:.6f}h, CPU{result["cpu_seconds"]:.6f}s. PróximoD2′. AberturaSHA256 {result["opening_sha256"]}.\n'.encode(),True)
q=R/'A7/CONTINUIDADE.json';c=json.loads(q.read_bytes());c.update(at=now.isoformat(),own_live_process=None,own_live_processes=[],D1prime_delivery=str(D/'RESULTS.json'),next='D2prime Maxwell StressTensorDataLocal_v2. D1prime local characters proved; global photon representation remains named. Three remote payloads still pending explicit egress approval, do not dispatch. B stays after Part D.');save(q,c,True)
print(json.dumps({k:result[k] for k in ['status','declarations','controls','bench_hours','cpu_seconds','wall_seconds']},ensure_ascii=False))
