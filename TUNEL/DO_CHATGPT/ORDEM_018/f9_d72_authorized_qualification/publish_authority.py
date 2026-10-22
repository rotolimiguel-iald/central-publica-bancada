import os,sys,json,hashlib,stat,datetime
from pathlib import Path
source=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_d72_authorized_qualification')
plan=json.loads((source/'PUBLISH_PLAN.json').read_bytes());base=Path(plan['private_root']);target=Path(plan['target'])
assert os.geteuid()==65534 and target.parent==base and target.name=='authority'
s=base.lstat();assert s.st_uid==65534 and stat.S_IMODE(s.st_mode)==0o700 and not base.is_symlink()
assert not (base/plan['unit']).exists() and not target.exists()
target.mkdir(mode=0o700);rows=[]
for item in plan['files']:
 name=item['name'];assert Path(name).name==name
 raw=(source/name).read_bytes();assert {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}==item['pin']
 dest=target/name;tmp=target/(name+'.pending');fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
 with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==raw;os.replace(tmp,dest);assert dest.read_bytes()==raw
 rows.append({'path':str(dest),'pin':item['pin'],'uid':dest.stat().st_uid,'mode':oct(stat.S_IMODE(dest.stat().st_mode))})
for p in (target,base):
 fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);os.fsync(fd);os.close(fd)
print(json.dumps({'schema':'F9_ROOT_AUTHORITY_PUBLICATION_V1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unit':plan['unit'],'files':rows,'science_executions':0}))
