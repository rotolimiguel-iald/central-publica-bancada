"""Compare already computed contacts only after putting them in one external-jet convention."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from full_loop_extension_engine import Q
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'euler_subtotal_placement_audit'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'balanced_current_source/results.json',
        H/'balanced_cubic_euler_contact/results.json',H/'balanced_euler_metric_vertex/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        question='Can the converted subtotal already equal either fixed-sign sum of the three raw Euler graphs?',
        meaning='A placement diagnostic, not a choice of Ward coefficient; both signs retained if neither identity holds',
        mapping='Subtotal A(q) with both cutoff multipliers at Y becomes A(D+lambda+eta) acting on c. New Euler matrices already act on c with h to the left.',
        tests='Each order and symmetric mean; plus/minus unit coefficients only. No fitting or claim of complete A2.',
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();loc={str(q):q for q in Q};parse=lambda f:s.sympify(f,locals=loc)
    mat=lambda rows:s.Matrix([[parse(v) for v in row] for row in rows]);L=(2,-1,0,0)
    subtotals=[];graphs=[];checks=[];details=[]
    for order in range(2):
        S=s.zeros(10,4)
        for a in range(10):
            for r in range(4):
                p=H/f'balanced_current_source/component_{order}_{a}_{r}.json'
                row=json.loads(p.read_bytes());paths.append(p)
                S[a,r]=parse(row['converted_subtotal']).subs({Q[i]:Q[i]+L[i] for i in range(4)},simultaneous=True)
                checks.append('common right-acting external basis '+str((order,a,r)))
        ghfile=H/f'balanced_cubic_euler_contact/order_{order}.json'
        metfile=H/f'balanced_euler_metric_vertex/order_{order}.json';paths.extend([ghfile,metfile])
        gh=json.loads(ghfile.read_bytes());met=json.loads(metfile.read_bytes())
        E=mat(gh['total'])+mat(met['matrix'])
        subtotals.append(S.applyfunc(s.expand));graphs.append(E.applyfunc(s.expand))
    for label,S,E in [('order0',subtotals[0],graphs[0]),('order1',subtotals[1],graphs[1]),
                      ('symmetric_mean',(subtotals[0]+subtotals[1])/2,(graphs[0]+graphs[1])/2)]:
        row=dict(label=label)
        for sign in [1,-1]:
            residual=(S-sign*E).applyfunc(s.expand)
            nonzero=[(i,j) for i in range(10) for j in range(4) if residual[i,j]!=0]
            value=None
            if nonzero:
                i,j=nonzero[0];expr=residual[i,j]
                value=dict(row=i,column=j,expression=str(expr),
                    value_at_1234=str(expr.subs(dict(zip(Q,[1,2,3,4])))))
            row[str(sign)]=dict(nonzero=len(nonzero),witness=value)
            put(D/f'{label}_sign_{sign}.json',dict(residual=[[str(v) for v in r] for r in residual.tolist()],**row[str(sign)]))
        details.append(row)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        comparisons=details,fitted_coefficients=False,combined=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    counts=[dict(label=r['label'],plus=r['1']['nonzero'],minus=r['-1']['nonzero']) for r in details]
    note=f'''[DERIVED+CAS — comparação de posicionamento dos contatos, sem nova soma adotada]

Convertidos os dois conjuntos à mesma convenção: h à esquerda, polinômio
de derivadas agindo sobre c à direita. O subtotal anterior escreve suas
derivadas de delta com ambos os cutoffs em Y; por isso A(q) vira
A(D+lambda+eta). Os grafos Euler novos já estavam nessa forma, incluindo
a adjunção da apresentação c_X,h_Y. Comparar sem essa tradução seria erro.

Comparada a soma dos três grafos Euler cúbicos com o subtotal convertido,
com coeficientes fixos +1 e -1, separadamente e na média simétrica.
Contagens de diferenças não nulas (40 componentes por comparação): {counts}.
As diferenças e testemunhas racionais estão nos arquivos; nenhum peso
foi ajustado para forçar uma igualdade. Igualdade de valores, se presente,
também não dispensaria o dicionário entre Tc2 e a representação efetiva.

Esse controle determina se uma identificação imediata já é possível; não
autoriza adicionar os grafos ao subtotal nem descartar uma contribuição.
A origem precisa ser rastreada em qTc2-Tc2(qV,V)-Tc2(V,qV)-(V,V), com
as correções de aridade1 no mesmo esquema. A família curva segue OPEN.
{len(checks)} conversões exatas, CPU{result['cpu_seconds']}s,rc0.
Nenhum original/gate alterado. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_posicionamento_Euler_subtotal.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']+sorted(D.glob('*_sign_*.json'))]))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='EULER_SUBTOTAL_PLACEMENT_DIAGNOSTIC',
        checks=len(checks),cpu_seconds=result['cpu_seconds'],target='A7.b',remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: comparação Euler/subtotal na mesma base de jatos: {counts}; nenhum peso/soma escolhido. {len(checks)}conversões CPU{result["cpu_seconds"]}s. Q2OPEN;aberturaSHA256={opening}.\n')
    print(json.dumps(dict(checks=len(checks),cpu_seconds=result['cpu_seconds'],comparisons=counts)),flush=True)

if __name__=='__main__':main()
