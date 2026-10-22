"""Add complete declaration prints; bodies still byte-equivalent as UTF-8 text."""
from pathlib import Path
import json,re,hashlib
D=Path(__file__).resolve().parent;reg=json.loads((D/'SOURCE_GROUPS.json').read_bytes())
lines=Path(reg['source']).read_text('utf-8').splitlines();stack=[];decls=[]
for number,line in enumerate(lines,1):
    if m:=re.match(r'^namespace\s+(\S+)',line):stack.append(('namespace',m[1]))
    elif re.match(r'^(?:noncomputable )?section(?:\s|$)',line):stack.append(('section',''))
    elif re.match(r'^end(?:\s|$)',line):stack.pop()
    elif m:=re.match(r'^(?:theorem|lemma|def)\s+(\S+)',line):
        name='.'.join([v for k,v in stack if k=='namespace']+[m[1]])
        decls.append((number,name))
assert not stack
original={'TGLExt.ContratoQGv31.'+n for n in reg['original_print_names']}
assert original<={name for _,name in decls}
out=[]
for i,g in enumerate(reg['groups']):
    p=Path(g['path']);text=p.read_text('utf-8')
    if i:text=text.replace('import ContractGroup'+reg['groups'][i-1]['group']+'\n','import ContractGroup'+reg['groups'][i-1]['group']+'_v2\n',1)
    lo,hi=g['source_lines'];names=[n for k,n in decls if lo<=k<=hi]
    text+='\n'+'\n'.join('#print axioms '+n for n in names)+'\n'
    v=p.with_stem(p.stem+'_v2');assert not v.exists();v.write_bytes(text.encode())
    out.append(dict(group=g['group'],path=str(v),sha256=hashlib.sha256(v.read_bytes()).hexdigest(),names=names,source_lines=g['source_lines'],source_body_sha256=g['source_body_sha256']))
data=dict(source_sha256=reg['source_sha256'],original_prints=sorted(original),groups=out,all_decl_count=len(decls))
p=D/'GROUP_AUDIT_PLAN.json';assert not p.exists();p.write_bytes(json.dumps(data,ensure_ascii=False,indent=2).encode())
print(json.dumps({'all_declarations':len(decls),'audited_original':len(original),'groups':[(x['group'],len(x['names'])) for x in out]}))
