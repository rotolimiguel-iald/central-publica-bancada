"""Deliver exact counterexample and reconcile already-established Fourier phase."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import hashlib,json,uuid
H=Path(__file__).resolve().parent;D=H/'deepseek_cutoff_audit';O=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b,new=False):
 if new:assert not p.exists(),p
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex)
  bak.write_bytes(old);assert bak.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def append(p,v):write(p,p.read_bytes()+v.encode())
m=D/'manifest.json'
for row in json.loads(m.read_bytes())['artifacts']:assert sha(Path(row['path']))==row['sha256']
r=json.loads((D/'results.json').read_bytes());log=H/'deepseek_cutoff_audit_run.log'
assert json.loads(log.read_text('utf-8-sig').splitlines()[-1])==r
receipt=json.loads((D/'RECEIPT.json').read_bytes());ledger=O/'LEDGER_016.jsonl'
rows=[json.loads(v) for v in ledger.read_text('utf-8-sig').splitlines() if v.strip()]
if not any(v.get('execution_task_id')==receipt['execution_task_id'] for v in rows):
 append(ledger,json.dumps(receipt,ensure_ascii=False)+'\n');rows.append(receipt)
cost=Decimal(0);seen=set()
for row in rows:
 v=row.get('cost_estimate_usd')
 if v is None:v=row.get('cost_usd')
 if v is None:continue
 k=row.get('execution_task_id') or row.get('job_id') or row.get('request_id')
 if k and k in seen:continue
 if k:seen.add(k)
 cost+=Decimal(str(v))
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],
 command='A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/deepseek_cutoff_audit_check.py',rc=0,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in [m,log,D/'DERIVACAO.md',Path(__file__)]],
 partial_metered_cost_usd=str(cost),full_Q2=False)
p=D/'delivery_manifest.json';write(p,json.dumps(manifest,ensure_ascii=False,indent=2).encode(),True)
note=f'''[DERIVED — cutoff corrigido no parecer; fase do par já resolvida]

{now.isoformat()}. Abertura SHA256 {opening}.

DeepSeek omitiu [N,chi]/2 ao variar a primitiva localizada. O controle
integrado exato confirma a fórmula da bancada Mchi=(chiN+Nchi)/2:
o termo omitido/C_E é {r['omitted_term_over_C']}. No mesmo exemplo,
integral h.[N,chi]h=0; portanto essa nulidade não salva a variação mista.

Foram{r['checks']} controles novos, CPU{r['cpu_seconds']}s, rc0.
Reutilizados, com hashes conferidos:528 controles prévios do cutoff,
30 da fase menos e134 da fase mais. Não foram executados novamente.

A pendência ímpar do parecer Fourier era de convenção: no par a perna
móvel usa exp(+ipx), cuja fase é i^m; a transformada isolada exp(-ipx)
usa (-i)^m. O rastreio completo do gerador já existe e foi recuperado.
Não é preciso outro motor nem alterar coeficientes do par.

Nota: {D/'DERIVACAO.md'}.
Manifesto: {p}; SHA256 {sha(p)}. Log SHA256 {sha(log)}.
Parecer DeepSeek estimado US${receipt['cost_estimate_usd']}; total
parcial medido da missão US${cost}, não fatura nem custo integral.
Nenhuma chamada nova nesta auditoria. Q2 completa OPEN; gate intacto.
'''
write(O/'ENTREGA_016_A7b_cutoff_auditado_e_fase_reconciliada.md',note.encode(),True)
measure=f'''[REAL — MEDIDA da eliminação indevida do comutador]

{now.isoformat()}. Abertura SHA256 {opening}.
Hipótese testada do parecer: antiadjunticidade elimina o termo do cutoff.
Contraexemplo integrado: diferença/C_E={r['omitted_term_over_C']}.
Comando {manifest['command']}; rc0; log {log}, SHA256 {sha(log)}.
CPU{r['cpu_seconds']}s; custo do parecer US${receipt['cost_estimate_usd']}.
Próximo: compor a consistência dos contatos já medidos usando Mchi,
sem refazer a prova de fase já recuperada nem inferir Q2 integral.
'''
write(O/'ENTREGA_016_MEDIDA_comutador_cutoff_no_parecer.md',measure.encode(),True)
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: DeepSeek cutoff refutado por41controles CPU0.34375s; fases reconciliadas com artefatos prévios, sem nova execução; custo parcial US${cost}; Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes())
c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',partial_metered_cost_usd=str(cost),
 cutoff_review_manifest=str(D/'delivery_manifest.json'),
 phase_pending=False,phase_resolution='Pair plus-plane already verified in pair_fourier_phase; no engine edits',
 next=['Assemble Wess-Zumino consistency for computed contact sectors with cutoff and source',
       'Continue missing quantum contributions before A7b20:32Z deadline; then A7c/d,A8,PartB,final'],
 completed_this_turn=['DeepSeek cutoff audit with integrated counterexample','Recovered existing Fourier phase proof without rebuilding'])
write(p,json.dumps(c,ensure_ascii=False,indent=2).encode())
print(json.dumps(dict(checks=r['checks'],cpu_seconds=r['cpu_seconds'],partial_cost=str(cost),manifest_sha256=sha(D/'delivery_manifest.json'))))
