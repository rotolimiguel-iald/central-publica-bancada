# mutar.py — mutação campo a campo do contrato v3 (frente contrato_v3, 23/09/2026)
# Para cada campo Prop das 4 estruturas de ContratoQG_v3.lean: troca o tipo do campo por True, compila o
# núcleo mutante e, contra ele, as guardas, os teoremas e os probes negativos; lê os erros por SÍTIO
# (declaração, campo) e compara com a linha de base. Só escreve em mutacao/runs/. Nunca toca o kernel.
import os, re, shutil, subprocess, json, sys, hashlib
from concurrent.futures import ThreadPoolExecutor
V3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(V3, 'mutacao', 'runs')
CORE = 'ContratoQG_v3.lean'
DEPENDENTES = ['GuardasV3.lean', 'ContratoQG_v3_Teoremas.lean', 'ProbeToyV3.lean', 'ProbeLegacyV3.lean',
               'ProbeVacuousImportV3.lean', 'ProbeTrivialH3v3.lean']
PROP_FIELDS = {
 'WedgeBoostRep': ['V_zero','V_add','V_continuous','V_vac','V_translations','V_net'],
 'ContratoH2': ['kappa_pos','flow_implemented','kms','bw','translations_continuous','translations_faithful',
                'positive_energy','null_ergodic','observer_in_wedge','observer_unit','smooth_on','det_unit_on',
                'dragged','fiducial_is_modular'],
 'ContratoH3': ['G_pos','screen_measurable','screen_pos','screen_finite','eps_pos','lam0_neg','lam0_in_wedge',
                'admissible_unit','vac_admissible','admissible_energy','admissible_nontrivial','response_vac',
                'response_det_unit_on','area_differentiable','matter_is_state','area_law'],
 'ContratoImportH3': ['same_horizon'],
}
def winpath(p):
    p = os.path.abspath(p)
    return p.replace('/', chr(92))

def mutate(src_lines, struct, field):
    # localiza a estrutura
    i0 = None
    for i, l in enumerate(src_lines):
        if re.match(r'^structure %s\b' % re.escape(struct), l):
            i0 = i; break
    assert i0 is not None, struct
    # corpo: após a linha que termina com 'where'
    j = i0
    while not src_lines[j].rstrip().endswith('where'):
        j += 1
    body_start = j + 1
    k = body_start
    while k < len(src_lines) and (src_lines[k].startswith('  ') or src_lines[k].strip() == ''):
        if src_lines[k].strip() == '' :
            break
        k += 1
    body_end = k
    # acha o campo
    fs = None
    for i in range(body_start, body_end):
        if re.match(r'^  %s :' % re.escape(field), src_lines[i]):
            fs = i; break
    assert fs is not None, (struct, field)
    fe = fs + 1
    while fe < body_end and re.match(r'^    ', src_lines[fe]) and not re.match(r'^  \S', src_lines[fe]):
        fe += 1
    new = src_lines[:fs] + ['  %s : True\n' % field] + src_lines[fe:]
    return new, (fs + 1, fe)

def run_compile(src, log, root):
    r = subprocess.run(['bash', os.path.join(V3, 'compile.sh'), src, log, winpath(root)],
                       capture_output=True, text=True)
    return r.stdout.strip()

def decl_sites(path):
    """mapa linha -> (declaração, campo) do arquivo-fonte."""
    lines = open(path, encoding='utf-8').read().split('\n')
    decl = None; field = None; out = {}
    for n, l in enumerate(lines, start=1):
        m = re.match(r'^(?:private |protected |noncomputable )*(theorem|def|lemma|abbrev|instance|example)\s+([^\s(:{\[]*)', l)
        if m:
            decl = m.group(2) or m.group(1); field = None
        m2 = re.match(r'^  ([A-Za-zΔ_][\w\'Δ]*) :=', l)
        if m2 and decl is not None:
            field = m2.group(1)
        out[n] = (decl, field)
    return out

def error_sites(log, src):
    if not os.path.exists(log):
        return None
    s = open(log, encoding='utf-8', errors='replace').read()
    rc = re.findall(r'rc=(\d+)', s)
    sites = decl_sites(src)
    errs = set()
    base = os.path.basename(src)
    for m in re.finditer(re.escape(base) + r':(\d+):(\d+): error', s):
        ln = int(m.group(1))
        errs.add(sites.get(ln, ('?', None)))
    return {'rc': int(rc[-1]) if rc else None, 'invalid_oom': ('bad_alloc' in s) or (rc and rc[-1] == '127'), 'errors': sorted([f'{d}' + (f'.{f}' if f else '') for d, f in errs]),
            'kernel_touched': re.findall(r'kernel_files_newer_than_stamp=(\d+)', s)}

def one_run(name, struct=None, field=None):
    d = os.path.join(RUNS, name)
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    src = open(os.path.join(V3, CORE), encoding='utf-8').read().split('\n')
    src = [l + '\n' for l in src[:-1]] + [src[-1]]
    span = None
    if struct:
        src, span = mutate(src, struct, field)
    open(os.path.join(d, CORE), 'w', encoding='utf-8', newline='\n').write(''.join(src))
    for f in DEPENDENTES:
        shutil.copyfile(os.path.join(V3, f), os.path.join(d, f))
    res = {'name': name, 'struct': struct, 'field': field, 'span': span}
    run_compile(CORE, os.path.join(d, 'log_core.txt'), d)
    res['core'] = error_sites(os.path.join(d, 'log_core.txt'), os.path.join(d, CORE))
    with ThreadPoolExecutor(max_workers=len(DEPENDENTES)) as ex:
        futs = {f: ex.submit(run_compile, f, os.path.join(d, 'log_' + f.replace('.lean', '.txt')), d) for f in DEPENDENTES}
        for f in futs: futs[f].result()
    for f in DEPENDENTES:
        res[f] = error_sites(os.path.join(d, 'log_' + f.replace('.lean', '.txt')), os.path.join(d, f))
    # limpa oleans (grandes) para não encher o scratchpad
    for fn in os.listdir(d):
        if fn.endswith('.olean') or fn.endswith('.ilean'):
            os.remove(os.path.join(d, fn))
    return res

if __name__ == '__main__':
    jobs = [('BASE', None, None)] + [(f'{s}__{f}', s, f) for s in PROP_FIELDS for f in PROP_FIELDS[s]]
    if len(sys.argv) > 1 and sys.argv[1] == '--so-base':
        jobs = jobs[:1]
    os.makedirs(RUNS, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=int(os.environ.get('MUT_WORKERS', '6'))) as ex:
        for r in ex.map(lambda j: one_run(*j), jobs):
            results.append(r); print(r['name'], 'core rc', r['core']['rc'] if r['core'] else None, flush=True)
    json.dump(results, open(os.path.join(V3, 'mutacao', 'resultado_mutacao.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
