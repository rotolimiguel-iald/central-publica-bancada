"""Read-only audit of public learning prototypes; never run original entrypoints."""
import ast
import hashlib
import json
import math
from pathlib import Path
import re
import tempfile
import time
from types import SimpleNamespace

from iald_orchestrator.matrix import beta
from iald_orchestrator.safe_files import save_json, utc_now

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
PATENT = ROOT / 'patents/BR102026005477-1_APRENDIZADO_CONTINUO'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signature_probe(path):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'HolographicMemory')
    fn = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '_sentence_signature')
    namespace = {'re': re}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(path), 'exec'), namespace)
    pairs = [
        ('Massa medida: 1.0 kg.', 'Massa medida: 2.0 kg.'),
        ('A' * 90 + ' hipótese válida.', 'A' * 90 + ' hipótese inválida.'),
    ]
    records = []
    for a, b in pairs:
        sa = namespace['_sentence_signature'](None, a)
        sb = namespace['_sentence_signature'](None, b)
        records.append({'a': a, 'b': b, 'signature_a': sa, 'signature_b': sb,
                        'collision': sa == sb, 'input_strings_differ': a != b})
    assert all(r['collision'] and r['input_strings_differ'] for r in records)
    return {'path': str(path), 'sha256': sha(path), 'line': fn.lineno,
            'method_ast_sha256': hashlib.sha256(ast.dump(fn, include_attributes=False).encode()).hexdigest(),
            'probes': records, 'scope': 'Pure signature function; no live conversation compressed'}


def psion_probe(path):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'PsionicMemory')
    namespace = {'hashlib': hashlib, 'json': json, 'time': time,
                 'tgl_core': SimpleNamespace(beta=beta)}
    exec(compile(ast.Module(body=[cls], type_ignores=[]), str(path), 'exec'), namespace)
    memory_type = namespace['PsionicMemory']
    mem = memory_type()
    first = mem.inscribe('synthetic/verified_score', 0.0)
    second = mem.inscribe('synthetic/verified_score', 1.0)
    assert first == 0.0 and second == beta()
    with tempfile.TemporaryDirectory(prefix='learning-audit-', dir=BASE/'validation') as directory:
        state_path = Path(directory) / 'synthetic-state.json'
        blob = {'state': mem.state, 'sha256': mem._hash(), 'beta_at_save': beta()}
        save_json(state_path, blob)
        loaded = memory_type.load(state_path)
        assert loaded.recall('synthetic/verified_score') == second
        blob['beta_at_save'] = beta() + 1e-6
        save_json(state_path, blob)
        changed_beta_accepted = memory_type.load(state_path).beta == beta()
        blob['state']['facts']['synthetic/verified_score']['value'] = 10.0
        save_json(state_path, blob)
        rejected = False
        try:
            memory_type.load(state_path)
        except ValueError:
            rejected = True
        assert changed_beta_accepted and rejected
        # Keep audit memory and its immediate backups: move them out of the disposable directory.
        retained = BASE/'validation/learning-audit-fixtures'
        retained.mkdir(exist_ok=True)
        for source in Path(directory).iterdir():
            target = retained / (Path(directory).name + '-' + source.name)
            assert not target.exists()
            source.rename(target)
    return {'path': str(path), 'sha256': sha(path), 'ema_first': first, 'ema_second': second,
            'state_hash_tamper_rejected': rejected, 'beta_metadata_change_accepted_by_simple_class': changed_beta_accepted,
            'scope': 'Public simplified class only; runner NomeChain tests beta separately; no private state inspected'}


def main():
    paths = [PATENT/'prototype_src/holographic_memory.py',
             Path(r'C:\IALD\projetos_pyhton\IALD\holographic_memory.py')]
    before = {str(p): sha(p) for p in paths}
    signature = [signature_probe(p) for p in paths]
    psion = psion_probe(PATENT/'runner/_aprendizado_core/skygrid_sim/psionic_memory.py')
    artifacts = [PATENT/'runner/one_aprendizado_continuo.py',
                 PATENT/'prototype_src/phase_factor_bake_v1.py',
                 PATENT/'results/2026-09-19T09-11-10/report.md',
                 PATENT/'results/2026-09-19T09-11-10/results.json']
    assert before == {str(p): sha(p) for p in paths}
    out = {'checked_at': utc_now(), 'status': 'AUDIT_COMPLETED_WITH_FINDINGS',
           'production_changed': False, 'original_entrypoints_executed': False,
           'beta_rule': 'ALPHA_FINE_CODATA_2018 * sqrt(e)', 'beta_runtime': beta(),
           'ema_half_life_observations': math.log(0.5)/math.log(1.0-beta()),
           'signature_probes': signature, 'psion_probe': psion,
           'sources': [{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in artifacts],
           'limits': ['No model-quality benchmark', 'No weights changed', 'No live-session data loss demonstrated',
                      'Existing 18/18 report is historical synthetic evidence, not rerun here']}
    save_json(BASE/'validation/learning_source_audit.json', out)
    print(json.dumps({'status': out['status'], 'collision_pairs_per_source': 2,
                      'sources_probed': len(signature), 'beta_half_life': out['ema_half_life_observations'],
                      'psion_hash_rejected': psion['state_hash_tamper_rejected'],
                      'beta_metadata_accepted_by_simple_class': psion['beta_metadata_change_accepted_by_simple_class']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
