"""Inspect released parameter-estimation metadata without executing stored code."""
from pathlib import Path
import hashlib
import json
import h5py
import numpy as np
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def scalar(value):
    if isinstance(value,bytes):return value.decode('utf-8',errors='replace')
    if isinstance(value,np.generic):return scalar(value.item())
    if isinstance(value,np.ndarray):
        return [scalar(x) for x in value.tolist()] if value.size<200 else dict(shape=value.shape)
    return value if isinstance(value,(str,int,float,bool)) or value is None else str(value)

def main():
    reg=ROOT/'REGISTRO_C4.json'
    regsha=hashlib.sha256(reg.read_bytes()).hexdigest()
    receipt=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md'
    if regsha not in receipt.read_text(encoding='utf-8'):
        raise ValueError('Prespecified registration has changed')
    base=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr'
    path=base/'posterior_samples.h5'
    structures=[]
    with h5py.File(path,'r') as h:
        root_attrs={str(k):scalar(v) for k,v in h.attrs.items()}
        def visit(name,obj):
            rec=dict(name=name,kind=type(obj).__name__,attrs={str(k):scalar(v) for k,v in obj.attrs.items()})
            if isinstance(obj,h5py.Dataset):
                rec.update(shape=obj.shape,dtype=str(obj.dtype),fields=obj.dtype.names)
                if obj.size<200 and obj.dtype.kind in ('S','O','U'):
                    rec['small_text']=scalar(obj[()])
                if any(k in name.lower() for k in ['prior','config']) and obj.size<200:
                    rec['prior_or_config']=scalar(obj[()])
            structures.append(rec)
        h.visititems(visit)
    with np.load(base/'pseob_remnant_samples.npz',allow_pickle=False) as data:
        remnant=[dict(key=k,shape=data[k].shape,dtype=str(data[k].dtype)) for k in data.files]
    report=dict(status='SCHEMA_READ_BEFORE_MODEL_EVIDENCE',registration_sha256=regsha,
                h5_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),root_attrs=root_attrs,
                structures=structures,remnant_npz=remnant,readme=(base/'README.md').read_text())
    atomic_json(ROOT/'C4_SCHEMA.json',report)
    relevant=[r for r in structures if r['name'].endswith(('/priors/analytic/domega220','/priors/analytic/dtau220'))]
    posterior=next(r for r in structures if r['name'].endswith('/posterior_samples'))
    print(json.dumps(dict(status=report['status'],posterior_shape=posterior['shape'],
                          prior_220=relevant,remnant_npz=remnant)),flush=True)

if __name__=='__main__':main()
