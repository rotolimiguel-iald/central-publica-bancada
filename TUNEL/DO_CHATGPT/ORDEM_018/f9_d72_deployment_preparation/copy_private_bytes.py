import os,sys,stat,json,hashlib,uuid,datetime
from pathlib import Path
PLAN_PATH=Path('/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_d72_deployment_preparation/COPY_PLAN.json')
plan=json.loads(PLAN_PATH.read_bytes());base=Path('/opt/iald_ordem018_d72_d72f7125')
assert plan['root']==str(base) and os.getuid()==os.geteuid()==65534 and os.getgid()==65534
fd=os.open(base,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);s=os.fstat(fd)
assert s.st_uid==s.st_gid==65534 and stat.S_IMODE(s.st_mode)==0o700 and not os.listdir(fd)
records=[]
for role,sourcekey,filekey in [('package','source_posix','package_files'),('inspection','inspection_source_posix','inspection_files')]:
 os.mkdir(role,0o700,dir_fd=fd);dest=base/role
 for item in plan[filekey]:
  name=item['name'];assert Path(name).name==name
  raw=(Path(plan[sourcekey])/name).read_bytes();expected=item['pin']
  assert {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}==expected
  target=dest/name;temp=dest/(name+'.tmp_'+uuid.uuid4().hex);assert not target.exists()
  w=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
  with os.fdopen(w,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  assert temp.read_bytes()==raw;os.replace(temp,target)
  actual=target.read_bytes();assert actual==raw
  records.append({'role':role,'path':str(target),'bytes':len(actual),'sha256':hashlib.sha256(actual).hexdigest(),'mode':oct(stat.S_IMODE(target.stat().st_mode)),'uid':target.stat().st_uid})
 dfd=os.open(dest,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);os.fsync(dfd);os.close(dfd)
os.fsync(fd);os.close(fd)
print(json.dumps({'schema':'F9_PRIVATE_BYTE_COPY_RECEIPT_V1','status':'COPIED_BYTES_MATCH','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uid':os.getuid(),'root':str(base),'root_device':s.st_dev,'root_inode':s.st_ino,'source_windows':plan['source_windows'],'files':records,'candidate_imports':0,'scientific_execution':False},indent=2))
