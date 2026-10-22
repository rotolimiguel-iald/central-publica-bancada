"""Read-only provenance audit; never imports or executes scientific programs."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, sys, time

OUT = Path(__file__).resolve().parent

def atomic(path, data):
    raw = data if isinstance(data, bytes) else data.encode('utf-8')
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(path.read_bytes())
    temp = path.with_name(path.name + '.tmp')
    temp.write_bytes(raw)
    assert temp.stat().st_size == len(raw) and len(raw) > 0
    os.replace(temp, path)
    assert path.read_bytes() == raw

def metadata(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'mtime_utc': datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat()}, raw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['index', 'read', 'list'])
    ap.add_argument('name')
    ap.add_argument('target')
    ap.add_argument('--pattern', default='beta|alpha|Hubble|D1b|predict_H0|MCMC|v22|20[12][0-9]')
    ap.add_argument('--context', type=int, default=3)
    ap.add_argument('--max-hits', type=int, default=80)
    ap.add_argument('--search-args', nargs=argparse.REMAINDER, default=[])
    args = ap.parse_args()
    began = time.monotonic()
    record = {'action':args.action, 'name':args.name, 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'originals_modified':False}
    if args.action == 'index':
        script = Path(r'C:\IALD\INDICE_DO_ACERVO\buscar.py')
        record['search_script'], _ = metadata(script)
        command = [sys.executable, '-X', 'utf8', str(script), args.target, *args.search_args]
        result = subprocess.run(command, capture_output=True, encoding='utf-8', errors='strict')
        record.update(command=command, returncode=result.returncode, output=result.stdout, stderr=result.stderr)
        print(result.stdout[:22000])
    elif args.action == 'list':
        root = Path(args.target)
        rx = re.compile(args.pattern, re.I)
        record['root'] = str(root)
        record['entries'] = [{'path':str(p), 'is_file':p.is_file()} for p in root.rglob('*') if rx.search(p.name)]
        print(json.dumps(record['entries'], ensure_ascii=False, indent=2)[:26000])
    else:
        path = Path(args.target)
        record['source'], raw = metadata(path)
        lines = raw.decode('utf-8-sig').splitlines()
        rx = re.compile(args.pattern, re.I)
        hits = [i for i, line in enumerate(lines) if rx.search(line)]
        record.update(pattern=args.pattern, matched_lines=len(hits), total_lines=len(lines), excerpts=[])
        for i in hits[:args.max_hits]:
            first, last = max(0,i-args.context), min(len(lines),i+args.context+1)
            record['excerpts'].append({'match_line':i+1, 'first_line':first+1, 'last_line':last, 'text':'\n'.join(lines[first:last])})
        print(json.dumps(record, ensure_ascii=False, indent=2)[:36000])
    record['elapsed_seconds'] = time.monotonic()-began
    atomic(OUT/(args.name+'.json'), json.dumps(record, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__':
    main()
