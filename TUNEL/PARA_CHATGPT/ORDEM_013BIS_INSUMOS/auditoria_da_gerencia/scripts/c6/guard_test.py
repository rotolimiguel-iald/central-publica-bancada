import sys, importlib, shutil
from pathlib import Path
R = Path(sys.argv[1]); sys.path.insert(0, str(R))
import c6_engine
def check(label):
    try:
        importlib.reload(c6_engine); reg, d = c6_engine.checked_registration(); print(label, "ACCEPTED", d[:16])
    except Exception as e:
        print(label, "REFUSED", type(e).__name__, str(e)[:90])
check("identical")
p = R/"REGISTRO_C6.json"; o = p.read_bytes(); p.write_bytes(o.replace(b'"primary_start_tM": 10.0', b'"primary_start_tM": 6.0')); check("registry_primary_changed"); p.write_bytes(o)
p = R/"tgl_ringdown_likelihood.py"; o = p.read_bytes(); p.write_bytes(o + b"\n#x\n"); check("likelihood_code_changed"); p.write_bytes(o)
p = R/"fetch_public.py"; o = p.read_bytes(); p.write_bytes(o.replace(b"return md5.hexdigest(), sha.hexdigest()", b"return md5.hexdigest(), 'forged'")); check("UNREGISTERED_fetch_public_digests_forged"); p.write_bytes(o)
r = R.parent/"TUNEL/DO_CHATGPT/ENTREGA_013_C6a_REGISTRO_TOEPLITZ.md"; o = r.read_bytes(); r.write_bytes(o + b"\n(edited after the fact)\n"); check("receipt_edited_but_hash_kept"); r.write_bytes(o)
