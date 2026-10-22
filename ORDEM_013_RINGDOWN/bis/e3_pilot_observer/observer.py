"""Opt-in, bounded Linux metadata observer. Never launches or controls a job."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import time

HERE = Path(__file__).resolve().parent
B = HERE.parents[1]
PILOT = B / 'cache/E3_PSEOB_PILOT_V1'
OBSERVATIONS = B / 'cache/E3_PILOT_OS_OBSERVER_V1'
MAX_BYTES = 65536
MAX_PROCESSES = 128


def require(ok, message):
    if not ok:
        raise ValueError(message)


def strict(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate key')
            result[key] = value
        return result
    def bad(value):
        raise ValueError('nonfinite JSON')
    value = json.loads(data, object_pairs_hook=pairs, parse_constant=bad)
    def check(item):
        if isinstance(item, float):
            require(math.isfinite(item), 'nonfinite JSON number')
        elif isinstance(item, dict):
            for entry in item.values(): check(entry)
        elif isinstance(item, list):
            for entry in item: check(entry)
    check(value)
    return value


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bounded_read(path):
    # All callers supply paths constrained by their own fixed allowlist.
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    try:
        import stat
        require(stat.S_ISREG(os.fstat(fd).st_mode), 'not a regular metadata file')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            value = stream.read(MAX_BYTES + 1)
        require(len(value) <= MAX_BYTES, 'metadata size bound')
        return value
    finally:
        os.close(fd)


def parse_stat(text):
    # Last ')' terminates comm; spaces and ')' inside comm are legitimate.
    left = text.index('(')
    right = text.rindex(')')
    pid = int(text[:left].strip())
    values = text[right + 1:].split()
    require(len(values) >= 20, 'truncated stat')
    result = dict(pid=pid, state=values[0], ppid=int(values[1]), pgid=int(values[2]),
                  sid=int(values[3]), utime=int(values[11]), stime=int(values[12]),
                  start_ticks=int(values[19]))
    require(pid > 1 and result['start_ticks'] > 0, 'invalid identity')
    require(all(result[k] >= 0 for k in ('ppid', 'pgid', 'sid', 'utime', 'stime')), 'negative stat')
    return result


class Proc:
    """Only these /proc metadata paths can be opened; no generic file accessor."""
    @staticmethod
    def allowed(relative):
        return bool(relative == 'sys/kernel/random/boot_id' or
                    re.fullmatch(r'[1-9][0-9]*/(?:stat|status|task/[1-9][0-9]*/children)', relative))

    def read(self, relative):
        require(self.allowed(relative), 'proc path denied')
        return bounded_read(Path('/proc') / relative).decode('ascii')

    def namespace(self, pid):
        require(type(pid) is int and pid > 1, 'invalid pid')
        value = os.readlink('/proc/' + str(pid) + '/ns/pid')
        require(re.fullmatch(r'pid:\[[0-9]+\]', value) is not None, 'invalid namespace')
        return value

    def record(self, pid):
        require(type(pid) is int and pid > 1, 'invalid pid')
        first = parse_stat(self.read(str(pid) + '/stat'))
        rows = [x for x in self.read(str(pid) + '/status').splitlines() if x.startswith('Uid:')]
        require(len(rows) == 1, 'UID missing')
        uids = [int(x) for x in rows[0].split()[1:]]
        require(len(uids) == 4 and len(set(uids)) == 1, 'UID ambiguity')
        namespace = self.namespace(pid)
        last = parse_stat(self.read(str(pid) + '/stat'))
        require(first['pid'] == last['pid'] == pid and first['start_ticks'] == last['start_ticks'], 'identity race')
        last.update(uid=uids[0], namespace=namespace)
        return last

    def children(self, pid):
        require(type(pid) is int and pid > 1, 'invalid pid')
        tids = list((Path('/proc') / str(pid) / 'task').iterdir())
        require(len(tids) <= MAX_PROCESSES, 'thread discovery bound')
        children = set()
        for tid in tids:
            require(tid.name.isdigit(), 'invalid task name')
            value = self.read(str(pid) + '/task/' + tid.name + '/children')
            for item in value.split():
                number = int(item)
                require(number > 1, 'invalid child')
                children.add(number)
                require(len(children) <= MAX_PROCESSES, 'child discovery bound')
        return sorted(children)


class Tracker:
    def __init__(self, proc, controller_pid, controller_ticks, uid, namespace, boot_id, hz):
        require(type(hz) is int and hz > 0, 'invalid clock tick scale')
        self.proc, self.pid, self.ticks = proc, controller_pid, controller_ticks
        self.uid, self.namespace, self.boot_id, self.hz = uid, namespace, boot_id, hz
        self.leader = None
        self.known = {}
        self.error_count = 0
        self.controller_max = 0

    @staticmethod
    def key(record):
        return str(record['pid']) + ':' + str(record['start_ticks'])

    def read_owned(self, pid, ticks=None):
        r = self.proc.record(pid)
        require(r['uid'] == self.uid and r['namespace'] == self.namespace, 'UID/namespace mismatch')
        require(ticks is None or r['start_ticks'] == ticks, 'PID reused')
        return r

    def children_stable(self, record):
        values = self.proc.children(record['pid'])
        self.read_owned(record['pid'], record['start_ticks'])
        require(len(values) <= MAX_PROCESSES, 'child limit')
        return values

    def admit(self, r, parent):
        require(len(self.known) < MAX_PROCESSES, 'lifetime process bound')
        require(r['start_ticks'] >= parent['start_ticks'], 'child older than parent')
        require(r['ppid'] == parent['pid'], 'unproven ancestry')
        if self.leader is not None:
            require(r['pgid'] == self.leader['pid'] and r['sid'] == self.leader['pid'], 'group/session mismatch')
        key = self.key(r)
        self.known[key] = dict(identity=r, max_ticks=0, observed_parent_key=self.key(parent),
                               quarantined=False, last_seen_sequence=None)
        return key

    def sweep(self, sequence):
        errors, seen = [], []
        controller = None
        try:
            controller = self.read_owned(self.pid, self.ticks)
            ticks = controller['utime'] + controller['stime']
            require(ticks >= self.controller_max, 'controller counter decreased')
            self.controller_max = ticks
        except (OSError, ValueError, KeyError) as e:
            errors.append('controller:' + type(e).__name__ + ':' + str(e))
        if self.leader is None and controller is not None:
            try:
                children = self.children_stable(controller)
                require(len(children) == 1, 'leader absent or ambiguous')
                candidate = self.read_owned(children[0])
                require(candidate['pid'] == candidate['pgid'] == candidate['sid'], 'not session/group leader')
                self.admit(candidate, controller)
                self.leader = candidate
            except (OSError, ValueError, KeyError) as e:
                errors.append('leader:' + type(e).__name__ + ':' + str(e))
        queue = list(self.known)
        visited = set()
        while queue:
            key = queue.pop(0)
            if key in visited: continue
            visited.add(key)
            entry = self.known[key]
            if entry['quarantined']: continue
            old = entry['identity']
            try:
                r = self.read_owned(old['pid'], old['start_ticks'])
                require(r['pgid'] == old['pgid'] and r['sid'] == old['sid'], 'group/session changed')
                ticks = r['utime'] + r['stime']
                require(ticks >= entry['max_ticks'], 'counter decreased')
                entry['max_ticks'] = ticks
                entry['last_seen_sequence'] = sequence
                seen.append(dict(key=key, **r))
            except FileNotFoundError:
                errors.append('unseen_or_exited:' + key)
                continue
            except (OSError, ValueError, KeyError) as e:
                entry['quarantined'] = True
                errors.append('quarantined:' + key + ':' + type(e).__name__ + ':' + str(e))
                continue
            try:
                for pid in self.children_stable(r):
                    child = self.read_owned(pid)
                    child_key = self.key(child)
                    if child_key not in self.known:
                        child_key = self.admit(child, r)
                        queue.append(child_key)
            except (OSError, ValueError, KeyError) as e:
                errors.append('discovery_gap:' + key + ':' + type(e).__name__ + ':' + str(e))
        self.error_count += len(errors)
        return dict(sequence=sequence, owned_identity_records=seen,
                    identity_ledger=list(self.known.values()), errors=errors,
                    cpu_observed_lower_bound_seconds=sum(v['max_ticks'] for v in self.known.values()) / self.hz,
                    controller_cpu_separate_seconds=self.controller_max / self.hz,
                    ownership_resolved=self.leader is not None,
                    coverage_complete=False, scientific_progress=None)


def metadata(name):
    require(name in ('LAUNCH_CONTEXT.json', 'CONTROLLER.json'), 'job metadata denied')
    require(PILOT.resolve() == PILOT.absolute(), 'linked pilot output denied')
    return bounded_read(PILOT / name)


def publish(path, value):
    data = (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + '\n').encode('utf-8')
    with path.open('xb') as f:
        f.write(data)
    return digest(data)


def observation_directory(name):
    require(isinstance(name, str) and re.fullmatch('observation_[0-9]{3,6}', name), 'output name denied')
    cache = B / 'cache'
    require(cache.resolve() == cache.absolute() and cache.is_dir(), 'cache confinement')
    require(OBSERVATIONS.resolve() == OBSERVATIONS.absolute(), 'linked observer output denied')
    OBSERVATIONS.mkdir(mode=0o700, exist_ok=True)
    require(OBSERVATIONS.is_dir(), 'observer root must be directory')
    target = OBSERVATIONS / name
    require(target.parent.resolve() == OBSERVATIONS and not target.exists() and not target.is_symlink(), 'exclusive observation required')
    target.mkdir(mode=0o700)
    return target


def utc():
    return datetime.now(timezone.utc).isoformat()


def deadline(stop_epoch, wall_now, mono_now, max_seconds):
    require(all(type(v) in (int, float) and math.isfinite(v) for v in (stop_epoch, wall_now, mono_now, max_seconds)), 'finite times required')
    require(0 < max_seconds <= 10 * 3600 + 15, 'observer duration bound')
    remaining = stop_epoch + 15 - wall_now
    require(remaining > 0, 'observation window expired')
    return mono_now + min(remaining, max_seconds)


def remaining(end_mono, stop_epoch, mono_now, wall_now):
    return max(0., min(end_mono - mono_now, stop_epoch + 15 - wall_now))


def snapshot_write(stream, value, chain):
    data = (json.dumps(value, allow_nan=False) + '\n').encode('utf-8')
    require(stream.write(data) == len(data), 'short metadata write')
    stream.flush()
    chain.update(data)
    return len(data)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--observe', action='store_true')
    p.add_argument('--context-sha256')
    p.add_argument('--registration-sha256')
    p.add_argument('--config-sha256')
    p.add_argument('--output-name')
    p.add_argument('--max-seconds', type=float, default=8 * 3600 + 15)
    args = p.parse_args()
    if not args.observe:
        print('INACTIVE: no process or job metadata read')
        return
    require(os.name == 'posix' and Path('/proc').is_dir(), 'Linux /proc required')
    for value in (args.context_sha256, args.registration_sha256, args.config_sha256):
        require(isinstance(value, str) and re.fullmatch('[a-f0-9]{64}', value), 'explicit hashes required')
    require(isinstance(args.output_name, str) and re.fullmatch('observation_[0-9]{3,6}', args.output_name), 'new output name required')
    require(math.isfinite(args.max_seconds) and 0 < args.max_seconds <= 10 * 3600 + 15, 'observer duration bound')
    raw = metadata('LAUNCH_CONTEXT.json')
    require(digest(raw) == args.context_sha256, 'context hash mismatch')
    ctx = strict(raw)
    require(ctx['job'] == 'GW250114_PILOT', 'pilot only')
    require(ctx['registration_sha256'] == args.registration_sha256 and ctx['config_sha256'] == args.config_sha256, 'registration/config mismatch')
    require(type(ctx['controller_pid']) is int and ctx['controller_pid'] > 1, 'controller pid')
    ticks = int(ctx['controller_start_ticks'])
    require(ticks > 0, 'controller ticks')
    stop = datetime.fromisoformat(ctx['stop_utc'])
    require(stop.tzinfo is not None, 'timezone required')
    end = deadline(stop.timestamp(), time.time(), time.monotonic(), args.max_seconds)
    proc = Proc()
    boot = proc.read('sys/kernel/random/boot_id').strip()
    require(re.fullmatch('[0-9a-f-]{36}', boot) is not None, 'boot identity')
    ns = proc.namespace(os.getpid())
    tracker = Tracker(proc, ctx['controller_pid'], ticks, os.getuid(), ns, boot, os.sysconf('SC_CLK_TCK'))
    root = tracker.read_owned(ctx['controller_pid'], ticks)
    require(root['pgid'] != os.getpgrp(), 'observer must be outside controller group')
    started, cpu_started = time.monotonic(), time.process_time()
    out = observation_directory(args.output_name)
    manifest = dict(status='OBSERVER_RUNNING_NOT_SCIENCE', created_utc=utc(), boot_id=boot,
                    pid_namespace=ns, clock_ticks_per_second=tracker.hz, context_sha256=digest(raw),
                    registration_sha256=args.registration_sha256, config_sha256=args.config_sha256,
                    script_sha256=digest(Path(__file__).read_bytes()), controller_pid=ctx['controller_pid'],
                    controller_start_ticks=ticks, interval_seconds=5, original_stop_utc=ctx['stop_utc'],
                    observer_max_seconds=max(0., end-started), output_root=str(OBSERVATIONS),
                    nonblocking_for_pilot=True)
    publish(out / 'MANIFEST.json', manifest)
    terminal = None
    reason = 'OBSERVER_TIME_BOUND'
    sequence = 0
    prefix_bytes = 0
    chain = hashlib.sha256()
    try:
        with (out / 'SNAPSHOTS.ndjson').open('xb') as stream:
            while remaining(end, stop.timestamp(), time.monotonic(), time.time()) > 0:
                before = time.monotonic()
                stamp = utc()
                snap = tracker.sweep(sequence)
                snap.update(utc_start=stamp, utc_end=utc(), monotonic_start=before,
                            monotonic_end=time.monotonic(), observer_cpu_seconds=time.process_time()-cpu_started)
                prefix_bytes += snapshot_write(stream, snap, chain)
                sequence += 1
                try:
                    value = metadata('CONTROLLER.json')
                except FileNotFoundError:
                    value = None
                if value is not None:
                    result = strict(value)
                    require(result['job'] == ctx['job'] and result['registration_sha256'] == args.registration_sha256, 'terminal receipt identity')
                    require(isinstance(result['status'], str) and result['status'], 'terminal status missing')
                    finished = datetime.fromisoformat(result['finished_utc'])
                    require(finished.tzinfo is not None, 'terminal timestamp timezone')
                    terminal = digest(value)
                    reason = 'CONTROLLER_RECEIPT_PRESENT_NOT_SCIENCE_ACCEPTANCE'
                    break
                # Bounded adaptive cadence; only the observer waits or exits.
                pause = min(max(5., 2 * (time.monotonic()-before)), 30.,
                            remaining(end, stop.timestamp(), time.monotonic(), time.time()))
                time.sleep(pause)
    except Exception as error:
        reason = 'OBSERVER_ERROR:' + type(error).__name__
    status = 'OBSERVER_COMPLETE' if terminal is not None else 'OBSERVER_INCOMPLETE'
    if tracker.leader is None: status = 'OWNERSHIP_UNRESOLVED'
    publish(out / 'SUMMARY.json', dict(status=status, reason=reason, snapshots=sequence,
            complete_snapshot_prefix_sha256=chain.hexdigest(), complete_snapshot_prefix_bytes=prefix_bytes,
            controller_receipt_sha256=terminal,
            observer_wall_seconds=time.monotonic()-started, observer_cpu_seconds=time.process_time()-cpu_started,
            cpu_observed_lower_bound_seconds=sum(v['max_ticks'] for v in tracker.known.values())/tracker.hz,
            controller_cpu_separate_seconds=tracker.controller_max/tracker.hz,
            coverage_complete=False, error_count=tracker.error_count, scientific_acceptance=False,
            likelihood_calls=None, source_calls=None, converged_event_cost=None, pilot_control_actions=[]))


if __name__ == '__main__':
    main()
