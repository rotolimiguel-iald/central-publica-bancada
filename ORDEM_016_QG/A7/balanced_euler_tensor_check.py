"""Transport the actual ordered Euler/ghost tensor contractions, with no fitted weight."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,time
import sympy as s
from balanced_tensor_transport_engine import balanced_euler_line,Q
import euler_ghost_descendant_contact_engine as old
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=H/'balanced_euler_tensor'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    src=H/'euler_ghost_descendant_contact_engine.py'
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='ordered_descendant']
    ns=dict(vars(old));ns['euler_line_contact']=balanced_euler_line
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    sources=[Path(__file__),src,H/'balanced_tensor_transport_engine.py',H/'balanced_pair_normalization_v2/manifest.json',
        H/'euler_ghost_descendant_contact/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),method='Reuse identical tensor/Grassmann contraction function; substitute only explicitly derived balanced scalar Euler insertion.',
        no_fit=True,weights_unchanged=True,scope='Principal Euclidean ordered Euler/current graph, not full A2',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    start=time.process_time();checks=[]
    def eq(label,a,b=0):assert s.expand(a-b)==0,(label,a,b);checks.append(label)
    lam=(1,-1,0,0);eta=(1,0,0,0);L=tuple(a+b for a,b in zip(lam,eta))
    a,count1=ns['ordered_descendant'](lam,eta);b,count2=ns['ordered_descendant'](eta,lam)
    da=old.weighted_defect(a,L);db=old.weighted_defect(b,L)
    # This parity is about two odd ghost fields, not antisymmetrizing two even inputs.
    adj=lambda M:M.T.applyfunc(lambda f:s.expand(f.subs({Q[i]:-Q[i]-L[i] for i in range(4)},simultaneous=True)))
    for k,v in enumerate((da+adj(da))):eq('first graded adjoint '+str(k),v)
    for k,v in enumerate((db+adj(db))):eq('second graded adjoint '+str(k),v)
    olddata=json.loads((H/'euler_ghost_descendant_contact/results.json').read_bytes())
    symbols={str(q):q for q in Q};symbols['tau']=old.TAU
    parse=lambda rows:s.Matrix([[s.sympify(t,locals=symbols) for t in row] for row in rows])
    olda=parse(olddata['B']).subs(old.TAU,1)
    oldb=parse(olddata['reverse_B']).subs(old.TAU,1)
    rows=[]
    for i in range(4):
        for j in range(4):
            maps=[dict(s.Poly(s.expand(m[i,j]),*Q).terms()) for m in [olda,oldb,a,b]]
            for p in set().union(*(m.keys() for m in maps)):
                row=[m.get(p,0) for m in maps]
                if any(row):rows.append(row)
    ranks=dict(old=s.Matrix(rows)[:,:2].rank(),augmented=s.Matrix(rows).rank())
    eq('Euler trace normalization',balanced_euler_line((),()),3*sum(q*q for q in Q)/32)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        lambda_x=lam,eta_y=eta,contractions=[count1,count2],
        B=[[str(v) for v in row] for row in a.tolist()],reverse_B=[[str(v) for v in row] for row in b.tolist()],
        weighted_antisymmetric_part=[[str(v) for v in row] for row in da.tolist()],
        reverse_weighted_antisymmetric_part=[[str(v) for v in row] for row in db.tolist()],
        old_and_balanced_span_ranks=ranks,nonzero=[sum(v!=0 for v in m) for m in [a,b,da,db]],
        full_Q2=False,raw_other_diagrams_combined=False,normalization_fitted=False,gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — contato composto Euler/ghost na prescrição balanceada; Q2 completa OPEN]

Reutilizada literalmente a função ordered_descendant do motor anterior, com
os mesmos vértices, duas contrações Grassmann e fatores de adjunção. Somente
o contato escalar mudou para soma_i DeltaR_(u+ii,v), declarado antes da conta.
O termo livre soma_i f_(u+ii) vale zero fora da diagonal; sua extensão composta
balanceada não é fixada por essa igualdade pontual. Ela não foi escolhida para
cancelar o resíduo Ward. Não se escolheu tau nem novo peso global.

Foram calculados os16 componentes em cada ordem de cutoffs lambda={lam},eta={eta},
com {count1}/{count2} contrações. Não nulos B,Brev,defeito,defeito-rev: {result['nonzero']}.
Rangos das colunas dos dois antigos kernels e dos dois novos: {ranks}.
O teste compara os contatos, não procura coeficientes para ajustar o resultado.
A antissimetria graduada verificada é entre os DOIS CAMPOS GHOST ímpares;
ela não é antissimetrização das duas entradas pares F,G da identidade A2.
{len(checks)} controles, CPU{result['cpu_seconds']}s, rc0.

Os demais diagramas ainda precisam ser convertidos à mesma prescrição.
Não somamos esses valores aos coeficientes R_raw como se fossem da mesma família.
Não prova anulação de A2 nem constrói a extensão curva causal completa.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_Euler_tensor_balanceado.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_EULER_TENSOR_TRANSPORT',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b: Euler tensor balanceado32componentes, {len(checks)}controles CPU{result['cpu_seconds']}s. Outrosdiagramas não misturados; Q2OPEN. AberturaSHA256={opening}.\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ['B','reverse_B','weighted_antisymmetric_part','reverse_weighted_antisymmetric_part']}),flush=True)

if __name__=='__main__':main()
