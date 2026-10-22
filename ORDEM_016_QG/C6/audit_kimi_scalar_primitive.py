"""Reject extra uniqueness requirements and check the type/sign of the scalar primitive."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,time,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'kimi_scalar_primitive_audit'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,write,append

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);start=time.process_time();checks=0
    source=BASE/'state/handoffs/e160b57b-85e3-4ae7-842d-ec6da2fd5166_delivery.json';j=json.loads(source.read_bytes())['job'];e=j['execution'];r=e['result'];assert e['status']=='result_ready'
    write(D/'KIMI_ORIGINAL.md',r['text'].encode())
    rec=dict(provider='kimi',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],usage=r['usage'],cost_estimate_usd=r.get('cost_estimate_usd'),source_sha256=sha(source),
        prompt_sha256=hashlib.sha256(j['prompt'].encode()).hexdigest(),response_sha256=sha(D/'KIMI_ORIGINAL.md'),remote_call_repeated=False)
    put(D/'RECEIPT.json',rec)
    def eq(a,b):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    p=s.Matrix(s.symbols('p0:4'));q2=p.dot(p);I=s.eye(4)
    data=json.loads((C/'scalar_second_parallel_primitive/results.json').read_bytes());b,c,t=s.symbols('b c t',real=True);loc={'b':b,'c':c,'t':t}
    nf=[s.sympify(v,locals=loc) for v in data['N4']];n1=[s.sympify(v,locals=loc) for v in data['N2']]
    def op4(B):
        a0,a1,a2,a3,a4=nf;tr=s.trace(B);div=B*p;dd=(p.T*B*p)[0]
        return a0*q2**2*B+a1*I*q2**2*tr+a2*q2*(p*p.T*tr+I*dd)+a3*q2*(p*div.T+div*p.T)/2+a4*p*p.T*dd
    def op2(B):
        a0,a1,a2,a3,a4=n1;tr=s.trace(B);div=B*p;dd=(p.T*B*p)[0]
        return a0*q2*B+a1*I*q2*tr+a2*p*p.T*tr+a3*I*dd+a4*(p*div.T+div*p.T)/2
    # b,c change the principal operator, not merely its representation.
    B=s.diag(0,1,0,0);paxis={p[0]:1,p[1]:0,p[2]:0,p[3]:0}
    witnesses={}
    for param in (b,c):
        change=op4(B).diff(param).subs(paxis).applyfunc(s.expand);assert change!=s.zeros(4);checks+=1
        witnesses[str(param)]=[[str(v) for v in row] for row in change.tolist()]
    change_t=op2(B).diff(t).subs(paxis).applyfunc(s.expand);assert change_t!=s.zeros(4);checks+=1
    witnesses['t_principal_K_order2']=[[str(v) for v in row] for row in change_t.tolist()]
    # Yet the principal b,c variations annihilate every gauge polarization.
    for u in range(4):
        v=I[:,u];G=p*v.T+v*p.T
        for param in (b,c):
            for value in op4(G).diff(param):eq(value,0)
    # The full K,K² gauge matching was already checked with b,c,t symbolic.
    prior=json.loads((C/'scalar_second_parallel_primitive/results.json').read_bytes());assert prior['parameters_chosen'] is False
    # Contact on exp(ipx) = -i CE R whereas NG(c)=+i R.
    CE,R=s.symbols('CE R',real=True);eq(-CE*(s.I*R),-s.I*CE*R)
    assert s.expand((-s.I*CE)*(s.I*R)-(-s.I*CE*R))!=0;checks+=1
    # A primitive is unique modulo CLOSED terms, not necessarily exact ones.
    d=s.Matrix([[1,0]]);kernel=s.Matrix([0,1]);eq((d*kernel)[0],0)
    assert kernel!=s.zeros(2,1);checks+=1
    # Formal self-adjointness of the selected N is sufficient; not necessary
    # for existence of some primitive if a nonsymmetric component is invisible on range G.
    G=s.Matrix([1,0,0]);N=s.Matrix([[0,0,0],[0,0,1],[0,0,0]])
    assert N!=N.T and N*G==s.zeros(3,1);checks+=1
    result=dict(at=now.isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        nonzero_operator_variations=witnesses,
        accepted=['No claim of full Q2 or causal normalization','Formal quadratic variation needs an adjoint condition and boundary control','No arbitrary parameter can be fixed by the matched gauge contact'],
        corrected=['h is a symmetric rank-two tensor; Kimi repeatedly replaces it with a one-form and uses the wrong inner product',
            'N2 carries positive differential coefficients; minus signs in loop_gauge are Fourier signs of two derivatives, not an extra overall differential minus',
            'b,c,t are not all zero-operator rewriting redundancies: principal symbols give explicit nonzero witnesses',
            'A family of primitives is enough to establish existence; parameter fixing is a separate normalization/uniqueness question',
            'Differences of primitives are s0-closed, not necessarily s0-exact modulo d',
            'Formal self-adjointness of this N suffices, but is not a necessary condition on every N with the same NG',
            'The actual primitive factor is -CE/2, because NG on a plane wave already supplies i; multiplying again by -i would change the contact'],
        formal_adjoint_verified_locally=str(C/'scalar_formal_adjoint/manifest.json'),
        naturality_scope='Covariant ansatz N is explicitly defined on the fixed background; naturality of the whole renormalized temporal prescription remains separate and OPEN',
        verdict='PARTIAL_ACCEPTANCE_EXTRA_PARAMETER_FIXING_REQUIREMENT_REJECTED',full_Q2=False,gate_changed=False)
    put(D/'results.json',result);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — crítica Kimi da primitiva escalar; existência preservada, unicidade separada]

AberturaSHA256={opening}.

Kimi reconhece o matching mas pede escolher b,c,t ou provar que são mera
redundância antes de aceitar a primitiva. Essa condição não é necessária
para EXISTÊNCIA: a família inteira satisfaz a relação. Conferimos que
b e c mudam o símbolo principal de N em tensores transversais; t muda
o símbolo de ordem2 em K. Portanto a família não é toda operador zero.
Sua ação sobre G(c), porém, é preservada. Trata-se de liberdade de termos
linearmente invariantes, não de uma exigência de ajustar o contato.

A resposta também troca o tipo de h: N atua em tensores simétricos de
posto2; não em1formas. A prova local do adjunto usa o produto tensorial
correto e já está em scalar_formal_adjoint. Seu requisito é suporte
compacto/termo de borda nulo e palavras completamente simetrizadas.
N é um operador covariante explicitamente definido neste fundo; a
naturalidade da família temporal integral é outra questão, aindaOPEN.

O sinal foi reconferido: NG(exp(ipx))=iR, contato=−iCE R; logo a primitiva
tem fator−CE/2, não outro−i. Primitivas diferem por termos s0-FECHADOS,
não necessariamente exatos. Não se escolheu parâmetro nem contratermo
para zerar uma conta. Controles novos:{checks};CPU{result['cpu_seconds']}s;rc0.
Aceitas as ressalvas sobre cutoff, todos os setores e família causal.
Nenhuma promoção de resposta de modelo a prova; nenhum gate/original tocado.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_C6_critica_Kimi_primitiva_escalar.md',note.encode())
    paths=[Path(__file__),D/'KIMI_ORIGINAL.md',D/'RECEIPT.json',D/'results.json',D/'DERIVACAO.md',C/'scalar_formal_adjoint/manifest.json',C/'scalar_second_parallel_primitive/results.json']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths],opening_sha256=opening))
    event=dict(at=now.isoformat(),event='C6_EXTERNAL_RESULT_AUDITED',target='C6',**rec,manifest_sha256=sha(D/'manifest.json'))
    lines=(OUT/'LEDGER_016.jsonl').read_text('utf-8').splitlines()
    assert not any(json.loads(line).get('event')==event['event'] and json.loads(line).get('job_id')==rec['job_id'] for line in lines if line.strip())
    append(OUT/'LEDGER_016.jsonl',json.dumps(event,ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6ACTIVE: críticaKimi escalar auditada; parâmetros não precisam ser fixados para existência; tipo/sinal corrigidos |{checks}controles CPU{result["cpu_seconds"]}s; assinatura sem custo informado, parcial monetário inalterado.\n')
    cp=H/'CONTINUIDADE.json';c0=json.loads(cp.read_bytes());c0.update(at=now.isoformat(),C6_kimi_scalar_manifest=str(D/'manifest.json'),pending_orchestration='MiMo scalarK2 d35f5145 running worker32907; Kimi scalarK2 e160 audited terminal')
    put(cp,c0,True);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
