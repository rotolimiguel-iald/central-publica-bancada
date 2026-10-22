"""Read-only recheck of explicitly inventoried inputs and delivered artifacts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

B = Path(__file__).resolve().parents[1]
R = B.parent


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    baseline = B / 'bis/INPUT_INTEGRITY_013BIS_retry.json'
    old = json.loads(baseline.read_bytes())
    rows = []
    for category in ('inputs', 'sources'):
        for row in old[category]:
            p = Path(row['path'])
            if p.name.lower() in ('.env', 'iald_stack_v7.py', 'iald_psion_state.json'):
                raise ValueError('Confidential input unexpectedly inventoried')
            digest = sha(p)
            rows.append(dict(category=category, path=str(p), expected_sha256=row['sha256'],
                actual_sha256=digest, bytes=p.stat().st_size, matches=digest == row['sha256']))
    manifests = [B / 'bis/M6_MA_DELIVERY_MANIFEST.json']
    for manifest in manifests:
        data = json.loads(manifest.read_bytes())
        for name, expected in data['files'].items():
            p = Path(name)
            digest = sha(p)
            rows.append(dict(category='delivered_part_A', path=str(p), expected_sha256=expected,
                actual_sha256=digest, bytes=p.stat().st_size, matches=digest == expected))
    oversized = []
    unreadable_metadata = []
    scan_errors = []
    def record_walk_error(exc):
        scan_errors.append(dict(path=exc.filename, error=str(exc), type=type(exc).__name__))
    for parent, dirs, files in os.walk(B, followlinks=False, onerror=record_walk_error):
        location = Path(parent)
        # Exclude the whole cache: large files belong there, and private seed is never opened.
        if location == B:
            dirs[:] = [d for d in dirs if d != 'cache']
        for name in files:
            p = location / name
            try:
                size = p.stat().st_size
            except OSError as exc:
                unreadable_metadata.append(dict(path=str(p), error=str(exc),
                    lstat_bytes=p.lstat().st_size, scope='No content read; link/fixture must be classified independently'))
                continue
            if size > 25 * 1024 * 1024:
                oversized.append(dict(path=str(p), bytes=size))
    now = datetime.now(timezone.utc)
    result = dict(status='PASS_FROZEN_INPUTS_DELIVERED_A_AND_SIZE_LAYOUT'
        if all(r['matches'] for r in rows) and not oversized and not scan_errors and not unreadable_metadata else 'VISIBLE_INTEGRITY_OR_LAYOUT_DIFFERENCE',
        measured_utc=now.isoformat(), directory_enumeration_errors=scan_errors,
        supersedes_script_sha256='064c0704cc62d618febad74d489bb4e5352b7eba097caf1fb6398cae29e03d91', baseline_sha256=sha(baseline), checks=rows,
        oversized_outside_cache=oversized, metadata_exceptions=unreadable_metadata, cache_content_not_scanned=True,
        prior_attempts=['Sandbox denied canonical source read; same read-only check retried with escalation',
            'Windows stat could not follow WSL symlink in negative fixture; explicit metadata exception retained'],
        scope='Named frozen inputs and Part A delivered manifest only; no blanket claim over all historical outputs',
        script_sha256=sha(Path(__file__)))
    target = B / ('bis/015/t13/FINAL_INTEGRITY_015_' + now.strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
    tmp = target.with_suffix('.pending')
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.stat().st_size != len(raw):
        raise OSError('Short audit write')
    os.link(tmp, target); tmp.unlink()
    print(json.dumps(dict(status=result['status'], receipt=str(target), sha256=sha(target),
        counts={c: sum(r['category'] == c for r in rows) for c in ('inputs','sources','delivered_part_A')},
        mismatches=[r for r in rows if not r['matches']], oversized=oversized,
        directory_enumeration_errors=scan_errors, metadata_exceptions=unreadable_metadata), ensure_ascii=False))


if __name__ == '__main__':
    main()
