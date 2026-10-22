"""Read the executable Python AST, excluding embedded source-string contents."""
from pathlib import Path
import ast, datetime, hashlib, json, sys
src=Path(sys.argv[1]).resolve(strict=True)
dest=Path(sys.argv[2])
raw=src.read_bytes();text=raw.decode('utf-8');lines=text.splitlines()
class Inspect(ast.NodeVisitor):
    def __init__(self):self.stack=[];self.self_refs=[];self.fixed_name_literals=[]
    def visit_FunctionDef(self,n):
        self.stack.append(n.name);self.generic_visit(n);self.stack.pop()
    visit_AsyncFunctionDef=visit_FunctionDef
    def visit_Name(self,n):
        if n.id=='__file__':
            self.self_refs.append(dict(line=n.lineno,function='.'.join(self.stack) or '<module>',text=lines[n.lineno-1][:1000]))
    def visit_Constant(self,n):
        if isinstance(n.value,str) and n.value in {'um.py','./um.py','.\\um.py'}:
            self.fixed_name_literals.append(dict(line=n.lineno,function='.'.join(self.stack) or '<module>',text=lines[n.lineno-1][:1000]))
v=Inspect();v.visit(ast.parse(text))
result=dict(source=dict(path=str(src),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),
    inspected_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    executable_ast_only=True,embedded_programs_are_data_and_not_recursively_parsed=True,
    self_references=v.self_refs,fixed_self_filename_literals=v.fixed_name_literals,
    interpretation='Self hash/custody consumers using __file__ follow the executed path. Fixed-name literals require individual review; a filename-independent claim is not inferred merely from this scan.')
with dest.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(self_references=len(v.self_refs),fixed_literals=v.fixed_name_literals,receipt=str(dest),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()),ensure_ascii=False))
