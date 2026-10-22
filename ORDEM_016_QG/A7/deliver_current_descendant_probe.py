"""Publish the restricted measured identity and preserve the live matrix handle."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'current_descendant_probe_delivery';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,existing=False):
    if p.exists():
        assert existing,p;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b)
    assert b and t.read_bytes()==b;t.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,indent=2,ensure_ascii=False).encode('utf-8'),existing)
def append(p,t):write(p,p.read_bytes()+t.encode('utf-8'),True)
v1=json.loads((H/'current_distributional_descendant_probe/results.json').read_bytes())
v2=json.loads((H/'current_distributional_descendant_probe_v2/results.json').read_bytes())
assert v2['comparison_zero'] and v2['bilocal_closed_off_diagonal']
cpu=v1['cpu_seconds']+v2['cpu_seconds'];opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — identidade distribucional medida na componente00; Q2 integral OPEN]

A diferença de consistência anteriormente medida na componente00 é reproduzida
exatamente pela descida da corrente de campo já construída. Foram mantidos os
cinco blocos e seus pesos: Ymetric/2, Ymixed, Yghost, Xmetric, Xmixed. Não se
escolheu tau, nem se ajustou coeficiente, nem se acrescentou grafo por analogia.

Se P_C é o núcleo da corrente estendida e F_C seu núcleo fora da diagonal,
escreva P_C=R(F_C)+A_C, onde A_C é o contato local já calculado. Variar o h
externo produz -(d_i+lambda_i)P_C. Com C_i(F)=R(d_iF)-d_iR(F), resulta

 -(d_i+lambda_i)R(F)=R(-(d_i+lambda_i)F)+C_i(F).

A parcela C_i(F) não está contida simplesmente na variação de A_C. É o
contato da derivada EXTERNA com a extensão. O coeficiente simétrico h_(i0)
entra uma vez quando i!=0 e duas quando i=0. Para cada orientação dos cutoffs
calculamos a soma correspondente, conservando x simbólico, não só um ponto.

Para lambda=(1,-1,0,0),eta=(1,0,0,0) e a ordem trocada, a parte bilocal
antissimetrizada da componente00 é identicamente ZERO como função racional
de x, com z=x.x. A descida é portanto local nesta componente. A multiplicação
do cutoff em X e a passagem ao operador local dão q->q-lambda e depois
q->D+lambda+eta, isto é, q->D+eta no contato adicional.

Somando a variação do contato antigo à nova parcela e aplicando a adjunção
ponderada D->-D-L, obteve-se exatamente o polinômio inteiro de grau5 antes
medido para a componente00 do defeito de h,c. Diferença: ZERO.
Controle em D=0: ambos -9259/1920, diferença0, nas unidades CE=-4pi².
Isto explica essa diferença como termo da identidade INHOMOGÊNEA; não diz
que o representante isolado virou cociclo homogêneo nem que a anomalia acabou.
A identificação geral com J2, outras componentes/cutoffs e o modelo curvo
continuam sob seus escopos; nenhuma classe de cohomologia foi promovida.

ERRATA PRESERVADA: v1 leu parts.Ymetric como se ainda faltasse o fator1/2.
O produtor full_current_contact_matrix.py já o aplicava. A leitura local v1
estava errada, embora os oito núcleos racionais e os contatos externos estivessem
corretos. V2 soma parts diretamente, verifica a soma contra polynomial e reutiliza
os oito núcleos, sem repetir loops. O predecessor e seu hash constam da V2.

Comandos: runtime SymPy A4, -X utf8 -B, scripts
current_distributional_descendant_probe.py e ..._v2.py. Ambos rc0 observados
nas ferramentas;18controles na V2;CPU conjunta{cpu}s. Não houve captura
independente de stdout em arquivo; resultados estruturados/checkpoints e hashes
estão preservados. O rc0 da v1 não aprova sua leitura de peso corrigida.

Ampliação registrada, ainda NÃO concluída: current_distributional_descendant_matrix.py,
session19789, processo próprio observado ativo. Calcula40componentes h/c nas duas
orientações e as16componentes de dois ghosts, reutilizando8núcleos. Não reiniciar
por demora; consultar o mesmo handle e depois seus resultados. Não presumir
que as16entradas repetirão a identidade00. Orquestração externa prossegue separada.
Originais/kernel/gate intactos. Abertura sha256={opening}.
'''
write(D/'DERIVACAO.md',report.encode('utf-8'))
write(OUT/'ENTREGA_016_MEDIDA_descida_distribucional_corrente_00.md',report.encode('utf-8'))
put(D/'EXECUTION_RECEIPT.json',dict(at=now.isoformat(),completed=[
 dict(script='current_distributional_descendant_probe.py',session_id=85678,rc=0,source='write_stdin terminal result'),
 dict(script='current_distributional_descendant_probe_v2.py',rc=0,source='exec_command result')],
 running=dict(script='current_distributional_descendant_matrix.py',session_id=19789,
 status='RUNNING_OBSERVED',source='exec_command session and first checkpoint'),
 independent_stdout_file=False))
paths=[Path(__file__),D/'DERIVACAO.md',D/'EXECUTION_RECEIPT.json']+[H/p for p in [
 'current_distributional_descendant_probe.py','current_distributional_descendant_probe_v2.py',
 'current_distributional_descendant_probe/results.json','current_distributional_descendant_probe_v2/results.json',
 'current_distributional_descendant_probe_v2/manifest.json',
 'current_distributional_descendant_matrix.py','current_distributional_descendant_matrix/PRE_REGISTER.json']]
put(D/'manifest.json',dict(at=now.isoformat(),checks=v2['checks'],cpu_seconds=cpu,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],full_Q2=False,gate_changed=False))
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='ACTUAL_CURRENT_DISTRIBUTIONAL_DESCENT_00',
 target='A7.b',checks=v2['checks'],cpu_seconds=cpu,remote_call=False,
 manifest_sha256=sha(D/'manifest.json')))+'\n')
cost=Decimal(0);seen=set()
for line in ledger.read_text('utf-8').splitlines():
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd'))
    if v is None:continue
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b MEDIDA: descida distribucional da corrente reproduz exatamente defeito00, sem ajuste;18checks,CPU{cpu}s. Matriz16 emexecucao session19789. Custo conhecido parcialUSD{cost}. Abertura sha256={opening}.\n')
p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
keys=['at','previous_goal_turn','completed_this_turn','next','pending_orchestration','partial_metered_cost_usd']
state.setdefault('head_history',[]).append({k:state.get(k) for k in keys})
state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['Actual distributional current descendant reproduces entire component00 defect without fitting',
 'V1 local subtotal factor error corrected in v2; raw kernels reused;18exact checks'],
 next=['Poll own live session19789, do not restart; inspect full16component matrix before claiming generalization',
 'Use actual insertion normalization rather than tau refitting; A2/J2 identification still needed',
 'Receive independent Kimi/MiMo reviews; A7b deadline20:32UTC; A7c/d,A8,PartB/final remain'],
 pending_orchestration='Coordinator polled91153 live16:07:12UTC: Kimi5e1 RUNNING; MiMoa46 awaiting new audited worker; other FIFO unchanged',
 partial_metered_cost_usd=str(cost))
state['current_descendant_probe_update']=dict(at=now.isoformat(),manifest=str(D/'manifest.json'),
 own_processes=[dict(session_id=19789,script=str(H/'current_distributional_descendant_matrix.py'),
 status='RUNNING_OBSERVED',do_not_restart=True)],component00_matches=True,
 full_matrix_not_yet_measured=True,full_Q2=False,gate_changed=False)
put(p,state,True)
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=v2['checks'],cpu_seconds=cpu,
 known_partial_cost_usd=str(cost),own_live_session=19789)))
