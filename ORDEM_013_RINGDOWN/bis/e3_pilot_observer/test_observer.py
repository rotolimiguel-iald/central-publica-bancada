"""Finite fake-process and own-file tests; never observes live /proc."""
import ast
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import time
from contextlib import redirect_stdout
from unittest.mock import patch
import observer as o


def record(pid, parent, group, ticks, cpu=0, uid=1000, ns='pid:[9]'):
    return dict(pid=pid, ppid=parent, pgid=group, sid=group, start_ticks=ticks,
                utime=cpu, stime=0, uid=uid, namespace=ns, state='S')


class FakeProc:
    def __init__(self):
        self.records = {10: record(10, 2, 10, 100, 3), 20: record(20, 10, 20, 110, 10),
                        21: record(21, 20, 20, 120, 20)}
        self.tree = {10: [20], 20: [21], 21: []}
        self.reads = []
    def record(self, pid):
        self.reads.append(pid)
        if pid not in self.records: raise FileNotFoundError('fixture absent')
        return copy.deepcopy(self.records[pid])
    def children(self, pid):
        return list(self.tree.get(pid, []))


def fixture():
    proc = FakeProc()
    return proc, o.Tracker(proc, 10, 100, 1000, 'pid:[9]', 'fixture-boot', 100)


def run():
    checks = []
    def check(name, condition):
        if condition is not True: raise RuntimeError('FAILED:' + name)
        checks.append(dict(name=name, passed=True))
    def refused(name, action):
        try: action()
        except (ValueError, OSError): check(name, True)
        else: check(name, False)

    for name, data in [('duplicate', '{"x":1,"x":2}'), ('NaN', '{"x":NaN}'),
                       ('Infinity', '{"x":Infinity}'), ('exponent_overflow', '{"x":1e999}')]:
        refused('strict_' + name, lambda data=data: o.strict(data))
    check('finite_json', o.strict('{"x":1}') == {'x': 1})
    fields = ['S','10','20','20'] + ['0'] * 16
    fields[11], fields[12], fields[19] = '123', '7', '110'
    parsed = o.parse_stat('20 (strange ) process ( name)) ' + ' '.join(fields))
    check('comm_parentheses_spaces', parsed['utime'] == 123 and parsed['stime'] == 7 and parsed['start_ticks'] == 110)
    refused('truncated_stat', lambda: o.parse_stat('20 (name) S 10'))
    for path in ['20/cmdline','20/environ','20/mem','20/fd/1','20/../PRIVATE.log','/proc/20/stat',
                 '20/task/21/stat','20/ns/pid','sys/kernel/random/../boot_id']:
        refused('path_denied:' + path, lambda path=path: o.Proc().read(path))
    for path in ['20/stat','20/status','20/task/21/children','sys/kernel/random/boot_id']:
        check('path_allowed:' + path, o.Proc.allowed(path))

    f, t = fixture()
    first = t.sweep(0)
    check('ancestry_admitted', first['ownership_resolved'] and len(t.known) == 2)
    check('own_cpu_sum', first['cpu_observed_lower_bound_seconds'] == .3)
    check('controller_separate', first['controller_cpu_separate_seconds'] == .03)
    check('repeated_snapshot_no_double_count', t.sweep(1)['cpu_observed_lower_bound_seconds'] == .3)
    f.records[21]['utime'] = 30
    check('monotone_growth', t.sweep(2)['cpu_observed_lower_bound_seconds'] == .4)
    f.records[21]['ppid'] = 1
    f.tree[20] = []
    check('known_reparented_retained', len(t.sweep(3)['owned_identity_records']) == 2)
    del f.records[21]
    snap = t.sweep(4)
    check('disappeared_keeps_last_cpu', snap['cpu_observed_lower_bound_seconds'] == .4 and len(snap['errors']) > 0)
    check('no_coverage_claim', snap['coverage_complete'] is False and snap['scientific_progress'] is None)
    f.records[21] = record(21, 1, 20, 999, 999)
    snap = t.sweep(5)
    check('pid_reuse_not_counted', snap['cpu_observed_lower_bound_seconds'] == .4 and t.known['21:120']['quarantined'])

    for name, change in [
        ('wrong_uid', lambda f: f.records[20].update(uid=999)),
        ('wrong_namespace', lambda f: f.records[20].update(namespace='pid:[8]')),
        ('wrong_parent', lambda f: f.records[20].update(ppid=99)),
        ('wrong_leader_group', lambda f: f.records[20].update(pgid=99)),
        ('older_child', lambda f: f.records[20].update(start_ticks=90)),
        ('controller_reused', lambda f: f.records[10].update(start_ticks=999)),
        ('ambiguous_children', lambda f: f.tree.update({10: [20, 21]})),
        ('missing_children', lambda f: f.tree.update({10: []})),
    ]:
        f, t = fixture(); change(f)
        check(name, t.sweep(0)['ownership_resolved'] is False)
    for field, value in [('utime', 1), ('pgid', 99), ('sid', 99)]:
        f, t = fixture(); t.sweep(0); f.records[21][field] = value
        snap = t.sweep(1)
        check('quarantine_' + field, t.known['21:120']['quarantined'] and snap['cpu_observed_lower_bound_seconds'] == .3)
    f, t = fixture()
    f.records[21]['ppid'] = 99
    snap = t.sweep(0)
    check('unproven_descendant_excluded', len(t.known) == 1 and any('discovery_gap' in x for x in snap['errors']))
    f, t = fixture(); f.records[20]['cutime'] = 100000
    check('child_aggregate_not_added', t.sweep(0)['cpu_observed_lower_bound_seconds'] == .3)
    f, t = fixture(); f.tree[20] = [21,21,21]
    check('duplicate_discovery_not_added', t.sweep(0)['cpu_observed_lower_bound_seconds'] == .3)
    f, t = fixture()
    with patch.object(f, 'children', side_effect=PermissionError('fixture')):
        check('access_denied_visible', len(t.sweep(0)['errors']) > 0 and t.leader is None)
    f, t = fixture()
    original = f.children
    def race(pid):
        result = original(pid)
        f.records[pid]['start_ticks'] += 1
        return result
    with patch.object(f, 'children', side_effect=race):
        check('discovery_identity_race', t.sweep(0)['ownership_resolved'] is False)

    with tempfile.TemporaryDirectory(prefix='finite_', dir=o.HERE) as folder:
        root = Path(folder)
        check('temporary_cleanup_confined', root.resolve().is_relative_to(o.HERE.resolve()))
        small = root / 'own_metadata.json'; small.write_bytes(b'{"x":1}')
        check('own_fixture_read', o.bounded_read(small) == b'{"x":1}')
        large = root / 'oversize.json'; large.write_bytes(b'0' * (o.MAX_BYTES + 1))
        refused('oversize_refused', lambda: o.bounded_read(large))
        refused('directory_refused', lambda: o.bounded_read(root))
        output = root / 'exclusive.json'
        o.publish(output, {'x': 1})
        refused('overwrite_refused', lambda: o.publish(output, {'x': 2}))
        check('exclusive_original_preserved', json.loads(output.read_bytes()) == {'x': 1})
        (root/'cache').mkdir()
        with patch.object(o, 'B', root), patch.object(o, 'OBSERVATIONS', root/'cache/E3_PILOT_OS_OBSERVER_V1'):
            target=o.observation_directory('observation_001')
            check('cache_output_route', target==root/'cache/E3_PILOT_OS_OBSERVER_V1/observation_001')
            refused('cache_exclusivity',lambda:o.observation_directory('observation_001'))
            for name in ['../escape','observation_001/escape','observation_1','C:/escape']:
                refused('cache_bad_name:'+name,lambda name=name:o.observation_directory(name))
        # A resolve mismatch simulates a linked cache without OS symlink privileges.
        original_resolve=Path.resolve
        def fake_resolve(path,*args,**kwargs):
            if path==root/'cache':return root/'elsewhere'
            return original_resolve(path,*args,**kwargs)
        with patch.object(o,'B',root),patch.object(o,'OBSERVATIONS',root/'cache/E3_PILOT_OS_OBSERVER_V1'),patch.object(Path,'resolve',fake_resolve):
            refused('cache_link_escape',lambda:o.observation_directory('observation_002'))
    end=o.deadline(1000.,900.,50.,200.)
    check('deadline_original_plus_grace',end==165.)
    check('clock_backwards_no_extension',o.remaining(end,1000.,165.,800.)==0.)
    check('clock_forward_stops_observer_only',o.remaining(end,1000.,60.,1020.)==0.)
    check('shorter_observer_bound',o.deadline(1000.,900.,50.,10.)==60.)
    refused('expired_window',lambda:o.deadline(1000.,1015.,50.,100.))
    refused('nonfinite_time',lambda:o.deadline(float('nan'),900.,50.,100.))
    refused('excessive_observer_budget',lambda:o.deadline(1000.,900.,50.,36016.))
    chain=hashlib.sha256(); buf=io.BytesIO()
    size=o.snapshot_write(buf,{'sequence':0},chain)
    check('snapshot_hash_and_bytes',size==len(buf.getvalue()) and chain.hexdigest()==hashlib.sha256(buf.getvalue()).hexdigest())
    class ShortWrite(io.BytesIO):
        def write(self,data):return super().write(data[:3])
    previous=chain.hexdigest()
    refused('short_snapshot_write',lambda:o.snapshot_write(ShortWrite(),{'sequence':1},chain))
    check('incomplete_tail_does_not_change_prefix_hash',previous==chain.hexdigest())
    refused('nonfinite_snapshot',lambda:o.snapshot_write(io.BytesIO(),{'x':float('nan')},chain))
    # Even default CLI may not inspect live metadata.
    with (patch.object(sys, 'argv', ['observer.py']),
          patch.object(o, 'metadata', side_effect=RuntimeError('unexpected I/O')),
          patch.object(o.Proc, 'read', side_effect=RuntimeError('unexpected /proc'))):
        buf = io.StringIO()
        with redirect_stdout(buf): o.main()
        check('default_inactive', 'INACTIVE' in buf.getvalue())
    tree = ast.parse(Path(o.__file__).read_text(encoding='utf-8'))
    imports = {alias.name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)) for alias in node.names}
    check('no_science_or_control_imports', not bool(imports & {'subprocess','signal','h5py','numpy','bilby','gwpy','pickle'}))
    calls = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
    check('no_process_control_calls', not bool(calls & {'kill','killpg','waitpid','fork','execv','Popen','system','popen'}))
    return checks


if __name__ == '__main__':
    start, cpu = time.perf_counter(), time.process_time()
    result = run()
    report = dict(status='FINITE_SYNTHETIC_AND_OWN_FILE_TESTS_PASS', checks=result,
                  optimize=sys.flags.optimize, wall_seconds=time.perf_counter()-start,
                  cpu_seconds=time.process_time()-cpu, live_proc_read=False,
                  live_pilot_observed=False, own_processes_launched=False,
                  scope='Fake process graph plus bounded files in temporary owned subdirectory; no Linux live adapter certification')
    print(json.dumps(report, ensure_ascii=False, allow_nan=False))
