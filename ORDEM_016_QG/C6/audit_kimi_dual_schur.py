"""Audit the actual skeptic response: density and involution algebra, not a vote."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,time,hashlib,ast
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6'
sys.path[:0]=[str(C),str(H)]
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,write,append
import labelled_nonminimal_metric_euler as N
import labelled_covariant_xy as M
import labelled_bilocal_jet_engine as L


def main():
    D=C/'kimi_dual_schur_audit';D.mkdir(exist_ok=False)
    now=datetime.now(timezone.utc);start=time.process_time();checks=[]
    source=BASE/'state/handoffs/b86007e9-8574-46dc-b950-0da6347191c9_delivery.json'
    job=json.loads(source.read_bytes())['job'];exe=job['execution'];r=exe['result'];assert exe['status']=='result_ready'
    write(D/'KIMI_ORIGINAL.md',r['text'].encode())
    receipt=dict(provider='kimi',request_id=job['request_id'],job_id=job['id'],execution_task_id=exe['id'],usage=r['usage'],
        cost_estimate_usd=r.get('cost_estimate_usd'),source_sha256=sha(source),prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),response_sha256=sha(D/'KIMI_ORIGINAL.md'),remote_call_repeated=False)
    put(D/'RECEIPT.json',receipt)
    def eq(name,a,b):
        diff=a-b
        vals=list(diff) if isinstance(diff,s.MatrixBase) else [diff]
        assert all(s.cancel(s.expand(v))==0 for v in vals),(name,diff)
        checks.append(name)
    # Formal expansion: sqrt(det(g))=(sin(sqrt(K)r)/(sqrt(K)r))^3 in dimension4.
    u,K,rr,a=s.symbols('u K r a',real=True)
    sinc=1-u*u/6+u**4/120
    density=s.series(sinc**3,u,0,5).removeO()
    eq('volume density coefficient K r2',density.expand().coeff(u,2),-s.Rational(1,2))
    eq('volume density coefficient K2 r4',density.expand().coeff(u,4),s.Rational(13,120))
    vvm=s.series(sinc**(-s.Rational(3,2)),u,0,5).removeO()
    eq('Van Vleck square root is a different object',vvm.expand().coeff(u,2),s.Rational(1,4))
    A0,A1,S0,S1=s.symbols('A0 A1 S0 S1')
    expression=(1-K*rr**2/2)*(A0+K*A1-S0-K*S1)
    eq('Schur density at order1',s.expand(expression).coeff(K,1),A1-rr**2*A0/2-S1+rr**2*S0/2)
    # The first summand is already densitized by M.euler; S is not.
    engine=(C/'labelled_covariant_xy.py').read_text('utf-8')
    assert '(-T.xx*a/2,p,w)' in engine
    checks.append('density term read in existing M.euler')
    # The sign of the mixed density term has no numerical effect in the present
    # flat-Ward-zero case; its general bookkeeping is established above.
    labels=[(i,j) for i in range(4) for j in range(i,4)]
    for i,j in labels:
        for k,l in labels:
            assert not N.cstar_mixed(0,(i,j,k,l))
            checks.append('flat mixed block zero '+str((i,j,k,l)))
    # Commuting with an involution does not remove a single occurrence of it.
    I=s.eye(4);z=s.symbols('h0:10');X=s.zeros(4)
    for value,(i,j) in zip(z,labels):X[i,j]=X[j,i]=value
    R=lambda x:x-I*s.trace(x)/2
    V=lambda x:-2*x+2*I*s.trace(x) # curvature potential of Lh, with K stripped
    eq('trace reversal squared',R(R(X)),X)
    eq('trace reversal commutes with curvature potential',R(V(X)),V(R(X)))
    eq('both products equal minus2X minusgtrace',R(V(X)),-2*X-I*s.trace(X))
    eq('two trace reversals cancel',R(V(R(X))),V(X))
    wrong=s.expand(1) # explicit pure trace counterexample to the reply C2 last step
    witness=R(V(R(I)))-R(V(I))
    eq('reply dropped involution counterexample',witness,12*I)
    assert witness!=s.zeros(4);checks.append('reply Itr Lh Itr = Itr Lh rejected')
    Ra=lambda x:x-a*I*s.trace(x)
    eq('general involution coefficient',Ra(Ra(X))-X,(4*a*a-2*a)*I*s.trace(X))
    roots=s.solve(4*a*a-2*a,a)
    assert roots==[0,s.Rational(1,2)];checks.append('nontrivial qualifier required for uniqueness')
    # This false step does not appear in the implemented PH block: it trace
    # reverses Lh P exactly once, with P=Hh Itr already stipulated.
    source_engine=(C/'labelled_nonminimal_metric_euler.py').read_text('utf-8')
    assert 'terms=list(M.euler' in source_engine and 'Trace reverse the OUTPUT' in source_engine
    checks.append('implemented single output reversal preserved')
    result=dict(at=now.isoformat(),checks=len(checks),check_names=checks,cpu_seconds=time.process_time()-start,
        accepted=['Schur signs and metric dualization correct in the inspected files','Grassmann signs and vertex weights remain a separate assembly','First curvature only; independent contact engine not reproduced by Kimi'],
        corrected=['Density is sqrt(det(g))=1-K|x|²/2+..., not a Van Vleck factor. M.euler already includes it; minus density times CstarS produces the positive correction.',
          'Commutation gives Itr Lh Itr=Lh, not Itr Lh. Pure trace curvature-potential witness has difference12 Id. The code did not make the false reduction.',
          'Itr coefficient1/2 is the nontrivial involutive choice; coefficient0 is also involutive.'],
        convention_kappa_vs_curvature='Distinct symbols throughout the block identity; no physical identification selected',
        full_Q2=False,gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — crítica Kimi Schur/dual auditada; sem mudança do motor]

AberturaSHA256={opening}.

Kimi não encontrou erro demonstrável de sinais/índices/fatores nas fontes
enviadas. Isso é parecer estático, não reprodução dos contatos. O texto
integral e o recibo foram arquivados. Duas correções são necessárias:

1. A densidade é sqrt(det(g))=1−K|x|²/2+..., não Delta_VV nem sua raiz.
M.euler já densitiza o primeiro termo. Portanto −sqrt(g)CstarS contribui
+K|x|²(CstarS)_0/2, exatamente o código. A fórmula geral foi verificada;
neste truncamento (CstarS)_0=0 por Ward plano, verificado nas100 entradas.

2. De [Itr,Lh]=0 e Itr²=1 segue Itr Lh Itr=Lh. A resposta escreve
Itr Lh Itr=Itr Lh, o que é falso. No potencial de curvatura, o teste
X=Id dá diferença12Id. O motor NÃO faz essa simplificação: aplica
Itr uma vez à saída LhP, mantendo P=HhItr. Nenhum coeficiente mudou.
Também se precisa dizer reversão NÃO TRIVIAL ao chamar1/2 de único:
o fator0 corresponde à identidade, que também é involutiva.

{len(checks)} controles, CPU{result['cpu_seconds']}s,rc0.
Mantidas as ressalvas úteis: escopo primeira curvatura, sinais Wick na
montagem, uso único de cada dualização, contatos não reproduzidos pelo
executor e Q2 integral aindaOPEN. Não adotada a redução falsa do parecer.
Tokens do recibo:{r['usage']['total_tokens']}; custo de assinatura não
informado, não tratado como zero; parcial monetário anterior preservado.
Nenhum original/kernel/gate alterado, nenhuma chamada repetida.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C6_critica_Kimi_Schur_dual.md',note.encode())
    paths=[Path(__file__),D/'KIMI_ORIGINAL.md',D/'RECEIPT.json',D/'results.json',D/'DERIVACAO.md',C/'labelled_nonminimal_metric_euler.py',C/'labelled_covariant_xy.py',C/'dual_schur_delivery/manifest.json',C/'nonminimal_yjets/manifest.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths],opening_sha256=opening))
    event=dict(at=now.isoformat(),event='C6_EXTERNAL_RESULT_AUDITED',target='C6',**receipt,manifest_sha256=sha(D/'manifest.json'))
    lines=[json.loads(x) for x in (OUT/'LEDGER_016.jsonl').read_text('utf-8').splitlines() if x.strip()]
    assert not any(v.get('event')==event['event'] and v.get('job_id')==job['id'] for v in lines)
    append(OUT/'LEDGER_016.jsonl',json.dumps(event,ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6ACTIVE: KimiSchur/dual auditado, redução falsa da involução recusada e densidade esclarecida; {len(checks)}controles CPU{result["cpu_seconds"]}s,rc0. Assinatura sem custo informado; parcial monetário inalterado.\n')
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes());state.update(at=now.isoformat(),C6_kimi_dual_schur_manifest=str(D/'manifest.json'),pending_orchestration='All C6 units terminal and audited; no active external unit')
    put(p,state,True);print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
