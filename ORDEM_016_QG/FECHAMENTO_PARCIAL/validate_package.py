"""Independent consistency checks on assembled delivery; never edits the package."""
from pathlib import Path
import json,hashlib,re,ast,sys,importlib.util
S=Path(__file__).resolve().parent
P=S.parent.parent/'TUNEL/DO_CHATGPT/FECHAMENTO_PARCIAL_016'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p1=read(P/'P1_QUADRO.json');p2=read(P/'P2_COMPILACAO.json');checks=[]
    def check(n,v):
        checks.append(dict(name=n,passed=bool(v)))
        if not v:raise AssertionError(n)
    expected={f'A{i}' for i in range(9)}|{f'C{i}' for i in range(1,7)}|{'D1prime','D2prime','D3prime','D4','D5','D6','D1','D2','D3'}
    check('all_24_items_no_duplicates',{x['item'] for x in p1['items']}==expected and len(p1['items'])==24)
    check('all_MEDIDA_named',all(x['named_open_hypotheses'] for x in p1['items'] if x['status']=='MEDIDA'))
    check('cancelled_old_D',all(x['status']=='CANCELADO' for x in p1['items'] if x['item'] in ('D1','D2','D3')))
    aggregate=next(x for x in p2['units'] if x['item']=='P2')
    check('joint_receipt_real',read(P/aggregate['receipt'])['rc']==0)
    census={ln.split('\t')[1] for ln in (P/'evidencias/kernel_census_01.log').read_text('utf-8').splitlines() if ln.startswith('KERNEL_DECL\t')}
    own={}
    all_audited_names={n for u in p2['units'] for n in u['axioms']}
    for u in p2['units']:
        check(u['module']+':rc',u['rc']==0)
        r=read(P/u['receipt'])
        check(u['module']+':source_pin',r['source_sha256']==sha(P/u['source']))
        check(u['module']+':log_pin',r['log_sha256']==sha(P/u['log']))
        for kind in ('source','log','receipt'):check(u['module']+':'+kind,sha(P/u[kind])==u[kind+'_sha256'])
        actual={}
        for line in (P/u['log']).read_text('utf-8').splitlines():
            if line.startswith('BENCH_DECL\t'):
                _,n,k,axs=line.split('\t');actual[n]=list(filter(None,axs.split(',')))
                check(n+':not_axiom',k!='axiom')
        check(u['module']+':axioms_exact',actual==u['axioms'])
        check(u['module']+':trio',all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in actual.values()))
        for n in actual:
            m=re.match(r'^(.*)\.eq_[0-9]+$',n)
            generated=bool(m and (m[1] in census or m[1] in all_audited_names))
            check(n+':unique_or_imported_equation',n not in own or generated)
            own[n]=u['module']
        check(u['module']+':audited_count',u['audited_declaration_count']==len(actual))
    # All active imports are earlier in the reproduction list.
    order=p2['reproduction_order'];done=set();names=set(order)
    for n in order:
        text=(P/'lean'/(n+'.lean')).read_text('utf-8')
        local=set(re.findall(r'^import (\S+)\s*$',text,re.M))&names
        check(n+':dependency_order',local<=done);done.add(n)
    clauses=read(P/'P3_CLAUSULAS.json');canonical=P/'kernel_v371/TGLExt/ContratoQG_v31.lean';t=canonical.read_text('utf-8')
    for name in ('ContratoH2','ContratoH3','ContratoImportH3'):
        tail=t[t.index('structure '+name):];end=re.search(r'\n(?:structure |def |theorem |namespace |end |/-!)',tail)
        block=tail[:end.start()] if end else tail
        fields=re.findall(r'^  ([^ /\n:]+)\s*(?:\([^\n]*\))?\s*:',block,re.M)
        check(name+':all_clauses',fields==[x['field'] for x in clauses if x['contract']==name])
    check('clauses_source_pin',all(x['canonical_source_sha256']==sha(canonical) for x in clauses))
    for n in ('PROPOSTA_RUNTIME.py','reproduzir.py','run_lean.py'):ast.parse((P/n).read_text('utf-8'))
    check('P4_no_gate',read(P/'P4_PREVISAO.json')['gate_changed'] is False)
    check('P9_resumption',read(P/'P9_PARTE_B.json')['resume']=='T11')
    for p in P.rglob('*'):
        if p.is_file():check('privacy:'+p.name,p.name not in ('iald_stack_v7.py','iald_psion_state.json','.env'))
    result=dict(checks_count=len(checks),passed=True,active_own_declarations=len(own),gate_changed=False)
    output=S/('PACKAGE_VALIDATION_SEALED.json' if (P/'PRONTO.json').exists() else 'PACKAGE_VALIDATION_PRESEAL.json')
    if output.exists():raise FileExistsError(output)
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
if __name__=='__main__':main()
