"""Read bytes and literal AST nodes only; never execute or import um.py."""
from pathlib import Path
import ast,hashlib,json,re
from reader import sha_obj
S=Path(__file__).resolve().parent
B=S.parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    raw=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
    if p.exists():raise FileExistsError(p)
    tmp=p.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
def excerpt(lines,name):
    start=next(i for i,x in enumerate(lines) if x.startswith(('def '+name+'(').encode()))
    end=next((i for i in range(start+1,len(lines)) if lines[i].startswith(b'def ')),len(lines))
    return b''.join(lines[start:end]),start+1,end
def main():
    source=B/'cache/casa/um.py';registry=B/'cache/casa/um_absoluto.json';raw=source.read_bytes();lines=raw.splitlines(keepends=True)
    rule,start,end=excerpt(lines,'prove_neutrino_m2');hash_source,hs,he=excerpt(lines,'sha_obj')
    (S/'prove_neutrino_m2_source.txt').write_bytes(rule);(S/'sha_obj_source.txt').write_bytes(hash_source)
    function=ast.parse(rule.decode('utf-8')).body[0]
    values={}
    for node in function.body:
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('frozen','dets'):
            values[node.targets[0].id]=ast.literal_eval(node.value)
    alpha=float(re.search(rb'^SEALED_CODATA_ALPHA\s*=\s*([^\r\n#]+)',raw,re.M)[1].strip())
    record=json.loads(registry.read_bytes())['core']['neutrino_m2'];actual=sha_obj(values['frozen'])
    if actual!=record['frozen_hash']:raise ValueError('FROZEN_MISMATCH '+actual+' '+record['frozen_hash'])
    snapshot=dict(version='T11_EXTRACTED_READ_ONLY',frozen=values['frozen'],legacy_determinations=values['dets'],
        alpha_fine_codataa2018=alpha,registry_frozen_hash=record['frozen_hash'],registry_tension=record['values']['tensao_atual_sigma'],registry_verdict=record['verdict'],
        source_sha256=sha(source),registry_sha256=sha(registry),rule_excerpt_sha256=sha(S/'prove_neutrino_m2_source.txt'),sha_obj_excerpt_sha256=sha(S/'sha_obj_source.txt'),
        rule_lines=[start,end],sha_obj_lines=[hs,he],extraction='literal_eval of selected assignments only; no exec/import of original',experimental_sources_independently_verified=False)
    save(S/'EXTRACTED_RULES.json',snapshot)
    save(S/'EXTRACTION_RECEIPT.json',dict(snapshot_sha256=sha(S/'EXTRACTED_RULES.json'),frozen_hash=actual,source_sha256=sha(source),registry_sha256=sha(registry),original_executed=False,gate_changed=False))
    print(json.dumps(dict(frozen_hash=actual,snapshot_sha256=sha(S/'EXTRACTED_RULES.json'))))
if __name__=='__main__':main()
