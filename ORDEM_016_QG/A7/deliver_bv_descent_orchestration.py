"""Record prepared reviews and exact local controls with byte custody."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent
OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
BASE=H.parents[1]/'IALD_ORQUESTRACAO_20260923'
D=H/'bv_descent_orchestration_delivery';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,replace=False):
    assert b
    if p.exists():
        assert replace,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        assert not backup.exists();backup.write_bytes(old);assert backup.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    temp.write_bytes(b);assert temp.read_bytes()==b;temp.replace(p)
def put(p,v,replace=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'),replace)
def append(p,v):write(p,p.read_bytes()+v.encode('utf-8'),True)
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
catalog=H/'orchestration_bv_descent/prepared_units.json'
units=json.loads(catalog.read_bytes())
ack=BASE/'state/handoffs/a7_bv_descent_pending_submissions.json'
assert ack.exists()
for row in units:
    assert sha(Path(row['payload']))==row['payload_sha256']
    assert row['request_id'] in ack.read_text('utf-8')
write(D/'coordinator_acceptance.json',ack.read_bytes())
results={name:json.loads((H/name/path).read_bytes()) for name,path in [
    ('localized_brst_anticommutator','results.json'),
    ('inhomogeneous_bv_consistency','results.json'),
    ('kimi_lorentzian_normalization_review','local_audit.json')]}
checks=sum(v['checks'] for v in results.values())
cpu=sum(v['cpu_seconds'] for v in results.values())
report=f'''[DERIVED — controles locais; novas revisões em STAGING; Q2 completa OPEN]

Acrescentadas duas unidades Kimi (descida BV/Ward localizada e contatos Euler
com contagem de grafos) e uma unidade MiMo (adjunção graduada do setor h,c).
As três prévias selecionaram o executor exigido; a coordenação confirmou os
IDs/bytes e a espera em FIFO. Aceitação em staging não é execução. Kimi e
MiMo já executavam outras unidades em paralelo na confirmação14:59:17UTC.
Foi solicitada prioridade condicional à unidade DeepSeek70e9 previamente
autorizada para aproveitar o terceiro executor; despacho ainda não confirmado
por esta entrega. Não houve novo pedido a Claude/Antigravity, nem treinamento.

As duas verificações locais de descida têm escopo preciso. Com
s0h=Gc, s1h=L_c h, s1c=w=c.dc, e s1_chi=chi*s1 nos geradores:
{{s0,s1_chi}}h=[G,chi]w=(d_mu chi)w_nu+(d_nu chi)w_mu.
São68 controles exatos, incluindo uma configuração não nula e chi constante.
Na convenção de fontes s0hdagger=E_h e
s0cdagger|hdagger=-G* hdagger, o termo hdagger de s0Vaf_chi é
-hdagger[G,chi]w. Portanto J_af^mu=-2hdagger^(mu,nu)w_nu.
Essa afirmação é condicional à convenção explicitada. Uma convenção canônica
com c*= -cdagger troca simultaneamente o sinal do termo c*w e da sua variação;
não muda por si só o sinal de qualquer loop de campos já calculado.
O Euler E_h precisa incluir b, como derivada da ação livre completa.

Em separado,20 controles numa álgebra exterior finita verificam a identidade
de Jacobi: I=(S,S)/2 e Q1=(S,W) implicam (S,Q1)+(W,I)=0.
Quando I não é zero, não é lícito omitir o segundo termo e exigir a identidade
homogênea por esse argumento. Não identificamos W com uma ação efetiva da
gravitação calculada. Não demonstramos cancelamento do resíduo local medido.
Restam a descida quântica/inserções EOM e suas normalizações de coincidência.
Antifields não ganham propagadores para completar diagramas artificialmente.

A resposta Kimi588 sobre passagem lorentziana foi recebida integralmente e
ledgerada uma vez. A auditoria exata42 verificações detectou quatro erros:
coeficiente da Hessiana8 versus4; identificação de (eps+i sigma)^(-1) com
ramo oposto; sinal de box(1/(sigma+i eps)); e confusão entre derivadas no
mesmo extremo e em extremos diferentes no comutador de extensão.
Logo a normalização lorentziana proposta não foi incorporada. A auditoria
não pretende demonstrar existência/normalização do limite distribucional.

Total desta entrega: {checks} controles locais, CPU{cpu}s; zero novas chamadas
remotas executadas por estes scripts. Gate intacto; originais/kernel intactos.
A7.b mantém prazo de despacho20:32UTC25/09; não prolongar por fila acumulada.
Abertura sha256={opening}.
'''
write(D/'DERIVACAO_E_ESTADO.md',report.encode('utf-8'))
write(OUT/'ENTREGA_016_A7b_descida_BV_e_novas_revisoes.md',report.encode('utf-8'))
paths=[catalog,H/'orchestration_bv_descent/manifest.json',D/'coordinator_acceptance.json',
    H/'localized_brst_anticommutator_check.py',H/'localized_brst_anticommutator/results.json',
    H/'inhomogeneous_bv_consistency_check.py',H/'inhomogeneous_bv_consistency/results.json',
    H/'kimi_lorentzian_normalization_review/manifest.json',
    H/'kimi_lorentzian_normalization_review/local_audit.json',D/'DERIVACAO_E_ESTADO.md',Path(__file__)]
manifest=dict(at=now.isoformat(),opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in paths],
    checks=checks,cpu_seconds=cpu,new_units=units,execution_status='STAGING_ACCEPTED',
    quantum_descent_complete=False,full_Q2=False,gate_changed=False)
put(D/'manifest.json',manifest)
ledger=OUT/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='BV_DESCENT_CONTROLS_AND_MORE_MODEL_UNITS',
    target='A7.b',checks=checks,cpu_seconds=cpu,prepared_units=3,
    manifest_sha256=sha(D/'manifest.json'),remote_call=False))+'\n')
continuity=H/'CONTINUIDADE.json';state=json.loads(continuity.read_bytes())
state['bv_descent_orchestration_update']=dict(at=now.isoformat(),manifest=str(D/'manifest.json'),
    catalog=str(catalog),status='STAGING_ACCEPTED',checks=checks,cpu_seconds=cpu,
    local_result='Classical antifield localization and abstract inhomogeneous consistency only',
    next='Compute full free-Euler time-ordered descendant contacts; review model responses without assuming cancellation',
    kimi_lorentzian_normalization='REJECTED_AS_VALIDATED_TRANSFER_AFTER_FOUR_ALGEBRAIC_ERRORS',
    deepseek_priority='CONDITIONAL_REQUEST_SENT_NOT_DISPATCH_CONFIRMED',gate_changed=False)
put(continuity,state,True)
seen=set();cost=Decimal(0)
for line in ledger.read_text('utf-8').splitlines():
    e=json.loads(line);v=e.get('cost_estimate_usd',e.get('cost_usd'))
    if v is None:continue
    key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(v))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESSO:3 revisões adicionais em staging;{checks} controles de descida/auditoria;CPU{cpu}s. Custo monetário conhecido parcial USD{cost};assinaturas não quantificadas;Q2 OPEN, gate intacto. Abertura sha256={opening}.\n')
for item in manifest['artifacts']:assert sha(Path(item['path']))==item['sha256']
print(json.dumps(dict(manifest=str(D/'manifest.json'),checks=checks,cpu_seconds=cpu,
    known_partial_cost_usd=str(cost),gate_changed=False),ensure_ascii=False))
