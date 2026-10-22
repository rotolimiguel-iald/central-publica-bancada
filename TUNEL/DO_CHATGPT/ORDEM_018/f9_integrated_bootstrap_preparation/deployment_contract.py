"""Strict preparation/deployment/authority bindings. No generated authority."""
import os
from pathlib import Path
import sys
from posix_protocol import absolute, canonical, digest, document, exact, need, pinned, read_bytes, sha

PREPARATION_ID='d72f7125-bd1a-4e04-96e2-470ec6a823b0'
SCOPE='F9_FULL_PRIOR_SYNTHETIC_ENGINEERING_ONLY'

def bundle(deployment_path,decision_path,decision_sha256,check):
    check();dr=read_bytes(deployment_path,8*1024*1024);deployment=document(dr)
    exact(deployment,('schema','package_root','preparation_manifest_pin','recipe_pin','runtime_inventory','independent_review','root_binding','scope'))
    need(deployment['schema']=='F9_INTEGRATED_DEPLOYMENT_V1' and deployment['scope']==SCOPE,'DEPLOYMENT_SCHEMA')
    base=Path(absolute(deployment['package_root']))
    need(base==Path(__file__).resolve().parent,'DEPLOYED_SOURCE_ROOT')
    mr=pinned(str(base/'MANIFESTO_PREPARACAO.json'),deployment['preparation_manifest_pin'],8*1024*1024);manifest=document(mr)
    need(manifest['request_id']==PREPARATION_ID,'MANIFEST_ID')
    pins={}
    for item in manifest['files']:
        check();name=item['name'];need(Path(name).name==name and name not in pins,'FLAT_UNIQUE_MANIFEST')
        pin={k:item[k] for k in ('bytes','sha256')};pinned(str(base/name),pin,max(1,pin['bytes']));pins[name]=pin
    pins['MANIFESTO_PREPARACAO.json']=deployment['preparation_manifest_pin']
    recipe_raw=pinned(str(base/'INPUT_RECIPE_PROPOSAL.json'),deployment['recipe_pin'],1024*1024)
    need(deployment['recipe_pin']==pins['INPUT_RECIPE_PROPOSAL.json'],'RECIPE_MANIFEST_PIN')
    external={}
    for role in ('runtime_inventory','independent_review','root_binding'):
        check();item=deployment[role];exact(item,('path','pin'))
        external[role]=pinned(absolute(item['path']),item['pin'],32*1024*1024)
    decision_raw=read_bytes(decision_path,1024*1024);need(sha(decision_raw)==digest(decision_sha256),'ORIGINAL_ROOT_DECISION_PIN')
    decision=document(decision_raw)
    exact(decision,('schema','preparation_request_id','execution_unit_id','preparation_manifest_sha256','input_recipe_sha256',
        'authorize_single_execution','scope','may_read_observations','supervisor_adapter_pin','independent_review_reference',
        'runtime_inventory_sha256','deployment_sha256','root_binding_sha256'))
    need(decision['schema']=='F9_INTEGRATED_ROOT_DECISION_V1' and decision['preparation_request_id']==PREPARATION_ID
         and decision['scope']==SCOPE and decision['authorize_single_execution'] is True and decision['may_read_observations'] is False,'EXPLICIT_ORIGINAL_ROOT_DECISION')
    need(decision['preparation_manifest_sha256']==sha(mr) and decision['input_recipe_sha256']==sha(recipe_raw)
         and decision['deployment_sha256']==sha(dr) and decision['runtime_inventory_sha256']==sha(external['runtime_inventory'])
         and decision['root_binding_sha256']==sha(external['root_binding']),'DECISION_DEPLOYMENT_BINDING')
    need(decision['supervisor_adapter_pin']==pins['integrated_supervisor.py'],'ACTUAL_SUPERVISOR_SOURCE_PIN')
    review=document(external['independent_review']);ref=decision['independent_review_reference'];exact(ref,('id','sha256'))
    need(ref['sha256']==sha(external['independent_review']) and ref['id']==review['review_id']
         and review['preparation_manifest_sha256']==sha(mr) and review['status']=='ACCEPTED_FOR_SYNTHETIC_INTEGRATED_QUALIFICATION'
         and review['reviewer_is_author'] is False and review['I02_99e2_review_accepted'] is True,'INDEPENDENT_INTEGRATED_REVIEW_REQUIRED')
    binding=document(external['root_binding']);exact(binding,('schema','execution_unit_id','stable_consumption_root','registry_reference','status'))
    need(binding['schema']=='F9_STABLE_ROOT_BINDING_V1' and binding['execution_unit_id']==decision['execution_unit_id']
         and binding['status']=='ROOT_REGISTERED_ONCE_NO_ALTERNATE_ROOT_REPLAY','STABLE_UNIT_REGISTRATION')
    absolute(binding['stable_consumption_root']);exact(binding['registry_reference'],('id','sha256'));digest(binding['registry_reference']['sha256'])
    unit=decision['execution_unit_id'];need(type(unit) is str and len(unit)<=96 and unit and all(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in unit),'SAFE_NEW_UNIT_ID')
    runtime=document(external['runtime_inventory']);exact(runtime,('schema','status','python_executable','python_version','python_search_path','files','absent_paths','scan_directories','native_map_pins','trust_scope','measurement_reference'))
    need(runtime['schema']=='F9_CURRENT_POSIX_RUNTIME_INVENTORY_V1' and runtime['status']=='MEASURED_CURRENT_AUTHORIZED_INVENTORY'
         and runtime['trust_scope']=='TRUSTED_PINNED_NATIVE_COOPERATIVE_PYTHON_NOT_OS_ISOLATION','CURRENT_RUNTIME_REQUIRED')
    need(os.name=='posix' and sys.platform=='linux' and os.geteuid()!=0 and str(Path(sys.executable).resolve())==runtime['python_executable']
         and sys.version==runtime['python_version'],'EXACT_NONROOT_LINUX_PYTHON')
    for path,pin in runtime['files'].items():check();pinned(absolute(path),pin,max(1,pin['bytes']))
    for path,pin in runtime['native_map_pins'].items():check();pinned(absolute(path),pin,max(1,pin['bytes']))
    for path in runtime['absent_paths']:need(not os.path.lexists(absolute(path)),'ABSENT_RUNTIME_PROBE_CHANGED')
    for path in runtime['python_search_path']+runtime['scan_directories']:need(Path(absolute(path)).is_dir(),'RUNTIME_DIRECTORY_MISSING')
    check()
    return {'package':base,'pins':pins,'manifest_raw':mr,'deployment_raw':dr,'decision_raw':decision_raw,
            'decision':decision,'recipe_raw':recipe_raw,'recipe':document(recipe_raw),'runtime':runtime,
            'runtime_raw':external['runtime_inventory'],'review_raw':external['independent_review'],'binding':binding}
