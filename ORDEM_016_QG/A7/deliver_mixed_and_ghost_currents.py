"""Publish partial current computations; preserve failed v1 and all prior results."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'mixed_ghost_current_delivery';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw,existing=False):
    if p.exists():
        assert existing
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);assert not bak.exists()
        bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw)
    assert len(raw)>0 and t.read_bytes()==raw;t.replace(p)
def put(p,obj,existing=False):write(p,json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8'),existing)
def txt(p,t):write(p,t.encode('utf-8'))
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
b=json.loads((H/'mixed_b_h_current_v2/results.json').read_bytes())
g=json.loads((H/'ghost_current_insertion/results.json').read_bytes())
checks=b['checks']+g['checks'];cpu=b['cpu_seconds']+g['cpu_seconds']
ledger=OUT/'LEDGER_016.jsonl';events=[json.loads(l) for l in ledger.read_text('utf-8').splitlines() if l.strip()]
seen=set();cost=Decimal(0);items=[]
for row in events:
    value=row.get('cost_estimate_usd')
    if value is None:value=row.get('cost_usd')
    if value is None:continue
    key=row.get('execution_task_id') or row.get('job_id') or row.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(value));items.append(dict(key=key,amount=str(value)))
put(D/'cost_summary.json',dict(at=now.isoformat(),known_estimated_usd=str(cost),items=items,
    scope='Partial priced provider estimates, not invoice; unknown calls/subscription not zero'))

txt(D/'DERIVACAO.md',f'''[DERIVED — blocos planos de correntes calculados; Q2 OPEN]

## Normalização livre antes da contração

Use10 componentes simétricas, Gram R=diag(2-delta_ab), reversão de traço Itr
e S=Itr R^-1. Para símbolos diferenciais reais p, escreva Gc=p_a c_b+p_b c_a,
C(h)=p.h-p trh/2, q=p.p e E=-q Itr+Itr G C.
A matriz bosônica da ação é P=[[R E/(4kappa),-C^T],[C,-2kappa I]].
A inversa simbólica é P^-1=(1/q)[[-4kappa S,G],[-G^T,0]].
CAS verificou os DOIS produtos, com p e kappa simbólicos, além de CG=q I,
EG=0 e CS=G^T/2. O sinal inferior vem do adjunto formal de uma derivada.
Isso realiza a fórmula BV069; o zero b-b não elimina a linha mista b-h.

O vértice raw quadrático do motor em momentos Fourier(p,-p) foi comparado
com -2 R E em todos100 pares de fibras e dois momentos não axiais.
Assim o sinal de símbolos diferenciais não foi confundido com o de i.p.
Raw V3=16kappa V3fisico, GD=-4kappa S GQ e Ghb=G GQ dão fator-1/4
para UM emparelhamento ordenado X(h,h)-Y(b,h), antes dos fatoriais do diagrama.
Esse fator vem da inversão/ação; não foi escolhido para zerar resultado.

## Corrente mista

Jb^mu=b_nu[Z_mu,nu-delta_mu,nu trZ/2], Z=L_c h.
Seu vértice foi expandido em b_nu, h_ab, suas derivadas e c_r, dc_r.
160 comparações simbólicas verificam a expansão para todos r,nu,ab.
O vértice EH emX inclui a fronteira -8dchiX.b3. A contração preserva as
duas orientações b-h; elas foram medidas iguais. O engine retorna UMA
orientação. Somar ambas e ainda incluir o fatorial1/2 é uma decisão que
deve sair da expansão de Wick global, não de comparação numérica.
575checks, CPU{b['cpu_seconds']}s, rc0.

## Corrente ghost

Jgh^mu=(d_mu barc_nu)c^rho d_rho c^nu
 -barc_nu(d_mu c^rho)d_rho c^nu-barc_nu c^rho d_mu d_rho c^nu.
No produto ordenado(barX,cX,barY,cYA,cYB), as duas escolhas de cY externo
têm sinais totais-,+ (incluindo <barX cY>=-GQ). Uma álgebra exterior
independente calculou Gamma_G²/2 sobre o monômio de cinco geradores e
recuperou esses sinais. Inverter a covariância muda ambos os resultados.
As duas contrações dirigidas foram incluídas, com fronteira ghost emX e
adjunção dos jatos de h_X e c_Y. Omitir qualquer uma altera o controle.
286checks, CPU{g['cpu_seconds']}s, rc0.

## Números no escopo declarado

Para h11,c0, x=(1,2,-1,1) e contato emq=(2,1,0,0), unidade CE=-4pi²:

| jatos(lambda,eta) | b-h ordenado fora diagonal | contato b-h | ghost fora diagonal | contato ghost |
|---|---:|---:|---:|---:|
| (0,0) |0|0|0|0|
| (0,e0) |-128/16807|259/192|2671/117649|-4391/3840|
| (e0-e1,e0) |1222/16807|35/32|-4941/235298|-2651/3840|

A extensão é a prescrição anterior R=FP[(1-a)mu^(2a)z^a], com C_D=RD-DR
e transferência completa q->q-lambda. Os polinômios completos estão nos JSON.
Não somamos esses blocos como Q2: faltam pesos globais conferidos, curvatura,
partes suaves/tadpoles e demais aridades/continuação causal exigidas na A7b.

Falha inicial preservada: eta=0 deixa soma vazia, int0 sem método subs.
v2 muda apenas o acumulador de contato para Integer(0). Não mudou coeficiente.
Script/check/log v1 e diagnóstico permanecem com hashes no manifesto.

Total{checks}checks, CPU{cpu}s. Nenhuma chamada externa nova nesta computação.
Custo externo conhecido recontado no ledger:US${cost}, parcial/estimativa,
não fatura; assinaturas e chamadas sem consumo informado continuam desconhecidas.
Originais, um.py, kernel e gate não foram alterados.
Abertura sha256:{opening}.
''')
txt(OUT/'ENTREGA_016_A7b_correntes_mista_e_ghost.md',f'''[DERIVED — duas contribuições locais explícitas; Q2 OPEN]

Verificada a inversa bosônica14x14 nos dois sentidos, com símbolos arbitrários:
GD=-4kappa S/Q, Ghb=G/Q, Gbh=-G^T/Q, Gbb=0. Logo b-b=0 não elimina b-h.
Construída a inserção b.Zbar contra EH localizado, fator-1/4 por contração
ordenada derivado da ação. Construída a inserção ghost com seus dois
emparelhamentos Grassmann, sinais-,+ conferidos por álgebra exterior.

{checks} verificações exatas, rc0; CPU{cpu}s. A soma ainda exige pesos globais
da Ward, revisão independente, curvatura/estado suave/aridades. Não é Q2 completa.
V1 do teste misto falhou em int0.subs; preservada, corrigida emv2 sem mudar física.
Prova, tabela de contatos e hashes:{D/'DERIVACAO.md'}; manifest.json ao lado.
US${cost} estimados conhecidos no ledger, parcial; zero nova chamada nesta rodada.
Próximo: ligar os pesos derivados, conferir revisão dos modelos e completar
as contribuições dentro do timeboxA7b. Nenhum gate alterado.
Abertura sha256:{opening}.
''')
txt(OUT/'ENTREGA_016_MEDIDA_corrente_mista_zero_tipado.md',f'''[REAL — falha de implementação corrigida ao lado]

Comando v1:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/mixed_b_h_current_check.py.
rc1:AttributeError 'int' object has no attribute 'subs' no contato com eta=0.
Log:{H/'mixed_b_h_current_run.log'}; sha256:{sha(H/'mixed_b_h_current_run.log')}.
v2 usa Integer(0), preserva todo coeficiente e passa575checks,CPU{b['cpu_seconds']}s,rc0.
Logv2:{H/'mixed_b_h_current_run_v2.log'};sha256:{sha(H/'mixed_b_h_current_run_v2.log')}.
Próximo dentro deA7b: montagem dos pesos das correntes com pares/fonte.
Nenhuma nova chamada externa. Custo estimado conhecido parcialUS${cost}.
Abertura sha256:{opening}.
''')
files=[Path(__file__),D/'DERIVACAO.md',D/'cost_summary.json',
    OUT/'ENTREGA_016_A7b_correntes_mista_e_ghost.md',OUT/'ENTREGA_016_MEDIDA_corrente_mista_zero_tipado.md',
    H/'mixed_b_h_current_failure.json',H/'mixed_b_h_current_engine.py',H/'mixed_b_h_current_check.py',H/'mixed_b_h_current_run.log',
    H/'mixed_b_h_current_engine_v2.py',H/'mixed_b_h_current_check_v2.py',H/'mixed_b_h_current_run_v2.log',H/'mixed_b_h_current_v2/manifest.json',H/'mixed_b_h_current_v2/results.json',
    H/'ghost_current_insertion_engine.py',H/'ghost_current_insertion_check.py',H/'ghost_current_insertion_run.log',H/'ghost_current_insertion/manifest.json',H/'ghost_current_insertion/results.json']
put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,
    gate_changed=False,full_Q2=False,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
event=dict(at=now.isoformat(),event='MIXED_BH_AND_GHOST_CURRENTS_COMPUTED',target='A7.b',
    checks=checks,cpu_seconds=cpu,rc=0,manifest_sha256=sha(D/'manifest.json'),remote_call=False)
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
progress=OUT/'ENTREGA_016_PROGRESSO.md';cont=H/'CONTINUIDADE.json';v=json.loads(cont.read_bytes())
elapsed=(now-datetime.fromisoformat(v['at'])).total_seconds()/3600
write(progress,progress.read_bytes()+f'\r\n- {now.isoformat()} A7.b PROGRESS: correntes mista575+ghost286={checks}checks;CPU{cpu}s;bancada{elapsed:.6f}h;parcialUS${cost};pesos globais/Q2 OPEN.\r\n'.encode(),True)
v.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
    completed_this_turn=['Bosonic inverse and mixed-current575checks; graded ghost-current286checks'],
    mixed_ghost_current_manifest=str(D/'manifest.json'),scientific_partial_metered_cost_usd=str(cost),
    next=['Derive and cross-check complete Ward weights without fitting cancellations',
          'Compare independent Kimi/MiMo replies with local current diagrams',
          'Curvature,smooth,tadpoles,higher arities within A7b deadline20:32UTC',
          'A7c/d,A8,PartB015 and final complete audit remain'])
put(cont,v,True)
for artifact in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(artifact['path']))==artifact['sha256']
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,known_partial_usd=str(cost),manifest=str(D/'manifest.json'),verified_files=len(files))))
