"""Seal documentary candidate; validate inherited custody without using centres."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from itertools import product
from datetime import datetime, timezone
import json
ROOT=Path(__file__).resolve().parent
J=ROOT.parent
P=J.parent

def digest(p): return sha256(p.read_bytes()).hexdigest()
def put(name,obj):
    p=ROOT/name;b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    if p.exists():
        assert p.read_bytes()==b,'Changed artifact: '+str(p)
    else:
        q=p.with_suffix(p.suffix+'.tmp')
        with q.open('xb') as f:f.write(b)
        assert q.stat().st_size==len(b);q.replace(p)

def main():
    verified=[]
    for man,base in [(P/'UPSTREAM_MANIFEST.json',P/'upstream'),(J/'SOURCES.json',J/'upstream'),(J/'MANIFESTO_ENTREGA.json',J),(ROOT/'PRIMARY_SOURCES.json',ROOT)]:
        m=json.loads(man.read_text(encoding='utf-8'))
        for r in m['files']:
            path=Path(r['path']);path=path if path.is_absolute() else base/path
            assert digest(path)==r['sha256'],str(path)
            verified.append(str(path))
            if 'text_path' in r:
                assert digest(Path(r['text_path']))==r['text_sha256']
                verified.append(r['text_path'])
    e=json.loads((ROOT/'ERROR_COMPONENTS.json').read_text(encoding='utf-8'))
    metadata=json.loads((J/'SELECTION_V01_IDENTIFIERS.json').read_text(encoding='utf-8'))
    keys={r['mas_key'] for r in e['mas_reference_errors']}
    ref_blocks=[]
    for source in ['CCHP','SH0ES']:
        block=[f'{method}_jwst&N4258&{source}' for method in ['ceph','trgb','jagb']]
        assert set(block)<=keys
        ref_blocks.append(block)
    jagb_pair=['jagb_jwst&N4258&CCHP','jagb_jwst&N4258&SH0ES']
    byhost={}
    for r in e['eleven_host_method_rows']:
        if r['method'].split('_')[0] in ['ceph','trgb','jagb']:
            byhost.setdefault(r['host'],set()).add(r['hms_key'])
    host_blocks=[sorted(byhost[h]) for h in sorted(byhost)]
    pair5643=['N5643&jagb_jwst&CCHP','N5643&jagb_jwst&SH0ES']
    assert set(pair5643)<=byhost['N5643']
    flat=[k for block in host_blocks for k in block]
    assert len(flat)==len(set(flat))
    grid=[Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(3,4)]
    points=[list(map(str,t)) for t in product(grid,repeat=4) if t[0]+t[1]<=Fraction(3,4) and t[2]+t[3]<=Fraction(3,4)]
    contract={
      'request_id':'54feb986-d927-4ff9-aa69-3c07680ee78b',
      'status':'DOCUMENTARY_CANDIDATE_NOT_RATIFIED_NOT_EXECUTED',
      'upstream_variant':'V01','upstream_commit':metadata['upstream_commit'],
      'upstream_V01_is_not_preregistration_V1':True,
      'selection':{'path':str(J/'SELECTION_V01_IDENTIFIERS.json'),'sha256':digest(J/'SELECTION_V01_IDENTIFIERS.json')},
      'errors':{'path':str(ROOT/'ERROR_COMPONENTS.json'),'sha256':digest(ROOT/'ERROR_COMPONENTS.json')},
      'family':'C = D0 + A diag(a^2) A.T + B Dm Rm Dm B.T + H Dh Rh Dh H.T',
      'scope':'STELLAR_HOST_BLOCK_ONLY',
      'baseline':'Rm=Rh=I exactly reproduces the reviewed anchor/MAS/HMS construction',
      'primitive_key_order':'use explicit keys; never align groups by guessed positions',
      'latent_cross_MAS_HMS':'not included in this restricted family; physical cross-level effects require Alternative A signed differential Jacobian and budget reallocation',
      'groups':{'MAS_same_program_at_N4258':ref_blocks,'MAS_JAGB_reference_pair':jagb_pair,
                'HMS_by_eleven_hosts':host_blocks,'HMS_N5643_JAGB_pair':pair5643},
      'parameterization':{'Rm':'(1-u-v)I + u E_ref + v E_J',
                          'Rh':'(1-p-q)I + p E_host + q E_5643',
                          'E':'signed rank-one block epsilon epsilon.T within each listed group; identity outside groups; zero between disjoint blocks',
                          'parameters':['u','v','p','q'],'units':'variance fractions, dimensionless',
                          'physical_parameter_status':'SENSITIVITY_CHOICES_NOT_FITTED_TGL_PARAMETERS',
                          'bounds':'u,v,p,q >= 0; u+v <= 1; p+q <= 1'},
      'candidate_grid':{'axis_values':list(map(str,grid)),'interior_sum_ceiling':'3/4',
                        'fraction_tuples_order_u_v_p_q':points,
                        'sign_scenarios':[{'id':'all_same','negative_key_predicate':None},
                          {'id':'cepheid_opposite','negative_key_predicate':'method starts ceph_'},
                          {'id':'SH0ES_JAGB_opposite','negative_key_predicate':'method starts jagb_ AND source equals SH0ES'}],
                        'boundary_sum_one':'diagnostic only; may change rank/support',
                        'not_exhaustive_of_all_PSD_matrices':True,
                        'duplicate_covariance_cases':'collapse duplicates deterministically; do not count as independent evidence'},
      'proofs':{'PSD':'sum of congruences of PSD matrices',
                'marginals':'each row maps to one MAS and one HMS; diag R=1',
                'interior_same_nullspace':'Rm,Rh >= I/4; intersection of nullspaces of unchanged primitive factors equals baseline'},
      'candidate_pair_coefficients_mag2':e['algebraic_coefficient_examples_mag2'],
      'alternatives':[{'id':'A','kind':'primitive joint resampling / signed nuisance Jacobian','executed':False},
                      {'id':'B','kind':'pre-specified PSD sensitivity envelope preserving V01 marginals','executed':False}],
      'published_numeric_residual_three_method_matrix':'NOT_LOCATED_IN_REVIEWED_SOURCES',
      'already_included_do_not_add_again':['N4258 geometric 0.032 mag','MAS 0.05 mag JAGB per source','HMS repeated measurement','shared SN calibrator rows','upstream SN covariance'],
      'nonautomatic_additions':['0.06 mag methodological allowance from expanded JAGB compilation','NIRCam zeropoint before testing host-anchor cancellation','aggregate H0 results'],
      'ratification_required':['A or B selection','groups/signs/grid','robustness report rule','five physical mean models and normalization contract'],
      'guard_required':'reuse existing support/design guard from coordination; no duplicate implementation',
      'centres_used_to_select_family':False,'observed_tables_seen_in_sources':True,
      'no_blinding_claim':True,'S_g_H0_lnB_computed':False,'global_C_assembled':False,
      'upstream_executed':False,'remote_model_calls':0,'new_verdict':None}
    put('CONTRATO_PSD_CANDIDATO.json',contract)
    checks={'source_hash_entries_verified':len(verified),'source_hash_paths_unique':len(set(verified)),
       'V01_host_rows':e['checks']['host_rows'],'primitive_HMS':e['checks']['unique_hms'],
       'hms_errors_equal':e['checks']['all_hms_errors_exactly_equal_within_group'],
       'all_candidate_MAS_keys_present':True,'all_candidate_HMS_keys_present':True,
       'host_blocks_disjoint':True,'grid_parameter_tuples':len(points),'sign_scenarios':3,
       'no_C_assembly_or_fitting':True,'prior_six_artifacts_unchanged':True}
    put('VALIDACAO_DOCUMENTAL.json',checks)
    names=['archive_primary.py','audit_errors.py','seal_documentary.py','PRIMARY_SOURCES.json','ERROR_COMPONENTS.json','REVISAO_RESIDUAIS.md','CONTRATO_PSD_CANDIDATO.json','VALIDACAO_DOCUMENTAL.json']
    artifacts=[{'path':str(ROOT/n),'bytes':(ROOT/n).stat().st_size,'sha256':digest(ROOT/n)} for n in names]
    put('MANIFESTO_ENTREGA.json',{'scope':'RESIDUAL_SYSTEMATICS_DOCUMENTARY_NO_FIT',
       'request_id':contract['request_id'],'files':artifacts,
       'inherited_manifests':[{'path':str(p),'sha256':digest(p)} for p in [P/'UPSTREAM_MANIFEST.json',J/'SOURCES.json',J/'MANIFESTO_ENTREGA.json']],
       'archive_custody':'PRIMARY_SOURCES.json pins raw HTML and derived text separately',
       'memory_and_map':'mutable append-only delivery metadata outside scientific artifact seal'})
    print(json.dumps(checks,indent=2))
    print('report_sha256='+digest(ROOT/'REVISAO_RESIDUAIS.md'))

if __name__=='__main__':main()