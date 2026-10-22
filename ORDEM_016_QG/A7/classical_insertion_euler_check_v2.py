"""Calculate the previously missing classical two-input Euler insertion pieces."""
from pathlib import Path
from datetime import datetime,timezone
import json,time
import sympy as s
from classical_insertion_euler_engine import calculate,build_terms,odd_pair_sign,Q
from euler_ghost_descendant_contact_engine import weighted_defect
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

D=H/'classical_insertion_euler_v2'

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc)
    paths=[Path(__file__),H/'classical_insertion_euler_check.py',H/'classical_insertion_euler_run.log',H/'classical_insertion_euler_engine.py',H/'balanced_euler_tensor/results.json',
        H/'balanced_current_source/results.json',H/'temporal_known_arity_one_terms/results.json',
        H/'classical_current_insertion_delivery/DERIVACAO.md']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        previous_failure='v1 stopped before graphs: handwritten expected signs were reversed. Pairing engine unchanged; v2 validates it using independent Grassmann derivatives.',
        target='Actual internal Euler contractions in a2(q0Vchi,Veta)+a2(q0Veta,Vchi), principal flat metric/ghost sector',
        inventory=['-E_h[G,chi]w with Vghost, already calculated',
            'qVaf_eta Euler part with q0Vchi field currents: metric,mixed,ghost'],
        weights='No fit: Iaf=-hdag[G,chi]w. For odd I, a2(I,V) has minus T2(I,qV), which becomes plus T2(qV,I) after swapping two odd factors.',
        temporal_order='Two ordered even-input placements contribute to a2(Vchi,Veta); previous symmetric_mean is half that sum.',
        expected_identity='q0(2*previous_symmetric_mean) = weighted_defect(field_current_Euler_sum - previous_Eh_commutator_sum)',
        scope='Finite cutoff jets and principal flat terms only; no complete curved causal family asserted',
        no_fit=True,stop_on_nonzero=False,
        sources=[dict(path=str(p),sha256=sha(p)) for p in paths]))
    start=time.process_time();checks=[];lam=(1,-1,0,0);eta=(1,0,0,0);L=(2,-1,0,0)
    # Six ordered odd factors: all four Wick matchings retained.
    signs=[odd_pair_sign([(0,4+y),(1+x,3)]) for x in range(2) for y in range(2)]
    assert signs==[1,-1,-1,1],signs;checks.append('four ghost Euler Wick signs')
    # Independent composition of left Grassmann derivatives on the ordered monomial.
    def left_derivative(poly,index):
        out={}
        for word,value in poly.items():
            if index in word:
                place=word.index(index);key=word[:place]+word[place+1:]
                out[key]=out.get(key,0)+(-1)**place*value
        return out
    for x in range(2):
        for y in range(2):
            poly={(0,1,2,3,4,5):1}
            for a,b in [(0,4+y),(1+x,3)]:
                poly=left_derivative(left_derivative(poly,a),b)
            assert list(poly.values())==[signs[2*x+y]]
            checks.append('independent left derivative Wick sign')

    assert all(not v for v in build_terms((0,0,0,0)).values());checks.append('all classical currents vanish for constant chi')
    data=[];matrices=[]
    for order,(left,right) in enumerate([(lam,eta),(eta,lam)]):
        parts,counts=calculate(left,right);total=sum(parts.values(),s.zeros(4)).applyfunc(s.expand)
        for value in total:
            assert not value.has(s.Float);checks.append('exact classical insertion coefficient')
        row=dict(order=order,lambda_Vaf=left,eta_I=right,terms=counts,
            parts={k:[[str(v) for v in r] for r in m.tolist()] for k,m in parts.items()},
            total=[[str(v) for v in r] for r in total.tolist()])
        put(D/f'order_{order}.json',row);data.append({k:v for k,v in row.items() if k not in ['parts','total']});matrices.append(total)
        print(json.dumps(dict(order=order,terms=counts,cpu_seconds=time.process_time()-start)),flush=True)
    loc={str(q):q for q in Q};mat=lambda rows:s.Matrix([[s.sympify(v,locals=loc) for v in row] for row in rows])
    old=json.loads((H/'balanced_euler_tensor/results.json').read_bytes())
    desc=mat(old['B'])+mat(old['reverse_B'])
    rhs=weighted_defect(matrices[0]+matrices[1]-desc,L)
    lhs=2*mat(json.loads((H/'balanced_current_source/results.json').read_bytes())['polarized_graded_defect'])
    residual=(lhs-rhs).applyfunc(s.expand)
    result=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        orders=data,wick_signs=signs,
        lhs=[[str(v) for v in r] for r in lhs.tolist()],rhs=[[str(v) for v in r] for r in rhs.tolist()],
        residual=[[str(v) for v in r] for r in residual.tolist()],nonzero_residual=sum(v!=0 for v in residual),
        coefficient_two_derived_before_comparison=True,weights_fitted=False,
        full_Q2=False,curved_completion=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — inserções clássicas de duas entradas, setor principal plano]

O termo a2(q0Vchi,Veta) não é somente o descendente com
Iaf=-hdag[G,chi]w já calculado. Vaf_eta também encontra a PARTE DE CAMPOS
de q0Vchi. Foram calculados esses três canais adicionais: corrente
métrica hh c, corrente mista b h c e corrente ghost barc c c.
O canal ghost conserva quatro emparelhamentos, com sinais{signs}.

Usam-se exatamente os vértices, correntes e R_bal anteriores.
I_metric=+dchi.Jraw/(16kappa), uma linha métrica -4kappa S e uma
linha Euler box f Id dão o fator-Jraw*S/4. O fator1/2 da Hessiana
interna é removido pelos dois emparelhamentos. No canal misto,
E_h--b=0 e E_h--h=box f Id; a segunda linha é h--b=Gf.

Os sinais da entrada ímpar são retidos: a2(I,V) contém -T2(I,qV),
que vira +T2(qV,I) ao trocar os dois fatores ímpares. A parte Iaf
contribui com menos o descendente Euler anterior. Nenhum peso foi
selecionado após conhecer a soma. O a2 de entradas pares tem DUAS
colocações ordenadas; a média simétrica anterior é metade dessa soma.

Comparação predefinida:
 q0(2*subtotal_simetrizado)
 contra o defeito graduado da soma dos novos contatos menos os
 dois descendentes Euler anteriores.
Diferenças não nulas: {result['nonzero_residual']}/16.

Todas as matrizes foram preservadas. Este controle de jatos de cutoff
não substitui uma identidade universal nem os termos curvos/escalares.
Se houver diferença, ela permanece como diagnóstico, sem trocar fatores.
{len(checks)} controles, CPU{result['cpu_seconds']}s,rc0.
Originais/gate intactos. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_insercoes_classicas_Euler_v2.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths+
        [D/'PRE_REGISTER.json',D/'results.json',D/'DERIVACAO.md']+sorted(D.glob('order_*.json'))],full_Q2=False))
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='CLASSICAL_TWO_INPUT_EULER_INSERTIONS',target='A7.b',
        checks=len(checks),cpu_seconds=result['cpu_seconds'],remote_call=False,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b: três canais clássicos adicionais calculados;consistência localizada residual{result["nonzero_residual"]}/16,{len(checks)}controles CPU{result["cpu_seconds"]}s. Sem ajuste;Q2curvaOPEN. AberturaSHA256={opening}.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['lhs','rhs','residual']}),flush=True)

if __name__=='__main__':main()
