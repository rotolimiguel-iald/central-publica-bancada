"""Independent invariant-variable Euler check and audit of the MiMo heat split."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, sys, time
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
H, C = ROOT/'A7', ROOT/'C6'
D = C/'mimo_scalar_K2_audit'
sys.path.insert(0, str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT, BASE, sha, write, put, append


def main():
    D.mkdir(exist_ok=False)
    now = datetime.now(timezone.utc)
    start = time.process_time()
    source = BASE/'state/handoffs/d35f5145-adb0-43ce-8636-1863a2d13dd3_delivery.json'
    job = json.loads(source.read_bytes())['job']
    execution = job['execution']
    assert execution['status'] == 'result_ready'
    answer = execution['result']
    write(D/'MIMO_ORIGINAL.md', answer['text'].encode('utf-8'))
    receipt = dict(provider='mimo', request_id=job['request_id'], job_id=job['id'],
        execution_task_id=execution['id'], usage=answer['usage'],
        cost_estimate_usd=answer['cost_estimate_usd'], source_sha256=sha(source),
        prompt_sha256=hashlib.sha256(job['prompt'].encode()).hexdigest(),
        response_sha256=sha(D/'MIMO_ORIGINAL.md'), remote_call_repeated=False)
    put(D/'RECEIPT.json', receipt)
    checks = []

    def eq(name, a, b):
        assert s.cancel(s.expand(a-b)) == 0, (name, a, b)
        checks.append(name)

    # A=|x|², B=|y|², C=x.y in RNC around a third, fixed point.
    # These are independent formal invariants, not evaluation at y=0.
    A, B, Z, K = s.symbols('A B C K')
    w = A+B-2*Z
    d1 = -(A*B-Z**2)/3
    d2 = -(A+B-4*Z)*(A*B-Z**2)/45
    h0 = 1/w
    h1 = s.Rational(1,4)-s.log(w)/2-d1/w**2
    h2 = d1**2/w**3-d2/w**2-d1/(2*w)+s.Rational(19,480)*w

    def dil(f):
        return 2*A*s.diff(f,A)+Z*s.diff(f,Z)

    def lap(f):
        return 8*s.diff(f,A)+4*A*s.diff(f,A,2)+4*Z*s.diff(f,A,Z)+B*s.diff(f,Z,2)

    def l1(f):
        return (A*lap(f)-dil(dil(f))-5*dil(f))/3

    def l2(f):
        return (A*A*lap(f)-A*dil(dil(f))-3*A*dil(f))/15

    defects = [s.cancel(lap(h0)), s.cancel(lap(h1)+l1(h0)),
               s.cancel(lap(h2)+l1(h1)+l2(h0))]
    for n, expected in enumerate((0,0,s.Rational(29,20))):
        eq(f'bilocal scalar Euler coefficient K^{n}', defects[n], expected)
    for v in (A,B,Z):
        eq(f'derivative of bilocal K2 defect with respect to {v}',s.diff(defects[2],v),0)
    for n,h in enumerate((h0,h1,h2)):
        eq(f'endpoint exchange symmetry K^{n}',h.xreplace({A:B,B:A}),h)
    # Densitization cannot change the first nonzero coefficient.
    eq('densitized defect through K2',defects[2]-A*defects[1]/2+s.Rational(13,120)*A*A*defects[0],s.Rational(29,20))

    # Independently verify the heat transport recurrence, not just its log combination.
    r, lam = s.symbols('r lambda', positive=True)
    u0 = 1+K*r*r/4+s.Rational(19,480)*K*K*r**4
    u1 = 2*K+s.Rational(29,60)*K*K*r*r
    u2 = s.Rational(29,15)*K*K
    radial = lambda f: s.diff(f,r,2)+(3/r-K*r-K*K*r**3/15)*s.diff(f,r)
    transport = lambda f,n: r*s.diff(f,r)+(n-K*r*r/2-K*K*r**4/30)*f
    for n,u,prev in ((1,u1,u0),(2,u2,u1)):
        for k in range(3):
            eq(f'heat transport U{n} order {k}',s.expand(transport(u,n)-radial(prev)).coeff(K,k),0)
    composite = -u1/4+u2*r*r/16
    eq('combined logarithm',composite,-K/2)
    changed_u1, changed_u2 = u1+4*lam*K*K*r*r, u2+16*lam*K*K
    eq('formal split leaves the composite unchanged',-changed_u1/4+changed_u2*r*r/16,composite)
    changed_residue = s.expand(transport(changed_u1,1)-radial(u0)).coeff(K,2)
    eq('but split change violates U1 heat recurrence',changed_residue,12*lam*r*r)
    assert changed_residue != 0
    checks.append('nonzero heat recurrence rejects gauge interpretation')

    result = dict(at=now.isoformat(), checks=len(checks), check_names=checks,
        cpu_seconds=time.process_time()-start,
        bilocal_Euler_coefficients=list(map(str,defects)),
        domain='Formal K jet through K2 on a local convex normal neighborhood, w!=0; no global all-order or diagonal-distribution claim',
        accepted='Same composite parametrix through K2; no added smooth state term; Euler defect 29K2/20',
        corrections=['Heat coefficients obey individual transport recurrences; equality of the combined log is not gauge freedom of heat coefficients.',
          'The engine simplifies the sum; it does not set individual K2 heat coefficients to zero.',
          'At this order the defect is bilocally constant, not only at coincidence; its Y derivative vanishes off diagonal. This is not an all-order/global statement.'],
        independent_engine_audit_by_MiMo=False, full_Q2=False, gate_changed=False)
    put(D/'results.json',result)
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — auditoria MiMo do parametrix escalar K²; composto confirmado no escopo local]

AberturaSHA256={opening}.

A resposta MiMo concorda com o parametrix composto já usado: H=1/z+
K(1/4−log(z)/2)+19K²z/480, sem termo suave de estado acrescentado.
Os dois termos K²z log(z) oriundos de U1 e U2 se cancelam.
A recorrência de calor foi verificada separadamente para U1 e U2.
Correção à resposta: alterar U1 em4λK²z e U2 em16λK² conserva o composto,
mas viola a recorrência de U1 por12λK²z. Não é uma liberdade de gauge
dos coeficientes de calor. O motor apenas simplifica a soma.

Verificação nova, sem fixar y=0: escrevemos o Laplaciano em invariantes
A=|x|²,B=|y|²,C=x·y. Os coeficientes K⁰,K¹,K² de Δx H são
0,0,29/20. Logo ∂Y do defeito suave K² é zero também bilocalmente,
no domínio local/truncamento indicado. Sua densitização não altera
esse resultado. Isto não afirma bisolução exata, comportamento global,
igualdade de distribuições na diagonal ou validade em todas as ordens.
O valor 29K²/20 continua presente quando não há derivada sobre ele.

{len(checks)} verificações simbólicas; CPU={result['cpu_seconds']}s; rc0.
MiMo não executou o motor e não recebeu todos os seus componentes:
sua concordância analítica não substitui os testes locais da extensão.
Primitiva escalar anterior preservada. Montagem métrica/ghost e Q2 inteira
continuam pendentes. Nenhum original, kernel ou gate alterado.
Uso do recibo: {answer['usage']['total_tokens']} tokens;
custo estimado desta chamada US${answer['cost_estimate_usd']}.
'''
    write(D/'DERIVACAO.md',note.encode())
    write(OUT/'ENTREGA_016_MEDIDA_C6_auditoria_MiMo_escalar_K2.md',note.encode())
    paths=[Path(__file__),D/'MIMO_ORIGINAL.md',D/'RECEIPT.json',D/'results.json',D/'DERIVACAO.md',C/'scalar_second_curvature_engine.py']
    put(D/'manifest.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in paths],opening_sha256=opening))
    event=dict(at=now.isoformat(),event='C6_EXTERNAL_RESULT_AUDITED',target='C6',**receipt,manifest_sha256=sha(D/'manifest.json'))
    lines=[json.loads(line) for line in (OUT/'LEDGER_016.jsonl').read_text('utf-8').splitlines() if line.strip()]
    assert not any(v.get('event')==event['event'] and v.get('job_id')==job['id'] for v in lines)
    cp=H/'CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    total=Decimal(state['partial_metered_cost_usd'])+Decimal(answer['cost_estimate_usd'])
    append(OUT/'LEDGER_016.jsonl',json.dumps(event,ensure_ascii=False)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6ACTIVE: MiMo escalarK2 auditado; recorrência impede suposta gauge; defeito bilocal29/20 | {len(checks)}controles,CPU{result["cpu_seconds"]}s; parcial monetário US${total}; custos sem medição não são zero.\n')
    state.update(at=now.isoformat(),partial_metered_cost_usd=str(total),C6_mimo_scalar_manifest=str(D/'manifest.json'),pending_orchestration='All C6 external units terminal and audited; no new remote unit submitted')
    put(cp,state,True)
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
