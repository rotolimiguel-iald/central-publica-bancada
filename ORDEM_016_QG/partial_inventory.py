"""Custody and inventory for ADENDO016-004; no canonical writes or provider calls."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json, re, hashlib
from prepare_part_d import save, write, sha, R, ROOT, IN, OUT

S = R / 'FECHAMENTO_PARCIAL'
P = OUT / 'FECHAMENTO_PARCIAL_016'

def start():
    S.mkdir(exist_ok=True)
    if (S/'START.json').exists():
        return
    now = datetime.now(timezone.utc)
    adendo = IN/'ADENDO_016_004_fechamento_parcial_antes_do_ringdown.md'
    pins = {str(p):sha(p) for p in sorted(IN.glob('*016*.md'))}
    refs = [OUT/'ENTREGA_016_ABERTURA_operador.md', OUT/'ENTREGA_016_PARTE_D_quadro_final.md',
            ROOT/'ORDEM_013_RINGDOWN/bis/015/t06/RESULT.json',
            ROOT/'ORDEM_013_RINGDOWN/bis/015/t05/RESULT.json']
    pins.update({str(p):sha(p) for p in refs})
    d = dict(at=now.isoformat(), deadline=(now+timedelta(hours=6)).isoformat(),
             status='CONSOLIDATION_OPEN', sources=pins, adendo_sha256=sha(adendo),
             part_B='PAUSED_INTERNALLY_AFTER_T06', resume_B='T11',
             new_heavy_work=False, gate_changed=False, new_lemma_allowed=False,
             package=str(P), opening_sha256=sha(refs[0]))
    save(S/'START.json',d)
    q=R/'A7/CONTINUIDADE.json'; x=json.loads(q.read_bytes())
    x.update(at=now.isoformat(), partial_closure_004=d, own_live_process=None,
             next='ADENDO016-004: consolidate nine pieces in six hours; PRONTO.json LAST; then resume B/T11. No new B unit before package. Prioritize any management correction receipt.')
    save(q,x,True)
    p=OUT/'ENTREGA_016_PROGRESSO.md'
    write(p,p.read_bytes()+f'\n{now.isoformat()} — ADENDO016-004: T06 terminado; B pausada internamente antes de T11. Consolidação P1–P9 aberta (teto6h), PRONTO.json somente após verificação. Gate intacto. AberturaSHA256 {d["opening_sha256"]}.\n'.encode(),True)
    write(OUT/'ENTREGA_016_FECHAMENTO_PARCIAL_ABERTURA.md',
        (f'[REAL — leitura e início da consolidação; pacote ainda não entregue]\n\n'
         f'Adendo SHA256 {sha(adendo)}. Abertura016SHA256 {d["opening_sha256"]}.\n'
         f'Início {d["at"]}; teto {d["deadline"]}. T06 terminou; B retoma T11 após P1–P9 e PRONTO.json. '
         'Não há nova unidade pesada, alteração canônica ou gate. Arquivos faltantes ou falhas de compilação serão MEDIDA explícita, conforme adendo.\n').encode())
    print(json.dumps(d,ensure_ascii=False))

def inventory():
    records=[]
    for p in R.rglob('*.json'):
        if any(x in p.parts for x in ['compiler_env','.lake','FECHAMENTO_PARCIAL']):continue
        try:d=json.loads(p.read_bytes())
        except (ValueError,OSError):continue
        if not isinstance(d,dict) or 'rc' not in d or 'command' not in d:continue
        command=d['command']
        if not isinstance(command,list):continue
        src=[Path(x) for x in command if isinstance(x,str) and x.endswith('.lean')]
        if not src:continue
        src=src[-1]
        if not src.is_file() or not src.is_relative_to(R):continue
        log=p.with_suffix('.log')
        records.append(dict(receipt=str(p),receipt_sha256=sha(p),source=str(src),
            source_sha256=sha(src),recorded_sha256=d.get('source_sha256'),
            matches=d.get('source_sha256')==sha(src),rc=d['rc'],
            command=command,lean_path=d.get('lean_path'),log=str(log) if log.exists() else None,
            cpu_seconds=sum(d.get(k) or 0 for k in ['cpu_user_seconds','cpu_kernel_seconds']),
            wall_seconds=d.get('wall_seconds'),utc=d.get('utc')))
    lean=[]
    for p in R.rglob('*.lean'):
        if any(x in p.parts for x in ['compiler_env','.lake','FECHAMENTO_PARCIAL']):continue
        hits=[r for r in records if r['source']==str(p) and r['matches'] and r['rc']==0]
        text=p.read_text('utf-8-sig')
        lean.append(dict(path=str(p),relative=str(p.relative_to(R)),sha256=sha(p),
            imports=re.findall(r'^import\s+([^\n]+)',text,re.M),
            valid_receipts=[r['receipt'] for r in hits],
            printed_axioms=re.findall(r'^#print axioms\s+(\S+)',text,re.M)))
    save(S/'INVENTORY.json',dict(records=records,lean=lean))
    from collections import Counter
    print(json.dumps(dict(receipts=len(records),lean=len(lean),successful=len([x for x in lean if x['valid_receipts']]),
        branches=dict(Counter(Path(x['relative']).parts[0] for x in lean if x['valid_receipts']))),ensure_ascii=False))

if __name__=='__main__':
    start(); inventory()
