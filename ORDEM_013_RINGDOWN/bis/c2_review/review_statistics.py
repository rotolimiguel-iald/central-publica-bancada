"""Read-only independent reduction of recorded C2 fits; stdlib only."""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def quantile(values, probability):
    values = sorted(values)
    position = (len(values) - 1) * probability
    i = math.floor(position)
    return values[i] if i == len(values)-1 else values[i] + (position-i)*(values[i+1]-values[i])

def standard_error(influence, groups):
    if groups is None:
        return statistics.stdev(influence) / math.sqrt(len(influence))
    sums = defaultdict(list)
    for g, value in zip(groups, influence):
        sums[g].append(value)
    return math.sqrt(len(sums)/(len(sums)-1)*math.fsum(math.fsum(v)**2 for v in sums.values()))/len(influence)

def write_new(path, data):
    if path.exists():
        raise FileExistsError(path)
    raw = (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8')
    tmp = path.with_name(path.name+'.tmp')
    with tmp.open('xb') as handle:
        handle.write(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(path)

def main():
    path = ROOT/'bis/C2_TRAJECTORY_expanded_1000.json'
    data = json.loads(path.read_bytes())
    groups = data['noise_indices']
    counts = Counter(groups)
    paths = list(data['sources']) + ['refeito/record_c2_013bis.py',
        'C2_ADENDO_OBSERVAVEL.md','REAPROVEITAMENTO_C2.md',
        'bis/C2_TRAJECTORY_expanded_1000.json','bis/C2_TRAJECTORY_benchmark.json',
        'C2_TRAJECTORY_RECOVERY.json','prepare_recolored_noise.py',
        'C5_EMPIRICAL_NOISE.json','cache/psd/aLIGO_O4_high_asd.txt']
    hashes = {rel:dict(bytes=(ROOT/rel).stat().st_size,sha256=digest(ROOT/rel)) for rel in paths}
    hash_checks = {rel:hashes[rel]['sha256']==h for rel,h in data['sources'].items()}
    noise_meta=json.loads((ROOT/'C5_RECOLORED_NOISE.json').read_bytes())
    scenario=next(x for x in noise_meta['scenarios'] if x['psd']=='O4')
    hash_checks['recoloring_source']=hashes['prepare_recolored_noise.py']['sha256']==noise_meta['source_sha256']
    hash_checks['O4_curve']=hashes['cache/psd/aLIGO_O4_high_asd.txt']['sha256']==scenario['curve']['sha256']
    reports=[]; max_difference=0.; problems=[]
    for row in data['rows']:
        for kind in ('noise_free','recolored'):
            cell=row[kind]; fits=cell['fits']; n=len(fits)
            x=[f['df'] for f in fits]; y=[f['dtau'] for f in fits]
            mx=statistics.mean(x); my=statistics.mean(y); sd=statistics.stdev(x)
            centered_squares=[(v-mx)**2 for v in x]; vx=statistics.mean(centered_squares)
            influence=[(v-vx)/(2*sd) for v in centered_squares] if sd else [0.]*n
            g=groups if kind=='recolored' else None
            computed=dict(N=n,mean_df=mx,mean_dtau=my,df_standard_deviation=sd,
                mean_dtau_standard_error=standard_error([v-my for v in y],g),
                df_standard_deviation_standard_error=standard_error(influence,g),
                df_05_50_95=[quantile(x,p) for p in (.05,.5,.95)],
                dtau_05_50_95=[quantile(y,p) for p in (.05,.5,.95)],
                boundary_count=sum(f['boundary'] for f in fits),
                optimizer_failures=sum(not f['optimizer_success'] for f in fits))
            diffs={}
            for key,value in computed.items():
                delta=max(abs(a-b) for a,b in zip(value,cell[key])) if isinstance(value,list) else abs(value-cell[key])
                diffs[key]=delta; max_difference=max(max_difference,delta)
                if delta>1e-12:problems.append([row['reading'],row.get('occupation'),kind,key,delta])
            bad=[]; boundary_indices=[]
            for i,f in enumerate(fits):
                bounded=(-.5-1e-12<=f['df']<=.5+1e-12 and math.expm1(-2)-1e-12<=f['dtau']<=math.expm1(2)+1e-12)
                finite=all(math.isfinite(f[k]) for k in ('df','dtau','cost'))
                boundary=(abs(f['df'])>.499 or abs(math.log1p(f['dtau']))>1.999)
                if not bounded or not finite or boundary!=f['boundary'] or f['cost']<0:bad.append(i)
                if boundary:boundary_indices.append(i)
            label=row['reading']+(' N='+str(row['occupation']) if 'occupation' in row else '')
            textrow=f"| {label} | {'sem ruído' if kind=='noise_free' else 'recolorido'} | {computed['mean_dtau']:.7g} ± {computed['mean_dtau_standard_error']:.3g} | {computed['df_standard_deviation']:.7g} ± {computed['df_standard_deviation_standard_error']:.3g} | {computed['boundary_count']} / {computed['optimizer_failures']} |"
            table_match=textrow in (ROOT/'C2_ADENDO_OBSERVAVEL.md').read_text(encoding='utf-8')
            reports.append(dict(reading=row['reading'],occupation=row.get('occupation'),kind=kind,
                recalculated=computed,max_difference=max(diffs.values()),table_row_match=table_match,
                bad_fits=bad,boundary_indices=boundary_indices,
                iid_mean_dtau_se=statistics.stdev(y)/math.sqrt(n),
                finite_n_sd_influence_factor=n/(n-1),
                fit_record_keys=sorted(fits[0])))
    result=dict(scope='Independent stdlib reduction; no project imports or inference rerun',
        hashes=hashes,source_hash_checks=hash_checks,cell_count=len(reports),
        fit_count=sum(c['recalculated']['N'] for c in reports),
        max_absolute_statistic_difference=max_difference,problems=problems,cells=reports,
        noise=dict(draws=len(groups),distinct_used=len(counts),library=data['original_noise_windows'],
            min_repetitions=min(counts.values()),max_repetitions=max(counts.values()),
            absent_indices=sorted(set(range(data['original_noise_windows']))-counts.keys()),
            index_effective_count=len(groups)**2/sum(v*v for v in counts.values()),
            gps_count=len(data['original_noise_GPS']),gps_unique=len(set(data['original_noise_GPS'])),
            gps_min_step=min(b-a for a,b in zip(data['original_noise_GPS'],data['original_noise_GPS'][1:]))),
        top_level_keys=list(data),row_keys=list(data['rows'][0]))
    write_new(OUT/'statistics.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('hashes','cells')},indent=2))
    for c in reports:print(c['reading'],c['occupation'],c['kind'],c['table_row_match'],c['boundary_indices'])

if __name__=='__main__':
    main()
