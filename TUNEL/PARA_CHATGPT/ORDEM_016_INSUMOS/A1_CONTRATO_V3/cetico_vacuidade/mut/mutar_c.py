# mutar_c.py — cético 2: mutação campo a campo (campo := True) medindo MORDIDA em probes negativos e
# QUEBRA em teoremas (inclusive Paredes, FlagNet e os dois arquivos do cético). Só escreve em cetico_vacuidade/mut.
import os, re, shutil, subprocess, json, sys
from concurrent.futures import ThreadPoolExecutor
CV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(CV, 'src'); RUNS = os.path.join(CV, 'mut', 'runs')
CORE = 'ContratoQG_v3.lean'
STAGE1 = ['ContratoQG_v3_Teoremas.lean', 'ProbeToyV3.lean', 'ProbeLegacyV3.lean', 'ProbeVacuousImportV3.lean', 'ProbeTrivialH3v3.lean']
STAGE2 = ['ContratoQG_v3_Paredes.lean', 'FlagNetV3.lean', 'ProbeAjusteH3v3.lean', 'CeticoKappaGauge.lean', 'CeticoH3Ajuste.lean']
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
def win(p): return os.path.abspath(p).replace('/', chr(92))
def mutate(lines, struct, field):
    i0 = next(i for i, l in enumerate(lines) if re.match(r'^structure %s\b' % re.escape(struct), l))
    j = i0
    while not lines[j].rstrip().endswith('where'): j += 1
    k = j + 1
    while k < len(lines) and lines[k].strip() != '' and (lines[k].startswith('  ')): k += 1
    fs = next(i for i in range(j + 1, k) if re.match(r'^  %s :' % re.escape(field), lines[i]))
    fe = fs + 1
    while fe < k and re.match(r'^    ', lines[fe]): fe += 1
    return lines[:fs] + ['  %s : True\n' % field] + lines[fe:], (fs + 1, fe)
def comp(run, f):
    subprocess.run(['bash', os.path.join(CV, 'mut', 'mc.sh'), win(run), f, os.path.join(run, 'log_' + f[:-5] + '.txt')],
                   capture_output=True, text=True)
def sites(path):
    out = {}; decl = None; fld = None
    for n, l in enumerate(open(path, encoding='utf-8').read().split('\n'), start=1):
        m = re.match(r'^(?:private |protected |noncomputable )*(theorem|def|lemma|abbrev|instance|example)\s+([^\s(:{\[]*)', l)
        if m: decl = m.group(2) or m.group(1); fld = None
        m2 = re.match(r'^  ([A-Za-zΔ_][\w\'Δ]*) :=', l)
        if m2 and decl is not None: fld = m2.group(1)
        out[n] = decl + ('.' + fld if fld else '') if decl else '?'
    return out
def errs(run, f):
    p = os.path.join(run, 'log_' + f[:-5] + '.txt')
    s = open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else ''
    st = sites(os.path.join(run, f))
    e = sorted(set(st.get(int(m.group(1)), '?') for m in re.finditer(re.escape(f) + r':(\d+):\d+: error', s)))
    rc = re.findall(r'rc=(\d+)', s)
    sorry = sorted(set(re.findall(r"'([^']+)' depends on axioms: \[[^\]]*sorryAx", s, re.S)))
    return {'rc': int(rc[-1]) if rc else None, 'errors': e, 'sorry_decls': sorry, 'oom': 'bad_alloc' in s,
            'kt': re.findall(r'kernel_files_newer_than_stamp=(\d+)', s)}
def one(name, struct=None, field=None):
    run = os.path.join(RUNS, name)
    if os.path.exists(run): shutil.rmtree(run)
    os.makedirs(run)
    src = open(os.path.join(SRC, CORE), encoding='utf-8').read().split('\n')
    src = [l + '\n' for l in src[:-1]] + [src[-1]]
    span = None
    if struct: src, span = mutate(src, struct, field)
    open(os.path.join(run, CORE), 'w', encoding='utf-8', newline='\n').write(''.join(src))
    for f in STAGE1 + STAGE2: shutil.copyfile(os.path.join(SRC, f), os.path.join(run, f))
    comp(run, CORE)
    with ThreadPoolExecutor(max_workers=len(STAGE1)) as ex: list(ex.map(lambda f: comp(run, f), STAGE1))
    with ThreadPoolExecutor(max_workers=len(STAGE2)) as ex: list(ex.map(lambda f: comp(run, f), STAGE2))
    res = {'name': name, 'struct': struct, 'field': field, 'span': span}
    for f in [CORE] + STAGE1 + STAGE2: res[f] = errs(run, f)
    for fn in os.listdir(run):
        if fn.endswith('.olean') or fn.endswith('.ilean'): os.remove(os.path.join(run, fn))
    return res
if __name__ == '__main__':
    jobs = [('BASE', None, None)] + [(f'{s}__{f}', s, f) for s in PROP_FIELDS for f in PROP_FIELDS[s]]
    if len(sys.argv) > 1: jobs = [j for j in jobs if j[0] in sys.argv[1:]]
    os.makedirs(RUNS, exist_ok=True)
    out = []
    with ThreadPoolExecutor(max_workers=int(os.environ.get('W', '3'))) as ex:
        for r in ex.map(lambda j: one(*j), jobs):
            out.append(r); print(r['name'], r[CORE]['rc'], flush=True)
    json.dump(out, open(os.path.join(CV, 'mut', 'resultado_c.json' if len(sys.argv) == 1 else 'resultado_c_parcial.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
