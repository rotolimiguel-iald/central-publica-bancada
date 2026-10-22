import os,json,hashlib,uuid,stat,datetime
from pathlib import Path
assert os.geteuid()==65534
source=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_d72_deployment_preparation')
plan=json.loads((source/'PUBLISH_DOCUMENTS_PLAN.json').read_bytes());target=Path('/opt/iald_ordem018_d72_d72f7125/inspection');assert plan['target']==str(target)
fd=os.open(target,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);s=os.fstat(fd);assert s.st_uid==s.st_gid==65534 and stat.S_IMODE(s.st_mode)==0o700
rows=[]
for item in plan['files']:
 name=item['name'];assert Path(name).name==name
 raw=(source/name).read_bytes();assert {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}==item['pin']
 dest=target/name;temp=target/(name+'.tmp_'+uuid.uuid4().hex);assert not dest.exists()
 f=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
 with os.fdopen(f,'wb') as w:w.write(raw);w.flush();os.fsync(w.fileno())
 assert temp.read_bytes()==raw;os.replace(temp,dest);assert dest.read_bytes()==raw
 rows.append({'path':str(dest),'pin':item['pin'],'uid':dest.stat().st_uid,'mode':oct(stat.S_IMODE(dest.stat().st_mode))})
os.fsync(fd);os.close(fd)
print(json.dumps({'schema':'F9_RUNTIME_DOCUMENTS_BYTE_COPY_RECEIPT_V1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uid':os.geteuid(),'files':rows,'scientific_execution':False,'candidate_imports':0}))
