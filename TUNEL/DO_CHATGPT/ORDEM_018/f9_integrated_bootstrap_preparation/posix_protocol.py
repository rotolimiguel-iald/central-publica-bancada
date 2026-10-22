"""Prepared POSIX custody/process primitives; importing starts no process."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import signal
import stat
import time

class Refusal(RuntimeError):
    pass

def need(value, reason):
    if not value:
        raise Refusal(reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(',', ':'), allow_nan=False).encode('ascii')

def document(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def constant(_):
        raise Refusal('NONFINITE_JSON')
    need(type(raw) is bytes and raw, 'NONEMPTY_JSON_BYTES')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

def exact(obj, fields):
    need(type(obj) is dict and set(obj) == set(fields), 'EXACT_SCHEMA_REQUIRED')

def positive_integer(value, name):
    need(type(value) is int and value > 0, 'POSITIVE_INTEGER:' + name)

def digest(value):
    need(type(value) is str and len(value) == 64 and
         all(c in '0123456789abcdef' for c in value), 'SHA256_REQUIRED')
    return value

def absolute(path):
    need(type(path) is str and path.startswith('/') and '\\' not in path,
         'ABSOLUTE_POSIX_PATH')
    p = PurePosixPath(path)
    need(str(p) == path and '..' not in p.parts, 'CANONICAL_POSIX_PATH')
    return path

def read_bytes(path, maximum):
    positive_integer(maximum, 'read_cap')
    fd = os.open(absolute(path), os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_size <= maximum, 'REGULAR_BOUNDED_FILE')
        chunks = []
        remaining = maximum + 1
        while remaining:
            block = os.read(fd, min(65536, remaining))
            if not block:
                break
            chunks.append(block)
            remaining -= len(block)
        raw = b''.join(chunks)
        after = os.fstat(fd)
        need(len(raw) <= maximum and before.st_size == len(raw), 'FILE_SIZE_CHANGED')
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'FILE_CHANGED_DURING_READ')
        return raw
    finally:
        os.close(fd)

def pinned(path, expected, maximum):
    exact(expected, ('bytes', 'sha256'))
    need(type(expected['bytes']) is int and 0 <= expected['bytes'] <= maximum, 'PIN_SIZE')
    raw = read_bytes(path, maximum)
    need(len(raw) == expected['bytes'] and sha(raw) == digest(expected['sha256']), 'PIN_MISMATCH:' + str(path))
    return raw

class ProtectedDirectory:
    """Open every component without symlinks; exclusive no-overwrite records.

    The final root must be existing mode0700, owned by current euid. Ancestors
    must be root/current-euid owned and not group/world writable. ACLs, hostile
    same-uid mutation, and hardware durability require external qualification.
    """
    def __init__(self, path):
        self.path = absolute(path)
        need(os.name == 'posix' and os.geteuid() != 0, 'NONROOT_POSIX_REQUIRED')
        fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for part in PurePosixPath(path).parts[1:]:
                old = fd
                fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=old)
                os.close(old)
                s = os.fstat(fd)
                need(s.st_uid in (0, os.geteuid()) and not s.st_mode & 0o022, 'UNPROTECTED_ANCESTOR')
            s = os.fstat(fd)
            need(s.st_uid == os.geteuid() and stat.S_IMODE(s.st_mode) == 0o700, 'PRIVATE_OWNED_ROOT_REQUIRED')
            self.identity = (s.st_dev, s.st_ino, s.st_uid, stat.S_IMODE(s.st_mode))
            self.fd = fd
            os.fsync(fd)
        except BaseException:
            os.close(fd)
            raise

    def _name(self, name):
        need(type(name) is str and name and name not in ('.', '..') and
             '/' not in name and '\\' not in name, 'SINGLE_PATH_COMPONENT')
        return name

    def check(self):
        s = os.fstat(self.fd)
        current = os.stat(self.path, follow_symlinks=False)
        need((s.st_dev, s.st_ino, s.st_uid, stat.S_IMODE(s.st_mode)) == self.identity and
             (current.st_dev, current.st_ino) == self.identity[:2], 'PROTECTED_ROOT_CHANGED')

    def reserve(self, name):
        self.check()
        name = self._name(name)
        os.mkdir(name, mode=0o700, dir_fd=self.fd)  # EEXIST is permanent no-retry.
        os.fsync(self.fd)
        return ProtectedDirectory(self.path + '/' + name)

    def publish(self, name, raw, maximum):
        self.check()
        self._name(name)
        need(type(raw) is bytes and 0 < len(raw) <= maximum, 'PUBLICATION_SIZE')
        # The caller supplies a new deterministic terminal name. The temp name
        # remains a hardlink after publication for exact recovery, as in I02.
        temporary = '.pending_' + sha(name.encode() + raw)
        fd = os.open(temporary, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=self.fd)
        try:
            view = memoryview(raw)
            while view:
                n = os.write(fd, view)
                need(n > 0, 'SHORT_WRITE')
                view = view[n:]
            os.fsync(fd)
            os.lseek(fd, 0, os.SEEK_SET)
            parts = []
            while True:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                parts.append(chunk)
            need(b''.join(parts) == raw, 'TEMP_READBACK')
        finally:
            os.close(fd)
        os.link(temporary, name, src_dir_fd=self.fd, dst_dir_fd=self.fd, follow_symlinks=False)
        os.fsync(self.fd)
        self.check()
        return {'bytes':len(raw), 'sha256':sha(raw)}

    def close(self):
        os.close(self.fd)

def proc_identity(pid):
    need(type(pid) is int and pid > 0, 'PID_REQUIRED')
    base = Path('/proc') / str(pid)
    raw = (base / 'stat').read_text()
    tail = raw[raw.rfind(')') + 2:].split()
    return {'pid':pid, 'start_ticks':int(tail[19]), 'state':tail[0],
            'ppid':int(tail[1]), 'exe':str((base/'exe').resolve(strict=True)),
            'argv':[(x.decode('utf-8')) for x in (base/'cmdline').read_bytes().split(b'\0')[:-1]],
            'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}

def same_process(actual, expected):
    return all(actual[k] == expected[k] for k in ('pid','start_ticks','exe','argv','boot_id'))

def kill_exact(pidfd, expected):
    # pidfd binds the kernel task, avoiding PID-reuse signaling. Never signal by
    # pid alone; a missing or mismatched identity is an uncertain cleanup result.
    actual = proc_identity(expected['pid'])
    need(same_process(actual, expected), 'REFUSE_SIGNAL_IDENTITY_MISMATCH')
    signal.pidfd_send_signal(pidfd, signal.SIGKILL, None, 0)
    return actual

def bounded_error(exc):
    return {'type':type(exc).__name__[:100], 'message':str(exc)[:1000]}
