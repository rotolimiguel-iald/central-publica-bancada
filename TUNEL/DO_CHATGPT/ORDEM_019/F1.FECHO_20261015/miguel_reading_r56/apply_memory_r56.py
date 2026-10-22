"""Apply exactly the prepared append with immediate byte backups and CAS."""
from support_r56 import *

preflight()
plan=json.loads((ROOT/'MEMORY_PLAN_R56.json').read_text(encoding='utf-8'))
if (ROOT/'MEMORY_APPLIED_R56.json').exists():raise FileExistsError('delivery already exists')
for item in plan['surfaces']:
 if pin(item['path'])!=item['before']:raise RuntimeError('baseline changed: '+item['path'])
 if pin(item['append']['path'])!=item['append']:raise RuntimeError('append changed')
stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
receipts=[]
for index,item in enumerate(plan['surfaces']):
 p=Path(item['path']);raw=p.read_bytes();suffix=Path(item['append']['path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=item['before']['sha256']:raise RuntimeError('concurrent write')
 backup=p.with_name(p.name+'.bak_'+stamp)
 with backup.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert backup.read_bytes()==raw
 tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 with tmp.open('xb') as f:f.write(raw+suffix);f.flush();os.fsync(f.fileno())
 assert hashlib.sha256(tmp.read_bytes()).hexdigest()==item['after_sha256']
 if p.read_bytes()!=raw:raise RuntimeError('concurrent write before replace')
 os.replace(tmp,p)
 after=p.read_bytes()
 assert after==raw+suffix and after.startswith(backup.read_bytes())
 receipt={'before':item['before'],'backup':pin(backup),'after':pin(p),'pure_append':True}
 new(f'MEMORY_SURFACE_{index:02d}_R56.json',receipt);receipts.append(receipt)
new('MEMORY_APPLIED_R56.json',{'claim':933,'surfaces':receipts,'pure_append_all':True})
print(json.dumps({'surfaces':len(receipts),'pure_append_all':True},ensure_ascii=False))
