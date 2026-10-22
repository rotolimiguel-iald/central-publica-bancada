"""Partition existing theorem bodies without changing a proof or proposition."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
D=Path(__file__).resolve().parent;ROOT=D.parent;src=ROOT/'A1/v31/ContratoQG_v31_Teoremas.lean'
lines=src.read_text('utf-8').splitlines(keepends=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,b):
    assert not p.exists(),p
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;tmp.rename(p)
# Boundaries checked at namespace/section headers. End lines are inclusive.
groups=[('A',36,66,'',''),('B',67,178,'','\nend ContratoH2\n'),
 ('C',179,313,'namespace ContratoH2\nvariable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}\n',''),
 ('D',314,393,'',''),('E',394,606,'',''),('F',608,668,'',''),('G',669,762,'',''),
 ('H',763,1064,'','\nend ContratoH3\n'),
 ('I',1065,1189,'namespace ContratoH3\nvariable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}\n  {T : StressTensorData W}\n',''),
 ('J',1191,1279,'','')]
prints=[l for l in lines if l.startswith('#print axioms ')]
assert len(prints)==90
header=''.join(lines[1:34]);registry=[]
for i,(name,lo,hi,before,after) in enumerate(groups):
    body=''.join(lines[lo-1:hi]);decls=re.findall(r'^(?:theorem|lemma|def)\s+(\S+)',body,re.M)
    # The whole-name inventory below is for provenance; per-group audits add prints
    # for every declaration using the original namespace stack in the next step.
    imp='import ContratoQG_v31_Minimal\n' if i==0 else f'import ContractGroup{groups[i-1][0]}\n'
    text=imp+header+'\n'+before+body+after+'\nend\nend TGLExt.ContratoQGv31\n'
    p=D/f'ContractGroup{name}.lean';new(p,text.encode())
    registry.append(dict(group=name,path=str(p),source_lines=[lo,hi],source_body_sha256=hashlib.sha256(body.encode()).hexdigest(),
        source_body_unchanged=True,declared_local_names=decls,sha256=sha(p)))
new(D/'SOURCE_GROUPS.json',json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),ceiling_hours=6,source=str(src),source_sha256=sha(src),
    expected_original_prints=90,original_print_names=[x.strip().removeprefix('#print axioms ') for x in prints],groups=registry),ensure_ascii=False,indent=2).encode())
print(json.dumps({'groups':len(groups),'original_prints':len(prints)}))
