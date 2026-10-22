import os,json,stat,datetime
from pathlib import Path
assert os.geteuid()==65534
root=Path('/opt/iald_ordem018_d72_d72f7125')
old=json.loads(Path('/mnt/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/f9_d72_runtime_preparation/CURRENT_RUNTIME_OBSERVATIONS.json').read_bytes())
new=json.loads((root/'inspection'/'IMPORT_STDOUT.txt').read_bytes())
files=dict(old['files'])
for path,pin in new['files'].items():
 if path in files:assert files[path]==pin
 files[path]=pin
rows=[];issues=[]
for path,pin in sorted(files.items()):
 try:
  s=os.lstat(path);row={'path':path,'mode':oct(stat.S_IMODE(s.st_mode)),'uid':s.st_uid,'gid':s.st_gid,'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'inode':s.st_ino,'device':s.st_dev,'regular':stat.S_ISREG(s.st_mode),'symlink':stat.S_ISLNK(s.st_mode),'realpath':os.path.realpath(path)}
  if not row['regular'] or row['symlink'] or row['realpath']!=path or s.st_size!=pin['bytes']:issues.append(row)
  rows.append(row)
 except OSError as e:issues.append({'path':path,'error':str(e)})
roots=[]
for path in ['/','/opt',str(root),str(root/'package'),str(root/'inspection')]:
 s=os.lstat(path);roots.append({'path':path,'mode':oct(stat.S_IMODE(s.st_mode)),'uid':s.st_uid,'gid':s.st_gid,'device':s.st_dev,'inode':s.st_ino,'symlink':stat.S_ISLNK(s.st_mode),'directory':stat.S_ISDIR(s.st_mode)})
scans={str(root/'package'):sorted(os.listdir(root/'package'))}
probes=sorted(set(new['absent_paths'])|{'/usr/lib/python312.zip'})
absent={path:not os.path.lexists(path) for path in probes}
result={'schema':'F9_CURRENT_NOFOLLOW_METADATA_CHECK_V1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'euid':os.geteuid(),'files_checked':len(files),'rows':rows,'issues':issues,'root_chain':roots,'explicit_package_directory_scan':scans,'absent_path_checks':absent,'new_scientific_imports':0,'solver_calls':0,'file_contents_rehashed':0}
print(json.dumps(result,sort_keys=True))
assert not issues and all(absent.values())
