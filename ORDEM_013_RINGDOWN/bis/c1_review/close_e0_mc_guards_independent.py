"""Read-only negative/algebra checks; no Monte Carlo, no production imports."""
import os
os.environ.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
import ast, copy, hashlib, importlib.util, json, sys, types
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
B = Path(__file__).resolve().parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok, msg):
    if not ok: raise ValueError(msg)
def new(p, data):
    with p.open('xb') as f: f.write(data)
guard = B/'refeito/e0_mc_guarded_013bis.py'
spec = importlib.util.spec_from_file_location('guard_review', guard)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
d = json.loads((B/'bis/E0_ROUTE_IV_POWER_v2.json').read_bytes())
p = json.loads((B/'bis/E0_ROUTE_IV_PROVENANCE.json').read_bytes())
c = json.loads((B/'bis/E0_MC_GUARD_CLOSURE.json').read_bytes())
pins = {n:sha(B/n) for n in p['files']}
require(all(pins[n] == h['sha256'] and (B/n).stat().st_size == h['bytes'] for n,h in p['files'].items()), 'frozen provenance changed')
for field,path in [('original_provenance_sha256','bis/E0_ROUTE_IV_PROVENANCE.json'),('new_guard_code_sha256','refeito/e0_mc_guarded_013bis.py'),('test_code_sha256','refeito/test_e0_mc_guards_013bis.py')]:
    require(c[field] == sha(B/path), field)
rows,sel=d['per_event'],p['selected_events']; passed=[]
def reject(name,fn):
    try: fn()
    except ValueError: passed.append(name)
    else: raise RuntimeError('accepted '+name)
def forbidden(): raise RuntimeError('production delegation during negative test')
m.implementation = forbidden
reject('unknown member',lambda:m.validate_population(rows,sel[:-1]+['UNKNOWN_EVENT']))
reject('duplicate member',lambda:m.validate_population(rows,sel[:-1]+[sel[0]]))
bad=copy.deepcopy(rows);bad[0]['sigma_df']=float('nan')
reject('NaN width',lambda:m.validate_population(bad,sel))
reject('NaN statistic',lambda:m.lrt([[2]],[[float('nan')]],[[1]],[1]))
reject('inconsistent sums',lambda:m.lrt([[2]],[[4]],[[1]],[1]))
reject('empty class nonzero',lambda:m.lrt([[0,2]],[[1,0]],[[1,1]],[1,1]))
reject('NaN before counting',lambda:m.count_above([float('nan')]))
reject('invalid N',lambda:m.sufficient(0,[1],0,1,1))
reject('invalid variance',lambda:m.sufficient(2,[0],0,1,1))
require(passed == c['negative_tests'], 'negative inventory')
pops=m.frozen_populations();require(pops==c['populations'],'frozen populations')
lookup={r['event']:r for r in rows}
require([lookup[e]['sigma_df'] for e in sel] == p['selected_sigma_df'], 'selected widths')
for pop in pops.values(): require(abs(sum(pop['probabilities'])-1)<1e-14,'probability sum')
source=B/'refeito/e0_route_iv_power_013bis_v2.py'
require(sha(source)==d['code_sha256'],'algebra source')
tree=ast.parse(source.read_text(encoding='utf-8-sig'))
ns={'np':np}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('ll','lrt')],type_ignores=[]),str(source),'exec',optimize=1),ns)
m.implementation=lambda:types.SimpleNamespace(lrt=ns['lrt'])
t,q=m.lrt([[3]],[[0]],[[1]],[1]);require(t.tolist()==[0.] and q.tolist()==[0.] and m.count_above(t)==0,'analytic null')
for output in [(np.array([np.nan]),np.array([0.])),(np.array([0.]),np.array([np.inf]))]:
    m.implementation=lambda:types.SimpleNamespace(lrt=lambda *a:output)
    reject('nonfinite delegate output '+str(len(passed)),lambda:m.lrt([[3]],[[0]],[[1]],[1]))
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_CURRENT_CUSTODY_AND_POSTHOC_GUARDS','optimize':sys.flags.optimize,'negative_tests':passed,'frozen_file_hashes':pins,'populations':pops,'receipt_sha256':sha(B/'bis/E0_MC_GUARD_CLOSURE.json'),'code_sha256':sha(Path(__file__)),'scope':'Nine original pre-delegation negatives and two output negatives. Pure ll/lrt AST positive control only; no MC, posterior access, full builder import or production writes. Posthoc custody, not retrospective preregistration.'}
new(B/'bis/c1_review/e0_mc_guard_closing_results.json',(json.dumps(result,indent=2,allow_nan=False)+'\n').encode())
new(B/'bis/E0_MC_GUARD_CLOSING_REVIEW.md',('# E0 — fechamento independente das guardas MC\n\n[REAL — controles leves sob Python −O; congelamento POSTHOC]\n\nR1 e R2 fechados no escopo de custódia corrente e reutilização pelo módulo novo. Conferidos os 11 arquivos do recibo por bytes/SHA256, os três cross-hashes de fechamento e as populações explícitas de 1, 31 e 33 entradas, com larguras e probabilidades. Reproduzidas as nove recusas originais antes de qualquer delegação; mais duas recusas de saída não finita e um controle nulo algébrico passaram. Guardas por exceção permanecem ativas sob −O.\n\nO módulo antigo não foi modificado: chamadas futuras devem passar por `e0_mc_guarded_013bis.py`. O congelamento é posterior aos resultados; não torna a busca pré-registrada nem repete MC. Os valores científicos e os limites do parecer anterior permanecem. A implementação pura ll/lrt foi extraída por AST para o controle positivo; nenhum builder científico foi importado.\n\nRecibo independente: `bis/c1_review/e0_mc_guard_closing_results.json`; código: `bis/c1_review/close_e0_mc_guards_independent.py`. O recibo principal de sistemáticas, com 2388 comparações, é revisão distinta do agente principal e não trabalho numérico desta revisão. Nenhuma produção alterada.\n').encode())
old=B/'bis/E0_RATE_O5_INDEPENDENT_REVIEW.md'; target=B/'bis/E0_RATE_O5_REVIEW.md'
if not target.exists():
    add='\n## Adendo documental — adoção e selo\n\nO texto acima é preservado da revisão independente anterior (SHA256 '+sha(old)+'). A referência histórica a aguardar revisão do critério foi superada pela ordem expressa do usuário: [INPUT] SNR de rede GWOSC ≥12, mediana Mf_det ≥40 M☉, 0≤mediana chi_f<0,98; prioridade SNR≥30. Ausências permanecem AWAITING_GR_METADATA. Não é corte por largura de posterior nem estimativa de eficiência de seleção. E0 foi depois declarado selado pelo agente principal; a nova frente E1 não executa E2/E3.\n'
    new(target,old.read_bytes()+add.encode())
print(json.dumps({'negative_tests':len(passed),'populations':{k:len(v['events']) for k,v in pops.items()},'status':result['status']}))
