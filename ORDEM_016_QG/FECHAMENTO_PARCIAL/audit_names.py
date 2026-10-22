"""Compare original source names and elaborated package names to v371 census."""
from pathlib import Path
import re,json,hashlib
S=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def strip_comments(text):
    out=[];i=0;depth=0;string=False
    while i<len(text):
        if depth:
            if text.startswith('/-',i):depth+=1;i+=2
            elif text.startswith('-/',i):depth-=1;i+=2
            else:
                out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif string:
            if text[i]=='\\':out.extend('  ');i+=2
            elif text[i]=='"':string=False;out.append(' ');i+=1
            else:out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif text.startswith('/-',i):depth=1;i+=2
        elif text.startswith('--',i):
            j=text.find('\n',i);i=len(text) if j<0 else j
        elif text[i]=='"':string=True;out.append(' ');i+=1
        else:out.append(text[i]);i+=1
    return ''.join(out)
def declarations(text):
    stack=[];out=[]
    for line in strip_comments(text).splitlines():
        q=line.strip()
        if line.startswith('namespace '):stack.append(('namespace',q.split()[1]));continue
        if re.match(r'^(?:noncomputable )?section(?:\s|$)',line):stack.append(('section',''));continue
        if re.match(r'^end(?:\s|$)',line):
            if stack:stack.pop()
            continue
        m=re.match(r'^(?:(?:noncomputable|private|protected|unsafe|partial)\s+)*(?:def|theorem|lemma|abbrev|structure|class|inductive|axiom)\s+([^\s(:{]+)',line)
        if m:
            prefix='.'.join(v for k,v in stack if k=='namespace')
            name=m[1];out.append((prefix+'.' if prefix else '')+name)
    return out
def main():
    census={}
    for line in (S/'logs/kernel_census_01.log').read_text('utf-8').splitlines():
        if line.startswith('KERNEL_DECL\t'):
            _,name,module,kind=line.split('\t');census[name]=dict(module=module,kind=kind)
    assert census
    plan=json.loads((S/'SOURCE_PLAN.json').read_bytes())
    collisions=[];original_symbols=[]
    for row in plan['sources']:
        p=Path(row['original']);names=declarations(p.read_text('utf-8-sig'))
        for name in names:
            entry=dict(source=str(p),sha256=sha(p),name=name)
            original_symbols.append(entry)
            if name in census:collisions.append(dict(**entry,canonical=census[name],explicit_adaptations=row['changes']))
    active=[];axioms=[];lexical=[]
    for row in plan['sources']:
        p=Path(row['source']);clean=strip_comments(p.read_text('utf-8'))
        if re.search(r'\b(sorry|admit|axiom)\b',clean):lexical.append(str(p))
        log=S/'logs'/('unit_'+row['module']+'_01.log')
        if not log.exists():continue
        for line in log.read_text('utf-8',errors='replace').splitlines():
            if line.startswith('BENCH_DECL\t'):
                _,name,kind,ax=line.split('\t')
                if name in census:active.append(dict(source=str(p),name=name,canonical=census[name]))
                if kind=='axiom' or set(filter(None,ax.split(',')))-{'propext','Classical.choice','Quot.sound'}:axioms.append(dict(name=name,kind=kind,axioms=ax))
    result=dict(census_declarations=len(census),census_modules=len({v['module'] for v in census.values()}),
        census_sha256=sha(S/'logs/kernel_census_01.log'),original_collisions=collisions,
        original_scan_scope='Lexical explicit declarations (not generated/private names); compiled final names checked exhaustively by environment export',
        active_elaborated_collisions=active,unexpected_axioms=axioms,lexical_sorry_axiom_files=lexical,
        reserved_names_created=[x for x in original_symbols if '.qgPrice_' in x['name'] or '.qgImport_' in x['name']])
    p=S/'NAME_AUDIT.json'
    if p.exists():raise FileExistsError(p)
    p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in result.items() if k!='original_scan_scope'},ensure_ascii=False))
if __name__=='__main__':main()
