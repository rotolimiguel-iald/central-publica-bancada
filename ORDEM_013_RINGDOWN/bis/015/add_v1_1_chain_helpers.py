"""Add chain validation directly to the copied guard; activation remains absent."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,ast
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t03';P=B/'bis/e2_code_v1_1/registration_guard.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ADD='''

# V1.1 statistical and chronology contract. No caller may bypass the later runtime gate.
STATISTICAL_FIELDS=('observables','statistics','systematic_gate','nulls','route_IV',
    'conventions','planning_targets','permitted_verdicts','forbidden_verdicts','stopping','calibration_event_ids')


def statistical_subobject(reg):
    obj={key:reg[key] for key in STATISTICAL_FIELDS}
    obj['blinding']={key:reg['blinding'][key] for key in ('seed_commitment_sha256','offset_half_range')}
    return obj


def statistical_digest(reg):
    raw=json.dumps(statistical_subobject(reg),sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def verify_statistical_identity(original,candidate):
    wanted=statistical_digest(original)
    if statistical_subobject(candidate)!=statistical_subobject(original) or statistical_digest(candidate)!=wanted:
        raise ValueError('Frozen V1 statistical subobject changed')
    if candidate.get('statistical_subobject_sha256')!=wanted:raise ValueError('Statistical commitment differs')
    old_ids=[c['id'] for c in original['nulls']['cells']]
    new_ids=[c['id'] for c in candidate['nulls_v1_1']['cells']]
    if len(new_ids)!=len(set(new_ids)) or set(old_ids)&set(new_ids):raise ValueError('Old/repeated null cell id forbidden')
    return wanted


def numbered_chain(root,pattern,prefix,suffix='.json'):
    entries={}
    for p in root.glob(pattern):
        match=re.fullmatch(re.escape(prefix)+r'([1-9][0-9]*)'+re.escape(suffix),p.name)
        if match is None:raise ValueError('Malformed chain filename: '+p.name)
        n=int(match[1])
        if n in entries:raise ValueError('Repeated chain ordinal')
        if p.is_symlink() or p.resolve().parent!=root.resolve():raise ValueError('Redirected chain member')
        entries[n]=p
    if sorted(entries)!=list(range(1,len(entries)+1)):raise ValueError('Nonconsecutive amendment/allocation chain')
    return [entries[n] for n in sorted(entries)]


def load_registration_chain_v1_1():
    original_path=BASE/'RINGDOWN_5SIGMA_V1.json'
    original=strict_json(original_path.read_bytes());parent=sha(original_path)
    v1_note=contained(original['witness_relative_to_Chatgpt'])
    v1_witness=check_witness(v1_note,parent,original['registered_utc'])
    paths=[BASE/'RINGDOWN_5SIGMA_V1_1.json']+numbered_chain(BASE,'RINGDOWN_5SIGMA_V1_1_*.json','RINGDOWN_5SIGMA_V1_1_')
    previous=None;previous_time=utc(original['registered_utc']);root_time=None
    for index,path in enumerate(paths):
        if path.is_symlink():raise ValueError('Redirected amendment')
        reg=strict_json(path.read_bytes());digest=sha(path)
        if reg['parent_registration_sha256']!=parent:raise ValueError('Amendment parent mismatch')
        if reg['v1_witness_sha256']!=v1_witness:raise ValueError('V1 witness changed')
        verify_statistical_identity(original,reg)
        issued=utc(reg['registered_utc'])
        if issued<previous_time:raise ValueError('Amendment chronology reversed')
        expected='ENTREGA_015_E2_REGISTRO_V1_1'+('' if index==0 else '_'+str(index))+'.md'
        note=contained(reg['witness_relative_to_Chatgpt'])
        if note!=ROOT/'TUNEL/DO_CHATGPT'/expected:raise ValueError('Wrong amendment witness path')
        check_witness(note,digest,reg['registered_utc'])
        dates=re.findall(r'^registered_utc: (\\S+)\\s*$',note.read_text('utf-8-sig'),re.M)
        witnessed=utc(dates[0])
        if root_time is None:root_time=issued
        if previous is not None:
            if any(name not in reg['pe_jobs'] or reg['pe_jobs'][name]!=job for name,job in previous['pe_jobs'].items()):
                raise ValueError('Existing job removed or replaced by amendment')
        if set(reg['pe_jobs'])&set(original['pe_jobs']):raise ValueError('V1 job cannot be relaunched in V1.1')
        # Promotion metadata itself is not authorization: evidence and chronology must match.
        promotions={}
        for change in reg.get('test_candidates_amendments',[]):
            if change.get('promotion') is not True:continue
            event=change['event']
            if event in promotions:raise ValueError('Duplicate promotion')
            reviewed=utc(change['census_reviewed_utc'])
            if not root_time<=reviewed<=datetime.now(timezone.utc):raise ValueError('Census predates V1.1 or is future')
            if sha(contained(change['evidence_relative_to_Chatgpt']))!=change['evidence_sha256']:raise ValueError('Promotion evidence mismatch')
            if reg['test_candidates'][event]['eligible'] is not True:raise ValueError('Promotion/eligibility disagreement')
            promotions[event]=change
        antecedent=original if previous is None else previous
        for event,entry in reg['test_candidates'].items():
            old=antecedent['test_candidates'].get(event,{})
            if entry.get('eligible') is True and old.get('eligible') is not True and event not in promotions:
                raise ValueError('Eligibility changed without witnessed promotion')
        previous=reg;previous_time=witnessed;parent=digest
    return reg,digest,note
'''
def main():
    raw=P.read_bytes();before=sha(P);snap=D/'registration_guard_before_chain.py'
    with snap.open('xb') as f:f.write(raw)
    s=raw.decode('utf-8')+ADD;ast.parse(s)
    tmp=P.with_suffix('.pending')
    with tmp.open('xb') as f:f.write(s.encode())
    assert tmp.stat().st_size>len(raw);tmp.replace(P)
    result=dict(at=datetime.now(timezone.utc).isoformat(),status='CHAIN_HELPERS_ADDED_NOT_WIRED_NOT_REGISTERED',before=before,after=sha(P),
      pending=['wire checked_registration to V1.1 activation and R7','allocation chain','strict promotion/witness chronology tests','full guard negative tests'],
      scope='Statistical identity, disjoint null ids, consecutive parent/witness chain helpers in existing copied guard; no new module or bypass')
    with (D/'CHAIN_HELPERS_PATCH_001.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result))
if __name__=='__main__':main()
