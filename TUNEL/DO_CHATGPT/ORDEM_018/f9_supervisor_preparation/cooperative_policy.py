"""Scoped Python audit policy; explicitly not native syscall isolation."""
import os
from pathlib import Path
import sys
import threading
from audit_guard import AuditLatch, PreopenedJournal
from posix_protocol import need, read_bytes, sha

class CooperativePolicy:
    def __init__(self, *, read_pins, journal_path, output_fds, deadline):
        self.read_pins = dict(read_pins)
        self.deadline = deadline
        self.journal = PreopenedJournal(journal_path)
        self.latch = AuditLatch(self.journal)
        self.output_fds = set(output_fds) | {self.journal.fd}
        self.fd_identity = {fd:(os.fstat(fd).st_dev,os.fstat(fd).st_ino,os.fstat(fd).st_mode)
                            for fd in self.output_fds}
        self.installed = False
        self.network_denials = self.read_denials = 0
        self.read_events = 0
        self.native_syscalls_observed = False

    def _audit(self, event, args):
        reason = None
        target = str(args[:1])[:500]
        if event.startswith(('socket.','subprocess.','os.spawn')) or event in (
            'os.system','os.posix_spawn','os.fork','os.forkpty','os.remove','os.rmdir',
            'os.rename','os.mkdir','os.link','os.symlink','os.truncate','sys.addaudithook'):
            reason='OPERATION_OUTSIDE_STDLIB_QUALIFICATION'
            if event.startswith('socket.'):
                self.network_denials += 1
        if event == 'ctypes.dlopen':
            reason='NATIVE_DYNAMIC_LOAD_NOT_ALLOWED_IN_STDLIB_SCOPE'
        if event == 'open':
            target,mode,flags=args
            writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (
                isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
            if isinstance(target,int):
                if target not in self.output_fds:
                    reason='UNREGISTERED_FILE_DESCRIPTOR'
            elif writing:
                reason='NO_PATH_WRITES_AFTER_HOOK'
            else:
                name=os.path.normpath(str(target))
                if name not in self.read_pins:
                    self.read_denials += 1
                    reason='UNPINNED_READ'
                self.read_events += 1
        if reason:
            self.latch.deny(event,target,reason=reason)

    def install(self):
        need(not self.installed, 'AUDIT_ALREADY_INSTALLED')
        sys.addaudithook(self._audit)
        self.latch.installed()
        self.installed=True
        self.checkpoint('AFTER_HOOK')

    def checkpoint(self, phase):
        import time
        need(self.installed and time.monotonic()<self.deadline,'AUDIT_OR_DEADLINE')
        self.latch.checkpoint(phase)
        for fd,expected in self.fd_identity.items():
            s=os.fstat(fd)
            need((s.st_dev,s.st_ino,s.st_mode)==expected,'DESCRIPTOR_OWNERSHIP_CHANGED')
        need(len(threading.enumerate())==1,'PYTHON_THREADS_CHANGED')

    def verify_loaded_modules(self):
        # Paths and bytes measured again; trust remains cooperative: this is not
        # proof that arbitrary native code made no unobserved file/network call.
        for name,module in list(sys.modules.items()):
            path=getattr(module,'__file__',None)
            if not path or str(path).startswith('<'):
                continue
            path=os.path.normpath(str(path))
            need(path in self.read_pins,'UNPINNED_LOADED_MODULE:'+name)
            raw=read_bytes(path,max(self.read_pins[path]['bytes'],1))
            need(len(raw)==self.read_pins[path]['bytes'] and sha(raw)==self.read_pins[path]['sha256'],
                 'LOADED_SOURCE_BYTES_CHANGED:'+name)
        self.checkpoint('AFTER_LOADED_MODULE_PINS')

    def receipt(self):
        self.checkpoint('BEFORE_COOPERATIVE_RECEIPT')
        return {'scope':'PYTHON_AUDIT_EVENTS_COOPERATIVE_ONLY','snapshot':self.latch.snapshot(),
            'python_network_denials':self.network_denials,'python_unexpected_read_denials':self.read_denials,
            'python_read_events':self.read_events,'native_syscalls_observed':False,
            'native_network_operations':None,'native_file_operations':None,
            'OS_network_isolation':False,'OS_read_isolation':False}
