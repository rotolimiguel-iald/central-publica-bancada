"""Custody, independent-response audit, and conditional nonminimal result."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import ast,hashlib,json,time,uuid
import sympy as s

H=Path(__file__).resolve().parent
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'nonminimal_wick_delivery'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
    assert b
    if p.exists():
        assert replace,p
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
def put(p,obj,replace=False):write(p,json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8'),replace)
def append(p,text):
    old=p.read_bytes();write(p,old+text.encode('utf-8'),True);assert p.stat().st_size>len(old)

def main():
    D.mkdir(exist_ok=False)
    source=BASE/'state/handoffs/8669aebb-1631-449e-8f61-6155ad7e79fc_delivery.json'
    j=json.loads(source.read_bytes())['job'];e=j['execution'];r=e['result']
    assert e['status']=='result_ready'
    write(D/'MIMO_ORIGINAL.md',r['text'].encode('utf-8'))
    put(D/'MIMO_RECEIPT.json',dict(request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],
        source_sha256=sha(source),response_sha256=sha(D/'MIMO_ORIGINAL.md'),
        prompt_sha256=hashlib.sha256(j['prompt'].encode('utf-8')).hexdigest(),
        usage=r['usage'],cost_estimate_usd=r['cost_estimate_usd'],canonical_memory=r.get('canonical_memory')))
    start=time.process_time();checks=[]
    # Reuse pure graded-polynomial utilities only, not a module with top-level writes.
    src=H/'antifield_quadratic_primitive_check.py';names={'clean','add','scale','mul','atom'}
    nodes=[n for n in ast.parse(src.read_text('utf-8')).body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns={'s':s};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),ns)
    clean,add,scale,mul,atom=[ns[n] for n in ['clean','add','scale','mul','atom']]
    def odd_derivative(a,i):
        d={}
        for mon,v in a.items():
            if i in mon:
                k=mon.index(i);key=mon[:k]+mon[k+1:]
                d[key]=d.get(key,0)+(-1)**k*v
        return clean(d)
    def eq(name,a,b):
        assert s.cancel(a-b)==0,(name,a,b);checks.append(name)
    x,w,y=s.symbols('x w y');c,barc=atom(0),atom(1)
    # qx=c: the graded bracket of two odd operators is an anticommutator.
    actual=odd_derivative(c,0).get((),0)
    eq('odd derivative bracket on x is plus one',actual,1)
    assert actual!=-1;checks.append('ungraded minus formula rejected for odd derivative')
    product=mul(c,barc)
    left_order=scale(odd_derivative(odd_derivative(product,1),0),w/2)
    left_order=add(left_order,scale(odd_derivative(odd_derivative(product,0),1),-w/2))
    eq('written C_H ordered left derivatives contract cbarc to minus H',left_order.get((),0),-w)
    reverse_order=scale(odd_derivative(odd_derivative(product,0),1),w)
    eq('bench pair contraction uses opposite derivative order',reverse_order.get((),0),w)
    # The even toy in the reply is correct in its own sign convention.
    eq('reply even toy qdagger=-x gives plus w',-w*s.diff(-x*x,x,2)/2,w)
    eq('bench even toy qdagger=+x gives minus w',-w*s.diff(x*x,x,2)/2,-w)
    jet=x*x*y+x*y*y
    for i in range(3):
        for k in range(3-i):eq('smooth two-jet vanishes '+str((i,k)),s.diff(jet,x,i,y,k).subs({x:0,y:0}),0)
    eq('third mixed jet survives',s.diff(jet,x,2,y,1).subs({x:0,y:0}),2)
    audit=dict(at=now.isoformat(),checks=len(checks),cpu_seconds=time.process_time()-start,
        accepted=['PH can contribute through antifields even when field Ward defect is zero',
            'Initial C(Faf)=0 does not imply C(qFaf)=0','State/parametrix/normalization must be separated',
            'Even toy result is correct with qdagger=-x'],
        corrections=['The displayed commutator with an odd derivative lacks the graded sign',
            'Written left derivative order gives C(cbarc)=-H_cbarc; cannot transfer pair signs unchanged',
            'Its even toy does not fix odd derivative signs',
            'q(cdagger) contains second derivatives of barc for Q=nabla²+3K, not only first',
            'A second derivative on one covariance slot plus a first on the other requires a third mixed jet',
            'qhat1 is not arbitrary after the reference differential has been fixed',
            'A smooth bisolution shift alone is not necessarily a positive physical state'],
        verdict='PARTIAL_STRUCTURAL_ACCEPTANCE_COMPONENT_SIGNS_NOT_ADOPTED',
        full_Q2=False,gate_changed=False)
    put(D/'MIMO_AUDIT.json',audit)
    calc=json.loads((H/'nonminimal_wick_heat_ward/results.json').read_bytes())
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    report=f'''[DERIVED — jatos completos no setor antifield, prescrição euclidiana explícita; Q2 OPEN]

# A derivada do bloco misto participa da primeira ordem

Usamos o espaço-forma4D, K constante, os operadores mínimos Lh e Lq já
calculados e Hr=U0/z-U1 log(z/l²)/4+U2 z log(z/l²)/16+..., sem acrescentar
parte suave. Todos os números abaixo usam coeficiente comum de1/z igual a1;
o normalizador físico e a continuação lorentziana NÃO foram fixados aqui.

Da apresentação graduada068/069, transportada apenas como identidade de
blocos, Hfull tem hh=HD=-4κ Hh Itr, hb=Kg HQ, bh=HQ Kg*, bb=0,
cbarc=HQ, barcc=-HQ. ell=1/(2κ), D=H0+ell C*C. Defina

 S=ell C HD-HQ Kg*.
 (P Hfull)_hh=D HD-C*S, (P Hfull)_bh=S/ell,
 (P Hfull)_bb=(P Hfull)_cc=(P Hfull)_barcbarc=Q HQ.

A primeira igualdade mostra por que não bastava inserir3U2/4 diretamente.
S vale zero no ponto por isotropia, mas sua DERIVADA pode ser não nula.
Nenhum estado do fundo distinto de068 foi transferido para este modelo.

# O primeiro jato misto foi calculado

O entrelaçamento Lh Kg=Kg Lq implica, por unicidade formal de transporte do
calor, B_n=A_(n+1)/4, onde B_n=div_x U_h,n+sym nabla_y U_q,n e A_n usa
os mesmos slots com nabla z. A0=0. Diferenciando o parametrix, os termos
1/z e log(z) cancelam, restando B_H=A2/16+O(r³log r).
Como S=-2B_H, seu primeiro jato é -nabla A2/8. Usando os U2 já medidos:

 [nabla_lambda S_nu](h)=K²[-25g_lambda,nu tr(h)/12+10h_lambda,nu/3],
 [C*S]=K²[-10P_TL/3-5P_tr].

O passo de transporte teve um controle independente em16 componentes:
os segundos jatos ORDENADOS de U1h e U1q reproduzem nabla A2/4.
O jato misto do calor é -xx_ji por Synge; não foi confundido com o jato
logarítmico do Green (a2 delta/2-xx_ji). A identidade formal de calor é
hipótese/derivação escrita; o CAS confere estes jatos e a álgebra, não constrói
um estado global nem prova microlocalmente toda a expansão infinita.

Na convenção da bancada qhdagger=H0h+C*b e qcdagger=-Qbarc-Kg*hdagger,
os slots estendidos tornam-se

 Jh0=K²(137P_TL/60+579P_tr/20), Jc0=179K²I4/20.

Jh1/Jc1 têm posto ímpar e zeram sob a covariância natural/paridade assumidas.
Para Faf=int chi(hdagger Lie_c h+cdagger_i c^j nabla_j c^i):

 A1(Faf)/(i hbar)=(337/10)K² int chi div(c).

A expressão recebe ainda o fator comum de normalização física da covariância.
Ignorar C*S daria81/5; a contribuição perdida é35/2, todos multiplicados porK².
A primitiva algébrica deste setor é337K² int chi tr(h)/20, pois qtrh=2divc.
Não é ainda escolha de contratermo: admissibilidade, realidade e continuação
precisam acompanhar o dicionário físico. Inventário de todoV1 e Q2 permanecem
separados. São{calc['checks']}controles exatos, CPU{calc['cpu_seconds']}s, rc0.

# Revisão independente MiMo87d recebida e auditada

O MiMo identificou corretamente o canal antifield-Euler e a insuficiência
de C(Faf)=0. Seu teste par qdagger=-x dá+w e foi mantido nessa convenção.
Não adotamos os sinais compactos: a fórmula escrita para[q,partial_odd]
omite o sinal graduado. Contraexemplo qx=c: [q,partial_c]_graded x=+1;
a fórmula escrita daria-1. A ordem das derivadas ímpares no C_H escrito
também dá C(cbarc)=-H_cbarc, exigindo dicionário antes de transferir sinais.
Além disso, Qbarc contém duas derivadas; com a derivada do outro slot,
precisam-se jatos mistos de ordem3. x²y+xy² tem todos os jatos≤2 nulos
na origem e derivada xxy=2: o limite de ordem2 da resposta não basta.
São{audit['checks']}controles locais; detalhes e original preservados.

DeepSeek recebeu para admissão uma revisão cética distinta do jato misto
e do coeficiente337/10; preview selecionou o executor requerido. Kimi
mantém os pedidos existentes sujeitos à recuperação real da quota5h.
Nenhum original, kernel ou gate alterado. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO_E_AUDITORIA.md',report.encode('utf-8'))
    write(OUT/'ENTREGA_016_MEDIDA_Wick_nao_minimal_primeiro_jato.md',report.encode('utf-8'))
    put(D/'EXECUTION_RECEIPT.json',dict(command='A4/symbolic_runtime/Scripts/python.exe -B nonminimal_wick_heat_ward_check.py',
        observed_exit_code=0,results_sha256=sha(H/'nonminimal_wick_heat_ward/results.json'),
        note='Receipt of observed tool execution, not a reconstructed raw stdout log'))
    paths=[Path(__file__),D/'MIMO_ORIGINAL.md',D/'MIMO_RECEIPT.json',D/'MIMO_AUDIT.json',
        D/'DERIVACAO_E_AUDITORIA.md',D/'EXECUTION_RECEIPT.json',
        H/'nonminimal_wick_heat_ward/results.json',H/'nonminimal_wick_heat_ward/manifest.json']
    totalchecks=calc['checks']+audit['checks'];cpu=calc['cpu_seconds']+audit['cpu_seconds']
    put(D/'manifest.json',dict(at=now.isoformat(),artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],
        checks=totalchecks,cpu_seconds=cpu,full_Q2=False,gate_changed=False))
    ledger=OUT/'LEDGER_016.jsonl';entries=[json.loads(v) for v in ledger.read_text('utf-8').splitlines()];events=[]
    if not any(v.get('execution_task_id')==e['id'] for v in entries):
        events.append(dict(at=now.isoformat(),event='EXTERNAL_REVIEW_RECEIVED_AND_AUDITED',target='A7.b',
            provider='mimo',request_id=j['request_id'],job_id=j['id'],execution_task_id=e['id'],usage=r['usage'],
            cost_estimate_usd=r['cost_estimate_usd'],response_sha256=sha(D/'MIMO_ORIGINAL.md'),
            accepted=audit['verdict']))
    events.append(dict(at=now.isoformat(),event='NONMINIMAL_WICK_FIRST_JET_MEASURED',target='A7.b',
        checks=totalchecks,cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json'),remote_call=False))
    append(ledger,''.join(json.dumps(v,ensure_ascii=False)+'\n' for v in events))
    cost=Decimal(0);seen=set()
    for item in entries+events:
        value=item.get('cost_estimate_usd',item.get('cost_usd'))
        if value is None:continue
        key=item.get('execution_task_id') or item.get('job_id') or item.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(value))
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: primeiro jato misto Ward e slots antifield não mínimos medidos; coeficiente337/10 K² na prescrição euclidiana normalizada. {totalchecks}controles CPU{cpu}s. MiMo87d auditado parcialmente; DeepSeek6945 preparado para cético. Custo conhecido parcialUSD{cost}. Q2 OPEN; aberturaSHA256={opening}.\n')
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=[
        'Nonminimal first Ward jet from heat intertwining with independent U1 checks',
        'Normalized auxiliary Euclidean antifield coefficient337/10 K² with linear primitive',
        'MiMo87d received/audited; graded-sign and third-jet corrections preserved'],
        next=['Receive DeepSeek6945 independent coefficient review',
            'Check full V1 inventory and physical covariance normalization before exporting coefficient',
            'Connect to localized A2 dictionary and WZ, without equating primitive with admissible counterterm',
            'A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
        pending_orchestration='MiMo87d complete/audited; DeepSeek6945 prepared/sent coordinator; Kimi3 await actual quota recovery',
        partial_metered_cost_usd=str(cost))
    state['nonminimal_wick_update']=dict(manifest=str(D/'manifest.json'),A1_Faf_normalized_coefficient='337/10 K²',
        euclidean_auxiliary=True,full_Q2=False,own_processes=[])
    state['latest_verified_orchestration']['mimo_next']['status']='COMPLETED_RECEIVED_AUDITED_PARTIAL'
    state['latest_verified_orchestration']['own_live_processes']=[]
    state['latest_verified_orchestration']['deepseek_next']=json.loads((H/'orchestration_nonminimal_heat_ward/prepared_units.json').read_bytes())[0]
    put(p,state,True)
    for a in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(a['path']))==a['sha256']
    print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=totalchecks,cpu_seconds=cpu,known_partial_cost_usd=str(cost)),ensure_ascii=False))

if __name__=='__main__':main()
