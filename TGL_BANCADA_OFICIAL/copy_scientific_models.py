"""Freeze the existing, inspected ringdown executor without editing its sources."""
import hashlib,json,shutil
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
SOURCE=Path(r'C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN')
def main():
    dest=HERE/'models';dest.mkdir(exist_ok=True)
    records=[]
    for name in ('tgl_ringdown_prediction.py','tgl_ringdown_template.py'):
        src=SOURCE/name;target=dest/name;data=src.read_bytes()
        if target.exists() and target.read_bytes()!=data:raise ValueError('Existing model copy differs: review before replacing')
        tmp=target.with_suffix('.new');tmp.write_bytes(data);tmp.replace(target)
        records.append({'source':str(src),'copy':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    manifest=dest/'model_sources.json'
    if manifest.exists():
        previous=json.loads(manifest.read_text())
        if previous['files']!=records:raise ValueError('Model manifest changed')
    else:
        temp=manifest.with_suffix('.new');temp.write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'CONDITIONAL_RINGDOWN_EXECUTOR_COPY_NOT_NEW_PHYSICS','files':records},indent=2),encoding='utf-8');temp.replace(manifest)
    print(json.dumps(records))
if __name__=='__main__':main()
