"""Inspect GWTC-5 pSEOB products without executing release code or pickle."""
from pathlib import Path
import hashlib
import json
import h5py
import numpy as np
from fetch_public import atomic_json

ROOT=Path(__file__).resolve().parent

def main():
    folder=ROOT/'cache/public/21454847/extracted/pSEOB'
    custody=json.loads((folder.parents[1]/'extraction_receipt.json').read_bytes())
    expected={r['member']:r['sha256'] for r in custody['files']}
    rows=[]
    for path in sorted((folder/'metafiles').glob('*.h5')):
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        assert sha==expected['pSEOB/metafiles/'+path.name]
        with h5py.File(path,'r') as h:
            groups=[name for name in h if isinstance(h[name],h5py.Group) and 'posterior_samples' in h[name]]
            if len(groups)!=1:raise ValueError((path.name,groups))
            group=h[groups[0]];s=group['posterior_samples'][()]
            priors={}
            if 'priors/analytic' in group:
                for key in group['priors/analytic']:
                    if any(tag in key for tag in ['omega','tau','final','mass','spin']):
                        raw=group['priors/analytic/'+key][()]
                        priors[key]=[v.decode() if isinstance(v,bytes) else str(v) for v in np.atleast_1d(raw)]
            selected=[name for name in s.dtype.names if any(tag in name for tag in ['omega','tau','final_spin','final_mass','redshift'])]
            ident=np.column_stack([s[k] for k in selected])
            row=dict(event=path.name.removeprefix('pSEOB_').removesuffix('_Prod0.h5'),
                     filename=path.name,sha256=sha,posterior_selected_sha256=hashlib.sha256(ident.tobytes()).hexdigest(),
                     label=groups[0],N=len(s),fields=selected,priors=priors,
                     summary={k:dict(min=float(np.min(s[k])),max=float(np.max(s[k])),median=float(np.median(s[k]))) for k in selected})
            rows.append(row)
            print(json.dumps({k:row[k] for k in ['event','label','N','fields']}),flush=True)
    duplicate_groups=[]
    for field in ['sha256','posterior_selected_sha256']:
        buckets={}
        for row in rows:buckets.setdefault(row[field],[]).append(row['event'])
        duplicate_groups.extend(dict(field=field,events=events) for events in buckets.values() if len(events)>1)
    old=ROOT/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    old_sha=hashlib.sha256(old.read_bytes()).hexdigest()
    matches=[r['event'] for r in rows if r['sha256']==old_sha]
    atomic_json(ROOT/'C4_CATALOG_SCHEMA.json',dict(source_record=21454847,rows=rows,N_events=len(rows),
                duplicates=duplicate_groups,GW250114_matches_17018009=matches,
                not_read='No strain; notebooks treated as data; no pickle execution'))
    book=json.loads((folder/'pSEOBNR_main_figure.ipynb').read_bytes())
    for i,cell in enumerate(book['cells']):
        source=''.join(cell.get('source',[]))
        if any(s in source for s in ['metafiles','final_spin','domega','dtau','load','prior']):
            print(json.dumps(dict(cell=i,type=cell['cell_type'],source=source[:12000])),flush=True)
    print(json.dumps(dict(N_events=len(rows),duplicates=duplicate_groups,GW250114_matches=matches)),flush=True)

if __name__=='__main__':main()
