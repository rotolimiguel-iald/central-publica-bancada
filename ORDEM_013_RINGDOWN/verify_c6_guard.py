"""Adversarial receipt/code/input checks using disposable task-local copies."""
from pathlib import Path
import hashlib
import json
import tempfile
import c6_engine
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    reg,digest=c6_engine.checked_registration()
    folder=Path(tempfile.mkdtemp(prefix='guard_',dir=ROOT/'cache'))
    mock=folder/'run';mock.mkdir()
    receipt=folder/'TUNEL/DO_CHATGPT';receipt.mkdir(parents=True)
    real_receipt=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C6a_REGISTRO_TOEPLITZ.md'
    (receipt/real_receipt.name).write_bytes(real_receipt.read_bytes())
    registration=mock/'REGISTRO_C6.json'
    registration.write_bytes((ROOT/'REGISTRO_C6.json').read_bytes())
    for name in reg['code_and_input_hashes']:
        p=mock/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
    rows=[]
    def must_refuse(label,expected):
        try:c6_engine.checked_registration()
        except ValueError as exc:
            if expected not in str(exc):raise AssertionError('Wrong failure reason') from exc
            rows.append(dict(case=label,status='REFUSED_AS_REQUIRED',reason=str(exc)))
        else:raise AssertionError(f'Tampered case accepted: {label}')
    oldroot=c6_engine.ROOT
    try:
        c6_engine.ROOT=mock
        c6_engine.checked_registration();rows.append(dict(case='identical_copies',status='PASS'))
        original=registration.read_bytes();registration.with_suffix('.json.original').write_bytes(original)
        registration.write_bytes(original+b'\n')
        must_refuse('registration_byte_change','does not match delivered receipt')
        registration.with_suffix('.json.TAMPERED').write_bytes(registration.read_bytes())
        registration.write_bytes(original)
        code=mock/'c6_engine.py';code_original=code.read_bytes()
        code.with_suffix('.py.original').write_bytes(code_original);code.write_bytes(code_original+b'\n# altered\n')
        must_refuse('code_byte_change','Registered code/input changed: c6_engine.py')
        code.with_suffix('.py.TAMPERED').write_bytes(code.read_bytes());code.write_bytes(code_original)
        inp=mock/'QNM_GRID.json';inp_original=inp.read_bytes()
        inp.with_suffix('.json.original').write_bytes(inp_original);inp.write_bytes(inp_original+b' ')
        must_refuse('QNM_input_byte_change','Registered code/input changed: QNM_GRID.json')
    finally:c6_engine.ROOT=oldroot
    _,after=c6_engine.checked_registration()
    if digest!=after:raise AssertionError('Real registration changed')
    atomic_json(ROOT/'C6_GUARD_TEST.json',dict(status='PASS',tests=rows,
        real_registration_sha256=digest,real_registered_code_and_inputs_unchanged=True,
        no_strain_read=True,copy_folder=str(folder.relative_to(ROOT)),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    print(json.dumps(dict(status='PASS',tests=len(rows),registration_sha256=digest)))

if __name__=='__main__':main()
