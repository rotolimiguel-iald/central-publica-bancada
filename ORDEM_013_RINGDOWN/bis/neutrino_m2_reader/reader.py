"""T11: deterministic reader of the frozen neutrino rule; no um.py execution."""
from pathlib import Path
from datetime import date
from urllib.parse import urlparse
import argparse,hashlib,json,math

def sha_file(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def sha_obj(value):
    # Exact serialization from the read-only sha_obj excerpt, including defaults.
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()

def strict_json(path):
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:raise ValueError('DUPLICATE_JSON_KEY: '+k)
            result[k]=v
        return result
    def bad_constant(value):raise ValueError('NONFINITE_JSON: '+value)
    return json.loads(Path(path).read_bytes(),object_pairs_hook=pairs,parse_constant=bad_constant)

def load_snapshot(path,expected_sha256):
    if sha_file(path)!=expected_sha256:raise ValueError('SNAPSHOT_HASH_MISMATCH')
    snapshot=strict_json(path)
    actual=sha_obj(snapshot['frozen'])
    if actual!=snapshot['registry_frozen_hash']:raise ValueError('FROZEN_HASH_MISMATCH: '+actual+' != '+snapshot['registry_frozen_hash'])
    if snapshot['frozen']['version']!='NEUTRINO_M2_V2':raise ValueError('UNSUPPORTED_FROZEN_VERSION')
    return snapshot

def positive_number(value,name):
    if type(value) not in (int,float) or not math.isfinite(value) or value<=0:raise ValueError('INVALID_POSITIVE_NUMBER: '+name)
    return float(value)

def load_release(path,expected_sha256,allow_fixtures=False):
    path=Path(path).resolve()
    if sha_file(path)!=expected_sha256:raise ValueError('RELEASE_HASH_MISMATCH')
    release=strict_json(path)
    if release.get('schema')!='TGL_NEUTRINO_RELEASE_V1':raise ValueError('UNKNOWN_RELEASE_SCHEMA')
    if type(release.get('fixture')) is not bool:raise ValueError('FIXTURE_MARK_REQUIRED')
    if release['fixture'] and not allow_fixtures:raise ValueError('FIXTURE_NOT_SCIENTIFIC_DATA')
    date.fromisoformat(release['release_date'])
    source=release['primary_source'];url=urlparse(source['url'])
    if url.scheme!='https' or not url.netloc or not source.get('citation'):raise ValueError('PRIMARY_SOURCE_METADATA_REQUIRED')
    doc=(path.parent/source['document_path']).resolve()
    if not doc.is_relative_to(path.parent) or doc==path:raise ValueError('SOURCE_OUTSIDE_RELEASE_DIRECTORY')
    if doc.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise ValueError('CONFIDENTIAL_SOURCE_REFUSED')
    if sha_file(doc)!=source['document_sha256']:raise ValueError('PRIMARY_DOCUMENT_HASH_MISMATCH')
    determinations=release['determinations']
    if not isinstance(determinations,list) or not determinations:raise ValueError('EMPTY_RELEASE')
    for row in determinations:
        positive_number(row['dm21_1e5'],'dm21_1e5');positive_number(row['sig_1e5'],'sig_1e5')
        if type(row['autonoma']) is not bool:raise ValueError('AUTONOMY_BOOLEAN_REQUIRED')
        if not isinstance(row['grupo'],str) or not row['grupo'].strip():raise ValueError('GROUP_REQUIRED')
        if not row.get('independence_note'):raise ValueError('INDEPENDENCE_PROVENANCE_REQUIRED')
        if not row.get('fonte') or row['data']!=release['release_date']:raise ValueError('DATED_SOURCE_REQUIRED')
        if type(row.get('indep')) is not bool:raise ValueError('LEGACY_INDEP_BOOLEAN_REQUIRED')
    return release,dict(path=str(path),sha256=expected_sha256,document_sha256=sha_file(doc),url=source['url'],
        status='FILE_HASH_VERIFIED_NUMBERS_AND_INDEPENDENCE_OPERATOR_TRANSCRIBED',fixture=release['fixture'])

def evaluate(snapshot,determinations,fixture=False):
    ALPHA_FINE_CODATA_2018=positive_number(snapshot['alpha_fine_codataa2018'],'alpha')
    beta_tgl=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
    m2_tgl_mev=beta_tgl*math.sin(math.radians(45.0))*1000.0
    if not determinations:raise ValueError('EMPTY_DETERMINATIONS')
    ladder=[]
    for d in determinations:
        dm=positive_number(d['dm21_1e5'],'dm21_1e5');unc=positive_number(d['sig_1e5'],'sig_1e5')
        if type(d.get('autonoma')) is not bool or not d.get('grupo'):raise ValueError('INVALID_GROUP_OR_AUTONOMY')
        measured=math.sqrt(dm*1e-5)*1000.0;sigma=0.5*(unc/dm)*measured
        ladder.append(dict(fonte=d['fonte'],data=d['data'],grupo=d['grupo'],autonoma=d['autonoma'],
            m2_obs_meV=measured,sigma_meV=sigma,tensao_sigma=abs(measured-m2_tgl_mev)/sigma))
    current=ladder[-1]['tensao_sigma']
    groups=sorted({e['grupo'] for e in ladder if e['autonoma'] and e['tensao_sigma']>=5.0})
    killed=len(groups)>=2
    verdict=('TGL_NU_M2_FALSIFIED' if killed else 'TGL_NU_M2_TENSION' if current>=3.0 else 'TGL_NU_M2_ARMED_CONSISTENT')
    if verdict not in snapshot['frozen']['allowed_verdicts']:raise ValueError('VERDICT_OUTSIDE_FROZEN_SET')
    return dict(status='FIXTURE_NOT_DATA' if fixture else 'READER_OUTPUT_NOT_REGISTRY_VERDICT',verdict=verdict,
        beta_tgl=beta_tgl,m2_pred_meV=m2_tgl_mev,tensao_atual_sigma=current,escada_datada=ladder,
        grupos_autonomos_5sigma=groups,kill_rule_satisfeita=killed,
        tensao_global_5sigma_sem_2a_determinacao=bool(current>=5.0 and not killed),
        frozen_hash=sha_obj(snapshot['frozen']),dimensional_scale='1 eV [NORM], declared, not fitted or derived here',
        direction='Tension against the declared scale; not evidence in favor',gate_changed=False,
        registry_changed=False,requires_management_reseal=True,
        rule_scope='Exact v315+ executable branch; all supplied determinations, groups deduplicated. MATCHED_PROSPECTIVELY is allowed in frozen text but not emitted by that branch.')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--snapshot',type=Path,default=Path(__file__).with_name('EXTRACTED_RULES.json'))
    parser.add_argument('--snapshot-sha256',required=True)
    parser.add_argument('--release',type=Path);parser.add_argument('--release-sha256');parser.add_argument('--allow-fixtures',action='store_true')
    args=parser.parse_args();snapshot=load_snapshot(args.snapshot,args.snapshot_sha256)
    dets=list(snapshot['legacy_determinations']);provenance=[];fixture=False
    if args.release:
        if not args.release_sha256:raise ValueError('RELEASE_PIN_REQUIRED')
        release,receipt=load_release(args.release,args.release_sha256,args.allow_fixtures)
        dets+=release['determinations'];dets.sort(key=lambda r:r['data']);provenance.append(receipt);fixture=release['fixture']
    result=evaluate(snapshot,dets,fixture);result['provenance']=provenance
    result['legacy_scope']='Values copied from pinned um.py; this run does not independently verify experimental publications'
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
