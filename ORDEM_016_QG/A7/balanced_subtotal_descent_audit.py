"""Audit the converted subtotal and compare two known Euler descendants, without fitting."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from full_loop_extension_engine import Q
from euler_ghost_descendant_contact_engine import weighted_defect
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append
D=H/'balanced_subtotal_descent_audit'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[H/'balanced_current_source/results.json',H/'balanced_euler_tensor/results.json',
           H/'balanced_pair_tensor/results.json',Path(__file__)]
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),question='Do the two already computed balanced Euler descendants span the graded defect of the converted subtotal? Compare only; no Ward weight fitted.',
        required_check='Recompute pair/source free-BRST square and localized current contribution separately',
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();checks=[];loc={str(q):q for q in Q}
    parse=lambda t:s.sympify(t,locals=loc)
    mat=lambda x:s.Matrix([[parse(v) for v in row] for row in x])
    e=json.loads(paths[1].read_bytes());L=(2,-1,0,0)
    gen=[mat(e['weighted_antisymmetric_part']),mat(e['reverse_weighted_antisymmetric_part'])]
    report=json.loads(paths[0].read_bytes());target=mat(report['polarized_graded_defect'])
    matrices={key:[] for key in ['pair','source','currents','old','converted']}
    for order in range(2):
        blocks={key:s.zeros(4) for key in matrices}
        for p in sorted((H/'balanced_current_source').glob(f'component_{order}_*.json')):
            row=json.loads(p.read_bytes());i,j=row['h'];r=row['c']
            parts={k:parse(v) for k,v in row['delta_parts'].items()}
            values=dict(pair=parts['pair'],source=parts['source'],
                currents=sum(parts[k] for k in ['Ymetric','Ymixed','Yghost','Xmetric','Xmixed']),
                old=parse(row['raw_subtotal']),converted=parse(row['converted_subtotal']))
            assert s.expand(sum(values[k] for k in ['old','pair','source','currents'])-values['converted'])==0
            checks.append('component normalization sum')
            for key,f in values.items():
                f=f.subs({Q[k]:Q[k]+L[k] for k in range(4)},simultaneous=True)
                blocks[key][j,r]-=(Q[i]+L[i])*f;blocks[key][i,r]-=(Q[j]+L[j])*f
        for key in matrices:matrices[key].append(blocks[key].applyfunc(s.expand))
    defect={k:weighted_defect((ms[0]+ms[1])/2,L) for k,ms in matrices.items()}
    for name in ['pair','source']:
        for v in defect[name]:assert v==0,(name,v);checks.append(name+' free-BRST square')
    for v in (defect['converted']-target).applyfunc(s.expand):assert v==0;checks.append('independent descent assembly')
    for v in (defect['old']+defect['currents']-target).applyfunc(s.expand):assert v==0;checks.append('only current normalization changes the defect')
    coeffs=[];labels=[]
    for i in range(4):
        for j in range(4):
            ms=[dict(s.Poly(s.expand(m[i,j]),*Q).terms()) for m in gen+[target]]
            for mon in sorted(set().union(*(m.keys() for m in ms)),reverse=True):
                row=[m.get(mon,0) for m in ms]
                if any(row):coeffs.append(row);labels.append(dict(entry=[i,j],powers=mon))
    M=s.Matrix(coeffs);r0=M[:,:2].rank();r1=M.rank();witness=[];det=None
    if r0==2 and r1==3:
        piv=M.T.rref()[1];W=M[list(piv),:];det=W.det();assert det!=0;checks.append('nonzero rank witness')
        witness=[dict(**labels[k],coefficients=list(map(str,coeffs[k]))) for k in piv]
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        generator_rank=r0,augmented_rank=r1,coefficient_rows=len(coeffs),in_span=r0==r1,
        witness=witness,determinant=str(det),pair_and_source_square_zero=True,
        current_change_accounts_for_entire_defect_change=True,weights_fitted=False,full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — localização da diferença e teste restrito de span; Q2 completa OPEN]

Após a conversão dos sete blocos, o quadrado BV livre das mudanças do par
ordinário E da fonte é zero em todas as16 componentes, separadamente.
Logo toda a mudança do defeito medido vem da normalização das cinco
correntes. A soma foi reconstruída diretamente dos80arquivos componentes.
Isso localiza o próximo cálculo; não atribui uma classe de obstrução à TGL.

Comparando os dois descendentes Euler balanceados já calculados com esse
defeito convertido, os postos são{r0} e{r1}; linhas de coeficientes{len(coeffs)}.
Pertencimento ao span: {r0==r1}. Menor testemunha: {det}.
O teste não escolhe pesos nem constitui a identidade A2 inteira. Se o span
não contém o defeito, somar só esses dois kernels com constantes não basta;
faltam comparar os demais termos da identidade inhomogênea na mesma família.
Não se promove uma falha de subtotal a impossibilidade de renormalização.

{len(checks)} verificações, CPU{result['cpu_seconds']}s, rc0.
Nenhuma nova chamada remota ou alteração canônica/gate.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_descida_balanceada_localizada.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_DESCENT_SCOPE_AUDIT',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b: mudança de defeito localizada nas5correntes;spanEuler{r0}->{r1};{len(checks)}controles CPU{result['cpu_seconds']}s.Q2OPEN.AberturaSHA256={opening}.\n")
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
