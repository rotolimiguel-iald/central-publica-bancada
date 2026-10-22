"""Prepared durable store/controller. No instance or claim created on import.

Intended for a qualified POSIX local filesystem with fsync + exclusive hardlink.
Windows/native and remote filesystem durability are NOT silently emulated.
"""
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import uuid


class StoreError(RuntimeError):
    pass


def _canonical(obj):
    return json.dumps(obj, ensure_ascii=True, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise StoreError('DUPLICATE_KEY')
        result[key] = value
    return result


def _bad_constant(_):
    raise StoreError('NONFINITE_JSON')


class DurableStore:
    def __init__(self, root, *, max_record_bytes):
        if os.name != 'posix' or not hasattr(os, 'O_DIRECTORY'):
            raise StoreError('DURABILITY_BACKEND_NOT_QUALIFIED_ON_THIS_PLATFORM')
        if type(max_record_bytes) is not int or max_record_bytes <= 0:
            raise StoreError('EXPLICIT_POSITIVE_RECORD_CAP_REQUIRED')
        root = Path(root)
        if not root.is_absolute() or root.is_symlink() or not root.is_dir():
            raise StoreError('EXISTING_PROTECTED_ABSOLUTE_ROOT_REQUIRED')
        self.root, self.cap = root.resolve(strict=True), max_record_bytes
        self._flush_dir()

    def _flush_dir(self):
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _path(self, kind, key, suffix):
        if kind not in ('background', 'node') or type(key) is not str or len(key) != 64 or any(c not in '0123456789abcdef' for c in key):
            raise StoreError('INVALID_STORE_IDENTITY')
        if suffix not in ('claim', 'result', 'failure'):
            raise StoreError('INVALID_STORE_ARTIFACT')
        return self.root / (kind + '_' + key + '.' + suffix + '.json')

    def _read(self, path):
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        try:
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                raw = stream.read(self.cap + 1)
            if not raw or len(raw) > self.cap:
                raise StoreError('RECORD_SIZE')
            return raw, json.loads(raw, object_pairs_hook=_pairs, parse_constant=_bad_constant)
        finally:
            os.close(fd)

    def _exclusive_write(self, path, raw):
        if type(raw) is not bytes or not raw or len(raw) > self.cap:
            raise StoreError('RECORD_SIZE')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            with os.fdopen(fd, 'wb', closefd=False) as stream:
                stream.write(raw); stream.flush(); os.fsync(fd)
        finally:
            os.close(fd)
        self._flush_dir()

    def _publish(self, destination, record):
        raw = _canonical(record)
        temporary = self.root / ('.pending_' + uuid.uuid4().hex)
        self._exclusive_write(temporary, raw)
        # link is an atomic no-overwrite publication of already fsynced bytes.
        os.link(temporary, destination, follow_symlinks=False)
        self._flush_dir()
        # Keep the temporary hardlink for explicit recovery; no automatic cleanup.
        return _sha(raw)

    def lookup(self, kind, key, identity):
        claim_path = self._path(kind, key, 'claim')
        claim_raw, claim = self._read(claim_path)
        if (claim.get('schema') != 'F9_DURABLE_CLAIM_V1' or claim.get('kind') != kind
                or claim.get('key') != key or claim.get('identity') != identity
                or claim.get('identity_sha256') != _sha(_canonical(identity))
                or type(claim.get('token')) is not str or len(claim['token']) != 32
                or any(c not in '0123456789abcdef' for c in claim['token'])):
            raise StoreError('CLAIM_IDENTITY_MISMATCH')
        if os.path.lexists(self._path(kind, key, 'failure')):
            raise StoreError('FAILED_OR_UNCERTAIN_CLAIM_NO_RETRY')
        try:
            result_raw, result = self._read(self._path(kind, key, 'result'))
        except FileNotFoundError as exc:
            raise StoreError('PENDING_OR_UNCERTAIN_CLAIM_NO_RETRY') from exc
        if result.get('schema') != 'F9_DURABLE_RESULT_V1' or result.get('claim_sha256') != _sha(claim_raw):
            raise StoreError('RESULT_CLAIM_MISMATCH')
        files = result['files']
        if type(files) is not dict or not files:
            raise StoreError('EMPTY_RESULT')
        payload = {}
        for name, item in files.items():
            raw = base64.b64decode(item['base64'], validate=True)
            if len(raw) != item['bytes'] or _sha(raw) != item['sha256']:
                raise StoreError('RESULT_BYTES_MISMATCH')
            payload[name] = raw
        self._flush_dir()
        return {'created': False, 'kind': kind, 'key': key, 'claim': claim,
                'claim_sha256': _sha(claim_raw), 'payload': payload,
                'result_sha256': _sha(result_raw)}

    def acquire(self, kind, key, identity):
        claim_path = self._path(kind, key, 'claim')
        if os.path.lexists(claim_path):
            return self.lookup(kind, key, identity)
        if any(os.path.lexists(self._path(kind, key, suffix)) for suffix in ('result', 'failure')):
            raise StoreError('ORPHAN_RESULT_NO_REPAIR')
        claim = {'schema': 'F9_DURABLE_CLAIM_V1', 'kind': kind, 'key': key,
                 'identity': identity, 'identity_sha256': _sha(_canonical(identity)),
                 'token': uuid.uuid4().hex, 'at': datetime.now(timezone.utc).isoformat()}
        raw = _canonical(claim)
        try:
            self._exclusive_write(claim_path, raw)
        except FileExistsError:
            return self.lookup(kind, key, identity)
        return {'created': True, 'kind': kind, 'key': key, 'claim': claim,
                'claim_sha256': _sha(raw), 'payload': None, 'result_sha256': None}

    def _owned(self, ticket):
        if ticket.get('created') is not True:
            raise StoreError('ONLY_OWNER_CAN_PUBLISH')
        raw, claim = self._read(self._path(ticket['kind'], ticket['key'], 'claim'))
        if _sha(raw) != ticket['claim_sha256'] or claim != ticket['claim']:
            raise StoreError('CLAIM_CHANGED')

    def commit(self, ticket, payload):
        self._owned(ticket)
        if os.path.lexists(self._path(ticket['kind'], ticket['key'], 'failure')):
            raise StoreError('FAILED_CLAIM_CANNOT_COMMIT')
        if type(payload) is not dict or not payload or not all(type(k) is str and type(v) is bytes for k,v in payload.items()):
            raise StoreError('BYTE_PAYLOAD_REQUIRED')
        files = {name: {'bytes': len(raw), 'sha256': _sha(raw), 'base64': base64.b64encode(raw).decode('ascii')}
                 for name, raw in payload.items()}
        record = {'schema': 'F9_DURABLE_RESULT_V1', 'claim_sha256': ticket['claim_sha256'], 'files': files}
        return self._publish(self._path(ticket['kind'], ticket['key'], 'result'), record)

    def fail(self, ticket, exception):
        self._owned(ticket)
        code = getattr(exception, 'code', None)
        record = {'schema': 'F9_DURABLE_FAILURE_V1', 'claim_sha256': ticket['claim_sha256'],
                  'exception_type': type(exception).__name__,
                  'code': code[:256] if type(code) is str else None,
                  'status': 'FAILED_OR_UNCERTAIN_NO_RETRY', 'at': datetime.now(timezone.utc).isoformat()}
        self._publish(self._path(ticket['kind'], ticket['key'], 'failure'), record)


class DurableNodeCallback:
    def __init__(self, context, store, *, background_supplier, execution_guard):
        if not callable(background_supplier) or not callable(execution_guard):
            raise StoreError('TRUSTED_SUPPLIER_AND_EXTERNAL_GUARD_REQUIRED')
        self.ctx, self.store, self.supplier, self.guard = context, store, background_supplier, execution_guard

    def _guard(self, phase, payload):
        if self.guard(phase, payload) is not None:
            raise StoreError('GUARD_MUST_RETURN_NONE_OR_RAISE')

    def __call__(self, descriptor):
        ctx, store = self.ctx, self.store
        descriptor = ctx.descriptor(descriptor)
        node_identity = ctx.node_identity(descriptor)
        bg_identity = ctx.background_identity(descriptor)
        bg_key = _sha(_canonical(bg_identity))
        self._guard('NODE_ACCESS', {'identity': node_identity, 'admission': ctx.doc})
        node = store.acquire('node', descriptor['node_id'], node_identity)
        if not node['created']:
            bg = store.lookup('background', bg_key, bg_identity)
            bg_reference = ctx.background(bg['payload'], bg_identity, bg['claim'])
            expected_files = ('envelope_json', 'assembly_json', 'precision_json') + (('profile_json',) if ctx.doc['profile_enabled'] else ())
            ctx.c._keys(node['payload'], expected_files, 'durable node files')
            envelope = ctx.decode_envelope(node['payload']['envelope_json'])
            ctx.validate(envelope, descriptor, node['payload']['assembly_json'],
                         node['payload']['precision_json'], bg['payload'], bg_reference)
            if ctx.doc['profile_enabled']:
                ctx.validate_profile(node['payload']['profile_json'], descriptor, ctx.c._sha(node['payload']['assembly_json']))
            # Original bytes stay immutable; only this callback's usage receipt changes.
            envelope['receipt']['background_origin'] = 'VERIFIED_DURABLE_CACHE'
            envelope['receipt']['background_calls_this_callback'] = 0
            ctx._validator()._accept(envelope, descriptor)
            return envelope
        try:
            bg = store.acquire('background', bg_key, bg_identity)
            if bg['created']:
                try:
                    request = ctx.background_request(bg_identity, bg['claim'])
                    self._guard('BACKGROUND_EXECUTION', request)
                    payload = self.supplier(request)
                    bg_reference = ctx.background(payload, bg_identity, bg['claim'])
                    self._guard('BACKGROUND_ACCEPTANCE', {'request': request, 'original_bytes': payload})
                    store.commit(bg, payload)
                except BaseException as exc:
                    store.fail(bg, exc)
                    raise
                origin = 'NEW_EXECUTION'
            else:
                payload = bg['payload']
                bg_reference = ctx.background(payload, bg_identity, bg['claim'])
                origin = 'VERIFIED_DURABLE_CACHE'
            envelope, artifacts = ctx.compute(descriptor, payload, bg_reference, origin=origin)
            store.commit(node, artifacts)
            return envelope
        except BaseException as exc:
            store.fail(node, exc)
            raise
