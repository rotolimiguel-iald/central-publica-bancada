"""Check runtime literals, imports and parsable embedded Python for self-file dependencies."""
from pathlib import Path
import ast, datetime, hashlib, json, sys
src=Path(sys.argv[1]).resolve(strict=True);dest=Path(sys.argv[2])
raw=src.read_bytes();text=raw.decode('utf-8');tree=ast.parse(text);lines=text.splitlines()
findings=[];embedded=[]
class Inspect(ast.NodeVisitor):
    def __init__(self,label,source_lines):self.stack=[];self.label=label;self.lines=source_lines
    def rec(self,n,kind,value):
        findings.append(dict(source=self.label,line=n.lineno,function='.'.join(self.stack) or '<module>',
            kind=kind,value=value,source_line=self.lines[n.lineno-1][:350]))
    def visit_FunctionDef(self,n):
        self.stack.append(n.name);self.generic_visit(n);self.stack.pop()
    visit_AsyncFunctionDef=visit_FunctionDef
    def visit_Constant(self,n):
        if isinstance(n.value,str) and len(n.value)<2048 and ('um.py' in n.value.lower() or n.value=='um'):
            self.rec(n,'string_literal',n.value[:700])
    def visit_Import(self,n):
        for a in n.names:
            if a.name=='um' or a.name.startswith('um.'):self.rec(n,'import',a.name)
    def visit_ImportFrom(self,n):
        if n.module=='um' or (n.module or '').startswith('um.'):self.rec(n,'import_from',n.module)
Inspect('executable_main',lines).visit(tree)
for n in ast.walk(tree):
    if not (isinstance(n,ast.Constant) and isinstance(n.value,str) and len(n.value)>2048 and
            ('um.py' in n.value.lower() or 'import um' in n.value)):continue
    try:t=ast.parse(n.value)
    except (SyntaxError,ValueError):continue
    label='embedded_python_at_main_line_'+str(n.lineno)
    embedded.append(dict(label=label,chars=len(n.value),sha256=hashlib.sha256(n.value.encode()).hexdigest()))
    Inspect(label,n.value.splitlines()).visit(t)
result=dict(source=dict(path=str(src),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),
 inspected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),findings=findings,
 parsed_embedded_python=embedded,scope='Static AST inspection; no imports or program execution',
 limitation='Arbitrary dynamically synthesized paths are not excluded by a literal scan; findings reviewed against source.')
with dest.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(receipt=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),findings=findings,embedded_count=len(embedded)),ensure_ascii=False))
