"""Audit received C6 answers; checkpoint corrected labelled contacts."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,sys,time,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[1];H=ROOT/'A7';C=ROOT/'C6';D=C/'external_and_label_audit'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,write,put,append

def main():
    D.mkdir(exist_ok=False);now=datetime.now(timezone.utc);start=time.process_time();checks=0
    def eq(a,b):
        nonlocal checks
        assert s.expand(a-b)==0,(a,b);checks+=1
    g,a,v,w,k,l,phi,z=s.symbols('g a v w k l phi z',nonzero=True)
    Hess=a+g*v*phi+g**2*w*phi**2/2
    Ihess=g*k*phi+g**2*l*phi**2/2
    W=s.series(s.log(Hess)/2,g,0,3).removeO().expand()
    J=s.series(Ihess/(2*Hess),g,0,3).removeO().expand()
    eq(W.coeff(g,2),w*phi**2/(4*a)-v**2*phi**2/(4*a**2))
    eq(J.coeff(g,2),l*phi**2/(4*a)-k*v*phi**2/(2*a**2))
    assert J.coeff(g,2).subs(l,0)!=0;checks+=1
    # Same result by differentiation of the effective action with an insertion source.
    eta=s.symbols('eta')
    eq(s.series(s.diff(s.log(Hess+eta*Ihess)/2,eta).subs(eta,0),g,0,3).removeO(),J)
    # Even action V=hstar*c*h: left derivative hstar gives c*h, right gives -c*h.
    # Monomial odd labels are hstar=0, c=1, ordered left-to-right.
    mon=(0,1)
    left=(-1)**mon.index(0)
    right=(-1)**(len(mon)-1-mon.index(0))
    eq(left,1);eq(right,-1);eq(-right,1)
    assert -right!=-left;checks+=1
    # A derivative of a product is not a derivative on only one distinguished line.
    f=z**2;h=z**3
    eq(s.diff(f*h,z),s.diff(f,z)*h+f*s.diff(h,z))
    assert s.diff(f*h,z)-s.diff(f,z)*h!=0;checks+=1
    result=dict(at=now.isoformat(),checks=checks,cpu_seconds=time.process_time()-start,
        finite_model_W2=str(W.coeff(g,2)),finite_model_J2=str(J.coeff(g,2)),
        accepted=['Legendre inversion changes the sign of the connected amputated quadratic correction',
            'W1 and its nonlinear variation cannot be silently discarded',
            'Antifields are external sources and must remain during the Ward reduction'],
        corrections=['Given exp(-S/hbar), the log-determinant cubic bubble has negative sign and quartic tadpole positive sign; the answer reverses/inconsistently labels these signs',
            'J2 must include the I1-V1 bubble, shown explicitly by differentiating log(Hessian+eta I-Hessian); the answer gives only an I2 tadpole',
            'For even V and odd hstar, right and left derivatives have opposite signs; with its stated bracket the V1,W1 term has plus L_c h W1_h, not its displayed minus',
            'A derivative outside a product obeys Leibniz; K3-K1 cannot equal a single contact for arbitrary separately assigned derivative words',
            'Its P0 is Rraw whereas current bench uses labelled R_bal plus smooth completion; no automatic coefficient transport',
            'No full component comparison was delivered; inputs and gaps remain explicit'],
        status='PARTIAL_STRUCTURAL_ACCEPTANCE_NUMERICAL_DICTIONARY_NOT_ADOPTED',full_Q2=False,gate_changed=False)
    put(D/'KIMI_AUDIT.json',result)
    jobs=[('kimi','8b3884ac-d156-4843-9772-26bed53f525b'),('deepseek','b2c22962-38e5-4897-8204-164fdb8d2d6f')]
    receipts=[];events=[];cost=Decimal('0')
    ledger=(OUT/'LEDGER_016.jsonl').read_text('utf-8')
    for provider,jid in jobs:
        source=BASE/'state/handoffs'/f'{jid}_delivery.json';j=json.loads(source.read_bytes())['job'];e=j['execution'];r=e['result']
        assert e['status']=='result_ready'
        assert not any(json.loads(line).get('event')=='C6_EXTERNAL_RESULT_AUDITED' and json.loads(line).get('job_id')==jid for line in ledger.splitlines() if line.strip())
        p=D/f'{provider.upper()}_ORIGINAL.md';write(p,r['text'].encode('utf-8'))
        rec=dict(provider=provider,request_id=j['request_id'],job_id=jid,execution_task_id=e['id'],source_sha256=sha(source),
            prompt_sha256=hashlib.sha256(j['prompt'].encode('utf-8')).hexdigest(),response_sha256=sha(p),usage=r['usage'],cost_estimate_usd=r.get('cost_estimate_usd'),
            response_status='DECLARADO',remote_call_repeated=False)
        put(D/f'{provider.upper()}_RECEIPT.json',rec);receipts.append(rec)
        events.append(dict(at=now.isoformat(),event='C6_EXTERNAL_RESULT_AUDITED',target='C6',**rec))
        if rec['cost_estimate_usd'] is not None:cost+=Decimal(str(rec['cost_estimate_usd']))
    put(D/'DEEPSEEK_AUDIT.json',dict(status='NO_COEFFICIENT_DELIVERED',
        accepted='Answer does not invent coefficients or assert full Q2',
        correction='Scalar pair_delta can be applied componentwise with polynomial connection and trace coefficients; absent tensor wrapper is an implementation gap, not an impossibility',
        local_existing_answer=str(C/'tensor_zerojet/DELIVERY_MANIFEST.json'),
        independent_numeric_confirmation=False,classification='DECLARADO external methodological response, not INPUT/ONTO mathematical result',full_Q2=False))
    names=['LABELLED_REGRESSION.json','tensor_yjets_v2/results.json','tensor_yjets_v2/INDEPENDENT_AUDIT.json','scalar_vertex_v2/results.json','scalar_parallel/results.json']
    measurements={n:json.loads((C/n).read_bytes()) for n in names}
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    note=f'''[DERIVED+CAS — correção de representação; jatos e gráfico escalar até primeira curvatura. Q2 OPEN]

Abertura SHA256: {opening}.

A extensão R_bal usa linhas radiais identificadas e palavras de derivação.
Expandir a derivada de uma linha em polinômios vezes outro perfil ANTES
da extensão perde essa identificação. A tabela tensor_yjets inicial
passava controles de covariância, mas falhou no confronto com o contato
plano congelado: diferença não nula −Q0 Q²/384 no controle0101.
Ela permanece preservada como DIFFERENT_EXTENSION_NOT_ADOPTED.
O zerojet tensorial anterior não muda. Nenhuma nova prescrição foi escolhida.

labelled_bilocal_jet_engine conserva os três dados (coeficiente, perfil,
palavra radial). Seus4264controles incluem4200igualdades fora da diagonal
e64contatos escalares planos conhecidos. A tabela v2 tem57blocos,
representa570000pares e passa11400controles de forma+200regressões zerojet.
A auditoria adicional passou82200controles, incluindo2400comutadores e
48comutadores de curvatura não nulos. Permutações/reflexões não constituem,
sozinhas, prova de covariância sob toda mudança de coordenadas.

O gráfico real escalar Euler(X)×vértice métrico(Y), três sabores, dá
K CE [143/1536 δab Qr Q² −13/1536(δar Qb+δbr Qa)Q² −23/256 QaQbQr].
São coeficientes de derivadas COORDENADAS de delta, com duplicidade2
nos componentes a≠b. Seus272controles recuperam o contato principal.
A leitura adicional no fantasma contravariante transportado paralelamente
usa P1=(|x|²I−xxᵀ)/6; não pode omitir seus jatos. Resultado e controles
por dualidade distributiva estão em scalar_parallel/results.json.
Não chamamos essa leitura de operador covariante completo.

Kimi: mapa estrutural parcialmente útil; auditoria elementar detectou
sinal de bolha, omissão da bolha I1–V1 em J2 e conversão incorreta de
derivada direita do antifield ímpar. Não adotamos o dicionário numérico.
DeepSeek: não entregou o tensor solicitado. A lacuna de implementação
indicada já foi resolvida na medição local zerojet, não há confirmação
numérica independente nessa resposta. Recibos integrais preservados.

Todos os comandos Python desta correção terminaram rc0; tentativas
anteriores falhas foram mantidas. CPU/custos e hashes nos manifestos.
Não houve alteração de original, kernel, Atlas ou gate. Faltam montagem
temporal completa, setores restantes, K² e confronto da classe local
no problema integral. C6 continua ACTIVE dentro do teto original.
'''
    write(D/'DERIVACAO.md',note.encode('utf-8'));write(OUT/'ENTREGA_016_MEDIDA_C6_jatos_rotulados_e_escalar.md',note.encode('utf-8'))
    files=[Path(__file__),C/'labelled_bilocal_jet_engine.py',C/'labelled_jet_regression.py',C/'tensor_euler_yjet_engine_v2.py',C/'tensor_euler_yjet_check_v2.py',C/'audit_tensor_yjets_v2.py',C/'scalar_euler_curved_vertex_v2.py',C/'scalar_parallel_readout.py']
    files += [C/n for n in names]+list(D.glob('*.json'))+list(D.glob('*.md'))
    files += [C/'tensor_yjets_v2/manifest.json',C/'tensor_yjets_v2/AUDIT_MANIFEST.json',C/'scalar_vertex_v2/manifest.json',C/'scalar_parallel/manifest.json']
    put(D/'manifest.json',dict(at=now.isoformat(),files=[dict(path=str(p),sha256=sha(p)) for p in files],opening_sha256=opening,full_Q2=False))
    cp=H/'CONTINUIDADE.json';cont=json.loads(cp.read_bytes());total=Decimal(cont['partial_metered_cost_usd'])+cost
    events.append(dict(at=now.isoformat(),event='C6_LABELLED_REGRESSION_AND_SCALAR_GRAPH',target='C6',remote_call=False,manifest_sha256=sha(D/'manifest.json'),partial_metered_cost_usd=str(total),measurements=measurements,external_audit_checks=checks))
    append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6 ACTIVE: extensão rotulada corrigida; gráfico escalar O(K), auditorias Kimi/DeepSeek | custo parcial conhecido USD{total}; custos de assinatura/desconhecidos não são zero | Q2 OPEN; gate intacto.\n')
    cont.update(at=now.isoformat(),C6_labelled_manifest=str(D/'manifest.json'),partial_metered_cost_usd=str(total),own_live_process=None,
        C6_kimi_status='AUDITED_DICTIONARY_NOT_ADOPTED',C6_deepseek_status='AUDITED_NO_COEFFICIENT_DELIVERED',
        next=['C6 actual curved sector assembly within unchanged deadline','ORDEM015 PartB','Final audit/report'])
    put(cp,cont,True)
    print(json.dumps(dict(status='C6_ACTIVE',cost_known=str(total),audit_checks=checks,scalar_parallel=measurements['scalar_parallel/results.json'])),flush=True)
if __name__=='__main__':main()
