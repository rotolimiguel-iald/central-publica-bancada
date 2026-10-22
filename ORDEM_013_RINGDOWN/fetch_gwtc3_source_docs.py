"""Archive public source documentation used to interpret GWTC-3 parameters."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'LALInferenceInitCBC.html': 'https://lscsoft.docs.ligo.org/lalsuite/lalinference/_l_a_l_inference_init_c_b_c_8c_source.html',
    'LALInferenceInitCBC_7_26.html': 'https://lscsoft.docs.ligo.org/lalsuite/7.26/lalinference/_l_a_l_inference_init_c_b_c_8c_source.html',
    'LALSimIMREOBHybridRingdown.html': 'https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/_l_a_l_sim_i_m_r_e_o_b_hybrid_ringdown_8c_source.html',
}


def main():
    folder = ROOT / 'cache/literature/gwtc3_source'
    folder.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, url in SOURCES.items():
        path = folder / name
        if not path.exists():
            try:
                with urllib.request.urlopen(url, timeout=60) as response:
                    raw = response.read()
            except Exception as error:
                rows.append(dict(name=name, url=url, status='LOCAL_RETRIEVAL_FAILED', error=str(error),
                    limitation='Does not negate prior web-tool excerpt access; no local source hash is claimed'))
                continue
            temp = path.with_name(name + '.tmp')
            temp.write_bytes(raw)
            if temp.stat().st_size != len(raw):
                raise ValueError('Short documentation download')
            temp.replace(path)
        raw = path.read_bytes()
        rows.append(dict(name=name, url=url, status='RETRIEVED', path=path.relative_to(ROOT).as_posix(),
            bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    atomic_json(ROOT / 'C4_GWTC3_SOURCE_DOCS.json', dict(status='ACCESS_ATTEMPTS_RECORDED',
        at=datetime.now(timezone.utc).isoformat(), sources=rows,
        limitation='Source documentation version, not proof of the unavailable original inference binary; HDF5 version says no information'))
    print(json.dumps(rows), flush=True)


if __name__ == '__main__':
    main()
