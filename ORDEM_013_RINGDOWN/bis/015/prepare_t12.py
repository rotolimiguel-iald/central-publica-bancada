"""Prepare T12 in a new tree; never modify the V1 registered producer."""
from pathlib import Path
import ast, hashlib, json, sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write, save, sha, now
B = ROOT/'ORDEM_013_RINGDOWN'
D = B/'bis/e7_prepare_v1_1'
OLD = B/'bis/e7_prepare'
def main():
    D.mkdir(exist_ok=True)
    old = OLD/'producer/tgl_ringdown_ampliacao.py'
    source = old.read_text('utf-8-sig')
    tree = ast.parse(source)
    # The historical run API stays for regression/extraction, but its context
    # provider becomes an explicit refusal. Only run_rite is the new entrypoint.
    start = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='checked_context')
    lines=source.splitlines(keepends=True)
    lines[start.lineno-1:start.end_lineno]=['def checked_context(root, registration, registration_sha256):\n',
      '    require_pin(registration, registration_sha256)\n',
      '    raise ValueError("Legacy extraction context disabled; use the embedded run_rite reader")\n']
    source=''.join(lines).replace('import importlib.util\n','')
    mainnode=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    source=''.join(source.splitlines(keepends=True)[:mainnode.lineno-1])
    write(D/'producer/tgl_ringdown_ampliacao.py',source.encode())
    write(D/'producer/extrai_posteriores_pseob.py',(OLD/'producer/extrai_posteriores_pseob.py').read_bytes())
    copied={}
    for name in ('test_e7.py','test_review_fixes_v3.py','test_authorization_v4.py'):
        p=OLD/'tests'/name
        write(D/'legacy_tests'/name,p.read_bytes())
        # 52 applicable legacy tests target the new module. The external loader
        # test is retired explicitly; the original 53 also run against old code.
        text=p.read_text('utf-8-sig')
        if name=='test_review_fixes_v3.py':
            text=text.replace('    def test_stale_guard_pin_refused_before_import(self):',
              '    @unittest.skip("External guard removed by T12; replaced by embedded guard mutation tests")\n    def test_stale_guard_pin_refused_before_import(self):')
        write(D/'tests'/name,text.encode())
        copied[str(p.relative_to(ROOT))]=sha(p)
    save(D/'START.json',dict(at=now.isoformat(),source_sha256=sha(old),legacy_test_sources=copied,
      formula_functions=['conditional_projection','prediction_draws','reading_diagnostics','fullsample_diagnostics'],
      part_B_heavy_clock_started=(B/'bis/PART_015_BUDGET_START.json').exists(),gate_changed=False))
    print(D)
if __name__=='__main__':main()
