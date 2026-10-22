import os,sys,json,stat,signal,datetime
from pathlib import Path
def meta(p):
 try:
  s=os.lstat(p);return {'path':p,'uid':s.st_uid,'gid':s.st_gid,'mode':oct(stat.S_IMODE(s.st_mode)),'is_directory':stat.S_ISDIR(s.st_mode),'is_symlink':stat.S_ISLNK(s.st_mode),'readable':os.access(p,os.R_OK),'writable':os.access(p,os.W_OK),'searchable':os.access(p,os.X_OK)}
 except OSError as e:return {'path':p,'error':type(e).__name__,'errno':e.errno}
assert os.geteuid()==65534
rows=[]
for base in ['/home','/opt','/srv']:
 rows.append(meta(base))
 try:
  for name in sorted(os.listdir(base)):
   rows.append(meta(base+'/'+name))
 except OSError as e:rows.append({'path':base,'scan_error':str(e)})
rows.append(meta('/var/lib'))
print(json.dumps({'schema':'F9_RUNTIME_METADATA_SUPPLEMENT_V1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'euid':os.geteuid(),'python_executable':sys.executable,'python_version':sys.version,'builtins':list(sys.builtin_module_names),'api_presence_only':{'os.pidfd_open':hasattr(os,'pidfd_open'),'signal.pidfd_send_signal':hasattr(signal,'pidfd_send_signal'),'os.O_NOFOLLOW':hasattr(os,'O_NOFOLLOW'),'os.O_DIRECTORY':hasattr(os,'O_DIRECTORY'),'os.O_EXCL':hasattr(os,'O_EXCL'),'sys.addaudithook':hasattr(sys,'addaudithook')},'api_semantics_exercised':False,'mount_types':[line for line in Path('/proc/self/mountinfo').read_text().splitlines() if ' / ' in line or ' /mnt/c ' in line or ' /sys/fs/cgroup ' in line],'process_threads_sample':len(os.listdir('/proc/self/task')),'top_level_path_candidates_metadata_only':rows,'runtime_features_not_measured':['scientific_import_trace','scientific_native_maps','native_syscall_IO','scientific_transient_threads','directory_durability','hardlink_execution','pidfd_kill_reap_execution'],'candidate_imports':0,'solver_calls':0,'linux_writes':0},indent=2))
