"""Static re-verification of the E2 registry pins on Windows (no /opt runtime part). Read-only."""
import hashlib, json, re, datetime
from pathlib import Path
BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"); ROOT = BASE.parent

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

reg_path = BASE / 'RINGDOWN_5SIGMA_V1.json'; digest = sha(reg_path)
reg = json.loads(reg_path.read_text(encoding='utf-8-sig'))
out = {'registry_sha256': digest, 'status': reg['status'], 'registered_utc': reg['registered_utc'], 'created_utc': reg['created_utc']}
note = ROOT / reg['witness_relative_to_Chatgpt']; text = note.read_text(encoding='utf-8')
out['witness_hash_matches'] = re.findall(r'^registro_sha256: ([0-9a-f]{64})$', text, re.M) == [digest]
out['witness_registered_utc'] = re.findall(r'^registered_utc: (\S+)\s*$', text, re.M)
out['witness_sha256'] = sha(note)
out['witness_mtime_utc'] = datetime.datetime.utcfromtimestamp(note.stat().st_mtime).isoformat()
code = BASE / 'bis' / 'e2_code'
own = {p.relative_to(code).as_posix(): sha(p) for p in code.rglob('*.py')}
out['own_tree_matches'] = own == reg['own_code_tree_sha256']; out['own_tree_n'] = len(own)
bad = []
for e in reg.get('extra_code_roots', []):
    root = ROOT / e['relative_to_Chatgpt']
    actual = {p.relative_to(root).as_posix(): sha(p) for p in root.rglob('*.py')}
    if actual != e['files_sha256']:
        bad.append(e['relative_to_Chatgpt'])
out['extra_roots_ok'] = not bad; out['extra_roots_bad'] = bad
badpins = []
for name, w in reg['input_pins_relative_to_Chatgpt'].items():
    p = ROOT / name
    if not p.exists():
        badpins.append(('MISSING', name)); continue
    if sha(p) != w:
        badpins.append(('CHANGED', name))
out['input_pins_n'] = len(reg['input_pins_relative_to_Chatgpt']); out['input_pins_bad'] = badpins
rm = ROOT / reg['runtime_manifest_relative_to_Chatgpt']; out['runtime_manifest_ok'] = sha(rm) == reg['runtime_manifest_sha256']
env = json.loads(rm.read_bytes()); out['runtime_manifest_files_n'] = len(env['files']); out['runtime_python'] = env.get('python_executable')
b = ROOT / reg['budget_relative_to_Chatgpt']; out['budget_ok'] = sha(b) == reg['budget_sha256']; out['budget'] = json.loads(b.read_bytes())
act = reg['activation']; out['sealer_ok'] = sha(ROOT / act['sealer_relative_to_Chatgpt']) == act['sealer_sha256']
out['review_app_ok'] = sha(ROOT / act['review_application_relative_to_Chatgpt']) == act['review_application_sha256']
rec = json.loads((ROOT / act['receipt_relative_to_Chatgpt']).read_bytes())
out['receipt_ok'] = rec['registration_sha256'] == digest and rec['witness_sha256'] == sha(note)
for rel, pin in reg['independent_review_files_sha256'].items():
    if sha(BASE / rel) != pin:
        badpins.append(('REVIEW_CHANGED', rel))
seed = ROOT / reg['blinding']['seed_relative_to_Chatgpt']
try:
    out['seed_commitment_ok'] = sha(seed) == reg['blinding']['seed_commitment_sha256']
    out['seed_mtime_utc'] = datetime.datetime.utcfromtimestamp(seed.stat().st_mtime).isoformat()
except Exception as e:
    out['seed_commitment_ok'] = 'UNREADABLE (ACL): ' + type(e).__name__
for rel in ['bis/RESULT_E2_NULL_CAMPAIGN.json', 'bis/e4_e5_prepare/runs/authorized_001/DETERMINISTIC_DIAGNOSTICS.json',
            'bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json', 'ORCAMENTO_40H.json',
            'cache/POSTERIORES_PSEOB_GWTC5_33_013BIS_V1.json', 'bis/e3_wall_stages/candidates/test_actual_001/WALL_SOURCE.json']:
    p = BASE / rel
    if p.exists():
        d = json.loads(p.read_bytes())
        found = [k for k in d if 'registration' in k.lower() and isinstance(d[k], str) and d[k] == digest]
        out['embeds:' + rel] = {'sha256': sha(p), 'keys_with_registry_hash': found}
pt = reg['planning_targets']
out['I_targets'] = {f"{t['population']}/{t['reading']}": t['I_tau_expected_target90'] for t in pt}
out['min_info_to_unblind'] = reg['blinding']['minimum_information_to_unblind']
ok = []
for ev, e in reg['test_candidates'].items():
    if e['eligible'] is True and e['published_deformation_at_registration'] is False and e.get('publication_census_scope'):
        ok.append((ev, e['run'], e['SNR_network_GWOSC'], e['data_quality_hold']))
out['admissible_blind_today'] = ok; out['n_admissible'] = len(ok)
out['priority_ge30'] = [(ev, e['run'], e['SNR_network_GWOSC'], e['eligible']) for ev, e in reg['test_candidates'].items() if e['priority_ge30']]
print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
