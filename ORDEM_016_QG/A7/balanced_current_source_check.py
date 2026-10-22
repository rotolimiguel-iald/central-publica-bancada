"""Convert the previously measured full local subtotal, preserving its limited status."""
from pathlib import Path
from datetime import datetime,timezone
import json,time,gc
import sympy as s
from balanced_current_source_engine import all_currents,source_delta,Q,formal_source_coefficients
from balanced_tensor_transport_engine import realize
from localized_source_boundary_engine import source_coefficients
from position_metric_bubble_engine import LABELS
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,put,write,append
D=H/'balanced_current_source'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    sources=[Path(__file__),H/'balanced_current_source_engine.py',H/'balanced_pair_normalization_v2/manifest.json',
        H/'balanced_pair_tensor/PRE_REGISTER.json',H/'full_current_contact_matrix/results.json',
        H/'full_current_contact_matrix_swapped/results.json',H/'balanced_euler_tensor/results.json']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),target='Actual five current and source normalization changes; add only to explicitly matching ordinary-pair change and raw subtotal.',
        scope='Converts a previously measured subtotal, NOT full A2, no curved/arity1 terms supplied by fiat',
        stop_on_nonzero=False,no_fit=True,sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    start=time.process_time();checks=[];rows=[];matrices=[]
    loc={str(q):q for q in Q};parse=lambda v:s.sympify(v,locals=loc)
    for order,filename in enumerate(['full_current_contact_matrix/results.json','full_current_contact_matrix_swapped/results.json']):
        raw=json.loads((H/filename).read_bytes());lam=tuple(raw['lambda_x']);eta=tuple(raw['eta_y']);L=tuple(a+b for a,b in zip(lam,eta))
        sources_delta={r:source_delta(r,lam,eta) for r in range(4)}
        for r in range(4):
            fs=formal_source_coefficients(0,r,r,eta);rs=source_coefficients(0,r,r,eta)
            for a,b in [(fs[0],rs[0])]+list(zip(fs[1],rs[1])):
                assert s.expand(realize(a)-b)==0;checks.append('source formal realization')
        A={}
        for a,(i,j) in enumerate(LABELS):
            for r in range(4):
                pairfile=H/f'balanced_pair_tensor/component_{order}_{a}_{r}.json'
                assert pairfile.exists(),pairfile
                pair=json.loads(pairfile.read_bytes());assert tuple(pair['lambda_x'])==lam and tuple(pair['eta_y'])==eta
                cur=all_currents(a,r,lam,eta)
                cur['source']=(1 if i==j else 2)*sources_delta[r][i,j]
                cur['pair']=parse(pair['weighted_delta'])
                original=next(x for x in raw['rows'] if x['a']==a and x['c']==r)
                delta=s.expand(sum(cur.values()));value=s.expand(parse(original['polynomial'])+delta)
                A[a,r]=value
                rec=dict(order=order,a=a,h=[i,j],c=r,delta_parts={k:str(v) for k,v in cur.items()},
                    raw_subtotal=original['polynomial'],converted_subtotal=str(value),pair_file_sha256=sha(pairfile),cpu_seconds=time.process_time()-start)
                put(D/f'component_{order}_{a}_{r}.json',rec);rows.append(rec)
                print(json.dumps(dict(order=order,h=[i,j],c=r,cpu_seconds=rec['cpu_seconds'])),flush=True)
            gc.collect()
        B=s.zeros(4)
        for a,(i,j) in enumerate(LABELS):
            for r in range(4):
                f=A[a,r].subs({Q[k]:Q[k]+L[k] for k in range(4)},simultaneous=True)
                B[j,r]-=(Q[i]+L[i])*f;B[i,r]-=(Q[j]+L[j])*f
        matrices.append(B.applyfunc(s.expand))
    L=(2,-1,0,0);adj=lambda M:M.T.applyfunc(lambda f:s.expand(f.subs({Q[k]:-Q[k]-L[k] for k in range(4)},simultaneous=True)))
    pol=(matrices[0]+matrices[1])/2;defect=(pol-adj(pol)).applyfunc(s.expand)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),rows=len(rows),cpu_seconds=time.process_time()-start,
        nonzero_subtotal_components=sum(parse(x['converted_subtotal'])!=0 for x in rows),
        polarized_graded_defect=[[str(v) for v in row] for row in defect.tolist()],nonzero_defect_components=sum(v!=0 for v in defect),
        full_Q2=False,curved_completion=False,normalization_fitted=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — conversão de todos os sete blocos do subtotal principal; não é A2 completa]

Transportados para a prescrição balanceada os cinco blocos de corrente,
o bloco de fonte e o par métrico/ghost. Cada variação foi calculada antes
de colapsar as palavras de derivadas das duas linhas; derivadas externas
e cutoffs foram aplicados depois da extensão. Os coeficientes R_raw antigos
permanecem como referência: subtotal convertido=subtotal antigo+mudança dos
sete blocos. Nenhum coeficiente foi ajustado para cancelar o resultado.

80 componentes nas duas ordens de cutoffs, controles de fonte{len(checks)},
CPU{result['cpu_seconds']}s. Subtotal convertido não nulo em
{result['nonzero_subtotal_components']} componentes; defeito graduado polarizado
não nulo em{result['nonzero_defect_components']}/16. Os números corrigem a frase.

Isso transporta O SUBTOTAL que já estava medido, cujo alcance nunca foi A2
completa. Os contatos compostos Euler têm cálculo separado na mesma
prescrição; a ponderação da identidade conectada Tc2, aridade1 e termos
curvos não são substituídos por este subtotal. Não se declara anomalia
cohomológica, cancelamento completo nem gate novo.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_subtotal_balanceado_completo.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+[D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']+sorted(D.glob('component_*.json'))],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_CURRENT_SOURCE_TRANSPORT',target='A7.b',checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f"\n{now.isoformat()} A7.b: subtotal7blocos convertido R_bal,80componentes,defeito nãozero{result['nonzero_defect_components']};CPU{result['cpu_seconds']}s.Q2OPEN.AberturaSHA256={opening}.\n")
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
