"""Record the inspected LAL conventions and their exact source provenance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import re
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent


def main():
    target = ROOT/'C4_GWTC3_CONVENTIONS.json'
    if target.exists():
        raise FileExistsError('Keep the original inspection')
    specs = [
        ('LALInferenceInitCBC_7_26.html',
         'https://lscsoft.docs.ligo.org/lalsuite/7.26/lalinference/_l_a_l_inference_init_c_b_c_8c_source.html',
         [(662,682),(715,722),(2558,2560)]),
        ('LALSimIMREOBHybridRingdown.html',
         'https://lscsoft.docs.ligo.org/lalsuite/7.26/lalsimulation/_l_a_l_sim_i_m_r_e_o_b_hybrid_ringdown_8c_source.html',
         [(1071,1073)])]
    sources = []
    for filename,url,ranges in specs:
        path = ROOT/'cache/literature/gwtc3_source'/filename
        raw = path.read_bytes()
        stripped = html.unescape(re.sub('<[^>]+>','',raw.decode('utf-8')))
        selected = []
        for line in stripped.splitlines():
            match = re.match(r'\s*(\d+)\s*(.*)',line)
            if match and any(lo <= int(match[1]) <= hi for lo,hi in ranges):
                selected.append(dict(source_line=int(match[1]), text=match[2]))
        if not selected:
            raise ValueError('Source line extraction failed')
        sources.append(dict(path=path.relative_to(ROOT).as_posix(), url=url,
            bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), inspected_lines=selected))
    text='\n'.join(r['text'] for s in sources for r in s['inspected_lines'])
    for required in ['--%s-min','--%s-max','"domega220"','"dtau220"','/(1. + dtau220)']:
        if required not in text:
            raise ValueError('Convention evidence missing: '+required)
    schema=json.loads((ROOT/'C4_GWTC3_SCHEMA.json').read_bytes())
    assertions=dict(frequency='Re(omega) multiplied by 1+domega220',
        damping='Im(omega) divided by 1+dtau220: dtau is fractional damping TIME, not fractional rate',
        prior='Independent uniform parameter registrations; --name-min/--name-max override default bounds',
        ratio='For points/curves inside each released rectangular support, the deformation-prior density ratio is one under this convention')
    atomic_json(target,dict(status='SOURCE_IMPLEMENTATION_READ__LEGACY_BINARY_VERSION_UNAVAILABLE',
        date_utc=datetime.now(timezone.utc).isoformat(), sources=sources, assertions=assertions,
        release_files=len(schema['rows']),
        limitation='Later source documentation and released configs do not prove the precise original binary/postprocessing fit version; numerical ratios retain this conditional assumption',
        correction='The unversioned URL in C4_GWTC3_220.json returned 404. The versioned source URLs above were obtained, saved, hashed and inspected. No numerical result was changed.',
        misleading_source_comment='The InitCBC comment says inverse damping times; the waveform implementation determines the fractional TIME convention'))
    print(json.dumps(dict(status='RECORDED',sources=len(sources),output=str(target))))


if __name__=='__main__':
    main()
