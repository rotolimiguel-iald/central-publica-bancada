"""Validate documentary contract/pins only; do not evaluate scientific statistics."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
c=json.loads((HERE/'F9_VERDICT_CONTRACT_CANDIDATE.json').read_text());s=json.loads((HERE/'SOURCES.json').read_text());checks=[]
def check(name,cond):
 checks.append({'name':name,'passed':bool(cond)})
 assert cond,name
for x in s['files']:
 b=(HERE/x['snapshot']).read_bytes();check('source_bytes_'+x['snapshot'],len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'])
check('requested_candidate_pin',c['source_candidate_sha256']==s['requested_candidate_sha256'] and hashlib.sha256((HERE/'sources/F9_CANDIDATE_PINNED.json').read_bytes()).hexdigest()==s['requested_candidate_sha256'])
check('five_models',len(c['models'])==5)
check('primary_family_size',len(c['primary_family']['claims'])==c['primary_family']['m']==5)
check('unique_claim_ids',len({x['id'] for x in c['primary_family']['claims']})==5)
check('only_explicit_model_nulls',all(x['null'] in c['models'] for x in c['primary_family']['claims']))
check('nested_H3_declared',set(c['models']['H3_beta_free']['contains'])=={'H1_TGL','H2_LCDM'})
check('finite_conditional_systematics',c['systematics']['candidate_cartesian_labels']==c['systematics']['stellar_labels']*len(c['systematics']['SBF_labels']))
check('no_global_family_inflation',c['primary_family']['routes']==['F9_R-A_joint'])
check('no_observed_results',all(v is None for v in c['outputs_now'].values()))
check('not_opened_or_executed',not c['opening_authorized'] and not c['science_executed'] and not c['observed_values_read'])
check('two_alternatives_one_recommended',len(c['alternatives'])>=2 and sum(x['recommended'] for x in c['alternatives'])==1)
check('calibration_not_Wilks_or_lnB',c['calibration']['no_Wilks_assumption'] and c['calibration']['no_Bayes_to_sigma'])
check('power_is_separate',c['verdict']['fields'][-1]=='information_power' and 'compatibility' in c['verdict']['fields'])
check('conditional_not_confirmation',c['verdict']['no_CONFIRMED'] and c['verdict']['no_gate_change'])
check('preflight_is_subset',c['information_without_centres']['preflight_subset']+c['information_without_centres']['excluded_MM']==c['information_without_centres']['full_network'])
result={'status':'PASS_DOCUMENTARY_STRUCTURE_ONLY','checks':checks,'check_count':len(checks),'scientific_statistics_evaluated':False,'science_runs':0,'calibration_executed':False,'scope':'pins/schema/explicit contract relationships, NOT proof of numerical precision or tail calibration','contract_sha256':hashlib.sha256((HERE/'F9_VERDICT_CONTRACT_CANDIDATE.json').read_bytes()).hexdigest(),'note_sha256':hashlib.sha256((HERE/'CONTRATO_DE_VEREDITO_F9.md').read_bytes()).hexdigest()}
p=HERE/'VALIDACAO_DOCUMENTAL.json';t=p.with_name(p.name+'.new');b=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
if p.exists():raise FileExistsError(p)
with t.open('xb') as f:f.write(b)
assert t.stat().st_size==len(b);t.rename(p)
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))