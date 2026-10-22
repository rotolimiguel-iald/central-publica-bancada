"""Finite documentary review only. Never import/execute delivery or activation code."""
import ast
import collections
import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent
B=HERE.parents[1]
FILES=[
 'refeito/deliver_b3_wall_013bis.py','refeito/activate_wall_budget_013bis.py',
 'bis/e2_code/registration_guard.py',
 'bis/e3_budget_wall/ORCAMENTO_40H_CANDIDATE.json',
 'cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json',
 'bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json',
 'cache/E3_KERR220_CALIBRATION_V1/COST.json','cache/E3_KERR220_CALIBRATION_V2/COST.json',
 'cache/E3_PSEOB_PILOT_V1/CONTROLLER.json',
 'bis/FINAL_INTEGRITY_20260922T230100445220Z.json',
 'bis/e3_allocation_review/FIXTURE_RESULTS_001.json',
 'bis/e3_allocation_review/audit_fixtures.py',
 'bis/e3_allocation_review/INDEPENDENT_ALLOCATION_REVIEW_V1.md',
 'bis/e3_allocation_review/BOUNDARY_ADDENDUM_001.json',
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):
 raw=x if isinstance(x,bytes) else ((json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode() if not isinstance(x,str) else x.encode())
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
def main():
 pins={}; data={};checks=[]
 for rel in FILES:
  raw=(B/rel).read_bytes();pins[rel]=dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
  put(HERE/'snapshot'/rel,raw)
  if rel.endswith('.json'):data[rel]=json.loads(raw)
 def ck(name,value):
  checks.append(dict(name=name,passed=bool(value)))
  if not value:raise ValueError(name)
 candidate=data['bis/e3_budget_wall/ORCAMENTO_40H_CANDIDATE.json']
 comp=data['cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json']
 kr=data['bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json']
 delivery=(HERE/'snapshot/refeito/deliver_b3_wall_013bis.py').read_text(encoding='utf-8')
 activation=(HERE/'snapshot/refeito/activate_wall_budget_013bis.py').read_text(encoding='utf-8')
 ast.parse(delivery);ast.parse(activation)
 ck('scripts_parse_without_execution',True)
 ck('candidate_zero_PE_and_injections',candidate['allocation']['new_PE_count']==candidate['allocation']['new_injection_count']==0)
 ck('cost_unknown_not_zero',candidate['cost_per_converged_IMR_posterior_seconds'] is None)
 ck('five_alternatives',len(candidate['alternatives'])==5)
 ck('14_10_4',len(candidate['events'])==14 and sum(e['data_quality_hold'] for e in candidate['events'])==4)
 ck('ten_Ncalib_readings',len(candidate['Ncalib']['readings'])==10)
 counts=[]
 for r in candidate['Ncalib']['readings']:
  for c in r['illustrative_sigma_INPUT_from_order']:
   ck('Ncalc '+r['reading']+str(c['sigma_inj']),math.isclose(c['N_per_cell_floor5_continuous'],25*c['sigma_inj']**2/r['delta_reference_GW250114']**2,rel_tol=1e-14))
   ck('ceil '+r['reading']+str(c['sigma_inj']),c['N_per_cell_floor5_ceiling']==math.ceil(c['N_per_cell_floor5_continuous']))
   ck('ten cells '+r['reading']+str(c['sigma_inj']),c['N_ten_cells_floor5_ceiling']==10*c['N_per_cell_floor5_ceiling'])
   if c['sigma_inj']==.058:counts.append(dict(reading=r['reading'],N_cell=c['N_per_cell_floor5_ceiling'],N_ten=c['N_ten_cells_floor5_ceiling']))
 for name,row in comp['comparison'].items():
  ck('median difference '+name,math.isclose(row['median_difference'],row['own_05_50_95'][1]-row['released_05_50_95'][1],abs_tol=1e-14))
  ck('descriptive normalized difference '+name,math.isclose(row['difference_over_quadrature_width'],row['median_difference']/math.hypot(row['own_std_ddof1'],row['released_std_ddof1']),rel_tol=1e-14))
  ck('90 overlap '+name,max(row['own_05_50_95'][0],row['released_05_50_95'][0])<=min(row['own_05_50_95'][2],row['released_05_50_95'][2]))
 ck('comparison pin in independent Kerr review',kr['input_hashes']['/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json']==pins['cache/E3_KERR220_CALIBRATION_V2/public_psd/COMPARISON.json']['sha256'])
 ck('Kerr accepted scope',kr['blocking_findings']==[] and kr['equivalent_reproduction_paid'] is False)
 ck('samples/ESS/ncall',comp['samples']==2128 and comp['convergence']['ncall']==1356580 and math.isclose(comp['convergence']['ess'],3093.8512933753923,rel_tol=1e-14))
 k1=data['cache/E3_KERR220_CALIBRATION_V1/COST.json'];k2=data['cache/E3_KERR220_CALIBRATION_V2/COST.json']
 ck('Kerr wall',math.isclose(candidate['measured_costs']['Kerr_V1_V2_controller_sum_seconds'],k1['wall_seconds']+k2['wall_seconds'],abs_tol=1e-10))
 ck('Kerr CPU',math.isclose(candidate['measured_costs']['Kerr_V1_V2_CPU_sum_seconds'],k1['children_cpu_seconds']+k2['children_cpu_seconds'],abs_tol=1e-10))
 ck('pilot exact controller',candidate['measured_costs']['IMR_pilot_failed_controller']==data['cache/E3_PSEOB_PILOT_V1/CONTROLLER.json'])
 integrity=data['bis/FINAL_INTEGRITY_20260922T230100445220Z.json']
 categories=dict(collections.Counter(r['category'] for r in integrity['checks']))
 ck('295_receipt_rows',categories=={'inputs':217,'sources':31,'delivered_part_A':47})
 for i,row in enumerate(integrity['checks']):ck('reported_hash_equality_'+str(i),row['matches'] is True and row['expected_sha256']==row['actual_sha256'])
 ck('size_layout_metadata_only',integrity['oversized_outside_cache']==[] and integrity['cache_content_not_scanned'] is True)
 ck('one_metadata_exception',len(integrity['metadata_exceptions'])==1)
 fixture=next(c for c in data['bis/e3_allocation_review/FIXTURE_RESULTS_001.json']['cases'] if c['id']=='finding_symlink_output_escape')
 ck('fixture_prior_review',fixture['passed'] and 'still inside own fixture tree' in fixture['details']['observed_defect'])
 # Literal stdout from the scoped, successful WSL readlink command in this review.
 # Pure lexical processing only: no resolve(), stat(), enumeration or content read of target.
 target='/mnt/c/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/e3_allocation_review/fixtures_001/finding_symlink_output_escape/escaped_sidecar'
 exception=integrity['metadata_exceptions'][0]
 win=exception['path'].replace('\\','/')
 link='/mnt/c/'+win[3:]
 fixture_root=target.rsplit('/',1)[0]
 ck('same_negative_fixture_path','/finding_symlink_output_escape/' in link and link.endswith('/e3_allocation_prepare/candidates'))
 ck('readlink_target_inside_fixture_lexically',PurePosixPath(target).is_relative_to(PurePosixPath(fixture_root)))
 readlink={'command':['wsl.exe','--exec','readlink','--',link], 'returncode':0,'stdout':target+'\n',
           'evidence':'Executed once via exec tool during this review; only symlink text read. No readlink -f, target enumeration or target contents.',
           'classification':'KNOWN_NEGATIVE_FIXTURE_WSL_SYMLINK_METADATA_EXCEPTION',
           'scope':'Metadata exception explained, not an integrity hash failure of the295 named files and not blanket integrity proof of its target.'}
 # In-memory reproduction of only the witness formatting/regex contract, no production execution.
 witness_model='Orçamento `path` — SHA256 `'+('a'*64)+'`.\n\nRegistro UTC 2026-09-22T23:10:00+00:00; prazo final de integração ...\n'
 witness_regex_matches={'hash':re.findall(r'^allocation_sha256: ([0-9a-f]{64})\s*$',witness_model,re.M),
                       'date':re.findall(r'^registered_utc: (\S+)\s*$',witness_model,re.M)}
 missing_labels='allocation_sha256:' not in activation and 'registered_utc:' not in activation
 findings=[]
 if missing_labels:
  ck('witness_pattern_missing_in_draft',witness_regex_matches=={'hash':[],'date':[]})
  findings.append({'id':'B3-R1','severity':'P1_DEPENDENCY_BEFORE_ACTIVATION',
   'source':'refeito/activate_wall_budget_013bis.py:47; bis/e2_code/registration_guard.py:157,196',
   'issue':'Activation witness draft has prose but omits exact allocation_sha256: and registered_utc: lines required by frozen check_witness. Receipt alone does not make load_jobs accept it.',
   'proposed_fix':'Before activation, append exactly one machine hash line for the active budget bytes and one registered UTC line. Test those regexes against a finite mock witness; do not change guard. This review does not execute or activate anything.'})
 findings.append({'id':'B3-R2','severity':'P2_PIN_AND_ACTIVATION_PREFLIGHT',
  'source':'refeito/deliver_b3_wall_013bis.py:20-29,107',
  'issue':'Before first output the delivery checks only budget hash and review approved flag. It neither validates complete activation receipt/witness/parent/candidate bindings nor compares COMPARISON to the independently reviewed Kerr pin. Later listing hashes records current bytes but does not enforce reviewed identity.',
  'proposed_fix':'Preflight all named sources and destinations before new(fiche): activation status and parent/candidate/review/witness pins; approved review candidate binding; Kerr review hash and its input_hashes COMPARISON pin; empty new jobs/counts and bounded reserve. No scientific imports required. Use a snapshot of verified bytes for rendering.'})
 notes=[
 {'id':'B3-N1','source':'refeito/deliver_b3_wall_013bis.py:42-51','text':'Print mass_frame explicitly: Mf detector-frame Msun, af dimensionless. Replace razão de larguras by diferença de medianas dividida pela largura em quadratura.'},
 {'id':'B3-N2','source':'refeito/deliver_b3_wall_013bis.py:51','text':'A revisão conferiu os dados completos is too broad: B checked complete posterior samples and metadata/pins, not strain bytes or reconstructed covariance. Say posteriores completos e metadados/pins no escopo do parecer.'},
 {'id':'B3-N3','source':'refeito/deliver_b3_wall_013bis.py:98','text':'Cost totals agree. Add separate Welch diagnostic3.402371976s if claiming complete itemized E3 costs; otherwise explicitly say its receipt is in budget. Do not add launcher/runner totals twice.'},
 {'id':'B3-N4','source':'refeito/deliver_b3_wall_013bis.py:101-103','text':'Commands shown contain ellipses or omit actual WSL/Python prefix; label as abbreviated locators rather than exact replay commands. No rerun authorized by reproduction prose.'}]
 result={'status':'FINITE_B3_STATIC_REVIEW_CHANGES_REQUIRED_NO_EXECUTION', 'created_utc':datetime.now(timezone.utc).isoformat(),
         'reviewed_delivery_sha256':pins['refeito/deliver_b3_wall_013bis.py']['sha256'],
         'findings':findings,'editorial_notes':notes,'checks':checks,'check_count':len(checks),
         'counts_058':counts,'integrity_receipt_counts':categories,'integrity_scope':'Receipt internal consistency checked;295 original files NOT reread/rehashed by this review.',
         'symlink':readlink,'witness_mock':witness_regex_matches,'source_pins':pins,
         'execution':{'delivery':False,'activation':False,'scientific':False,'strain_or_posterior_payload':False,'symlink_target_contents':False},
         'scope':'Budget builder authored by this agent; this is review of the main delivery source and metadata, not independent approval of its own budget. B supplies that independent budget review.'}
 put(HERE/'REVIEW.json',result);put(HERE/'SYMLINK_CLASSIFICATION.json',readlink)
 md='# B3 — revisão estática finita\n\n**Alterações necessárias antes da entrega/ativação; nenhum script de produção executado.** Custos/contagens e números Kerr conferem com candidato e recibos.\n\n'
 for f in findings:md+=f"- **{f['id']} ({f['severity']})**, `{f['source']}`: {f['issue']} Correção proposta: {f['proposed_fix']}\n\n"
 md+='## Linguagem e escopo\n\n'+'\n\n'.join(f"- `{n['source']}`: {n['text']}" for n in notes)
 md+=f"\n\n## Integridade e symlink\n\nRecibo:217 insumos +31 fontes +47 entregas ParteA =295 comparações registradas, todas com hashes esperado/real iguais. Isto é conferência interna do recibo, **não nova rehash dos295 originais**. Cache não foi varrido; não há alegação de integridade universal.\n\nA única exceção WinError1920 é o symlink da fixture negativa `finding_symlink_output_escape`. `readlink` retornou `{target}`, lexicalmente dentro da própria fixture, coerente com audit_fixtures.py:218 e FIXTURE_RESULTS_001.json. Nenhum conteúdo do destino foi lido; não remover a exceção histórica nem declarar o destino auditado. Classificação separada em SYMLINK_CLASSIFICATION.json.\n\n{len(checks)} verificações finitas passaram. `REVIEW.json` traz hashes lidos e detalhes; `snapshot/` preserva os bytes efetivamente revisados. Reavaliação necessária se o principal alterar os drafts. Não executado deliver_b3, activate, ciência, strain ou posterior. A revisão independente do próprio candidato continua sendo de B. Todos os arquivos escritos estão em MANIFEST.json.\n"
 put(HERE/'REVIEW.md',md)
 changed=[r for r in FILES if sha(B/r)!=pins[r]['sha256']]
 put(HERE/'FINAL_SOURCE_RECHECK.json',{'changed_since_snapshot':changed,'scope':'If changed, findings bind the saved snapshot only; no automatic approval of successor.'})
 put(HERE/'MANIFEST.json',{'files':[dict(relative_path=p.relative_to(HERE).as_posix(),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(HERE.rglob('*')) if p.is_file()], 'self':'MANIFEST.json (no circular hash)'})
 print(json.dumps({'checks':len(checks),'changed':changed,'review_sha256':sha(HERE/'REVIEW.json'),'findings':[f['id'] for f in findings]}))

if __name__=='__main__':main()
