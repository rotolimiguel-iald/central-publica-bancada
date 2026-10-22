"""Cooperative Python audit policy for exact I02 operations and pinned runtime.

Not a syscall sandbox. Native IO counters remain unknown. The trusted runtime,
private roots and one-thread envelope must be qualified externally before use.
"""
import os
from pathlib import Path
import re
import stat
import sys
import time
from audit_guard import AuditLatch
from posix_protocol import canonical, need, pinned, sha

STORE_NAME=re.compile(r'(?:background|node)_[0-9a-f]{64}\.(?:claim|result|failure)\.json\Z')
TEMP_NAME=re.compile(r'\.pending_[0-9a-f]{32}\Z')

class RuntimePolicy:
    def __init__(self, *, package, package_pins, runtime, roots, resources,
                 deadline, journal, owned_fds):
        self.package=Path(package);self.runtime=runtime;self.deadline=deadline
        self.roots={str(Path(v)):k for k,v in roots.items()};need(set(self.roots.values())=={'nodes','runs'},'TWO_STORE_ROOTS')
        self.resources=resources;self.latch=AuditLatch(journal);self.fds={}
        for fd in owned_fds:
            s=os.fstat(fd);self.fds[fd]=(s.st_dev,s.st_ino,s.st_mode)
        self.read_pins=dict(runtime['files'])
        self.read_pins.update({str(self.package/k):v for k,v in package_pins.items()})
        self.absent=set(runtime['absent_paths']);self.scans=set(runtime['scan_directories'])
        self.native=runtime['native_map_pins'];self.reserved={};self.reserved_bytes=0
        self.root_ids={};self.max_threads=0;self.map_samples=0;self.maps_seen={};self.busy=False
        self.pid=os.getpid()
        self.proc={f'/proc/{self.pid}/stat',f'/proc/{self.pid}/cmdline',f'/proc/{self.pid}/maps',
                   '/proc/sys/kernel/random/boot_id'}
        self.taskdir=f'/proc/{self.pid}/task'
        for root in self.roots:
            s=os.stat(root,follow_symlinks=False)
            need(stat.S_ISDIR(s.st_mode) and s.st_uid==os.geteuid() and stat.S_IMODE(s.st_mode)==0o700,'STORE_PRIVATE_ROOT')
            need(not os.listdir(root),'STORE_MUST_START_EMPTY')
            self.root_ids[root]=(s.st_dev,s.st_ino,s.st_uid,stat.S_IMODE(s.st_mode))
        need(not(set(self.read_pins)&self.absent),'PRESENT_AND_ABSENT_CONFLICT')

    def install(self):
        sys.addaudithook(self.hook);self.latch.installed();self.checkpoint('HOOK_INSTALLED')

    def deny(self,event,target,reason):
        self.latch.deny(event,str(target),reason=reason)

    def store_path(self,path):
        if not isinstance(path,(str,bytes,os.PathLike)):return None
        s=os.fsdecode(path)
        if not os.path.isabs(s) or os.path.normpath(s)!=s:return None
        root,name=os.path.split(s)
        if root in self.roots and (STORE_NAME.fullmatch(name) or TEMP_NAME.fullmatch(name)):
            return (root,name)
        return None

    def _fd(self,fd):
        s=os.fstat(fd)
        if fd in self.fds:
            need((s.st_dev,s.st_ino,s.st_mode)==self.fds[fd],'PREOPENED_FD_CHANGED');return
        path=os.readlink(f'/proc/{self.pid}/fd/{fd}')
        need(self.store_path(path) is not None and stat.S_ISREG(s.st_mode) and s.st_uid==os.geteuid()
             and stat.S_IMODE(s.st_mode)==0o600,'UNOWNED_DYNAMIC_FD')
        a=os.stat(path,follow_symlinks=False)
        need((a.st_dev,a.st_ino)==(s.st_dev,s.st_ino),'FD_PATH_IDENTITY')

    def hook(self,event,args):
        try:self._dispatch_event(event,args)
        except BaseException as exc:
            # A descriptor/metadata failure is also sticky. A caught exception
            # must never erase an attempted policy violation.
            if self.latch._latched:raise
            self.deny(event,event,'AUDIT_POLICY_CHECK_FAILED:'+type(exc).__name__)

    def _dispatch_event(self,event,args):
        # Python audit hooks are reentrant. Internal metadata checks below only
        # use stat/readlink/fstat, never unguarded filesystem reads or mutations.
        if event=='open':
            path,mode,flags=args
            if isinstance(path,int):
                self._fd(path);return
            s=os.fsdecode(path);writing=bool(flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
            if writing:
                store=self.store_path(s)
                allowed=os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW
                extras=getattr(os,'O_CLOEXEC',0)
                if store is None or flags&~extras!=allowed:self.deny(event,s,'EXACT_I02_EXCLUSIVE_WRITE_REQUIRED')
                root,name=store
                if STORE_NAME.fullmatch(name) and not name.endswith('.claim.json'):self.deny(event,s,'RESULT_REQUIRES_HARDLINK_PUBLICATION')
                if s in self.reserved or os.path.lexists(s):self.deny(event,s,'PATH_ALREADY_CONSUMED')
                cap=self.resources['max_record_bytes'] if self.roots[root]=='nodes' else self.resources['max_run_record_bytes']
                if self.reserved_bytes+cap>self.resources['nominal_store_bytes']:self.deny(event,s,'AGGREGATE_CONSERVATIVE_STORE_QUOTA')
                self.reserved[s]=cap;self.reserved_bytes+=cap
                return
            if s in self.read_pins or s in self.proc:return
            if s in self.absent:
                if os.path.lexists(s):self.deny(event,s,'ABSENT_PROBE_NOW_PRESENT')
                return
            if s in self.roots and flags&os.O_DIRECTORY:return
            if self.store_path(s) is not None:return
            self.deny(event,s,'READ_NOT_IN_PINNED_CLOSURE_OR_EXACT_STORE')
        elif event in ('os.listdir','os.scandir'):
            target=args[0]
            if isinstance(target,int):self.deny(event,target,'DIRECTORY_FD_SCAN_NOT_ADMITTED')
            s=os.fsdecode(target)
            if s not in self.scans and s not in self.roots and s!=self.taskdir:self.deny(event,s,'UNADMITTED_DIRECTORY_SCAN')
        elif event=='os.link':
            src,dst,srcfd,dstfd=args
            a=self.store_path(src);b=self.store_path(dst)
            if srcfd!=-1 or dstfd!=-1 or a is None or b is None or a[0]!=b[0] or not TEMP_NAME.fullmatch(a[1]) or not b[1].endswith(('.result.json','.failure.json')):
                self.deny(event,args,'EXACT_I02_HARDLINK_REQUIRED')
            s=os.stat(src,follow_symlinks=False)
            if str(src) not in self.reserved or not stat.S_ISREG(s.st_mode) or s.st_uid!=os.geteuid() or os.path.lexists(dst):
                self.deny(event,args,'UNOWNED_OR_OVERWRITING_PUBLICATION')
        elif event.startswith('socket.') or event.startswith(('subprocess.','os.exec','os.spawn','os.fork','os.posix_spawn')):
            self.deny(event,event,'NO_PYTHON_NETWORK_OR_CHILD_PROCESS')
        elif event in ('os.remove','os.rename','os.rmdir','os.mkdir','os.symlink','os.chmod','os.chown','os.truncate','os.utime','os.chroot','os.chdir'):
            self.deny(event,args,'FILESYSTEM_MUTATION_OUTSIDE_EXACT_I02')
        elif event=='ctypes.dlopen':
            target=args[0]
            # Basename resolution is disallowed: the actual full native library
            # must be among the reviewed runtime pins, never an arbitrary path.
            if target is not None and target not in self.native:self.deny(event,target,'UNPINNED_NATIVE_DLOPEN')
            # ctypes.pythonapi obtains the existing process image with None.
            # It is admitted only for the already pinned interpreter and later
            # sampled map closure; it does not establish universal IO isolation.
            if target is None:need(self.runtime['python_executable'] in self.native,'PROCESS_IMAGE_NOT_PINNED')
        elif event=='import' and len(args)>1 and args[1] is not None:
            filename=args[1]
            if os.path.isabs(filename) and filename not in self.read_pins and filename not in self.native:self.deny(event,filename,'IMPORT_OUTSIDE_PINNED_RUNTIME')

    def checkpoint(self,phase):
        self.latch.checkpoint(phase);need(time.monotonic()<self.deadline,'WHOLE_COMMAND_DEADLINE')
        for root,expected in self.root_ids.items():
            s=os.stat(root,follow_symlinks=False)
            need((s.st_dev,s.st_ino,s.st_uid,stat.S_IMODE(s.st_mode))==expected,'STORE_ROOT_CHANGED')
        for fd in self.fds:self._fd(fd)
        count=len(os.listdir(self.taskdir));self.max_threads=max(self.max_threads,count)
        need(count==self.resources['threads']==1,'ACTUAL_THREAD_ENVELOPE_EXCEEDED')

    def verify_runtime_modules_and_maps(self):
        self.checkpoint('RUNTIME_MAPS')
        for name,module in tuple(sys.modules.items()):
            path=getattr(module,'__file__',None)
            if path is None:continue
            path=str(Path(path).absolute())
            expected=self.read_pins.get(path)
            need(expected is not None,'LOADED_MODULE_OUTSIDE_PINNED_CLOSURE:'+name)
            pinned(path,expected,max(1,expected['bytes']))
        lines=Path(f'/proc/{self.pid}/maps').read_text().splitlines()
        seen={}
        for line in lines:
            fields=line.split(None,5)
            if len(fields)<6 or not fields[5].startswith('/'):continue
            path=fields[5];need(not path.endswith(' (deleted)'),'DELETED_NATIVE_MAPPING')
            need(path in self.native,'NATIVE_MAPPING_OUTSIDE_INVENTORY:'+path)
            pinned(path,self.native[path],max(1,self.native[path]['bytes']));seen[path]=self.native[path]
        need(seen,'NO_NATIVE_MAPPING_EVIDENCE');self.maps_seen.update(seen);self.map_samples+=1
        return seen

    def measurements(self):
        self.checkpoint('RESOURCE_SNAPSHOT')
        return {'store_reserved_bytes':self.reserved_bytes,'store_exclusive_creations':len(self.reserved),
                'store_quota_bytes':self.resources['nominal_store_bytes'],'max_threads_observed':self.max_threads,
                'native_map_samples':self.map_samples,'native_map_pins':self.maps_seen,
                'quota_scope':'Python exact-store creation reserves full per-record cap before open; hardlinks share inode',
                'transient_native_threads_between_samples':None,'native_file_operations':None,'native_network_operations':None}
