"""Finite dummy-metadata fixtures. AST functions only; no main/publication/science."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
from types import SimpleNamespace
import ast,copy,hashlib,json,os

HERE=Path(__file__).resolve().parent
OUT=HERE/'fixtures_v2_001'
CASES=[]


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    raw=value if isinstance(value,bytes) else (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>25_000_000:raise ValueError('Fixture size')
    with p.open('xb') as f:f.write(raw)
    return dict(path=p.relative_to(OUT).as_posix(),sha256=digest(p))


def namespace():
    tree=ast.parse((HERE/'generate_reach_table.py').read_bytes())
    names={'LIMIT','ROUTES','GROUPS','METRICS','GATE_FIELDS','STAGES','PAID_FLAGS','FUTURE_GROUPS','EVIDENCE_VERDICTS','SEMANTIC_UNITS'}
    nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or
           isinstance(n,ast.FunctionDef) and n.name not in ('main','write_new','render') or
           isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id in names for t in n.targets)]
    ns={'__name__':'finite_ast_only'}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(HERE/'generate_reach_table.py'),'exec'),ns)
    ns.update(ROOT=OUT,BASE=OUT/'ORDEM_DUMMY',HERE=OUT/'ORDEM_DUMMY/bis/prepare_v2')
    return ns


def probe(name,reject,call):
    error=None;result=None
    try:result=call()
    except Exception as e:error=type(e).__name__+': '+str(e)
    CASES.append(dict(id=name,expected_rejection=reject,rejected=error is not None,
                      passed=(error is not None)==reject,error=error,result=result))


def main():
    if OUT.exists():raise FileExistsError('Preserve prior fixtures')
    OUT.mkdir();n=namespace();contract=json.loads((HERE/'CONTRACT.json').read_bytes())
    ph=n['HERE'];reg=dict(status='REGISTERED_NONBLIND_DESIGN_FOR_BLIND_TEST',registered_utc='2020-01-01T00:00:00Z',
        readings=contract['readings'],witness_relative_to_Chatgpt='TUNEL/DO_CHATGPT/DUMMY.md',
        activation={'receipt_relative_to_Chatgpt':'ORDEM_DUMMY/activation.json','review_application_sha256':hashlib.sha256(b'fake').hexdigest()})
    regref=write(n['BASE']/'RINGDOWN_5SIGMA_V1.json',reg)
    witness=write(OUT/reg['witness_relative_to_Chatgpt'],('registro_sha256: '+regref['sha256']+'\n').encode())
    activation=write(OUT/reg['activation']['receipt_relative_to_Chatgpt'],dict(status='E2_ACTIVATION_COMPLETE',
        registration_sha256=regref['sha256'],witness_sha256=witness['sha256'],
        review_application_sha256=reg['activation']['review_application_sha256'],finished_utc='2020-01-01T00:10:00Z'))
    for name in ('generate_reach_table.py','CONTRACT.json','OUTPUT_SCHEMA.json'):write(ph/name,(HERE/name).read_bytes())
    write(ph/'SOURCE_PINS.json',{'sources':{'E2':regref,'E2_ACTIVATION':activation}})
    package={name:digest(ph/name) for name in ('generate_reach_table.py','CONTRACT.json','OUTPUT_SCHEMA.json','SOURCE_PINS.json')}
    stamp=lambda minute:(datetime(2020,1,1,tzinfo=timezone.utc)+timedelta(minutes=minute)).isoformat()

    def activation_case(label,change=None,wall=False):
        stages={};previous=activation;previdence=activation
        for i,stage in enumerate(n['STAGES']):
            start=20+20*i
            evidence=dict(authorized=stamp(start-1),started=stamp(start),finished=stamp(start+1),
                          recorded=stamp(start),reason='DUMMY_WALL_ONLY',predecessor_sha256=previdence['sha256'])
            timeline=dict(kind='NO_EXECUTION' if wall else ('ALLOCATION_REGISTERED' if stage=='E3.2' else 'EXECUTED'),
                authorized_utc_pointer='/authorized',started_utc_pointer='/started',finished_utc_pointer='/finished',
                recorded_utc_pointer='/recorded',reason_pointer='/reason',predecessor_evidence_sha256_pointer='/predecessor_sha256')
            receipt=dict(schema='E6_REVIEWED_STAGE_V2',stage=stage,registration_sha256=regref['sha256'],
                outcome='BLOCKED' if wall else 'COMPLETED',issued_utc=stamp(start+5),bindings=[],predecessor=copy.deepcopy(previous))
            if change:change(stage,evidence,timeline,receipt)
            d=OUT/label/stage;artifact=write(d/'artifact.json',evidence);timeline['evidence']=artifact
            receipt.update(artifact=artifact,timeline=timeline)
            review=dict(status='ACCEPTED_FOR_E6_MAPPING',stage=stage,registration_sha256=regref['sha256'],
                artifact_sha256=artifact['sha256'],blocking_findings=[],reviewed_utc=receipt['issued_utc'],bindings=[],
                outcome=receipt['outcome'],reviewer='DUMMY_INDEPENDENT_REVIEWER',timeline=timeline,predecessor=receipt['predecessor'])
            receipt['review']=write(d/'review.json',review)
            previous=write(d/'receipt.json',receipt);previdence=artifact;stages[stage]=previous
        auth=dict(status='AUTHORIZED_E6_ASSEMBLY_AFTER_REVIEWED_E3_AND_TEST',new_scientific_computation_allowed=False,
            package_sha256=package,registration=regref,witness=witness,issued_utc=stamp(100),reviewed_stages=stages,run_id='dummy_'+label)
        p=OUT/label/'authorization.json';ref=write(p,auth)
        n['activate'](SimpleNamespace(execute=True,authorization=p,authorization_sha256=ref['sha256']))
        return 'Dummy activate only; no assembly/publication'

    probe('valid_actual_sequence',False,lambda:activation_case('valid'))
    probe('stage_before_E2_activation',True,lambda:activation_case('early',lambda s,e,t,r:(e.update(started=stamp(4),finished=stamp(5),authorized=stamp(3)),r.update(issued_utc=stamp(6))) if s=='E3.2' else None))
    probe('TEST_before_allocation_and_calibration',True,lambda:activation_case('reversed',lambda s,e,t,r:e.update(started=stamp(15),finished=stamp(16),authorized=stamp(14)) if s=='TEST' else None))
    probe('wrong_receipt_predecessor_hash',True,lambda:activation_case('pred',lambda s,e,t,r:r['predecessor'].update(sha256='0'*64) if s=='E3.3' else None))
    probe('wrong_actual_evidence_predecessor_hash',True,lambda:activation_case('sourcepred',lambda s,e,t,r:e.update(predecessor_sha256='0'*64) if s=='TEST' else None))
    probe('receipt_dates_cannot_hide_reversed_activity',True,lambda:activation_case('receiptmask',lambda s,e,t,r:e.update(started=stamp(12),finished=stamp(13),authorized=stamp(11)) if s=='E3.3' else None))
    probe('future_actual_time',True,lambda:activation_case('future',lambda s,e,t,r:e.update(finished='2100-01-01T00:00:00Z') if s=='TEST' else None))
    probe('naive_actual_time',True,lambda:activation_case('naive',lambda s,e,t,r:e.update(started='2020-01-01T00:20:00') if s=='E3.2' else None))
    probe('malformed_actual_time',True,lambda:activation_case('malformed',lambda s,e,t,r:e.update(finished='INVALID') if s=='TEST' else None))
    probe('authorization_after_activity',True,lambda:activation_case('lateauth',lambda s,e,t,r:e.update(authorized=stamp(80)) if s=='TEST' else None))
    probe('existing_GO_before_E2_allowed',False,lambda:activation_case('priorgo',lambda s,e,t,r:e.update(authorized=stamp(-60))))
    probe('retrospective_adapter_truthful_dates',False,lambda:activation_case('adapterlate',lambda s,e,t,r:r.update(issued_utc=stamp(80+n['STAGES'].index(s)))))
    probe('blocked_no_execution_walls_preserved',False,lambda:activation_case('walls',wall=True))
    probe('partial_no_execution_walls_preserved',False,lambda:activation_case('partialwalls',lambda s,e,t,r:r.update(outcome='PARTIAL'),wall=True))
    probe('unavailable_no_execution_walls_preserved',False,lambda:activation_case('unavailable',lambda s,e,t,r:r.update(outcome='UNAVAILABLE'),wall=True))
    probe('completed_without_execution_refused',True,lambda:activation_case('fakecomplete',lambda s,e,t,r:r.update(outcome='COMPLETED'),wall=True))
    probe('wall_without_reason_refused',True,lambda:activation_case('noreason',lambda s,e,t,r:e.update(reason=''),wall=True))
    probe('execution_after_missing_allocation_refused',True,lambda:activation_case('noallocation',lambda s,e,t,r:(t.update(kind='NO_EXECUTION'),r.update(outcome='UNAVAILABLE')) if s=='E3.2' else None))

    def binding_case(route='TAU220_POPULATION',group='O4_CEGO',color='green',data=True,verdict='NOT_FALSIFIED_POWERED',
                     physical=True,ratio=None,cal_ratio=None,paid=True,partial=False,units=None,metric=None,power='INSUFFICIENT_REVIEWED',wrongcal=False):
        key=(route,'R-B',group);cells={key:{'scenarios':[]}};sources={};stages={}
        valid=n['SEMANTIC_UNITS'][route]
        gate=dict(color=color,status='DUMMY_NOT_SCIENCE',decision_reviewed=True,**{k:paid for k in n['PAID_FLAGS']},
            **{k:None for k in n['GATE_FIELDS']},units={k:(valid[k][0] if valid[k] else 'INAPPLICABLE') for k in n['GATE_FIELDS']})
        if route=='DF220_POPULATION_WIDTH_IV':gate.update(sigma_sys_df=0.001,sigma_jit_recovered=0.01)
        else:gate.update(sigma_c_calibrated=0.001,floor5_INPUT=0.01,floor15_sensitivity=0.003)
        if units:gate['units'].update(units)
        summary=dict(verdict=verdict,test_data_present=data,unblinding_authorized=True,population_checks_passed=True,
            decision_rule_paid=True,reading_multiplicity_paid=True,relative_exclusion_rule_paid=True,power_assessment=power)
        for stage in n['STAGES']:
            ref=dict(path='DUMMY_'+stage+'.json',sha256=hashlib.sha256(stage.encode()).hexdigest())
            obj=dict(gate=copy.deepcopy(gate),summary=summary,value=0.2,conditional=6.0)
            obj['gate']['correction_over_sigma_physical']=ratio if stage=='TEST' else cal_ratio
            bindings=[]
            if stage!='E3.2':
                b=dict(route=route,reading='R-B',data_group=group,scenario_id='dummy',scope='DUMMY_CONDITIONAL',metrics={},gate_pointer='/gate')
                if stage=='TEST':
                    b.update(test_summary_pointer='/summary',calibration_scenario_id='dummy',calibration_receipt_sha256=stages['E3.3'][1]['sha256'])
                    if wrongcal:b['calibration_receipt_sha256']='0'*64
                    if physical:b['metrics']['z_physical']={'pointer':'/value','unit':'dimensionless'}
                    if metric:
                        field,unit=metric;b['metrics'][field]={'pointer':'/conditional','unit':unit}
                bindings=[b]
            stages[stage]=(dict(bindings=bindings,outcome='PARTIAL' if partial else 'COMPLETED',review=ref,artifact=ref),ref)
            sources['STAGE_'+stage]=(ref,obj)
        n['append_reviewed'](cells,sources,stages,contract['readings'],contract['permitted_verdicts'])
        return dict(verdict=cells[key]['scenarios'][-1]['verdict'],physical_z=cells[key]['scenarios'][-1]['metrics']['z_physical']['value'])

    probe('valid_tau220',False,lambda:binding_case())
    probe('valid_tau440',False,lambda:binding_case(route='TAU440_FIXED_SOURCE_FISHER'))
    probe('valid_df_width_IV',False,lambda:binding_case(route='DF220_POPULATION_WIDTH_IV'))
    probe('red_gate_physical_ratio',True,lambda:binding_case(color='red',physical=False,ratio=6,verdict='INCONCLUSIVE_SYSTEMATICS'))
    probe('red_calibration_physical_ratio',True,lambda:binding_case(color='red',physical=False,cal_ratio=6,verdict='INCONCLUSIVE_SYSTEMATICS'))
    probe('green_calibration_physical_ratio',True,lambda:binding_case(physical=False,cal_ratio=6))
    probe('valid_TEST_physical_ratio_only',False,lambda:binding_case(physical=False,ratio=0.2))
    probe('unpaid_partial_NOT_FALSIFIED_UNDERPOWERED',True,lambda:binding_case(physical=False,verdict='NOT_FALSIFIED_UNDERPOWERED',paid=False,partial=True))
    probe('valid_underpowered_z_below5',False,lambda:binding_case(verdict='NOT_FALSIFIED_UNDERPOWERED'))
    probe('valid_underpowered_without_physical_number',False,lambda:binding_case(verdict='NOT_FALSIFIED_UNDERPOWERED',physical=False))
    probe('underpowered_missing_reviewed_power_status',True,lambda:binding_case(verdict='NOT_FALSIFIED_UNDERPOWERED',power='OPEN'))
    probe('wrong_calibration_receipt',True,lambda:binding_case(wrongcal=True))
    probe('partial_physical_result',True,lambda:binding_case(partial=True))
    probe('unpaid_physical_result',True,lambda:binding_case(paid=False))
    probe('red_z_physical',True,lambda:binding_case(color='red'))
    probe('green_tau_gate_in_Hz',True,lambda:binding_case(units={'sigma_c_calibrated':'Hz','floor5_INPUT':'Hz'}))
    probe('cross_mode_440_gate_in_220_units',True,lambda:binding_case(route='TAU440_FIXED_SOURCE_FISHER',units={'sigma_c_calibrated':'fractional_dtau220'}))
    probe('IV_width_as_tau',True,lambda:binding_case(route='DF220_POPULATION_WIDTH_IV',units={'sigma_sys_df':'fractional_dtau220'}))
    probe('IV_width_as_fraction_without_width_type',True,lambda:binding_case(route='DF220_POPULATION_WIDTH_IV',units={'sigma_sys_df':'fractional_df220'}))
    probe('count_not_information',True,lambda:binding_case(metric=('N90_information_target','event_count')))
    probe('information_not_count',True,lambda:binding_case(metric=('N90_count_scenario','sum_inverse_variance_dtau')))
    probe('equivalents_channel_mismatch',True,lambda:binding_case(metric=('GW250114_equivalents','current_df_variance_information_equivalents')))
    probe('rate_wrong_time_base',True,lambda:binding_case(metric=('rate_per_year','per_second')))
    probe('z_in_Hz',True,lambda:binding_case(metric=('z_physical','Hz')))
    for group in n['FUTURE_GROUPS']:
        probe('future_'+group+'_physical_test',True,lambda g=group:binding_case(group=g))
        probe('future_'+group+'_conditional_projection',False,lambda g=group:binding_case(group=g,color='OPEN',data=False,physical=False,
              verdict='AWAITING_DATA',metric=('correction_over_sigma','dimensionless')))
    probe('future_ET_physical_test',True,lambda:binding_case(group='ET'))
    probe('red_data_AWAITING_DATA',True,lambda:binding_case(color='red',physical=False,verdict='AWAITING_DATA'))
    probe('open_data_AWAITING_DATA',True,lambda:binding_case(color='OPEN',physical=False,verdict='AWAITING_DATA'))
    probe('red_data_INCONCLUSIVE',False,lambda:binding_case(color='red',physical=False,verdict='INCONCLUSIVE_SYSTEMATICS'))
    probe('red_conditional_diagnostic_allowed',False,lambda:binding_case(color='red',physical=False,verdict='INCONCLUSIVE_SYSTEMATICS',metric=('correction_over_sigma','dimensionless')))
    probe('no_data_OPEN',False,lambda:binding_case(color='OPEN',data=False,physical=False,verdict='AWAITING_DATA'))
    probe('no_data_falsified',True,lambda:binding_case(data=False,physical=False,verdict='FALSIFIED_IN_READING'))
    dummy_ref={'path':'DUMMY.json','sha256':hashlib.sha256(b'DUMMY').hexdigest()}
    dummy={'E0':(dummy_ref,dict(planning_targets=[],all_calibration_combinations={},conditional_rates_scenarios={'forecasts':[],'rates':[]},
                              threeG_fixed_anchor_calculations=[],systematic_conditions=[])),
           'E4_RESULT':(dummy_ref,dict(E4_fisher=[],E5_information=[])),'E2':(dummy_ref,{'route_IV':{'targets':[]}})}
    grid=n['assemble_baselines'](contract,dummy)
    CASES.append(dict(id='empty_dummy_grid_180',passed=len(grid)==180 and len({k[1] for k in grid})==10,
                      expected_rejection=False,rejected=False,error=None,result={'cells':len(grid)}))
    result=dict(status='FINITE_METADATA_FIXTURES_V2',created_utc=datetime.now(timezone.utc).isoformat(),
        cases=CASES,total=len(CASES),passed=sum(c['passed'] for c in CASES),negative_accepted=[c['id'] for c in CASES if c.get('expected_rejection') and not c.get('rejected')],
        failures=[c['id'] for c in CASES if not c['passed']],generator_sha256=digest(HERE/'generate_reach_table.py'),
        fixture_script_sha256=digest(Path(__file__)),producer_main_called=False,real_scientific_baselines_assembled=False,
        actual_E6_executed=False,actual_authorization_created=False,physical_numbers='DUMMY_ONLY',
        limitation='Metadata unit/guard fixtures, not independent closing review or proof of real receipt chronology')
    raw=(json.dumps(result,indent=2)+'\n').encode()
    with (HERE/'FIXTURE_RESULTS_V2_001.json').open('xb') as f:f.write(raw)
    print(json.dumps({k:result[k] for k in ('total','passed','negative_accepted','failures')}))


if __name__=='__main__':main()
