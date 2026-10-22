"""Read source configuration for missing or inconsistent prior documentation."""
from pathlib import Path
import json
import h5py
import numpy as np
from fetch_public import atomic_json
ROOT=Path(__file__).resolve().parent

def main():
    schema=json.loads((ROOT/'C4_CATALOG_SCHEMA.json').read_bytes());rows=[]
    for row in schema['rows']:
        if row['priors'].get('dtau220') and 'reweighted' not in row['label']:continue
        path=ROOT/'cache/public/21454847/extracted/pSEOB/metafiles'/row['filename']
        info=dict(event=row['event'],label=row['label'],dtau_range=row['summary']['dtau220'],
                  df_range=row['summary']['domega220'],config={},metadata={})
        with h5py.File(path,'r') as h:
            g=h[row['label']]
            for parent in ['config_file','meta_data']:
                if parent not in g:continue
                def visit(name,item):
                    if isinstance(item,h5py.Dataset) and item.size<=10:
                        raw=item[()]
                        values=[x.decode(errors='replace') if isinstance(x,bytes) else str(x) for x in np.atleast_1d(raw)]
                        txt='\n'.join(values)
                        if any(k in txt.lower() for k in ['prior','uniform','reweight','gwtc','pesummary']) or any(k in name for k in ['version','label','prior']):
                            info['config' if parent=='config_file' else 'metadata'][name]=txt
                g[parent].visititems(visit)
        rows.append(info)
        print(json.dumps(dict(event=row['event'],config_fields=list(info['config']),
                              metadata_fields=list(info['metadata']))),flush=True)
    atomic_json(ROOT/'C4_CATALOG_PRIOR_AUDIT.json',dict(rows=rows))

if __name__=='__main__':main()
