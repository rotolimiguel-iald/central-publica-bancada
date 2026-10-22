"""Record the principal's application of the existing GO to exact reviewed bytes.

This document is a declared assessment by the principal, not a human signature.
It does not create a registration, seed, witness or execution activation.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,argparse,os
B=Path(__file__).resolve().parents[1];R=B.parent

def read(p):
    raw=p.read_bytes();return raw,hashlib.sha256(raw).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True)
    ap.add_argument('--expected-candidate-sha256',required=True)
    ap.add_argument('--apply-existing-go-after-reading-reviews',action='store_true');args=ap.parse_args()
    if not args.apply_existing_go_after_reading_reviews:raise ValueError('Principal assessment must be explicit')
    p=(B/'bis'/args.candidate).resolve()
    if not p.is_relative_to(B/'bis'):raise ValueError('Candidate outside bis')
    raw,candidate_pin=read(p);reg=json.loads(raw)
    if candidate_pin!=args.expected_candidate_sha256 or reg['status']!='DRAFT_NOT_REGISTERED__NO_EXECUTION_AUTHORIZATION':raise ValueError('Candidate differs')
    definitions={
      'PE':{'reviewer':'01a0ca1b-47e5-73c3-9c38-e334310b6c8c','builder':'Averroes_and_principal',
        'files':['bis/e4_e5_prepare/PE_R1_R2_R3_CLOSING_REVIEW.md'],
        'sources':['blinding.py','injection_design.py','pe_runner.py','pseob_source.py','remnant_conversion.py','run_controlled.py','strain_io.py','temporal_contract.py']},
      'MAIN':{'reviewer':'01a0cac1-c4c5-7de1-af2e-e0ba93627b41','builder':'principal',
        'files':['bis/e7_prepare/MAIN_CODE_REVIEW_CLOSING_V3.md'],
        'sources':['synthetic_null.py','route_iv_null.py','null_runner.py','null_campaign.py','fetch_registered.py']},
      'E7':{'reviewer':'01a0cac4-d5d0-79c3-85e1-32c4165adaf3','builder':'01a0cac1-c4c5-7de1-af2e-e0ba93627b41',
        'files':['bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V3.md','bis/e2_publication_census/E7_INDEPENDENT_REVIEW_V4.md'],
        'sources':['extrai_posteriores_pseob.py','tgl_ringdown_ampliacao.py']},
      'ACTIVATION':{'reviewer':'01a0cac4-d5d0-79c3-85e1-32c4165adaf3','builder':'principal_and_Averroes',
        'files':['bis/e2_publication_census/E2_SEALER_CLOSING_REVIEW_V2.md'],
        'sources':['registration_guard.py']}}
    reviews={};snapshots={str(p):candidate_pin}
    for role,spec in definitions.items():
        texts=[];pins={};covered={}
        for name in spec['files']:
            raw,pin=read(B/name);pins[name]=pin;snapshots[str(B/name)]=pin;texts.append(raw.decode('utf-8-sig'))
        for name in spec['sources']:
            prefix='bis/e7_prepare/producer/' if role=='E7' else 'bis/e2_code/'
            _,pin=read(B/prefix/name)
            expected=reg['e7']['producer_tree_sha256'][name] if role=='E7' else reg['own_code_tree_sha256'][name]
            if pin!=expected or not any(pin in text for text in texts):raise ValueError('Current source not evidenced by scoped review: '+name)
            covered[prefix+name]=pin;snapshots[str(B/prefix/name)]=pin
        reviews[role]={'status':'BLOCKERS_CLOSED','blocking_findings':[],'reviewer_agent_id':spec['reviewer'],
          'builder_identity':spec['builder'],'identity_statute':'DECLARADO_FROM_AGENT_ASSIGNMENTS_NOT_HUMAN_AUTHENTICATION',
          'files':pins,'covered_source_sha256':covered,
          'remaining_scope':'Physical convergence, coverage, selection normalization and calibration remain OPEN; finite or static closure only'}
        if role=='ACTIVATION':
            helper='ORDEM_013_RINGDOWN/refeito/e2_private_directory.ps1';_,pin=read(R/helper)
            if reg['input_pins_relative_to_Chatgpt'].get(helper)!=pin or not any(pin in text for text in texts):raise ValueError('ACL helper not reviewed/pinned')
            reviews[role]['covered_security_input_sha256']={helper:pin};snapshots[str(R/helper)]=pin
    order=R/'TUNEL/PARA_CHATGPT/ORDEM_013BIS_fechamento_e_ampliacao_dos_eventos_ate_5sigma.md'
    opening=R/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
    sealer=B/'refeito/seal_e2_013bis.py'
    _,order_pin=read(order);_,opening_pin=read(opening);_,sealer_pin=read(sealer)
    for path,pin in [(order,order_pin),(opening,opening_pin),(sealer,sealer_pin)]:snapshots[str(path)]=pin
    found=sorted(p.name for p in (B/'bis').glob('RESULT_E2_NULL*'))
    if found or (B/'cache/E3_PSEOB_PILOT_V1').exists():raise ValueError('Unexpected recorded execution before registration')
    value={'status':'APPLY_EXISTING_GO_TO_REVIEWED_CANDIDATE','created_utc':datetime.now(timezone.utc).isoformat(),
      'principal':'Codex main agent; application of the already authorized order after reading scoped reviews',
      'candidate_sha256':candidate_pin,'sealer_sha256':sealer_pin,'opening_sha256':opening_pin,
      'existing_go':{'relative_to_Chatgpt':order.relative_to(R).as_posix(),'sha256':order_pin,
        'scope':'Order section0/header and E2-E3, 40h maximum, no new human approval required'},
      'reviews':reviews,
      'exposure_declaration':{'statute':'DECLARADO_PRINCIPAL_WITH_SCOPED_CENSUS',
        'statement':'In the recorded agent work, no new blind-event posterior values or blind-event PE have been accessed/executed. This is a scoped principal declaration, not proof of absence outside the recorded work.',
        'incidental_exposure':reg['publication_census']['incidental_exposure'],
        'census_sha256':reg['publication_census']['sha256'],
        'test_event_scope':sorted(k for k,x in reg['test_candidates'].items() if x['eligible'] is True and x['published_deformation_at_registration'] is False),
        'external_unrecorded_exposure':'UNKNOWN','existing_null_result_files':found,
        'raw_seed_or_offsets_in_this_step':False},
      'E4_E5_preexecution_scope':'Principal read deterministic formulas/contract; archived-calibration execution allowed after E2; independent numeric review required before B2 delivery',
      'script_sha256':read(Path(__file__))[1]}
    for name,pin in snapshots.items():
        if read(Path(name))[1]!=pin:raise ValueError('Inputs changed before application publication')
    out=B/'bis/E2_REVIEW_APPLICATION_V1.json';temp=out.with_name(out.name+'.pending')
    data=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    with temp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    if temp.stat().st_size!=len(data):raise OSError('Incomplete application retained')
    os.link(temp,out);temp.unlink()
    print(json.dumps({'status':value['status'],'sha256':read(out)[1],'candidate_sha256':candidate_pin}))

if __name__=='__main__':main()
