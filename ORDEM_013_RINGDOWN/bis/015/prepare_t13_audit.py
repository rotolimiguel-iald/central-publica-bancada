"""Version the integrity check; inventory only named caches; inspect existing cleanup."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,ast
B=Path(__file__).resolve().parents[2];D=B/'bis/015/t13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,data):
    raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode();tmp=p.with_suffix(p.suffix+'.pending')
    if p.exists():raise FileExistsError(p)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.rename(p)
def main():
    original=B/'refeito/final_integrity_013bis.py'
    target=B/'refeito/final_integrity_015_v2.py'
    s=original.read_text('utf-8')
    s=s.replace('for parent, dirs, files in os.walk(B):',"scan_errors = []\n    def record_walk_error(exc):\n        scan_errors.append(dict(path=exc.filename, error=str(exc), type=type(exc).__name__))\n    for parent, dirs, files in os.walk(B, followlinks=False, onerror=record_walk_error):")
    s=s.replace("if all(r['matches'] for r in rows) and not oversized else", "if all(r['matches'] for r in rows) and not oversized and not scan_errors and not unreadable_metadata else")
    s=s.replace("measured_utc=now.isoformat(),", "measured_utc=now.isoformat(), directory_enumeration_errors=scan_errors,\n        supersedes_script_sha256="+repr(sha(original))+",")
    s=s.replace("'bis/FINAL_INTEGRITY_'", "'bis/015/t13/FINAL_INTEGRITY_015_'")
    s=s.replace("metadata_exceptions=unreadable_metadata),", "directory_enumeration_errors=scan_errors, metadata_exceptions=unreadable_metadata),")
    ast.parse(s)
    if target.exists():raise FileExistsError(target)
    with target.open('xb') as f:f.write(s.encode())
    names=['guard_7h3lo515','native_package_tamper_20260922_080445_470834','delivery_fresh_20260922_025830_447404','delivery_v2_fresh_20260922_032436_194092']
    rows=[]
    for name in names:
        p=B/'cache'/name;errors=[];n=total=0;top=[]
        for parent,dirs,files in os.walk(p,followlinks=False,onerror=lambda e:errors.append(str(e))):
            for name2 in files:
                q=Path(parent)/name2
                try:
                    v=q.lstat();total+=v.st_size;n+=1
                    if Path(parent)==p:top.append(name2)
                except OSError as e:errors.append(str(e))
        rows.append(dict(path=str(p),exists=p.exists(),files=n,bytes=total,errors=errors,top_level_names=top,
          role='Historical temporary guard/tamper or fresh-delivery working copy, inferred from directory name',
          deletable='NOT_DELETED__NO_CLOSED_REFERENCE_AUDIT',content_read=False))
    put(D/'CACHE_INVENTORY.json',dict(at=datetime.now(timezone.utc).isoformat(),rows=rows,scope='four literal cache paths; metadata only'))
    # Existing later revisions are checked before adding redundant wrappers.
    candidates=[B/n/'reproduce.py' for n in ['C7_POSTERIOR_REPRODUCTION_v3_2','C7_GWTC3_REPRODUCTION_v3_2','C7_INJECTION_REPRODUCTION_v3_2']]
    candidates += [B/'refeito/replay_legacy_in_temporary_v3.py',B/'refeito/reproduce_c6_v3_2.py']
    cleanup=[]
    for p in candidates:
        if not p.exists():cleanup.append(dict(path=str(p),status='MISSING'));continue
        tree=ast.parse(p.read_text('utf-8-sig'))
        clauses=[n for n in ast.walk(tree) if isinstance(n,ast.Try) and n.finalbody]
        cleanup.append(dict(path=str(p),sha256=sha(p),finally_blocks=len(clauses),cleanup_calls=[dict(line=n.lineno,call=ast.unparse(n.func)) for t in clauses for n in ast.walk(ast.Module(body=t.finalbody,type_ignores=[])) if isinstance(n,ast.Call) and any(x in ast.unparse(n.func) for x in ['rmtree','unlink'])],statute='STATIC_AST_CHECK_NOT_REEXECUTION'))
    put(D/'EXISTING_FINALLY.json',dict(rows=cleanup,F7_predecessor_sha256=sha(B/'bis/F7_POST_REMOVAL_CHECK.json')))
    put(D/'AUDIT_PREPARATION.json',dict(original=str(original),original_sha256=sha(original),new=str(target),new_sha256=sha(target),mutations='onerror + explicit nonpass on directory or metadata errors',seed_content_read=False))
    print(json.dumps(dict(inventory=[{k:r[k] for k in ['path','files','bytes','errors']} for r in rows],cleanup=cleanup),ensure_ascii=False))
if __name__=='__main__':main()
