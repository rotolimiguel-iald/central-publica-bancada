"""One future theory-only background evaluation plus pure H1-H5 assembly.

Prepared source. No invocation is authorized by this file's existence.
"""
import sys, os, json, hashlib, types, time, traceback
from pathlib import Path

BASE = Path(__file__).resolve().parent


def load_module(name, path):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def main():
    contract = json.loads((BASE/'CONTRATO_WSL.json').read_bytes())
    common = BASE/'common.py'
    expected = next(x for x in contract['local_pins'] if x['relative_path'] == 'common.py')
    raw = common.read_bytes()
    if len(raw) != expected['bytes'] or hashlib.sha256(raw).hexdigest() != expected['sha256']:
        raise RuntimeError('common.py pin mismatch')
    g = load_module('f9_protocol', common)
    g.need(sys.argv[1:3] == ['--child', g.REQUEST] and len(sys.argv) == 4, 'Exact child argv')
    nonce = sys.argv[3]
    g.check_pins(contract, linux=True)
    _, ah = g.authorization(contract)
    w, s = g.read(BASE/'CLAIM.json'), g.read(BASE/'RUN/LINUX_CLAIM.json')
    g.need(w['nonce'] == s['nonce'] == nonce and w['authorization_sha256'] == ah, 'Dispatch identity')
    g.need(s['request_id'] == w['request_id'] == g.REQUEST and
           s['contract_sha256'] == g.pin(BASE/'CONTRATO_WSL.json')['sha256'], 'Dispatch pins')
    parent = g.proc_identity(os.getppid())
    g.need(g.matches(parent, g.argv_for('--supervisor', nonce)) and
           parent['start_ticks'] == s['process']['start_ticks'] and parent['pid'] == s['process']['pid'], 'Exact parent incarnation')
    g.need(time.time() < w['work_deadline_epoch'] and not (BASE/'RUN/STOP.json').exists(), 'Expired/stopped')
    out = BASE/'RUN/CASE'; out.mkdir(exist_ok=False)
    self_id = g.serial_identity(g.proc_identity(os.getpid()))
    g.fresh(out/'CASE_CLAIM.json', {'request_id': g.REQUEST, 'nonce': nonce, 'process': self_id,
                                 'parent_pid': os.getppid(), 'retry_allowed': False})
    started = time.monotonic()
    inventory = g.read(BASE/'RUNTIME_INVENTORY.json')
    g.need(not inventory['unresolved_native_dependencies'], 'Unresolved native inventory')
    reads = {item['path']: item for item in inventory['pins']}
    aliases = inventory.get('loader_alias_checks_required', []) + inventory['alias_resolution_metadata']['checks_required_in_Linux']
    for alias in aliases:
        expected_alias = {k: alias[k] for k in ('bytes', 'sha256')}
        g.need(g.pin(alias['alias_path']) == expected_alias, 'Native alias hash mismatch: ' + alias['alias_path'])
        reads[alias['alias_path']] = {'path': alias['alias_path'], **expected_alias}
    for item in contract['local_pins']:
        reads[str(BASE/item['relative_path'])] = item
    for path, item in reads.items():
        g.need(g.pin(path) == {k: item[k] for k in ('bytes', 'sha256')}, 'Runtime pin changed: ' + path)
    g.need(inventory['stdlib_sysconfig_included'], 'sysconfig inventory missing')
    runtime_pin = g.pin(BASE/'RUNTIME_INVENTORY.json')['sha256']
    effective_raw = (BASE/'EFFECTIVE_CONFIGURATION.json').read_bytes()
    effective = json.loads(effective_raw)
    config_pin = g.digest(effective_raw)
    admission_raw = (BASE/'ASSEMBLY_ADMISSION.json').read_bytes()
    design_raw = (BASE/'sources/ESPECIFICACAO_LINEAR.json').read_bytes()
    layout_raw = (BASE/'sources/LAYOUT_ESTRUTURAL_3CMB_13BAO.json').read_bytes()
    parameters = g.read(BASE/'MODEL_PARAMETERS.json')
    # No site initialization or .pth execution under -I -S; one pinned distribution root.
    sys.path.append(inventory['site_packages'])
    guard = load_module('f9_audit_guard', BASE/'sources/audit_guard.py')
    journal_path = out/'journal.jsonl'
    latch = guard.AuditLatch(guard.PreopenedJournal(str(journal_path)))
    names = ['BACKGROUND_RESULT.json', 'ENGINE_EXECUTION_RECEIPT.json', 'BACKGROUND_PACKET.json',
             'FIVE_MODEL_OUTPUT.json', 'CASE_RESULT.json']
    fds = {name: os.open(out/name, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600) for name in names}
    artifacts, attempted, returned, module_errors = {}, [0], [0], []
    status, error = 'FAILED', None
    missing_runtime_probes, native_mapping_errors = [], []
    readonly_extra = {str(BASE/'RUN/STOP.json'), '/proc/self/maps'}
    native_paths = {p for p in reads if '.so' in Path(p).name}
    native_names = {Path(p).name for p in native_paths}

    def audit(event, args):
        reason, target = None, str(args[:1])[:500]
        if event.startswith(('socket.', 'subprocess.', 'os.spawn')) or event in (
                'os.system', 'os.posix_spawn', 'os.fork', 'os.forkpty', 'os.remove',
                'os.rmdir', 'os.rename', 'os.mkdir', 'os.link', 'os.symlink', 'sys.addaudithook'):
            reason = 'OPERATION_OUTSIDE_THEORY_UNIT'
        if event == 'open':
            target, mode, flags = args
            writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (
                isinstance(flags, int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
            name = os.path.normpath(str(target))
            if writing:
                reason = 'WRITE_AFTER_HOOK'
            elif name not in reads and name not in readonly_extra:
                # Missing bytecode/optional distribution files are normal loader probes.
                # Only a demonstrably absent path inside pinned runtime trees may pass;
                # an existing unpinned file or a path outside those trees still latches.
                within = any(name.startswith(root + '/') for root in inventory['roots'])
                if within and not os.path.lexists(name):
                    missing_runtime_probes.append({'path': name, 'status': 'ABSENT_RUNTIME_PROBE_NO_CONTENT'})
                else:
                    reason = 'UNPINNED_READ_OR_WRITE'
        if event == 'ctypes.dlopen':
            target = args[0]
            if target is not None and str(target) not in native_paths and str(target) not in native_names:
                reason = 'UNPINNED_NATIVE_LIBRARY'
        if reason:
            latch.deny(event, target, reason=reason)

    def checkpoint(phase):
        latch.refresh_counts(0, attempted[0])
        latch.checkpoint(phase)
        g.need(time.time() < w['work_deadline_epoch'] and not (BASE/'RUN/STOP.json').exists(), 'Expired/stopped: ' + phase)

    def module_check(phase):
        for name, module in sorted(sys.modules.copy().items()):
            filename = getattr(module, '__file__', None)
            if not filename or str(filename).startswith('<'):
                continue
            item = reads.get(str(filename))
            if item is None:
                module_errors.append({'phase': phase, 'module': name, 'file': str(filename), 'reason': 'PATH_NOT_PINNED'})
            elif g.pin(filename) != {k: item[k] for k in ('bytes', 'sha256')}:
                module_errors.append({'phase': phase, 'module': name, 'file': str(filename), 'reason': 'HASH_CHANGED'})
        g.need(not module_errors, 'UNPINNED_IMPORTED_MODULE: ' + json.dumps(module_errors[:16], sort_keys=True))
        for line in Path('/proc/self/maps').read_text().splitlines():
            fields = line.split(maxsplit=5)
            if len(fields) < 6 or not fields[5].startswith('/'):
                continue
            filename = fields[5]
            if '.so' not in Path(filename).name and filename != inventory['interpreter_target']:
                continue
            item = reads.get(filename)
            if item is None:
                native_mapping_errors.append({'phase': phase, 'file': filename, 'reason': 'MAPPED_NATIVE_FILE_NOT_PINNED'})
            elif g.pin(filename) != {k: item[k] for k in ('bytes', 'sha256')}:
                native_mapping_errors.append({'phase': phase, 'file': filename, 'reason': 'MAPPED_NATIVE_HASH_CHANGED'})
        g.need(not native_mapping_errors, 'UNPINNED_NATIVE_MAPPING: ' + json.dumps(native_mapping_errors[:16], sort_keys=True))


    def emit(name, obj):
        raw = (json.dumps(obj, sort_keys=True, allow_nan=False) + '\n').encode()
        g.writefd(fds[name], raw)
        artifacts[name] = {'path': str(out/name), 'bytes': len(raw), 'sha256': g.digest(raw)}
        return raw

    try:
        sys.addaudithook(audit); latch.installed(); latch.context('import_theory_libraries', 0, 0)
        import camb
        checkpoint('after_camb_import')
        engine = load_module('f9_existing_background', BASE/'sources/background_controls.py')
        assembler = load_module('f9_existing_assembly', BASE/'sources/five_model_assembly.py')
        module_check('after_imports'); checkpoint('before_solver')
        original = camb.get_background
        def once(*args, **kwargs):
            checkpoint('before_native_background')
            g.need(attempted[0] == 0, 'Second CAMB background call prohibited')
            attempted[0] += 1; latch.refresh_counts(0, attempted[0])
            value = original(*args, **kwargs)
            returned[0] += 1
            checkpoint('after_native_background')
            return value
        camb.get_background = once
        try:
            bg = engine.prediction_worker(effective, effective['points'][0]['id'], 'reference')
        finally:
            camb.get_background = original
        checkpoint('after_existing_engine'); module_check('after_existing_engine')
        g.need(attempted[0] == returned[0] == 1, 'One solver return required')
        bg_raw = emit('BACKGROUND_RESULT.json', bg)
        eraw = emit('ENGINE_EXECUTION_RECEIPT.json', {
            'status': 'ENGINEERING_BACKGROUND_RETURNED', 'request_id': g.REQUEST, 'nonce': nonce,
            'process': self_id, 'configuration_sha256': config_pin, 'runtime_sha256': runtime_pin,
            'background_result_sha256': g.digest(bg_raw), 'solver_calls_attempted': attempted[0],
            'solver_calls_returned': returned[0], 'wall_s': time.monotonic()-started,
            'uniform_error_bound': None, 'observed_reads': False})
        packet = {'schema': 'F9_BACKGROUND_PACKET_V1', 'status': 'ENGINEERING_RESULT', 'error': None, 'result': bg,
            'identity': {'engine_sha256': assembler.SOURCE_PINS['background_engine']['sha256'],
                'protocol_sha256': assembler.SOURCE_PINS['background_protocol']['sha256'],
                'engine_configuration_sha256': config_pin, 'runtime_sha256': runtime_pin,
                'theta': effective['points'][0]['theta'], 'z_law': effective['redshifts']['z_star_law'],
                'units': assembler.BACKGROUND_UNITS, 'execution_receipt_sha256': g.digest(eraw)}}
        packet_raw = emit('BACKGROUND_PACKET.json', packet)
        assembled = assembler.assemble_five(parameters, design_json=design_raw, layout_json=layout_raw,
            background_json=packet_raw, admission_json=admission_raw, admission_sha256=g.digest(admission_raw))
        checkpoint('after_assembly'); module_check('after_assembly')
        emit('FIVE_MODEL_OUTPUT.json', assembled)
        checkpoint('before_acceptance')
        status = 'ENGINEERING_PREDICTIONS_WRITTEN'
    except BaseException as exc:
        error = {'type': type(exc).__name__, 'message': str(exc)[:4000],
                 'traceback': traceback.format_exc(limit=8)[-8000:]}
    snap = latch.snapshot()
    if snap['latched'] or snap['journal_error'] is not None:
        status = 'FAILED_LATCHED'
    receipt = {'status': status, 'request_id': g.REQUEST, 'nonce': nonce, 'case_id': g.CASE,
        'process': self_id, 'parent_pid': os.getppid(), 'error': error,
        'solver_calls_attempted': attempted[0], 'solver_calls_returned': returned[0],
        'module_errors': module_errors, 'native_mapping_errors': native_mapping_errors,
        'missing_runtime_probes': missing_runtime_probes, 'audit_snapshot': snap, 'artifacts': artifacts,
        'scientific_calls': attempted[0], 'observed_reads': False, 'D_read': False,
        'new_children': 0, 'retry_allowed': False, 'wall_s': time.monotonic()-started,
        'runtime_inventory_sha256': runtime_pin, 'effective_configuration_sha256': config_pin,
        'numerical_certificate': None, 'uniform_error_bound': None}
    raw = emit('CASE_RESULT.json', receipt)
    for fd in fds.values():
        os.close(fd)
    print(raw.decode(), end='', flush=True)
    return 0 if status == 'ENGINEERING_PREDICTIONS_WRITTEN' else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(json.dumps({'status': 'FAILED_PREFLIGHT_OR_RECEIPT', 'error': type(exc).__name__, 'message': str(exc)[:4000]}))
        sys.exit(1)
