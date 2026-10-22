"""Inspect the declared GWTC-3 pSEOB products without presuming field names."""
from pathlib import Path
import hashlib
import json
import h5py
import numpy as np
from fetch_public import atomic_json

ROOT = Path(__file__).resolve().parent


def main():
    receipt = json.loads((ROOT / 'cache/public/17461225/extraction_receipt.json').read_bytes())
    rows = []
    for item in receipt['files']:
        path = ROOT / item['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('GWTC-3 source changed')
        labels = []
        with h5py.File(path, 'r') as handle:
            for name, group in handle.items():
                if not isinstance(group, h5py.Group) or 'posterior_samples' not in group:
                    continue
                samples = group['posterior_samples']
                fields = list(samples.dtype.names or [])
                relevant = [n for n in fields if any(k in n.lower() for k in ('domega', 'dtau', 'final_', 'redshift', 'geocent', 'time'))]
                summaries = {}
                for field in relevant:
                    value = samples[field]
                    if np.issubdtype(value.dtype, np.number):
                        summaries[field] = dict(min=float(np.min(value)), max=float(np.max(value)),
                            quantiles_05_50_95=np.quantile(value, [.05, .5, .95]).tolist())
                config = {}
                def visit(key, value):
                    if isinstance(value, h5py.Dataset) and any(k in key.lower() for k in ('config', 'prior', 'version', 'approximant', 'label')):
                        if value.size < 300:
                            values = np.atleast_1d(value[()])
                            text = [x.decode('utf-8', errors='replace') for x in values if isinstance(x, bytes)]
                            if text:
                                config[key] = text
                group.visititems(visit)
                labels.append(dict(label=name, N=len(samples), fields=fields, summaries=summaries,
                    source_text=config, root_keys=list(handle.keys())))
        row = dict(member=item['member'], path=item['path'], sha256=item['sha256'], labels=labels)
        rows.append(row)
        print(json.dumps(dict(member=item['member'], labels=[dict(label=r['label'], N=r['N'],
            relevant_fields=list(r['summaries']), config_keys=list(r['source_text'])) for r in labels])), flush=True)
    atomic_json(ROOT / 'C4_GWTC3_SCHEMA.json', dict(status='PUBLIC_SCHEMA_INSPECTED_NOT_BAYES_FACTOR',
        record=17461225, archive_sha256=receipt['archive_sha256'], rows=rows,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))


if __name__ == '__main__':
    main()
