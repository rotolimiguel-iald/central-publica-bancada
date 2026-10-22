"""Q02 controller graph PREPARATION ONLY. CLI always denies execution.

No scientific import, file write, claim, or model call occurs on module import.
Future run_once requires original ROOT decision bytes, pinned inputs and a real
qualified supervisor implementation. This module does not supply that runtime.
"""
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import sys
import time
import types

PREPARATION_ID='39f88c04-76b0-44dd-bf6f-11f937048fa9'
SCENARIO_FIELDS=('scenario_id','consumer_admission','backend_receipt','structure','row_ids',
                 'y_native','C_native','affine_origin_native','theta_plan','coupling_template')
GLOBAL_FIELDS=('engine_configuration','assembly_admission','runtime_inventory',
               'resource_plan','loaded_objects_receipt','guard_contract','scenario_manifest')
MODULE_ROLES=('theta','node','durable','assembler','consumer','prior','precision',
              'profile','linear','support','engine')
CONSUMED_SCOPES=('c4359a48-bf7c-4dd5-a753-8c3413774cdf','ffd6ccba-cd70-4747-aceb-a10003dfb7f4',
                 PREPARATION_ID,'99e2bfa7-36b8-4e0f-92e7-1a6918e80591')


class ControllerError(RuntimeError):
    pass

def need(ok, reason):
    if not ok: raise ControllerError(reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(obj):
    return json.dumps(obj,sort_keys=True,ensure_ascii=True,separators=(',', ':'),allow_nan=False).encode()

def pairs(items):
    result={}
    for key,value in items:
        need(key not in result,'DUPLICATE_JSON_KEY');result[key]=value
    return result

def invalid_constant(_):
    raise ControllerError('NONFINITE_JSON')

def document(raw):
    need(type(raw) is bytes and raw,'NONEMPTY_BYTES_REQUIRED')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=invalid_constant)

def keys(obj, fields):
    need(type(obj) is dict and set(obj)==set(fields),'EXACT_SCHEMA_REQUIRED')

def ref(identifier, raw):
    return {'id':identifier,'sha256':sha(raw)}

def positive(x, name):
    need(type(x) in (int,float) and math.isfinite(x) and x>0,'POSITIVE_RESOURCE_'+name)

def pin(raw, expected):
    need(type(raw) is bytes and len(raw)==expected['bytes'] and sha(raw)==expected['sha256'],
         'PINNED_BYTES_MISMATCH')


def _preparation(manifest_sha256):
    folder=Path(__file__).resolve().parent
    raw=(folder/'MANIFESTO_PREPARACAO.json').read_bytes()
    need(sha(raw)==manifest_sha256,'PREPARATION_MANIFEST_CHANGED')
    manifest=document(raw)
    need(manifest['request_id']==PREPARATION_ID,'PREPARATION_ID_CHANGED')
    for item in manifest['files']:
        name=item['name']
        need(type(name) is str and Path(name).name==name,'MANIFEST_MEMBER_NAME')
        pin((folder/name).read_bytes(),item)
    return document((folder/'SOURCE_PINS.json').read_bytes())


def _verify_bindings(bindings, source_pins, artifacts, supervisor, adapter_pin):
    expected=set(MODULE_ROLES)|{'numpy','camb','supplier','supervisor_port'}
    keys(bindings,expected)
    for role in MODULE_ROLES:
        module=bindings[role]
        need(type(module) is types.ModuleType,'MODULE_REQUIRED_'+role)
        pin(Path(module.__file__).read_bytes(),source_pins[role])
    for role in ('supplier','supervisor_port'):
        module=bindings[role]
        need(type(module) is types.ModuleType,'MODULE_REQUIRED_'+role)
        filename={'supplier':'background_supplier.py','supervisor_port':'supervisor_port.py'}[role]
        need(Path(module.__file__).read_bytes()==(Path(__file__).resolve().parent/filename).read_bytes(),
             'LOCAL_BINDING_SOURCE_CHANGED_'+role)
    need(isinstance(supervisor,bindings['supervisor_port'].QualifiedSupervisor),
         'CONCRETE_QUALIFIED_SUPERVISOR_REQUIRED')
    implementation=sys.modules.get(type(supervisor).__module__)
    need(type(implementation) is types.ModuleType and getattr(implementation,'__file__',None),
         'SUPERVISOR_IMPLEMENTATION_SOURCE_REQUIRED')
    pin(Path(implementation.__file__).read_bytes(),adapter_pin)
    need(bindings['linear'].SupportGaussian is bindings['support'].SupportGaussian,
         'GAUSSIAN_BACKEND_SUPPORT_BINDING')
    need(bindings['linear'].np is bindings['numpy'] and bindings['support'].np is bindings['numpy'] and
         sys.modules.get('numpy') is bindings['numpy'] and sys.modules.get('camb') is bindings['camb'],
         'NATIVE_MODULE_BINDING')
    # Source-file hashes alone are not proof of loaded function identity. The
    # supervisor's mandatory admit() performs the actual loaded-object review.
    engine_dir=Path(bindings['engine'].__file__).resolve().parent
    pin((engine_dir/'RUNTIME_METADATA.json').read_bytes(),source_pins['engine_runtime'])
    for role in source_pins:
        pin(artifacts['source:'+role],source_pins[role])


def _grid(configuration, plans, theta, template):
    # New metadata/points/resources are allowed; all scientific configuration
    # fields of the pinned reference configuration remain exact.
    mutable={'request_id','status','created_utc','points','point_selection','resources','next_authority'}
    need(set(configuration)==set(template),'CONFIGURATION_FIELDS')
    for name in set(template)-mutable:
        need(configuration[name]==template[name],'SCIENTIFIC_CONFIGURATION_CHANGED_'+name)
    first,last=plans[0]['first_level'],plans[0]['last_level']
    need(type(first) is int and type(last) is int and 1<=first<last<=theta.MAX_LEVEL,'GRID_LEVELS')
    need(all(p['first_level']==first and p['last_level']==last for p in plans),'SCENARIO_GRID_CHANGED')
    denominator=1<<last
    points=[]
    for indices in itertools.product(range(denominator+1),repeat=3):
        node=theta._node_key(indices,denominator)
        identifier='grid_'+'_'.join(str(x) for x in node[:3])+'_over_'+str(node[3])
        points.append({'id':identifier,'theta':list(theta._theta(node))})
    need(configuration['points']==points,'FULL_FINEST_GRID_REQUIRED_NO_SUBSET')
    need(configuration['prior']['coordinates']==list(theta.THETA_NAMES) and
         [configuration['prior']['bounds'][k] for k in theta.THETA_NAMES]==[list(v) for v in theta.BOUNDS],
         'ORIGINAL_PRIOR_BOX_REQUIRED')
    return len(points)


def run_once(*, request_json, request_sha256, decision_json, decision_sha256,
             artifacts, bindings, supervisor):
    """Future API; no default artifacts, modules, decision, supervisor or budgets.

    All arrays are explicit raw f64le bytes in artifacts. Loading/admission takes
    place under the future supervisor. Does not write canonical sources. A failed
    or already-claimed global unit is never restarted, even if its store is moved.
    ROOT/supervisor must bind protected store paths against alternate-root replay.
    """
    need(sha(request_json)==request_sha256 and sha(decision_json)==decision_sha256,'REQUEST_OR_DECISION_PIN')
    request,decision=document(request_json),document(decision_json)
    keys(request,('schema','preparation_request_id','execution_unit_id','artifact_pins',
                  'global_artifacts','scenarios','store_root','run_store_root','family_scope'))
    keys(decision,('schema','preparation_request_id','execution_unit_id','preparation_manifest_sha256',
                   'request_sha256','authorize_single_execution','scope','may_read_observations',
                   'supervisor_adapter_pin','independent_review_reference'))
    need(request['schema']=='F9_CONTROLLER_REQUEST_V1' and decision['schema']=='F9_CONTROLLER_ROOT_DECISION_V1'
         and request['preparation_request_id']==decision['preparation_request_id']==PREPARATION_ID,
         'CONTROLLER_SCHEMA_ID')
    unit=request['execution_unit_id']
    need(type(unit) is str and 0<len(unit)<=128 and unit not in CONSUMED_SCOPES and
         decision['execution_unit_id']==unit and decision['request_sha256']==request_sha256 and
         decision['authorize_single_execution'] is True and
         decision['scope']=='F9_FULL_PRIOR_ENGINEERING_ONLY','SPECIFIC_ROOT_DECISION_REQUIRED')
    need(type(decision['may_read_observations']) is bool,'EXPLICIT_DATA_RELEASE_REQUIRED')
    need(request['family_scope']=='EXACT_DECLARED_SCENARIOS_NOT_UNIVERSAL','FAMILY_SCOPE')
    keys(request['global_artifacts'],GLOBAL_FIELDS)
    keys(artifacts,request['artifact_pins'])
    for name,expected in request['artifact_pins'].items():pin(artifacts[name],expected)
    keys(decision['independent_review_reference'],('id','sha256'))
    need(any(sha(value)==decision['independent_review_reference']['sha256'] for value in artifacts.values()),
         'INDEPENDENT_REVIEW_BYTES_MISSING')
    source_pins=_preparation(decision['preparation_manifest_sha256'])
    _verify_bindings(bindings,source_pins,artifacts,supervisor,decision['supervisor_adapter_pin'])
    get=lambda role:artifacts[request['global_artifacts'][role]]
    resources=document(get('resource_plan'))
    keys(resources,('schema','status','max_callback_calls','max_solver_calls','nominal_wall_seconds',
                    'nominal_native_call_seconds','max_record_bytes','nominal_memory_bytes',
                    'nominal_store_bytes','threads','workers_parallel','automatic_retries'))
    need(resources['schema']=='F9_CONTROLLER_RESOURCE_INPUT_V1' and resources['status']=='INPUT_NOT_MEASURED',
         'RESOURCE_INPUT_NOT_BENCHMARK')
    for name in ('max_callback_calls','max_solver_calls','max_record_bytes','nominal_memory_bytes','nominal_store_bytes'):
        need(type(resources[name]) is int and resources[name]>0,'RESOURCE_INTEGER_'+name)
    for name in ('nominal_wall_seconds','nominal_native_call_seconds'):positive(resources[name],name)
    need(resources['threads']==resources['workers_parallel']==1 and resources['automatic_retries']==0,
         'SERIAL_NO_RETRY_REQUIRED')
    need(resources['nominal_native_call_seconds']<=resources['nominal_wall_seconds'],'DEADLINE_ORDER')
    scenario_specs=request['scenarios']
    need(type(scenario_specs) is list and scenario_specs,'NONEMPTY_SCENARIO_LIST')
    for spec in scenario_specs:keys(spec,SCENARIO_FIELDS)
    scenario_ids=[s['scenario_id'] for s in scenario_specs]
    need(all(type(x) is str and 0<len(x)<=128 for x in scenario_ids) and len(set(scenario_ids))==len(scenario_ids),
         'UNIQUE_SCENARIOS')
    scenario_manifest=document(get('scenario_manifest'))
    need(scenario_manifest['ordered_scenario_ids']==scenario_ids,'EXACT_DECLARED_FAMILY_REQUIRED')
    plans=[document(artifacts[s['theta_plan']]) for s in scenario_specs]
    need(len({p['common_measure_id'] for p in plans})==1,'COMMON_NUISANCE_MEASURE_ACROSS_SCENARIOS')
    configuration=document(get('engine_configuration'))
    required_nodes=_grid(configuration,plans,bindings['theta'],document(artifacts['source:configuration_template']))
    need(resources['max_callback_calls']>=required_nodes*len(scenario_specs) and
         resources['max_solver_calls']>=required_nodes,'COLD_CACHE_FULL_GRID_BUDGET_REQUIRED')
    background_scope=unit+':background'
    need(configuration['request_id']==background_scope,'BACKGROUND_SCOPE')
    cr=configuration['resources']
    need(cr['threads']==cr['profiles']==cr['workers_parallel']==1 and cr['automatic_retries']==0 and
         cr['points']==required_nodes and cr['max_solver_calls']==resources['max_solver_calls'] and
         cr['timeout_seconds_per_worker']==resources['nominal_native_call_seconds'] and
         cr['total_timeout_seconds']==resources['nominal_wall_seconds'],'CONFIGURATION_RESOURCE_BINDING')
    runtime_sha=sha(get('runtime_inventory'))
    assembly_sha=sha(get('assembly_admission')); config_sha=sha(get('engine_configuration'))
    own_raw=Path(__file__).read_bytes()
    supplier_raw=(Path(__file__).resolve().parent/'background_supplier.py').read_bytes()
    decision_reference=ref(unit+':root-decision',decision_json)
    resource_reference=ref(unit+':resources',get('resource_plan'))
    loaded_reference=ref(unit+':loaded-objects',get('loaded_objects_receipt'))
    supplier_reference=ref(PREPARATION_ID+':background-supplier',supplier_raw)
    prepared_specs=[]
    for spec,plan in zip(scenario_specs,plans):
        raw=lambda field:artifacts[spec[field]]
        consumer_doc=document(raw('consumer_admission'))
        need(consumer_doc['scenario_id']==spec['scenario_id'],'CONSUMER_SCENARIO')
        need(consumer_doc['data_kind'] in ('SYNTHETIC','OPERATOR_RELEASED_OBSERVATIONS'),'DATA_KIND')
        need(consumer_doc['data_kind']=='SYNTHETIC' or decision['may_read_observations'] is True,
             'OBSERVED_RELEASE_NOT_AUTHORIZED')
        # Operator release/V1 references must be backed by bytes, then actually
        # checked by supervisor.admit; a reference/flag alone is not authority.
        for reference in consumer_doc['references'].values():
            need(any(sha(value)==reference['sha256'] for value in artifacts.values()),'REFERENCE_BYTES_MISSING')
        need(plan['execution_unit_id']==unit+':'+spec['scenario_id'] and
             plan['consumer_admission_sha256']==sha(raw('consumer_admission')) and
             plan['assembly_admission_sha256']==assembly_sha and
             plan['engine_configuration_sha256']==config_sha and
             consumer_doc['prediction_admission_sha256']==assembly_sha,'SCENARIO_PLAN_BINDING')
        need(plan['controller_reference']==ref(PREPARATION_ID+':controller',own_raw) and
             plan['callback_reference']=={'id':bindings['node'].REQUEST_ID+':durable-callback',
                                        'sha256':source_pins['durable']['sha256']},'CONTROLLER_CALLBACK_BINDING')
        template=document(raw('coupling_template'))
        need('external_execution_authorization_reference' not in template,'NO_CIRCULAR_AUTHORIZATION_PIN')
        admission={**template,'external_execution_authorization_reference':decision_reference}
        need(admission['preparation_request_id']==bindings['node'].REQUEST_ID and
             admission['theta_plan_sha256']==sha(raw('theta_plan')) and
             admission['runtime_sha256']==runtime_sha and
             admission['background_scope_id']==background_scope and
             admission['supplier_reference']==supplier_reference and
             admission['loaded_objects_reference']==loaded_reference and
             admission['resource_limits_reference']==resource_reference,'COUPLING_TEMPLATE_BINDING')
        # Theta constructor is in-memory schema validation; callback never called.
        bindings['theta'].ThetaIntegrator(raw('theta_plan'),plan_sha256=sha(raw('theta_plan')),
                                          evaluate_node=lambda _: (_ for _ in ()).throw(ControllerError('PREFLIGHT_ONLY')))
        prepared_specs.append((spec,canonical(admission),consumer_doc))
    need(os.name=='posix','POSIX_DURABLE_STORE_REQUIRED')
    need(Path(request['store_root']).is_absolute() and Path(request['run_store_root']).is_absolute() and
         Path(request['store_root']).resolve()!=Path(request['run_store_root']).resolve(),'SEPARATE_PROTECTED_STORE_ROOTS')
    # Concrete external authority/enforcement; abstract port raises by default.
    need(supervisor.admit(request_json=request_json,decision_json=decision_json,
            guard_contract_json=get('guard_contract'),resources_json=get('resource_plan'),
            runtime_inventory_json=get('runtime_inventory'),artifacts=artifacts,bindings=bindings) is None,
         'SUPERVISOR_MUST_CHECK_OR_RAISE')
    store=bindings['durable'].DurableStore(request['store_root'],max_record_bytes=resources['max_record_bytes'])
    runs=bindings['durable'].DurableStore(request['run_store_root'],max_record_bytes=resources['max_record_bytes'])
    run_identity={'schema':'F9_CONTROLLER_RUN_IDENTITY_V1','execution_unit_id':unit,
                  'request_sha256':request_sha256,'decision_sha256':decision_sha256}
    run_key=sha(canonical({'controller_execution_unit_id':unit}))
    ticket=runs.acquire('node',run_key,run_identity)
    need(ticket['created'],'GLOBAL_UNIT_ALREADY_CONSUMED_READ_RECEIPTS_ONLY')
    started=time.monotonic(); callback_attempts=callback_returns=0
    supplier=None;results=[];coupling_documents={}
    def checkpoint(phase, context):
        need(time.monotonic()-started<=resources['nominal_wall_seconds'],'NOMINAL_WALL_EXCEEDED')
        need(supervisor.checkpoint(phase,{'execution_unit_id':unit,'request_sha256':request_sha256,
              'decision_sha256':decision_sha256,'elapsed_s':time.monotonic()-started,**context}) is None,
             'SUPERVISOR_MUST_CHECK_OR_RAISE')
    try:
        supplier=bindings['supplier'].ExistingEngineSupplier(configuration_json=get('engine_configuration'),
            runtime_sha256=runtime_sha,scope_id=background_scope,engine_module=bindings['engine'],
            camb_module=bindings['camb'],assembler_module=bindings['assembler'],supervisor=supervisor,
            required_references={'supplier_reference':supplier_reference,
                'external_execution_authorization_reference':decision_reference,
                'resource_limits_reference':resource_reference,'loaded_objects_reference':loaded_reference},
            max_solver_calls=resources['max_solver_calls'],nominal_call_seconds=resources['nominal_native_call_seconds'],
            checkpoint=checkpoint)
        for index,(spec,coupling_raw,consumer_doc) in enumerate(prepared_specs):
            raw=lambda field:artifacts[spec[field]]
            checkpoint('BEFORE_PREPARE_JOINT',{'scenario_id':spec['scenario_id']})
            joint=bindings['consumer'].prepare_joint(raw('y_native'),raw('C_native'),raw('row_ids'),
                affine_origin_native=raw('affine_origin_native'),structure_json=raw('structure'),
                admission_json=raw('consumer_admission'),admission_sha256=sha(raw('consumer_admission')),
                backend_receipt_json=raw('backend_receipt'),numpy_module=bindings['numpy'],
                flat_gaussian_class=bindings['linear'].FlatNuisanceGaussian)
            context=bindings['node'].NodeContext(joint,admission_json=coupling_raw,admission_sha256=sha(coupling_raw),
                theta_plan_json=raw('theta_plan'),theta_plan_sha256=sha(raw('theta_plan')),
                assembly_admission_json=get('assembly_admission'),design_json=artifacts['source:design'],
                layout_json=artifacts['source:layout'],assembler_module=bindings['assembler'],
                consumer_module=bindings['consumer'],prior_module=bindings['prior'],precision_module=bindings['precision'],
                theta_module=bindings['theta'],profile_module=bindings['profile'])
            def guard(phase,payload):
                need(phase in ('NODE_ACCESS','BACKGROUND_EXECUTION','BACKGROUND_ACCEPTANCE'),'UNKNOWN_NODE_GUARD_PHASE')
                if phase=='NODE_ACCESS':
                    need(payload['admission']==context.doc,'NODE_ADMISSION_MUTATED')
                checkpoint(phase,{'scenario_id':spec['scenario_id'],'payload':payload})
            callback=bindings['durable'].DurableNodeCallback(context,store,background_supplier=supplier,execution_guard=guard)
            seen=set()
            def evaluate(descriptor):
                nonlocal callback_attempts,callback_returns
                checkpoint('BEFORE_NODE',{'scenario_id':spec['scenario_id'],'node_id':descriptor['node_id']})
                need(descriptor['node_id'] not in seen and callback_attempts<resources['max_callback_calls'],
                     'NODE_REENTRY_OR_GLOBAL_CALLBACK_CAP')
                seen.add(descriptor['node_id']);callback_attempts+=1
                envelope=callback(descriptor)
                callback_returns+=1
                checkpoint('AFTER_NODE',{'scenario_id':spec['scenario_id'],'node_id':descriptor['node_id']})
                return envelope
            integrator=bindings['theta'].ThetaIntegrator(raw('theta_plan'),plan_sha256=sha(raw('theta_plan')),evaluate_node=evaluate)
            result=integrator.run()
            need(len(seen)==required_nodes and result['prior']['box_complete_rule'] is True and
                 result['refinement']['all_declared_levels_completed'] is True,'INCOMPLETE_PRIOR_NO_PARTIAL_RESULT')
            results.append({'scenario_id':spec['scenario_id'],'theta_result':result,'coupling_admission_sha256':sha(coupling_raw)})
            coupling_documents['coupling_'+str(index)+'.json']=coupling_raw
            checkpoint('AFTER_SCENARIO',{'scenario_id':spec['scenario_id']})
        need(callback_attempts==callback_returns==required_nodes*len(scenario_specs),'GLOBAL_NODE_COUNTS')
        need(supplier.entries==supplier.attempts==supplier.returns and supplier.attempts<=required_nodes,
             'GLOBAL_BACKGROUND_COUNTS')
        _verify_bindings(bindings,source_pins,artifacts,supervisor,decision['supervisor_adapter_pin'])
        checkpoint('BEFORE_TERMINAL_AUDIT',{})
        counts={'callback_attempts':callback_attempts,'callback_returns':callback_returns,
                'new_solver_attempts':supplier.attempts,'new_solver_returns':supplier.returns,
                'new_supplier_entries':supplier.entries}
        audit_raw=supervisor.terminal_audit(context={'execution_unit_id':unit,'request_sha256':request_sha256,
            'decision_sha256':decision_sha256,'runtime_sha256':runtime_sha,**counts})
        audit=document(audit_raw)
        need(audit['schema']=='F9_CONTROLLER_SUPERVISOR_TERMINAL_V1' and
             audit['execution_unit_id']==unit and audit['status']=='AUDIT_ACCEPTED' and audit['latched'] is False and
             audit['unexpected_reads']==audit['network_operations']==0 and audit['runtime_sha256']==runtime_sha and
             audit['execution_decision_sha256']==decision_sha256 and
             audit['new_solver_attempts']==supplier.attempts and audit['new_solver_returns']==supplier.returns,
             'TERMINAL_AUDIT_REJECTED')
        keys(audit['supervisor_reference'],('id','sha256'))
        need(audit['supervisor_reference']['sha256']==decision['supervisor_adapter_pin']['sha256'] and
             'resource_measurements' in audit,'SUPERVISOR_TERMINAL_IDENTITY_AND_MEASUREMENTS')
        need(audit['observed_reads'] is any(doc['data_kind']=='OPERATOR_RELEASED_OBSERVATIONS' for _,_,doc in prepared_specs),
             'OBSERVED_ACCESS_RECEIPT_MISMATCH')
        output={'schema':'F9_CONTROLLER_ENGINEERING_RESULT_V1','status':'ENGINEERING_ONLY',
            'execution_unit_id':unit,'request_sha256':request_sha256,'decision_sha256':decision_sha256,
            'scenarios':results,'family_scope':request['family_scope'],'complete_declared_family':True,
            'counts':counts,'wall_s':time.monotonic()-started,'runtime_sha256':runtime_sha,
            'supervisor_terminal_sha256':sha(audit_raw),'global_convergence':None,
            'uniform_theory_error_bound':None,'p':None,'sigma':None,'verdict':None,
            'acceptance':'REQUIRES_EXTERNAL_EXIT_AND_CLEANUP_VERIFICATION'}
        result_raw=canonical(output)
        runs.commit(ticket,{'controller_result.json':result_raw,'supervisor_terminal.json':audit_raw,
                            'request.json':request_json,'decision.json':decision_json,**coupling_documents})
        return output
    except BaseException as error:
        # If fail publication itself fails, exclusive run claim still blocks retry.
        runs.fail(ticket,error)
        raise


if __name__=='__main__':
    print(json.dumps({'status':'PREPARATION_ONLY_EXECUTION_DENIED',
        'request_id':PREPARATION_ID,'reason':'Qualified supervisor implementation, review and specific ROOT decision pending'}))
    raise SystemExit(2)
