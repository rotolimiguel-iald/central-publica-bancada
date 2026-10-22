"""Audit Kimi51c by explicit graph enumeration, graded signs and differential identities."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations, permutations
import ast, hashlib, json, time
import sympy as s
from deliver_nonminimal_wick_and_mimo_audit import H, OUT, BASE, sha, write, put, append

D=H/'kimi_euler_census_audit'

def main():
    D.mkdir(exist_ok=False); now=datetime.now(timezone.utc)
    source=BASE/'state/handoffs/039cab4b-a3a1-4cad-8d8c-349a55d705b3_delivery.json'
    job=json.loads(source.read_bytes())['job']; execution=job['execution']; result=execution['result']
    assert execution['status']=='result_ready'
    write(D/'KIMI_ORIGINAL.md',result['text'].encode())
    put(D/'RECEIPT.json',dict(at=now.isoformat(),request_id=job['request_id'],job_id=job['id'],
        execution_task_id=execution['id'],source_sha256=sha(source),
        prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),
        response_sha256=sha(D/'KIMI_ORIGINAL.md'),usage=result['usage'],model=result['model'],
        elapsed_seconds=result.get('elapsed_seconds'),cost_estimate_usd=result.get('cost_estimate_usd'),
        cost_status='SUBSCRIPTION_UNIT_COST_NOT_REPORTED_NOT_ZERO'))
    sources=[Path(__file__),H/'free_euler_insertion_contact_check.py',
        H/'balanced_cubic_euler_contact_check.py',H/'balanced_cubic_euler_contact/order_0.json',
        H/'bv_coordinate_inventory_delivery/DICIONARIO_E_INVENTARIO.md']
    put(D/'PRE_REGISTER.json',dict(at=now.isoformat(),
        target='Check excluded C x Vghost double contractions, odd matching signs, cutoff identity and auxiliary elimination',
        scope='Finite graph and polynomial counterexamples; no complete curved temporal-family construction',
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources]))
    start=time.process_time();checks=[]
    def eq(name,a,b=0):
        assert s.expand(a-b)==0,(name,a,b);checks.append(name)
    src=sources[1];nodes=[n for n in ast.parse(src.read_text('utf-8')).body
        if isinstance(n,ast.FunctionDef) and n.name in {'allowed','matchings'}]
    ns={'combinations':combinations,'permutations':permutations}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    matchings=ns['matchings']; C=['barc','c','c']; Vgh=['barc','h','c']
    cv=matchings(C,Vgh,2);cc=matchings(C,C,2)
    assert len(cv)==2;checks.append('C x Vghost has two double Wick matchings')
    assert len(cc)==4;checks.append('C x C has four double Wick matchings')
    for graph in cv:
        assert graph['external_left']==['c'] and graph['external_right']==['h']
        checks.append('C x Vghost leaves external c,h')
    assert not matchings(['cdagger','c','c'],Vgh,2)
    checks.append('unvaried cdagger vertex remains excluded, as claimed')
    def wick_sign(pairs):
        remaining=list(range(5));value=1
        for a,b in pairs:
            i,j=remaining.index(a),remaining.index(b);assert i<j
            value*=(-1)**(j-i-1);remaining.remove(a);remaining.remove(b)
        return value
    eq('first ghost matching sign',wick_sign([(0,4),(1,3)]),1)
    eq('second ghost matching sign',wick_sign([(0,4),(2,3)]),-1)
    # Independently re-read an actual contracted tensor, rather than infer nonzero from arity.
    tensor=json.loads(sources[3].read_bytes());witness=None
    for i,row in enumerate(tensor['ghost']):
        for j,expr in enumerate(row):
            polynomial=s.sympify(expr)
            value=s.expand(polynomial.subs({q:k+1 for k,q in enumerate(sorted(polynomial.free_symbols,key=str))}))
            if value!=0:
                witness=dict(row=i,column=j,expression=expr,test_value=str(value),
                    substitution={str(q):k+1 for k,q in enumerate(sorted(polynomial.free_symbols,key=str))})
                break
        if witness:break
    assert witness;checks.append('previous actual ghost Euler graph has a nonzero rational witness')
    x=s.symbols('x0:4'); chi=1+x[0]**2+x[1]*x[2]
    w=s.Matrix([x[i]**2+x[(i+1)%4]*x[(i+2)%4]+i*x[3] for i in range(4)])
    G=lambda u:s.Matrix(4,4,lambda i,j:s.diff(u[j],x[i])+s.diff(u[i],x[j]))
    div=lambda u:sum(s.diff(u[i],x[i]) for i in range(4))
    box=lambda u:sum(s.diff(u,z,2) for z in x)
    Cstar=lambda u:-G(u)/2+s.eye(4)*div(u)/2
    Gstar=lambda h:s.Matrix([-2*sum(s.diff(h[i,j],x[i]) for i in range(4)) for j in range(4)])
    Cmap=lambda h:s.Matrix([sum(s.diff(h[i,j],x[i]) for i in range(4))-s.diff(s.trace(h),x[j])/2 for j in range(4)])
    comm=G(chi*w)-chi*G(w)
    for i in range(4):
        for j in range(4):
            eq('cutoff commutator '+str((i,j)),comm[i,j],s.diff(chi,x[i])*w[j]+s.diff(chi,x[j])*w[i])
    b=s.Matrix([x[i]**2 for i in range(4)]); E=Cstar(b); adj=Gstar(E)
    for i in range(4):eq('Gstar Cstar equals Qstar '+str(i),adj[i],box(b[i]))
    assert adj!=s.zeros(4,1);checks.append('full Euler adjoint Bianchi term is not zero with b retained')
    contract=lambda a,b:sum(a[i,j]*b[i,j] for i in range(4) for j in range(4))
    lhs=-chi*contract(E,G(w)); ins=contract(E,comm)
    boundary=2*sum(s.diff(sum(E[i,j]*chi*w[j] for j in range(4)),x[i]) for i in range(4))
    eq('correct density identity including divergence',lhs,ins-(adj.T*(chi*w))[0]-boundary)
    wrong=-ins-chi*contract(E,G(w))
    assert s.expand(lhs-wrong)!=0;checks.append('printed Kimi commutator equality rejected')
    # An algebraic elimination is not an off-shell chain map for the unmodified qbarc.
    cg=Cmap(G(w))
    for i in range(4):eq('eliminated auxiliary q squared barc channel '+str(i),cg[i],box(w[i]))
    assert cg!=s.zeros(4,1);checks.append('qbarc=-ell C h has nonzero q squared off shell')
    audit=dict(at=datetime.now(timezone.utc).isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        verdict='PARTIAL_STRUCTURAL_ACCEPTANCE_GRAPH_CENSUS_AND_CUTOFF_IDENTITY_REJECTED',
        graph_counterexamples=dict(C_times_Vghost=cv,C_times_C=cc),actual_graph_witness=witness,
        accepted=['No antifield propagators','Constant chi kills [G,chi]w',
            'Normal ordering does not remove cross-vertex Euler contacts','No cohomology conclusion from isolated residue'],
        corrections=['C=(Qbarc)c.dc times Vghost has TWO double matchings; exclusion is false',
            'C times C also admits four double matchings before sign/differential evaluation',
            'Signs of open ghost contractions require graded order, not a minus per odd propagator',
            's0 A = I - integral (Gstar E_h) chi w; Gstar E_h=Qstar b in full auxiliary presentation',
            'Eliminating b alone does not preserve the displayed off-shell BRST complex',
            'Scalar coincident Nc does not specify all derivative contacts of the extended composite',
            'Canonical antifield coordinate map already audited changes antifields by parity, not b'],
        new_remote_call=False,full_Q2=False,gate_changed=False)
    put(D/'AUDIT.json',audit);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — revisão Kimi51c recebida e auditada; Q2 OPEN]

O Kimi preservou corretamente a ausência de propagadores de antifields e
a distinção entre autocontração normal-ordenada e contato Euler entre
vértices. Seu censo completo, porém, não foi adotado.

Em C=(Qbarc)_i c^j d_j c^i contra Vghost=barc h c, há DUAS duplas:
barc_X--c_Y e uma das duas c_X--barc_Y. Sobra c_X,h_Y. A enumeração
independente retorna2, com sinais Wick+ e-. C×C admite4 duplas antes
da soma de sinais. A exclusão de C na tabela e na receita R5 é falsa.
Além da contagem, o cálculo tensorial anterior em R_bal contém testemunha
não nula: célula({witness['row']},{witness['column']}), valor exato
{witness['test_value']} na substituição registrada em AUDIT.json. Não
se infere contribuição não nula só da existência de um emparelhamento.

A identidade de cutoff impressa na seção5 repete o membro esquerdo e
acrescenta -I. A identidade correta, modulo divergência, é

 s0 int chi E_h Z = I - int (G* E_h) chi w,
 I=int E_h [G,chi]w.

Com o setor auxiliar completo, E_h=H0h+C*b, H0G=0,
G*E_h=Q*b. Este termo NÃO pode ser apagado por Bianchi. O controle
polinomial verifica a igualdade pontual incluindo a divergência. Após
substituir b=ell C h, manter qbarc=-ell C h dá q²barc=-ell Qc:
igualdade gaussiana livre não autoriza eliminar o auxiliar na cadeia
off-shell sem transformar a estrutura BV. Nenhum novo sinal foi ajustado.

{len(checks)} controles locais, CPU{audit['cpu_seconds']}s. Original e
recibo preservados, consumo registrado uma vez pelo ID de execução.
Os resultados do Kimi permanecem DECLARADO onde não conferidos; esta
auditoria não reconstrói toda A2 nem sua família lorentziana. Gate intacto.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO_E_CORRECOES.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_Kimi_censo_Euler_corrigido.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in sources+
        [D/'KIMI_ORIGINAL.md',D/'RECEIPT.json',D/'PRE_REGISTER.json',D/'AUDIT.json',D/'DERIVACAO_E_CORRECOES.md']],full_Q2=False))
    ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf-8').splitlines() if v.strip()];events=[]
    if not any(v.get('execution_task_id')==execution['id'] for v in entries):
        events.append(dict(at=now.isoformat(),event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',provider='kimi',
            request_id=job['request_id'],job_id=job['id'],execution_task_id=execution['id'],usage=result['usage'],
            cost_estimate_usd=result.get('cost_estimate_usd'),prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),
            response_sha256=sha(D/'KIMI_ORIGINAL.md'),verdict=audit['verdict']))
    events.append(dict(at=now.isoformat(),event='KIMI_EULER_CENSUS_AUDIT',target='A7.b',checks=len(checks),
        cpu_seconds=audit['cpu_seconds'],manifest_sha256=sha(D/'manifest.json'),remote_call=False))
    append(ledger,''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in events))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: Kimi51c recebido/auditado; exclusão C×Vghost refutada por2emparelhamentos e tensor não nulo; corrigida identidade cutoff com Q*b preservado. {len(checks)}controles CPU{audit["cpu_seconds"]}s; assinatura sem custo unitário informado. Q2OPEN; aberturaSHA256={opening}.\n')
    print(json.dumps(audit),flush=True)

if __name__=='__main__':main()
