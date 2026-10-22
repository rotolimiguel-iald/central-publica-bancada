"""Remove only individually rehashed cache duplicates explicitly covered by F7."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

ROOT=Path(__file__).resolve().parents[1].resolve()
CACHE=(ROOT/'cache').resolve()
PLAN=ROOT/'bis/F7_DUPLICATE_REMOVAL_PLAN.json'
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while block:=f.read(4*1024*1024): h.update(block)
    return h.hexdigest()

def main():
    plan=json.loads(PLAN.read_bytes())
    groups={}
    for entry in plan['entries']:
        if not entry['eligible_for_authorized_removal']: continue
        p=Path(entry['path']).resolve(); q=Path(entry['canonical_path']).resolve()
        if not p.is_relative_to(ROOT) or p.is_relative_to(CACHE) or not q.is_relative_to(CACHE):
            raise ValueError('Path escaped authorized bench/cache boundary')
        group=ROOT/p.relative_to(ROOT).parts[0]
        if group.name not in {'C7_POSTERIOR_REPRODUCTION','C7_GWTC3_REPRODUCTION','C7_INDEPENDENT','C7_INJECTION_REPRODUCTION'}:
            raise ValueError('Not an authorized duplicate group')
        if p.is_symlink() or q.is_symlink() or p==q: raise ValueError('Invalid alias')
        if p.stat().st_size!=entry['bytes'] or q.stat().st_size!=entry['bytes']:
            raise ValueError('Sizes changed after plan')
        if sha(p)!=entry['sha256'] or sha(q)!=entry['sha256']:
            raise ValueError('Bytes changed after plan')
        groups.setdefault(group,[]).append(entry)
    # Fail before any deletion if this operation would overwrite an existing receipt.
    for group in groups:
        if (group/'DUPLICATAS_REMOVIDAS.json').exists(): raise FileExistsError(group)
    log=ROOT/'bis/F7_DELETION_JOURNAL.jsonl'
    with log.open('x',encoding='utf-8') as f:
        for group,entries in groups.items():
            for e in entries:
                p=Path(e['path']);q=Path(e['canonical_path'])
                # Canonical evidence remains present before every individual unlink.
                if not q.is_file() or not p.is_file(): raise FileNotFoundError(str(p))
                f.write(json.dumps(dict(action='INTENT',**e),ensure_ascii=False)+'\n');f.flush()
                p.unlink()
                if p.exists() or not q.exists(): raise RuntimeError('Removal invariant failed')
                e['removed_utc']=datetime.now(timezone.utc).isoformat()
                f.write(json.dumps(dict(action='REMOVED',**e),ensure_ascii=False)+'\n');f.flush()
            receipt=dict(status='EXACT_DUPLICATES_REMOVED__CANONICAL_BYTES_PRESERVED',
              plan_sha256=sha(PLAN),entries=entries,
              threshold_note='The audit counted 53 above 25 MiB; four additional exact duplicates are above 25 decimal MB. Both thresholds are enforced.')
            with (group/'DUPLICATAS_REMOVIDAS.json').open('x',encoding='utf-8') as r:
                json.dump(receipt,r,ensure_ascii=False,indent=2);r.write('\n')
            print(group.name,len(entries),sha(group/'DUPLICATAS_REMOVIDAS.json'),flush=True)
    print('removed',sum(len(rows) for rows in groups.values()),'files',flush=True)

if __name__=='__main__':main()
