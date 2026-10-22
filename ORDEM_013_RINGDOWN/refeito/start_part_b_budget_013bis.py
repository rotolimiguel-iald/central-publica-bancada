"""Register a conservative continuous wall-clock envelope before Part B computation."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json,sys
B=Path(__file__).resolve().parents[1];D=B.parent/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
p=B/'bis/PART_B_BUDGET_START.json'
if '--status' in sys.argv:
    d=json.loads(p.read_bytes());now=datetime.now(timezone.utc)
    elapsed=(now-datetime.fromisoformat(d['started_utc'])).total_seconds()/3600
    print(json.dumps(dict(started_utc=d['started_utc'],deadline_utc=d['hard_deadline_utc'],hours_elapsed=elapsed,hours_remaining=max(0,40-elapsed),within_budget=elapsed<40)));raise SystemExit
if p.exists():raise FileExistsError(p)
ma=D/'ENTREGA_013BIS_MA_fechamento.md';receipt=B/'bis/M6_MA_DELIVERY_MANIFEST.json'
r=json.loads(receipt.read_bytes())
for name,h in r['files'].items():
    if sha(Path(name))!=h:raise ValueError('Part A changed: '+name)
if str(ma) not in r['files']:raise ValueError('MA absent')
now=datetime.now(timezone.utc)
d=dict(status='PART_B_STARTED__NO_BLIND_DATA_AUTHORIZED_BEFORE_E2',started_utc=now.isoformat(),hard_deadline_utc=(now+timedelta(hours=40)).isoformat(),authorized_wall_hours=40,accounting='Conservative continuous wall time from this receipt, including orchestration and reviews; simultaneous workers count once. Part A and diagnostic jobs started before this receipt excluded as jobs, but overlapping elapsed wall time is still charged.',initial_envelope_hours={'E0_E1_existing_data':2,'E2_E5_E4_registration_and_light_controls':2,'E3_1_pilot_maximum':10,'E3_2_E3_3_calibration_and_blind_events_reserve':24,'test_E6_E7_final':2},allocation_scope='Provisional upper bounds before any Part B compute; E3.2 replaces reserves using actual pilot cost, without extending the fixed deadline. No guarantee to consume all budget.',old_jobs_policy='No heavy job before E3.1 termination of own old groups; lightweight existing-data calculations only meanwhile.',blind_gate='E2 registered hash and tunnel witness required before PE of blind events or reading posterior published after 2026-09-22.',ma_sha256=sha(ma),part_a_manifest_sha256=sha(receipt),opening_sha256=sha(D/'ENTREGA_013BIS_ABERTURA_operador.md'),code_sha256=sha(Path(__file__)))
new(p,(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
note=f'''[INPUT — orçamento autorizado; REAL — início contábil da Parte B, sem dado de teste]

# Início do orçamento de 40 horas

UTC {d['started_utc']}; limite absoluto conservador {d['hard_deadline_utc']}. Conta-se parede contínua, inclusive coordenação e revisão, sem multiplicar workers. A Parte A terminou antes deste carimbo. Processos antigos não ampliam o orçamento e nenhum novo job pesado começa antes de E3.1.

PAGO: envelope registrado antes da computação B: E0/E1 2h; E2/E5/E4 2h; piloto até10h; reserva calibração/cegos24h; teste/quadro/módulo/final2h. E3.2 registrará alocação pelo custo real do piloto dentro do mesmo prazo. NÃO PAGO ainda: qualquer computação, registro E2, piloto e calibração. Nenhuma leitura escolhida, nenhum teste cego iniciado.

Arquivo `{p}` SHA256 `{sha(p)}`. MA SHA256 `{sha(ma)}`. Abertura SHA256 `{d['opening_sha256']}`. Reprodução contábil: `python -B "{Path(__file__)}" --status`. Sem tentativa de instalação, escrita canônica ou posterior novo. Axiomas: N/A — sem Lean. Esta é nota operacional; não substitui B1–B5 nem o contrato final.
'''
target=D/'ENTREGA_013BIS_INICIO_ORCAMENTO_40H.md';new(target,note.encode())
print(json.dumps(dict(started_utc=d['started_utc'],hard_deadline_utc=d['hard_deadline_utc'],budget_sha256=sha(p),witness_sha256=sha(target))))
