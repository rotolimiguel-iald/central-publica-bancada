"""Publish measured curved defect and audit a provider's endpoint descent."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import json, hashlib, uuid, time
import sympy as s
from logarithmic_contact_engine import residue, Q

H = Path(__file__).resolve().parent
OUT = H.parents[1] / 'TUNEL/DO_CHATGPT'
BASE = H.parents[1] / 'IALD_ORQUESTRACAO_20260923'
D = H / 'curved_defect_descent_review_delivery'
now = datetime.now(timezone.utc)
stamp = now.strftime('%Y%m%d_%H%M%S_%f')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, data, replace=False):
    assert data
    if p.exists():
        assert replace, p
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        assert not backup.exists()
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    temp.replace(p)

def put(p, value, replace=False):
    write(p, json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'), replace)

def append(p, text):
    old = p.read_bytes()
    write(p, old + text.encode('utf-8'), True)
    assert p.stat().st_size > len(old)

def main():
    D.mkdir(exist_ok=False)
    measured = json.loads((H / 'curved_parametrix_euler_defect/results.json').read_bytes())
    receipt = BASE / 'state/handoffs/580fc181-e08e-4cd1-b298-bbbd4f032467_delivery.json'
    job = json.loads(receipt.read_bytes())['job']
    execution = job['execution']; result = execution['result']
    assert execution['status'] == 'result_ready'
    write(D / 'DEEPSEEK_ORIGINAL.md', result['text'].encode('utf-8'))
    put(D / 'DEEPSEEK_RECEIPT.json', dict(request_id=job['request_id'],
        job_id=job['id'], execution_task_id=execution['id'],
        status=execution['status'], receipt_sha256=sha(receipt),
        prompt_sha256=hashlib.sha256(job['prompt'].encode('utf-8')).hexdigest(),
        response_sha256=sha(D / 'DEEPSEEK_ORIGINAL.md'),
        usage=result['usage'], cost_estimate_usd=result['cost_estimate_usd'],
        canonical_memory=result.get('canonical_memory'), repeated=False))

    # New minimal controls, independent of the full 16-component calculation.
    start = time.process_time(); checks = []
    x = s.symbols('x0:4'); z = sum(v*v for v in x)
    lam, eta = s.symbols('lam eta'); L = lam + eta
    def eq(name, expression):
        assert s.cancel(expression) == 0, (name, expression)
        checks.append(name)
    # Only h00*c0 is nonzero; s0 h00 = 2 d0 c0.
    F = z**-2
    B0 = -2*(s.diff(F, x[0]) + lam*F)
    B1 = -2*(s.diff(F, x[0]) + eta*F)
    opposite = B1.subs(dict(zip(x, [-v for v in x])), simultaneous=True)
    antisym = s.cancel(B0 - opposite)
    eq('even rational kernel antisymmetric descendant',
        antisym - (16*x[0]/z**3 + 2*(eta-lam)/z**2))
    assert s.cancel(antisym.subs({lam:0, eta:0})) != 0
    checks.append('L zero does not cancel derivative terms')
    # Constant smooth kernel is a direct counterexample to the alleged
    # equivalence between L_i F=0 and L.dF=0.
    const_desc = -2*lam + 2*eta
    eq('constant kernel derivative zero', s.diff(s.Integer(1), x[0]))
    assert const_desc.subs({lam:1, eta:0}) == -2
    checks.append('constant kernel with L nonzero has nonlocal descendant')
    # Contact for F=d0(1/z)=-2*x0/z²: -2 Res(x0 F/z)/CE.
    additional = 4*residue(3, (2,0,0,0), (1,1,1,1))
    eq('omitting outer derivative contact rejected', additional + s.Rational(1,4))
    assert additional != 0
    q = Q[0]
    # Weighted adjoint of d0 is -d0-L0; not cancellation to L0.
    eq('weighted adjoint of first derivative', q-(-q-L)-(2*q+L))
    put(D / 'audit_results.json', dict(checks=len(checks), check_names=checks,
        cpu_seconds=time.process_time()-start, rational_descendant=str(antisym),
        constant_kernel_counterexample='lambda0=1,eta0=0,F=1: descendant=-2, L.dF=0',
        outer_contact_over_CE=str(additional), review_status='PARTIALLY_REJECTED',
        no_new_loop_engine=True, full_Q2=False, gate_changed=False))
    audit = json.loads((D / 'audit_results.json').read_bytes())
    opening = sha(OUT / 'ENTREGA_016_ABERTURA_operador.md')
    report = f'''[DERIVED — cálculo local auxiliar e auditoria; Q2 curvo OPEN]

# Resto de Euler do parametrix no espaço-forma

Reutilizados os coeficientes de calor e a conexão radial já calculados.
Em dimensão4 euclidiana, z=r², L=∇²+K E, na normalização singular1/z:

 Hsing=U0/z-U1 log(z/ell²)/4+U2 z log(z/ell²)/16.
 [L Hsing]=3 U2/4.

O coeficiente U2 já inclui K². A recorrência de transporte cancela o log;
o termo quadrático da conexão cancela a dependência direcional restante.
O controle que omite a conexão falha. Resultados dos blocos mínimos:

 [L Hsing]_metric=K²(-21 P_TL/20+479 P_tr/20),
 [L Hsing]_ghost=179 K² Id4/20.

Controle escalar radial independente com potencial E dimensional:
 [L Hsing]_scalar=3E²/8+3EK/2+29K²/20.

São {measured['checks']} verificações, CPU{measured['cpu_seconds']}s.
O traço ponderado métrica/2-ghost é -571K²/20; NÃO é A1 nem A2.
O sinal inverte ao usar D=-L. Para Hsing+W ser bisolução, a parte suave
deve satisfazer [L W]=-3U2/4 nessa separação. Isso é condição necessária;
nenhum W, estado, propagador não minimal22x22 ou continuação lorentziana
foi construído. Não se impôs uma escolha suave para cancelar a anomalia.

O resultado localiza por que a normalização plana anterior não se transfere
automaticamente ao fundo curvo: o argumento de comutação Wick-BV usava PH=0.
O próximo alvo é o defeito de aridade1 em termos de PH e QH, sem substituir
esse defeito por um traço de calor. Nova unidade MiMo87d preparada para isso.

# Auditoria DeepSeek6309 — aceitação parcial e correção explícita

Resposta original preservada integralmente como DECLARADO. Os passos1–3
conservam corretamente a multiplicidade de h_ii e o sinal:
 -(∂i+lambda_i)R(F)=R(-(∂i+lambda_i)F)+C_i(F).

Os passos6–7 são recusados. Não se somam operadores ∂+lambda e -∂+eta
antes de aplicá-los aos kernels trocados, que incluem índices transpostos,
cutoffs permutados e x invertido. A frase de que R comuta com derivadas
contradiz o C_i não nulo definido no próprio pedido. L_i F=0 tampouco
é equivalente a L·∂F=0.

Defina B_(ghost,r) pela soma real -(∂i+lambda_i)F_(ij),r, contando duas
vezes quando i=j. A condição de cancelamento da parte bilocal é

 B(lambda,eta;x)-B(eta,lambda;-x)^T=0 fora da diagonal,

com a compatibilidade da extensão explicitamente conservada. Ela precisa
ser verificada nos kernels; não é uma condição escalar L·∂F=0.
Contraexemplo: apenas F_(00),0=z^-2 não nulo dá
16x0/z³+2(eta0-lambda0)/z². Mesmo L=0 não remove a derivada.
Mais diretamente, F=1, lambda0=1, eta0=0 tem L·∂F=0, mas descendente=-2
fora da diagonal. Marcadores são jatos locais; não se assume integração
global convergente dos exponenciais. O adjunto local é D*=-D-L.
Também C0(∂0(1/z))/CE=-1/4: omitir a passagem da derivada por R perde contato.
São {audit['checks']} controles adicionais, CPU{audit['cpu_seconds']}s.

O passo10 também extrapola: igualdade de descendentes não prova trivialidade
BRST do funcional bilocal, nem identifica a classe de anomalia. A diferença
pode ser fechada sem ser exata. Conservamos a distinção entre contatos
medidos, inserção J2 e mapa A2, bem como a dependência de A1 ainda aberta.
A auditoria não modifica as16 componentes previamente calculadas, que já
verificavam os dois kernels e o contato C_i separadamente.

Nenhum original, kernel ou gate alterado. Abertura SHA256={opening}.
'''
    write(D / 'DERIVACAO_E_REVISAO.md', report.encode('utf-8'))
    write(OUT / 'ENTREGA_016_MEDIDA_resto_curvo_e_revisao_DeepSeek6309.md', report.encode('utf-8'))
    paths = [Path(__file__), D/'DERIVACAO_E_REVISAO.md', D/'DEEPSEEK_ORIGINAL.md',
        D/'DEEPSEEK_RECEIPT.json', D/'audit_results.json',
        H/'curved_parametrix_euler_defect_check.py', H/'curved_parametrix_euler_defect/results.json',
        H/'curved_parametrix_euler_defect/manifest.json',
        H/'orchestration_curved_wick_defect/prepared_units.json']
    put(D/'manifest.json', dict(at=now.isoformat(),
        artifacts=[dict(path=str(p), sha256=sha(p)) for p in paths],
        checks=measured['checks']+audit['checks'],
        cpu_seconds=measured['cpu_seconds']+audit['cpu_seconds'],
        full_Q2=False, gate_changed=False))
    ledger = OUT/'LEDGER_016.jsonl'
    entries = [json.loads(v) for v in ledger.read_text('utf-8').splitlines()]
    additions = []
    if not any(e.get('execution_task_id') == execution['id'] for e in entries):
        additions.append(dict(at=now.isoformat(), event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',
            target='A7.b', provider='deepseek', request_id=job['request_id'], job_id=job['id'],
            execution_task_id=execution['id'], usage=result['usage'],
            cost_estimate_usd=result['cost_estimate_usd'],
            response_sha256=sha(D/'DEEPSEEK_ORIGINAL.md'), accepted='PARTIAL_WITH_COUNTEREXAMPLES'))
    additions.append(dict(at=now.isoformat(), event='CURVED_PARAMETRIX_DEFECT_AND_DESCENT_REVIEW',
        target='A7.b', checks=measured['checks']+audit['checks'],
        cpu_seconds=measured['cpu_seconds']+audit['cpu_seconds'],
        manifest_sha256=sha(D/'manifest.json'), remote_call=False))
    append(ledger, ''.join(json.dumps(e, ensure_ascii=False)+'\n' for e in additions))
    cost = Decimal(0); seen=set()
    for e in entries+additions:
        value=e.get('cost_estimate_usd', e.get('cost_usd'))
        if value is None: continue
        key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
        if key and key in seen: continue
        if key: seen.add(key)
        cost += Decimal(str(value))
    append(OUT/'ENTREGA_016_PROGRESSO.md',
        f'\n{now.isoformat()} A7.b PROGRESS: resto Euler curvo [LHsing]=3U2/4; '
        f'14controles+6contraexemplos/identidades de auditoria DeepSeek6309. '
        f'MiMo87d preparado; Kimi com cota5h indisponível. Custo conhecido parcialUSD{cost}; '
        f'Q2curvo aberto. AberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json'; state=json.loads(p.read_bytes())
    state.setdefault('head_history', []).append({k:state.get(k) for k in
        ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    state.update(at=now.isoformat(), previous_goal_turn='PROGRESS',
        completed_this_turn=['Curved singular parametrix Euler defect calculated through K²',
            'DeepSeek6309 audited; nonlocal cancellation and cohomology claims rejected by controls',
            'Distinct MiMo arity-one Wick/BV task prepared and handed to coordinator'],
        next=['Receive MiMoa46/87d; derive actual curved arity-one Wick defect',
            'Preserve Kimi FIFO until actual quota recovery; no failed call retries',
            'A7b deadline20:32UTC; A7c/d,A8,PartB/final still remain'],
        pending_orchestration='DeepSeek6309 complete/audited; MiMoa46 running last official observation; MiMo87d admission pending; Kimi e710/51c/709 waiting, d3 staging quota-blocked',
        partial_metered_cost_usd=str(cost))
    state['curved_defect_descent_review_update']=dict(manifest=str(D/'manifest.json'),
        smooth_W_constructed=False, full_nonminimal_parametrix=False, A1_computed=False,
        full_Q2=False, gate_changed=False, own_processes=[])
    state['latest_verified_orchestration']['deepseek']['status']='COMPLETED_RECEIVED_AUDITED_PARTIAL'
    put(p,state,True)
    for item in json.loads((D/'manifest.json').read_bytes())['artifacts']:
        assert sha(Path(item['path'])) == item['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'), checks=measured['checks']+audit['checks'],
        known_partial_cost_usd=str(cost)), ensure_ascii=False))

if __name__ == '__main__':
    main()
