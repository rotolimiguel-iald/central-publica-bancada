import os,sys,stat,json,datetime
TARGET='/opt/iald_ordem018_d72_d72f7125'
assert os.geteuid()==0 and os.path.isabs(TARGET) and os.path.normpath(TARGET)==TARGET
parent=os.open('/opt',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
try:
 s=os.fstat(parent);assert s.st_uid==0 and not s.st_mode&0o022
 name=os.path.basename(TARGET)
 try:
  old=os.stat(name,dir_fd=parent,follow_symlinks=False)
  print(json.dumps({'status':'REFUSED_TARGET_EXISTS_NO_MUTATION','target':TARGET,'uid':old.st_uid,'gid':old.st_gid,'mode':oct(stat.S_IMODE(old.st_mode))}));sys.exit(10)
 except FileNotFoundError:pass
 os.mkdir(name,0o700,dir_fd=parent)
 os.chown(name,65534,65534,dir_fd=parent,follow_symlinks=False)
 fd=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
 try:
  s=os.fstat(fd);assert stat.S_IMODE(s.st_mode)==0o700 and s.st_uid==s.st_gid==65534 and not os.listdir(fd)
  os.fsync(fd);os.fsync(parent)
  print(json.dumps({'schema':'F9_PRIVATE_ROOT_CREATION_RECEIPT_V1','status':'CREATED_NEW_EMPTY_ROOT','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target':TARGET,'parent':'/opt','uid':s.st_uid,'gid':s.st_gid,'mode':oct(stat.S_IMODE(s.st_mode)),'device':s.st_dev,'inode':s.st_ino,'empty':True,'existing_directory_ownership_or_modes_modified':False}))
 finally:os.close(fd)
finally:os.close(parent)
