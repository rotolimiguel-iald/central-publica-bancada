"""Publish the measured tensor sub-block and preserve the live C6 checkpoint."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C6';H=ROOT/'A7'
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,write,put,append
now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
r=json.loads((D/'tensor_zerojet/results.json').read_bytes());a=json.loads((D/'tensor_zerojet/INVARIANT_AUDIT.json').read_bytes())
assert r['all_parametrix_equations_passed'] and r['endpoint_differences']==0
assert a['covariant_double_trace']=='4'
note=f'''[DERIVED+CAS — contato tensorial na primeira curvatura; Q2 completa OPEN]

AberturaSHA256={opening}.

Na continuação C6, mantém-se a prescrição parcial R_bal f/f, f/log e
a extensão com linha suave auditada. Modelo auxiliar euclidiano4D,
espaço-forma com K constante; nenhuma continuação causal física implícita.
Atuamos com sqrt(g)(roughBox-2K Id+2K g tr) somente na primeira linha
métrica H_ab,cd. Todos os índices são covariantes. Diferenciamos antes
de fixar y=0, incluindo duas conexões por ponta e a densidade.

As200 equações do parametrix passaram; os10000pares de componentes
coincidem nas duas pontas,484não nulos. Escrevendo
Si=(delta_ac delta_bd+delta_ad delta_bc-delta_ab delta_cd)/2 e
Ti=delta_ab delta_cd para i=(a,b,c,d), obtemos o coeficiente

 CE*K*[-Si Sj/8+(Si Tj-Ti Sj)/2] delta(x-y).

A decomposição das parcelas foi medida: primeira=-3Si/16-Ti/2,
segunda=Si/16+Ti/2. A segunda é a correção do propagador espectador;
o operador não age nele. Trocar qual linha recebe o operador dá a
expressão com i,j trocados; a soma é -CE*K*SiSj*delta/4.
Não se impõe simetria falsa a uma inserção com linha distinguida.

Controle de geometria: contrair com quatro deltas congelados dá-2.
O traço covariante usa inversas métricas em x e y; suas derivadas
multiplicam o contato principal3Box(delta)/32 e acrescentam+6.
Resultado4, igual a16vezes o contato escalarCE*K/4.
Independentemente, o traço bilocal completo de H dá-4vezes o perfil
escalar de potencial6K. Logo o confronto inclui os jatos da métrica.
Omitir densidade no componente0000 deixa diferença3/32 entre pontas;
inverter o sinal da conexão deixa resíduo racional não nulo fora da
diagonal. Auditoria:30408 controles exatos, CPU{a['cpu_seconds']}s.

A primeira auditoria falhou por usar x no lugar dos símbolos Q das
derivadas de delta; foi preservada. A v2 usa a representação correta
do motor existente. A tabela tensorial e seus coeficientes não mudaram.
CPU do cálculo:{r['cpu_seconds']}s. Estes números medem a execução,
não o tempo de raciocínio nem uma prova formal Lean.

Esta parcela reduz A7_Q2_CURVED_FULL_REPRESENTATIVE_PENDING. Não é
o inverso completo do bloco h,b, uma contração com vértices ou a
anomalia inteira; ainda faltam jatos de derivadas, montagem graduada,
ordemK² e a família temporal causal coerente. C6 continua ACTIVE.
Próximo cálculo já iniciado: até duas derivadas covariantes ordenadas
na pontaY das duas linhas. As respostas externas terão confronto
independente; não são promovidas por consenso. Nenhum original/gate tocado.
'''
write(D/'tensor_zerojet/DERIVACAO.md',note.encode())
write(OUT/'ENTREGA_016_MEDIDA_C6_tensor_Euler_primeira_curvatura.md',note.encode())
files=[D/'tensor_euler_zerojet.py',D/'audit_tensor_contact.py',D/'audit_tensor_contact_v2.py',D/'tensor_zerojet/results.json',D/'tensor_zerojet/INVARIANT_AUDIT.json',D/'tensor_zerojet/manifest.json',D/'tensor_zerojet/INVARIANT_MANIFEST.json',D/'tensor_zerojet/DERIVACAO.md']
put(D/'tensor_zerojet/DELIVERY_MANIFEST.json',dict(at=now.isoformat(),files=[dict(path=str(p),sha256=sha(p)) for p in files],full_Q2=False))
jobs=[dict(provider='mimo',request_id='f5eb94de-f1d6-43f9-add9-a5a236da3aeb',job_id='78e92782-75b2-4c66-91d8-038e450213c0',execution_task_id='b63936d4-a5a0-4180-b57d-ecca92dd69da'),
dict(provider='kimi',request_id='d3e54887-e65f-4d18-84b7-378611f72944',job_id='8b3884ac-d156-4843-9772-26bed53f525b',execution_task_id='62b777bd-b815-4cab-a3d7-371ed521e4a1'),
dict(provider='deepseek',request_id='e7239010-000d-4afa-ac6e-a54fda9189ba',job_id='b2c22962-38e5-4897-8204-164fdb8d2d6f',execution_task_id='c7c979cd-a963-4aab-938c-2f3512cdcc48')]
put(D/'orchestration/DISPATCH_REPORTED.json',dict(at=now.isoformat(),source_thread='01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
    source='Official inter-thread message: operator confirmed exact payloads; same reviewed worker accepted',status='RUNNING_REPORTED_BY_COORDINATOR',
    prior_rejections_retained=True,alternate_dispatch_performed=False,jobs=jobs))
append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='C6_TENSOR_ZEROJET_MEASURED',target='C6',remote_call=False,checks=r['checks']+a['checks'],cpu_seconds=r['cpu_seconds']+a['cpu_seconds'],manifest_sha256=sha(D/'tensor_zerojet/DELIVERY_MANIFEST.json')))+'\n'+
    ''.join(json.dumps(dict(at=now.isoformat(),event='C6_EXECUTION_RUNNING_REPORTED',source='official coordinator message',tokens=None,cost_usd=None,**job))+'\n' for job in jobs))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | C6 ACTIVE: tensorO(K),200equacoes/10000pares;30408controles;traco covariante -2+6=4 | CPU{r["cpu_seconds"]+a["cpu_seconds"]}s;semnova cobrança medida |3executores RUNNING reportados;Q2OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),C6_status='ACTIVE',C6_start=str(D/'START.json'),C6_tensor_manifest=str(D/'tensor_zerojet/DELIVERY_MANIFEST.json'),C6_jobs=jobs,
    C3_final_critique_status='AUDITED_AND_DELIVERED',C3_final_critique=str(ROOT/'C3/final_critique/manifest.json'),
    own_live_process=dict(session_id=32071,script=str(D/'tensor_euler_yjet_check.py'),log=str(D/'tensor_yjet_run.log')),
    next=['C6 tensor covariant derivative jets and Ward assembly within deadline','ORDEM015 PartB','Finalaudit/report'])
put(p,c,True)
print(json.dumps(dict(status='C6_ACTIVE',manifest_sha256=sha(D/'tensor_zerojet/DELIVERY_MANIFEST.json'))))
