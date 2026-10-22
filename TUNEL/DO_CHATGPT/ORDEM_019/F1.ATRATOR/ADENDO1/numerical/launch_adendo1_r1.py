"""Record before-run pins, launch the frozen A5/A6 experiment once, preserve outputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PREREG = HERE.parent / 'PREREGISTRO_ADENDO1_R1.json'
SCRIPT = HERE / 'run_adendo1_r1.py'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(path, value):
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    with path.open('xb') as stream:
        stream.write(raw)
    assert path.read_bytes() == raw


def main():
    if len(sys.argv) != 2 or sha(PREREG) != sys.argv[1]:
        raise ValueError('Expected frozen preregister SHA-256 is required')
    names = ['RUN_MANIFEST_R1.json', 'RUN_LOG_R1.txt', 'RUN_RECEIPT_R1.json', 'RESULTADOS_ADENDO1_R1.json']
    if any((HERE / name).exists() for name in names):
        raise FileExistsError('Refusing to overwrite run evidence')
    freeze_path = HERE.parent / 'FREEZE_ADENDO1_R1.json'
    freeze = json.loads(freeze_path.read_bytes())
    if not any(x['path'] == str(PREREG) and x['sha256'] == sha(PREREG) for x in freeze['files']):
        raise ValueError('Frozen preregister entry does not match')
    command = [sys.executable, '-B', '-X', 'utf8', str(SCRIPT)]
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(), 'preregister_path': str(PREREG), 'preregister_sha256': sha(PREREG),
                'freeze_path': str(freeze_path), 'freeze_sha256': sha(freeze_path), 'script_path': str(SCRIPT), 'script_sha256': sha(SCRIPT),
                'launcher_path': str(Path(__file__).resolve()), 'launcher_sha256': sha(__file__), 'command': command, 'cwd': str(HERE),
                'before_new_run': True}
    put(HERE / names[0], manifest)
    started = datetime.now(timezone.utc).isoformat()
    t = time.perf_counter()
    proc = subprocess.run(command, cwd=HERE, capture_output=True, check=False)
    seconds = time.perf_counter() - t
    ended = datetime.now(timezone.utc).isoformat()
    log = (f"START_UTC={started}\nEND_UTC={ended}\nSECONDS={seconds:.9f}\nEXIT_CODE={proc.returncode}\nCOMMAND={json.dumps(command,ensure_ascii=False)}\nCWD={HERE}\nSTDOUT\n".encode('utf-8')
           + proc.stdout + b'\nSTDERR\n' + proc.stderr)
    with (HERE / names[1]).open('xb') as stream:
        stream.write(log)
    result = HERE / names[3]
    receipt = {'started_utc': started, 'finished_utc': ended, 'seconds': seconds, 'exit_code': proc.returncode, 'command': command,
               'preregister_before': manifest['preregister_sha256'], 'preregister_after': sha(PREREG),
               'script_before': manifest['script_sha256'], 'script_after': sha(SCRIPT),
               'manifest_sha256': sha(HERE / names[0]), 'log_sha256': sha(HERE / names[1]),
               'result_present': result.exists(), 'result_sha256': sha(result) if result.exists() else None}
    put(HERE / names[2], receipt)
    print(json.dumps(receipt, ensure_ascii=False))
    raise SystemExit(proc.returncode)


if __name__ == '__main__':
    main()
