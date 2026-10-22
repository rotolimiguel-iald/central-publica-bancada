"""Normalize existing receipt spellings, deduplicate executions; unknown is not zero."""
from pathlib import Path
from decimal import Decimal
from datetime import datetime,timezone
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import OUT,sha,put,append
D=Path(__file__).resolve().parent;ledger=OUT/'LEDGER_016.jsonl'
rows=[json.loads(x) for x in ledger.read_text('utf-8').splitlines() if x.strip()]
units={};conflicts=[]
for i,x in enumerate(rows):
    usage=next((x[k] for k in ['usage','raw_usage','tokens'] if isinstance(x.get(k),dict) and 'completion_tokens' in x[k]),None)
    provider=x.get('provider') or x.get('provedor')
    key=x.get('execution_task_id') or x.get('execution_id') or x.get('task_id') or x.get('job_id') or x.get('request_id')
    if not usage or not provider or not key: continue
    cost=next((x[k] for k in ['cost_estimate_usd','cost_usd','custo_usd'] if x.get(k) is not None),None)
    if key in units and units[key]['usage']!=usage: conflicts.append(key)
    if cost is None and key in units: cost=units[key]['cost']
    units[key]=dict(provider=provider,usage=usage,cost=cost,row=i)
assert not conflicts
stats={}
for x in units.values():
    a=stats.setdefault(x['provider'],dict(units=0,prompt_tokens=0,completion_tokens=0,known_cost=Decimal(0),unknown_cost_units=0))
    a['units']+=1
    for k in ['prompt_tokens','completion_tokens']: a[k]+=x['usage'].get(k,0) or 0
    if x['cost'] is None:a['unknown_cost_units']+=1
    else:a['known_cost']+=Decimal(str(x['cost']))
total=sum(x['known_cost'] for x in stats.values())
for x in stats.values():x['known_cost']=str(x['known_cost'])
put(D/'LEDGER_TOTALS.json',dict(at=datetime.now(timezone.utc).isoformat(),ledger_sha256=sha(ledger),providers=stats,
    partial_metered_cost_usd=str(total),unknown_is_not_zero=True,scope='Only units with token receipts; failed/uncertain units without usage excluded from sum, not priced zero',
    alternate_estimate_note='A3 earlier receipt gives two differing price estimates; primary cost_estimate_usd retained, alternate accounted_usd not summed as another call',units=units))
append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{datetime.now(timezone.utc).isoformat()} ComplementoA8: ledgerSHA256={sha(ledger)}; custos tokenizados parciaisUSD{total}, demais desconhecidos. Porprovedor={json.dumps(stats)}. Sem nova chamada para esta reconciliação. ArtefatoA8/LEDGER_TOTALS.jsonSHA256={sha(D/"LEDGER_TOTALS.json")}.\n')
print(json.dumps(stats))
