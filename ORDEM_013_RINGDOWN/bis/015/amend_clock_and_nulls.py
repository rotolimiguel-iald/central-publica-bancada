"""T03 light-stage patch in the sibling tree; never starts the real clock."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os

B = Path(__file__).resolve().parents[2]
C = B / 'bis/e2_code_v1_1'
D = B / 'bis/015/t03'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def replace(s, a, b):
    if s.count(a) != 1:
        raise ValueError('Nonunique patch anchor: ' + a[:80])
    return s.replace(a, b)

def main():
    backup = D / 'clock_nulls_before_001'
    backup.mkdir(exist_ok=False)
    rows = []
    for name in ('registration_guard.py', 'null_runner.py', 'null_campaign.py'):
        path = C / name
        raw = path.read_bytes()
        with (backup / name).open('xb') as f:
            f.write(raw)
        s = raw.decode('utf-8')
        if name == 'registration_guard.py':
            s = replace(s, 'from datetime import datetime, timezone', 'from datetime import datetime, timezone, timedelta')
            start = s.index('def time_guard(reg):')
            end = s.index('\ndef authorize_event(', start)
            s = s[:start] + '''def time_guard(reg):
    """R7: the rule is registered in phase L; the witnessed clock starts in phase P."""
    rule=reg['budget_rule_v1_1']
    expected={
      'budget_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/PART_015_BUDGET_START.json',
      'source_receipt_relative_to_Chatgpt':'ORDEM_013_RINGDOWN/bis/FINAL_DELIVERY_RECEIPT.json',
      'machine_free_receipt_relative_to_Chatgpt':'TUNEL/PARA_CHATGPT/RECIBO_015_MAQUINA_LIVRE.md',
      'witness_relative_to_Chatgpt':'TUNEL/DO_CHATGPT/ENTREGA_015_RELOGIO.md'}
    if any(rule[k]!=v for k,v in expected.items()):raise ValueError('R7 paths differ from registered contract')
    if reg['budget_relative_to_Chatgpt']!=expected['budget_relative_to_Chatgpt'] or 'budget_sha256' in reg:
        raise ValueError('V1.1 registers the clock rule, not a premature clock hash')
    if type(rule['deadline_hours']) is not int or rule['deadline_hours']!=168:
        raise ValueError('R7 deadline must be the registered 168 hours')
    budget=contained(rule['budget_relative_to_Chatgpt'])
    if budget.is_symlink():raise ValueError('Redirected budget')
    raw=budget.read_bytes();digest=hashlib.sha256(raw).hexdigest();b=strict_json(raw)
    required={'start_utc','hard_deadline_utc','authorized_machine_hours',
      'source_receipt_relative_to_Chatgpt','source_receipt_sha256','recibo_maquina_livre_sha256'}
    if set(b)!=required:raise ValueError('R7 clock schema differs')
    source=contained(rule['source_receipt_relative_to_Chatgpt'])
    if sha(source)!=rule['source_receipt_sha256']:raise ValueError('Historical budget receipt changed')
    remaining=positive(strict_json(source.read_bytes())['remaining_of_40_hours'],'remaining machine hours')
    source_name=rule['source_receipt_relative_to_Chatgpt'];source_hash=rule['source_receipt_sha256']
    limit=rule.get('operator_reduction')
    if limit is not None:
        # An explicit, pinned operator opening is required; this is not an inferred reduction.
        opening=contained(limit['opening_relative_to_Chatgpt'])
        if opening.parent!=ROOT/'TUNEL/DO_CHATGPT' or not opening.name.startswith('ENTREGA_') or 'ABERTURA' not in opening.name:
            raise ValueError('Operator reduction needs an opening in the tunnel')
        if sha(opening)!=limit['opening_sha256']:raise ValueError('Operator reduction opening changed')
        remaining=min(remaining,positive(limit['authorized_machine_hours'],'operator machine hours'))
        source_name=limit['opening_relative_to_Chatgpt'];source_hash=limit['opening_sha256']
    if b['source_receipt_relative_to_Chatgpt']!=source_name or b['source_receipt_sha256']!=source_hash:
        raise ValueError('Clock budget provenance differs')
    if positive(b['authorized_machine_hours'],'authorized machine hours')!=remaining:
        raise ValueError('Clock budget differs from available hours')
    release=contained(rule['machine_free_receipt_relative_to_Chatgpt'])
    if sha(release)!=b['recibo_maquina_livre_sha256']:raise ValueError('Machine-free receipt changed')
    first_path=BASE/'RINGDOWN_5SIGMA_V1_1.json';first_digest=sha(first_path)
    first=strict_json(first_path.read_bytes())
    first_note=contained(first['witness_relative_to_Chatgpt'])
    if first_note!=ROOT/'TUNEL/DO_CHATGPT/ENTREGA_015_E2_REGISTRO_V1_1.md':raise ValueError('Wrong initial V1.1 witness')
    check_witness(first_note,first_digest,first['registered_utc'])
    witnessed=utc(re.findall(r'^registered_utc: (\\S+)\\s*$',first_note.read_text('utf-8-sig'),re.M)[0])
    start=utc(b['start_utc']);deadline=utc(b['hard_deadline_utc']);now=datetime.now(timezone.utc)
    if not max(utc(first['registered_utc']),witnessed,datetime.fromtimestamp(release.stat().st_mtime,timezone.utc))<=start<=now:
        raise ValueError('Clock begins before registration/release or in the future')
    if deadline!=start+timedelta(hours=rule['deadline_hours']):raise ValueError('Clock deadline arithmetic differs')
    check_witness(contained(rule['witness_relative_to_Chatgpt']),digest,b['start_utc'],'budget_sha256')
    if datetime.now(timezone.utc)>=deadline:raise TimeoutError('Part 015 hard deadline reached')
    if sha(budget)!=digest:raise ValueError('Clock changed during read')
    return deadline

''' + s[end:]
            s += '''
def new_null_cells(reg):
    """Only the new V1.1 design is executable; V1 cell identities stay retired."""
    cells=reg['nulls_v1_1']['cells'];old=reg['nulls']['cells']
    if not isinstance(cells,dict) or not isinstance(old,dict):raise ValueError('Null cells require id-keyed mapping')
    if set(cells)&set(old):raise ValueError('V1 null cell cannot be relaunched')
    for name in cells:
        if not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_]{1,120}',name):raise ValueError('Unsafe null cell identifier')
    return cells
'''
        elif name == 'null_runner.py':
            s = replace(s, 'time_guard,sha,publish_new', 'time_guard,sha,publish_new,new_null_cells')
            s = replace(s, "reg,digest=checked_registration();cells=reg['nulls']['cells']", 'reg,digest=checked_registration();cells=new_null_cells(reg)')
        else:
            s = replace(s, 'sha,time_guard,publish_new', 'sha,time_guard,publish_new,new_null_cells')
            s = replace(s, "reg,digest=checked_registration();names=sorted(reg['nulls']['cells'])", 'reg,digest=checked_registration();cells=new_null_cells(reg);names=sorted(cells)')
            s = replace(s, "out=BASE/'bis/RESULT_E2_NULL_CAMPAIGN.json'", "out=BASE/'bis'/('RESULT_E2_NULL_CAMPAIGN_V1_1_'+digest+'.json')")
            s = s.replace("reg['nulls']['cells'][name]", "cells[name]")
        ast.parse(s)
        encoded = s.encode('utf-8')
        temp = path.with_name(path.name + '.clock_nulls.pending')
        with temp.open('xb') as f:
            f.write(encoded);f.flush();os.fsync(f.fileno())
        assert temp.stat().st_size == len(encoded)
        os.replace(temp, path)
        rows.append(dict(file=name,before_sha256=sha(backup/name),after_sha256=sha(path)))
    receipt=dict(status='LIGHT_STAGE_CLOCK_NULLS_PATCH_NOT_REGISTERED',at=datetime.now(timezone.utc).isoformat(),files=rows,
                 real_clock_created=False,heavy_jobs=0,seed_read=False,activation_integration_pending=True)
    with (D/'CLOCK_NULLS_PATCH_001.json').open('xb') as f:
        f.write((json.dumps(receipt,indent=2)+'\n').encode())
    print(json.dumps(receipt))

if __name__=='__main__':main()
