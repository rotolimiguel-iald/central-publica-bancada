"""Copy twelve pinned sources; change local import headers only."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,re,hashlib
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C3';P=D/'package'
sys.path.insert(0,str(ROOT/'A7'))
from deliver_nonminimal_wick_and_mimo_audit import sha,write,put
f=ROOT/'A6_EQUACAO_DA_VERDADE/E_ficha/FICHA_TRANSPOSICAO_T20.json'
j=json.loads(f.read_bytes());P.mkdir(exist_ok=False)
items=[];known={Path(x['source']).stem for x in j['accepted_local_sources']}
for x in j['accepted_local_sources']:
    src=Path(x['source']);assert sha(src)==x['sha256'],src
    old=src.read_bytes();new=old;changes=[]
    for before,after in [(b'import TheEquationOfTruth_T20\r\n',b'import TheEquationOfTruth_T20_v3\r\n'),(b'import TheEquationOfTruth_T20\n',b'import TheEquationOfTruth_T20_v3\n')]:
        if before in new:
            new=new.replace(before,after);changes.append(dict(before=before.decode().strip(),after=after.decode().strip()))
    def sans_imports(b):return b''.join(v for v in b.splitlines(keepends=True) if not v.startswith(b'import '))
    assert sans_imports(new)==sans_imports(old)
    dst=P/src.name;write(dst,new)
    imports=re.findall(r'^import (\S+)',new.decode('utf-8-sig'),re.M)
    items.append(dict(source=str(src),source_sha256=sha(src),copy=str(dst),copy_sha256=sha(dst),
        changes=changes,body_bytes_equal=True,body_sha256=hashlib.sha256(sans_imports(old)).hexdigest(),
        imports=imports,local_imports=[v for v in imports if v in known],audited_names=list(x['audit']['axiomas'])))
assert len(items)==12
done=set();ordered=[]
while len(ordered)<len(items):
    ready=[x for x in items if Path(x['copy']).stem not in done and set(x['local_imports'])<=done]
    assert ready,'cycle'
    for x in ready:ordered.append(x);done.add(Path(x['copy']).stem)
names=sorted({n for x in items for n in x['audited_names']})
text=''.join('import '+Path(x['copy']).stem+'\n' for x in ordered)+'\n-- All twelve sources coexist; no new theorem or physical identification.\n'
text+=''.join('#print axioms '+n+'\n' for n in names)
write(P/'IntegrationAudit.lean',text.encode())
put(D/'PLAN.json',dict(at=datetime.now(timezone.utc).isoformat(),ceiling_hours=6,origin=str(f),origin_sha256=sha(f),
    groups=ordered,source_count=12,expected_names=names,body_changes=0,
    canonical_names_not_installed=True,strong_infinite_limit='OPEN: FlowTendsToFamily retained',
    only_import_edits=['InscriptionBridge: T20 -> T20_v3','PenaltyThreeLocksBridge_v2: T20 -> T20_v3'],
    strategy='One shared v3, isolated serial module compilation, aggregate isolated consumer; no lake build'))
print(json.dumps(dict(order=[Path(x['copy']).stem for x in ordered],declarations=len(names),sources=len(items))))
