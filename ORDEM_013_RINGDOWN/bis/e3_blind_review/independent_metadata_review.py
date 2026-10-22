"""Finite independent arithmetic and local metadata audit. No network/producer execution."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
from statistics import NormalDist
import ast,csv,hashlib,json,os

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
ROOT=BASE.parent
PRODUCER=BASE/'bis/e3_blind_prepare'
CHECKS=[]
SCALARS=[]
PINS={}
LIMIT=25_000_000


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    p=p.resolve()
    if not p.is_relative_to(ROOT) or p.stat().st_size>LIMIT:raise ValueError('Read scope/size')
    if p.suffix not in ('.json','.md','.py','.csv','.body'):raise ValueError('Metadata/code only')
    if any(x in p.name.lower() for x in ('seed','secret','posterior_samples')):raise ValueError('Excluded input')
    raw=p.read_bytes();PINS[p.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest();return raw


def load(p):return json.loads(read(p))


def check(name,okay,detail=None):
    CHECKS.append(dict(id=name,passed=bool(okay),detail=detail))


def number(name,expected,observed):
    a=Decimal(observed) if isinstance(observed,int) else Decimal.from_float(observed)
    error=abs(a-expected)/max(abs(expected),Decimal('1e-100'))
    okay=error<=Decimal('1e-11')
    SCALARS.append(dict(id=name,passed=okay,relative_error=float(error)))


def publish(name,obj):
    raw=(json.dumps(obj,ensure_ascii=False,allow_nan=False,indent=2)+'\n').encode()
    if len(raw)>LIMIT:raise ValueError('Output cap')
    p=HERE/name;tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.stat().st_size!=len(raw):raise ValueError('Short write')
    os.link(tmp,p);tmp.unlink()


def main():
    snapshot=HERE/'snapshot_001';snapshot.mkdir(parents=True,exist_ok=False)
    for p in sorted(PRODUCER.rglob('*')):
        if not p.is_file():continue
        raw=read(p);dst=snapshot/p.relative_to(PRODUCER);dst.parent.mkdir(parents=True,exist_ok=True)
        with dst.open('xb') as f:f.write(raw)
    manifest=load(PRODUCER/'MANIFEST.json')
    for entry in manifest['files']:
        p=ROOT/entry['relative_to_Chatgpt'];raw=read(p)
        check('manifest:'+entry['relative_to_Chatgpt'],hashlib.sha256(raw).hexdigest()==entry['sha256'] and len(raw)==entry['bytes'])
    addendum=load(PRODUCER/'TWO_PHASE_ADDENDUM_RECEIPT.json')
    for name,pin in addendum['pins'].items():check('addendum_pin:'+name,sha(PRODUCER/name)==pin)
    sources=load(PRODUCER/'SOURCE_PINS.json')['sources_sha256_relative_to_Chatgpt']
    for name,digest in sources.items():check('source_pin:'+name,hashlib.sha256(read(ROOT/name)).hexdigest()==digest)
    reg=load(BASE/'RINGDOWN_5SIGMA_V1.json')
    check('manifest_parent_E2',manifest['registration_sha256']==sha(BASE/'RINGDOWN_5SIGMA_V1.json'))
    guard=BASE/'bis/e2_code/registration_guard.py'
    check('guard_frozen_E2_pin',sha(guard)==reg['own_code_tree_sha256']['registration_guard.py'])
    candidates=load(PRODUCER/'CANDIDATES_SORTED.json');rows=candidates['candidates']
    expected=sorted((r for r in reg['test_candidates'].values() if r['eligible'] is True and r['published_deformation_at_registration'] is False),
                    key=lambda r:(-r['SNR_network_GWOSC'],r['event']))
    check('all14_exact_order',len(rows)==14 and [r['event'] for r in rows]==[r['event'] for r in expected])
    check('14_unique',len({r['event'] for r in rows})==14)
    check('all_hold_counts',candidates['count_total']==14 and candidates['count_unheld']==10 and candidates['count_held']==4)
    csvpath=BASE/'bis/e0_metadata/GWOSC_EVENTS.csv';read(csvpath)
    with csvpath.open(encoding='utf-8-sig',newline='') as f:csvrows=list(csv.DictReader(f))
    pub=load(BASE/'bis/e3_publication_refresh/PUBLICATION_METADATA_REVIEW_INDEX.json')
    parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(timezone.utc)
    dates=[]
    for row,entry in zip(rows,expected):
        event=row['event'];review=row['publication_metadata_review'];csvrow=csvrows[row['SNR_source']['line']-2]
        check('hold_preserved:'+event,type(row['data_quality_hold']) is bool and row['data_quality_hold']==entry['data_quality_hold']==pub['events'][event]['data_quality_hold'])
        check('SNR_exact_metadata:'+event,csvrow['event']==event and float(csvrow['network_matched_filter_snr'])==row['SNR_network']==entry['SNR_network_GWOSC'])
        check('SNR_provenance:'+event,row['SNR_source']['sha256']==sha(csvpath) and row['SNR_source']['version_key']==csvrow['version_key'])
        check('not_admitted:'+event,row['admission'] is None and row['blindness_certified_here'] is False)
        raw=read(ROOT/review['relative_to_Chatgpt'])
        check('publication_pin_and_descriptor:'+event,hashlib.sha256(raw).hexdigest()==review['sha256'] and review==pub['events'][event]['publication_metadata_review'])
        aware=datetime.fromisoformat(review['reviewed_utc']).utcoffset() is not None
        check('publication_chronology_aware:'+event,aware and parse(reg['registered_utc'])<=parse(review['reviewed_utc'])<=datetime.now(timezone.utc))
        dates.append(parse(review['reviewed_utc']).isoformat())
    info=load(PRODUCER/'EXPECTED_INFORMATION.json');fitdoc=load(BASE/'bis/E0_SNR_INFORMATION_FIT.json')
    fits={f['population']:f for f in fitdoc['fits']}
    expectedkeys={(r['event'],population) for r in rows for population in ('GWTC5_31','GWTC5_33')}
    actualkeys=[(r['event'],r['fit_population']) for r in info['rows']]
    check('information28_unique_coverage',len(actualkeys)==28 and len(set(actualkeys))==28 and set(actualkeys)==expectedkeys)
    for f in info['fits_preserved']:
        check('full_fit_preserved:'+f['population'],all(f[k]==fits[f['population']][k] for k in f))
    for item in info['stored_bootstrap_grid_preserved']:
        grid=[{'SNR':p['SNR_network'],'interval':p['event_bootstrap_information_025_50_975']} for p in fits[item['population']]['predictions']]
        check('bootstrap_grid_unchanged:'+item['population'],item['grid']==grid)
    byevent={r['event']:r for r in rows};samples=[]
    with localcontext() as ctx:
        ctx.prec=80
        d=lambda x:Decimal.from_float(x) if isinstance(x,float) else Decimal(x)
        for row in info['rows']:
            f=fits[row['fit_population']];rho=d(row['SNR_network']);a,b=map(d,f['coefficients_log_intercept_slope'])
            v=[Decimal(1),rho.ln()];cov=[[d(x) for x in line] for line in f['covariance']]
            mu=a+b*v[1];var=sum(v[i]*cov[i][j]*v[j] for i in range(2) for j in range(2))
            s=d(f['residual_sigma_ln_ddof_Nminus2']);t=d(f['coefficient_95_t_halfwidth'][0])/cov[0][0].sqrt()
            half=t*var.sqrt();median=mu.exp();proxy=(-2*mu).exp();meanI=(-2*mu+2*s*s).exp()
            fields=dict(ln_sigma_mean_mu=mu,mu_variance_from_full_coefficient_covariance=var,
                sigma_conditional_median=median,inverse_squared_conditional_median_proxy=proxy,
                expected_inverse_variance_lognormal_s_fixed=meanI,
                parameter_gaussian_integrated_information_s_fixed=( -2*mu+2*s*s+2*var).exp(),
                ratio_expectation_to_proxy=(2*s*s).exp())
            ident=row['fit_population']+':'+row['event']
            for field,value in fields.items():number(ident+':'+field,value,row[field])
            arrays=dict(sigma_residual_conditional_05_50_95=[(mu+s*d(NormalDist().inv_cdf(p))).exp() for p in (.05,.5,.95)],
                sigma_median_coefficient_only_95_t_interval=[(mu-half).exp(),(mu+half).exp()],
                expected_I_coefficient_only_95_t_interval_s_fixed=[(-2*mu+2*s*s-2*half).exp(),(-2*mu+2*s*s+2*half).exp()])
            for field,values in arrays.items():
                for i,value in enumerate(values):number(ident+':'+field+':'+str(i),value,row[field][i])
            check('SNR/hold_same:'+ident,row['data_quality_hold']==byevent[row['event']]['data_quality_hold'] and row['SNR_source']==byevent[row['event']]['SNR_source'])
            check('domain_flag:'+ident,row['outside_fit_SNR_domain']==(not f['SNR_domain'][0]<=row['SNR_network']<=f['SNR_domain'][1]))
            check('unpaid_fields:'+ident,row['bootstrap_interval_at_candidate_SNR'] is None and row['information_for_actual_new_PE'] is None)
            check('covariance_positive:'+ident,cov[0][0]>0 and cov[1][1]>0 and cov[0][0]*cov[1][1]-cov[0][1]*cov[1][0]>0 and var>0)
            if row['event']==rows[0]['event']:
                samples.append(dict(population=f['population'],event=row['event'],proxy=float(proxy),lognormal_expectation=float(meanI),
                    inverse_square_mean_sigma=float((-2*mu-s*s).exp()),expectation_proxy_ratio=float((2*s*s).exp()),
                    covariance_00=float(cov[0][0]),covariance_01=float(cov[0][1]),covariance_11=float(cov[1][1]),
                    propagated_mu_variance=float(var)))
    ready=load(PRODUCER/'METADATA_READINESS.json');templates=load(PRODUCER/'NONEXECUTABLE_TEMPLATES.json')
    license_doc=load(PRODUCER/'PER_FILE_LICENSE_METADATA.json')
    five=[r['event'] for r in rows if not r['data_quality_hold']][:5]
    check('five_unheld_metadata_targets',[r['event'] for r in ready['targets']]==five)
    check('five_templates_not_admission',[r['event'] for r in templates['templates']]==five and templates['cost_estimates'] is None)
    check('no_jobs_schema', 'schema_version' not in templates and all(t['not_jobs_schema'] is True for t in templates['templates']))
    filecount=0
    license_urls={f['url'] for f in license_doc['files']}
    for target in ready['targets']:
        check('target_unheld_unadmitted:'+target['event'],target['data_quality_hold'] is False and target['admission'] is None)
        for det in target['detectors']:
            for f in det['files']:
                filecount+=1
                check('unverified_bytes:'+target['event']+':'+f['filename'],f['local_sha256'] is None and f['expected_bytes'] is None and f['provider_checksum_verified_against_bytes'] is False)
                md5src=f['checksum_source'];body=ROOT/md5src['body']['relative_to_Chatgpt'];raw=read(body)
                tokens=raw.decode().splitlines()[md5src['line']-1].split()
                check('MD5_metadata_line:'+f['filename'],tokens[0]==f['provider_checksum'] and tokens[1]==md5src['provider_path'])
                check('license_mapping:'+f['filename'],f['url'] in license_urls)
    for t in templates['templates']:
        for frag in t['download_recipe_fragments']:
            check('recipe_nonexecutable:'+frag['filename'],frag['maximum_bytes'] is None and frag['expected_bytes'] is None and
                  frag['license_receipt_sha256']==sha(PRODUCER/'PER_FILE_LICENSE_METADATA.json'))
    # Reproduce the exact string-comparison predicate, no builder call or I/O.
    code=ast.parse(read(PRODUCER/'build_readiness.py').decode('utf-8-sig'))
    comparisons=[n for n in ast.walk(code) if isinstance(n,ast.Compare) and len(n.ops)==2 and
                 isinstance(n.left,ast.Subscript) and isinstance(n.left.value,ast.Name) and n.left.value.id=='reg']
    check('chronology_predicate_identified',len(comparisons)==1)
    naive_reg='2026-09-22T00:00:00+00:00';future_review='2026-09-22T09:30:00-02:00';fake_now='2026-09-22T10:00:00+00:00'
    chronology=dict(registration=naive_reg,review=future_review,now=fake_now,
        lexicographic_accepted=naive_reg<=future_review<=fake_now,
        actual_UTC_accepted=parse(naive_reg)<=parse(future_review)<=parse(fake_now),
        current14_aware_chronology_valid=all(c['passed'] for c in CHECKS if c['id'].startswith('publication_chronology_aware:')))
    check('reproduced_timezone_string_comparison_defect',chronology['lexicographic_accepted'] and not chronology['actual_UTC_accepted'])
    for name,digest in PINS.items():
        if sha(ROOT/name)!=digest:raise ValueError('Source changed during review: '+name)
    summary=dict(status='INDEPENDENT_DOCUMENTARY_AND_FINITE_ARITHMETIC_REVIEW_NOT_ADMISSION',
        finished_utc=datetime.now(timezone.utc).isoformat(),metadata_checks=len(CHECKS),metadata_passed=sum(c['passed'] for c in CHECKS),
        scalar_checks=len(SCALARS),scalar_passed=sum(c['passed'] for c in SCALARS),
        max_scalar_relative_error=max(c['relative_error'] for c in SCALARS),relative_tolerance=1e-11,
        arithmetic_method='Decimal 80 digits and vector-matrix-vector covariance; no producer import, refit, bootstrap or RNG',
        held_events=[r['event'] for r in rows if r['data_quality_hold']],unheld_count=sum(not r['data_quality_hold'] for r in rows),
        domain_extrapolations={p:[r['event'] for r in info['rows'] if r['fit_population']==p and r['outside_fit_SNR_domain']] for p in fits},
        top_event_examples=samples,provider_file_records=filecount,chronology_advisory=chronology,
        scientific_data_read=False,network_used=False,producer_executed=False,admission=False,
        checks=CHECKS,scalar_results=SCALARS)
    publish('AUDIT_RESULTS_V1.json',summary)
    publish('SOURCE_SNAPSHOT_V1.json',dict(status='IMMUTABLE_LOCAL_METADATA_SNAPSHOT',
        source_pins_relative_to_Chatgpt=PINS,review_script_sha256=sha(Path(__file__)),producer_copy='snapshot_001/',
        no_network=True,no_scientific_data=True))
    print(json.dumps({k:summary[k] for k in ('metadata_checks','metadata_passed','scalar_checks','scalar_passed','max_scalar_relative_error','held_events','domain_extrapolations')}))


if __name__=='__main__':main()
