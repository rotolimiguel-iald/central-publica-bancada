"""Fixed cp437 preload before the existing read hook; no wildcard permissions."""
import codecs
import hashlib
import importlib
from pathlib import Path
def preload_npz_codec(pin):
    if set(pin)-{"path","sha256","bytes","python_version","role"}:
        raise ValueError("Unknown codec pin metadata")
    path=Path(pin["path"]).resolve()
    if str(path)!="/usr/lib/python3.12/encodings/cp437.py":
        raise ValueError("Only the named standard-library cp437 codec")
    raw=path.read_bytes()
    if len(raw)!=pin["bytes"] or hashlib.sha256(raw).hexdigest()!=pin["sha256"]:
        raise ValueError("Codec bytes differ from fixed pin")
    module=importlib.import_module("encodings.cp437")
    if Path(module.__file__).resolve()!=path:
        raise ValueError("Loaded codec origin differs")
    info=codecs.lookup("cp437")
    if info.name!="cp437" or bytes(range(256)).decode("cp437").encode("cp437")!=bytes(range(256)):
        raise ValueError("Codec identity/roundtrip failed")
    return {"path":str(path),"sha256":pin["sha256"],"bytes":len(raw),"codec_name":info.name,
            "preloaded_before_hook":True,"byte_roundtrip_256":True}
