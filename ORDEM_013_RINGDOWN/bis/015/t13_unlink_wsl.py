"""Remove one named negative-test symlink; seed metadata only, never content."""
from pathlib import Path
from datetime import datetime, timezone
import os, stat, json
B=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN')
OUT=B/'bis/015/t13/WSL_UNLINK.json'
TARGET=B/'bis/e3_allocation_review/fixtures_001/finding_symlink_output_escape/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_allocation_prepare/candidates'
def metadata(p):
    try:
        s=p.stat();return dict(path=str(p),exists=True,bytes=s.st_size,mtime_ns=s.st_mtime_ns)
    except FileNotFoundError:return dict(path=str(p),exists=False)
    except OSError as e:return dict(path=str(p),exists=None,error=str(e))
def main():
    if OUT.exists():raise FileExistsError(OUT)
    seeds=[B/'cache/E2_PRIVATE/BLIND_SEED_V1.bin',B/'bis/cache/E2_PRIVATE/BLIND_SEED_V1.bin']
    before=[metadata(p) for p in seeds]
    row=dict(path=str(TARGET),status='NOT_ATTEMPTED',command='Path.unlink of literal symlink only; no recursion')
    try:
        assert TARGET.parent.resolve().is_relative_to(B.resolve())
        assert TARGET.parent.resolve()==TARGET.parent
        s=TARGET.lstat();row['lstat_before']=dict(mode=s.st_mode,bytes=s.st_size,mtime_ns=s.st_mtime_ns)
        if not stat.S_ISLNK(s.st_mode):raise ValueError('Not a symlink; refused')
        row['link_target']=os.readlink(TARGET)
        TARGET.unlink();row['status']='UNLINKED';row['link_absent']=not os.path.lexists(TARGET)
    except FileNotFoundError:row['status']='ALREADY_ABSENT'
    except Exception as e:row.update(status='NOT_REMOVED',error=str(e))
    after=[metadata(p) for p in seeds]
    r=dict(at=datetime.now(timezone.utc).isoformat(),seed_before=before,seed_after=after,
           seed_metadata_same=before==after,seed_content_read=False,unlink=row)
    raw=(json.dumps(r,indent=2)+'\n').encode();tmp=OUT.with_suffix('.pending')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.rename(OUT)
    print(json.dumps(r))
if __name__=='__main__':main()
