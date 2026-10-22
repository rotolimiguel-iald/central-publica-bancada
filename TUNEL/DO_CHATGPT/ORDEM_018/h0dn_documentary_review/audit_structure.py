"""Validate public file structure without executing H0DN or estimating parameters."""
from pathlib import Path
from collections import Counter
import ast
import fnmatch
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parent
UP = ROOT / 'upstream'

def main():
    manifest = json.loads((ROOT / 'UPSTREAM_MANIFEST.json').read_text())
    verified = []
    for record in manifest['files']:
        data = (UP / record['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == record['sha256']
        verified.append(record['path'])
    modules = {}
    for path in sorted(UP.rglob('*.py')):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        modules[str(path.relative_to(UP)).replace('\\','/')] = {
            node.name:[node.lineno,node.end_lineno]
            for node in tree.body if isinstance(node, (ast.FunctionDef,ast.AsyncFunctionDef))}
    # Raw source table: inspect identifiers only. No mu values or residuals.
    raw = []
    for line in (UP / 'data/host_data.dat').read_text().splitlines():
        line = re.split(r'[#;]',line,maxsplit=1)[0].strip()
        if not line or line.lower().startswith('host'): continue
        cols = line.split()
        assert len(cols) >= 6
        raw.append(dict(host=cols[0],method=cols[3],anchor=cols[4],source=cols[5]))
    anchors = {'N4258','MW','LMC','SMC','M31','ALL'}
    rows = [r for r in raw if r['host'] not in anchors and not any(
        fnmatch.fnmatch(v,p) for v in r.values() for p in ('*jagb*','*mira*','b25','SMC'))]
    ceph = {r['host'] for r in rows if r['method'].startswith('ceph')}
    trgb = {r['host'] for r in rows if r['method'].startswith('trgb')}
    # This is a supplied SN HF covariance, NOT the assembled network covariance.
    path = UP / 'data/sn1a_covar_pp.dat'
    tokens = path.read_text().split()
    header = float(tokens[0]); assert header.is_integer() and header > 0
    size = int(header); vals = list(map(float,tokens[1:]))
    assert len(vals) == size*size
    assert all(math.isfinite(v) for v in vals)
    diagonal = [vals[i*size+i] for i in range(size)]
    symmetry = max(abs(vals[i*size+j]-vals[j*size+i]) for i in range(size) for j in range(size))
    nonzero = sum(vals[i*size+j] != 0 for i in range(size) for j in range(size) if i!=j)
    report = dict(scope='STATIC_REVIEW_NO_FIT_NO_UPSTREAM_EXECUTION_NO_OBSERVED_VERDICT',
        commit=manifest['commit'], verified_file_count=len(verified), functions=modules,
        host_identifiers=dict(raw_rows=len(raw),
            selection='baseline pattern filters and anchor removal only; NOT full rung_equalize/config execution',
            selected_rows_before_calibrator_matching=len(rows), methods=dict(Counter(r['method'] for r in rows)),
            anchors=dict(Counter(r['anchor'] for r in rows)),
            hosts_with_cepheid_and_trgb_before_calibrator_matching=sorted(ceph & trgb)),
        supplied_sn_covariance=dict(path=str(path),dimension=size,finite=True,
            diagonal_positive=all(v>0 for v in diagonal),max_asymmetry=symmetry,
            nonzero_offdiagonal_entries=nonzero,
            limitation='No PSD/eigen/rank/Cholesky computation; NOT full network covariance; no fit'),
        network_covariance='Built at runtime in equations.build_equations; not generated in this review',
        parameters_estimated=False, upstream_executed=False)
    data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
    target=ROOT/'STRUCTURE_AUDIT.json'
    if target.exists():
        assert target.read_bytes()==data, 'Existing audit differs'
    else:
        temp=target.with_suffix('.tmp');temp.write_bytes(data)
        assert temp.stat().st_size==len(data);temp.replace(target)
    print(json.dumps({k:v for k,v in report.items() if k!='functions'},ensure_ascii=False,indent=2))

if __name__ == '__main__':main()
