# mutar.py — RODADA 2 (v3.1): mutação campo a campo (campo := True) no TIPO `ContratoQG_v31.lean`, medindo
#   (a) MORDIDA: erros de probes NEGATIVOS que DESAPARECEM (o dente sai) — resposta ao cético D-A;
#   (b) QUEBRA: teoremas/paredes/probes POSITIVOS que passam a errar ou a depender de sorryAx.
# Só escreve em v31/mutacao/runs. LEAN_PATH = RUN ; refolean (v2/W5/brinquedo, não dependem do tipo) ; v3 (só
# leitura, para a Ponte) ; kernel v370. O diretório v31 NÃO entra no LEAN_PATH (evita cair no olean não-mutado
# quando um arquivo da rodada falha). Nunca lake build; find -newer no kernel em cada compilação.
import os, re, shutil, subprocess, json, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
V31 = os.path.dirname(HERE)
RUNS = os.path.join(HERE, 'runs')
REF = os.path.join(V31, 'refolean')
V3 = os.path.join(os.path.dirname(V31), 'v3')
KERNEL = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
STAMP_R2 = os.path.join(V31, 'logs', '.STAMP_INICIO_R2')
CORE = 'ContratoQG_v31.lean'
STAGE1 = ['ContratoQG_v31_Teoremas.lean', 'ProbeToyV31.lean', 'ProbeLegacyV31.lean', 'ProbeVacuousImportV31.lean',
          'ProbeTrivialH3v31.lean', 'ProbeAjustadorV31.lean', 'ProbeRekappaV31.lean', 'ProbeResidualH3v31.lean']
STAGE2 = ['ContratoQG_v31_Paredes.lean', 'FlagNetV31.lean', 'PonteV3V31.lean']
NEG = ['ProbeToyV31.lean', 'ProbeLegacyV31.lean', 'ProbeVacuousImportV31.lean', 'ProbeTrivialH3v31.lean',
       'ProbeAjustadorV31.lean', 'ProbeRekappaV31.lean']
POS = ['ContratoQG_v31_Teoremas.lean', 'ContratoQG_v31_Paredes.lean', 'FlagNetV31.lean', 'PonteV3V31.lean',
       'ProbeResidualH3v31.lean']
PROP_FIELDS = {
 'WedgeBoostRep': ['V_zero', 'V_add', 'V_continuous', 'V_vac', 'V_translations', 'V_net'],
 'KillingNormalization': ['point_in_wedge'],
 'ContratoH2': ['kappa_pos', 'flow_implemented', 'kms', 'bw', 'translations_continuous', 'translations_faithful',
                'positive_energy', 'null_ergodic', 'observer_unit', 'smooth_on', 'det_unit_on', 'dragged',
                'fiducial_is_modular'],
 'StressTensorData': ['T_vac', 'T_covariant'],
 'ContratoH3': ['G_pos', 'admissible_unit', 'vac_admissible', 'admissible_translate', 'modular_charge',
                'admissible_nontrivial', 'energy_continuous', 'background_screen_flat', 'propagator_zero',
                'propagator_covariant', 'response_symm', 'lightcone_gauge', 'theta_is_expansion',
                'raychaudhuri_einstein'],
 'ContratoImportH3': ['same_horizon'],
}

sys.path.insert(0, V31)
from sitios import errs  # noqa: E402

def lake_lean_path():
    r = subprocess.run(['bash', '-c', 'cd "/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel" && lake env printenv LEAN_PATH'],
                       capture_output=True)
    return r.stdout.decode('utf-8').strip()

LP = lake_lean_path()

def mutate(lines, struct, field):
    i0 = next(i for i, l in enumerate(lines) if re.match(r'^structure %s\b' % re.escape(struct), l))
    j = i0
    while not lines[j].rstrip().endswith('where'):
        j += 1
    k = j + 1
    while k < len(lines) and lines[k].strip() != '' and lines[k].startswith('  '):
        k += 1
    fs = next(i for i in range(j + 1, k) if re.match(r'^  %s :' % re.escape(field), lines[i]))
    fe = fs + 1
    while fe < k and re.match(r'^    ', lines[fe]):
        fe += 1
    return lines[:fs] + ['  %s : True\n' % field] + lines[fe:], (fs + 1, fe)

def newer_count():
    r = subprocess.run(['bash', '-c', 'find "/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel" -newer "%s" -type f | wc -l'
                        % STAMP_R2.replace('\\', '/')], capture_output=True)
    return r.stdout.decode('utf-8').strip()

def comp(run, f):
    base = f[:-5]
    log = os.path.join(run, 'log_' + base + '.txt')
    env = dict(os.environ)
    env['LEAN_PATH'] = ';'.join([run, REF, V3, LP])
    with open(log, 'w', encoding='utf-8') as fh:
        p = subprocess.run(['lean', '-R', run, '-o', os.path.join(run, base + '.olean'), '-i',
                            os.path.join(run, base + '.ilean'), os.path.join(run, f)],
                           cwd=KERNEL, env=env, stdout=fh, stderr=subprocess.STDOUT)
    with open(log, 'a', encoding='utf-8') as fh:
        fh.write('\nrc=%d\n' % p.returncode)
    return p.returncode

def one(name, struct=None, field=None):
    run = os.path.join(RUNS, name)
    if os.path.exists(run):
        shutil.rmtree(run)
    os.makedirs(run)
    src = open(os.path.join(V31, CORE), encoding='utf-8').read().split('\n')
    src = [l + '\n' for l in src[:-1]] + [src[-1]]
    span = None
    if struct:
        src, span = mutate(src, struct, field)
    open(os.path.join(run, CORE), 'w', encoding='utf-8', newline='\n').write(''.join(src))
    for f in STAGE1 + STAGE2:
        shutil.copyfile(os.path.join(V31, f), os.path.join(run, f))
    comp(run, CORE)
    res = {'name': name, 'struct': struct, 'field': field, 'span': span}
    if os.path.exists(os.path.join(run, CORE[:-5] + '.olean')):
        with ThreadPoolExecutor(max_workers=len(STAGE1)) as ex:
            list(ex.map(lambda f: comp(run, f), STAGE1))
        if os.path.exists(os.path.join(run, 'ContratoQG_v31_Teoremas.olean')):
            with ThreadPoolExecutor(max_workers=len(STAGE2)) as ex:
                list(ex.map(lambda f: comp(run, f), STAGE2))
            res['stage2'] = 'rodou'
        else:
            res['stage2'] = 'BLOQUEADO (Teoremas não compilou)'
    else:
        res['stage2'] = 'BLOQUEADO (núcleo não compilou)'
    for f in [CORE] + STAGE1 + STAGE2:
        res[f] = errs(os.path.join(run, f), os.path.join(run, 'log_' + f[:-5] + '.txt'))
    res['kernel_newer_than_R2_start'] = newer_count()
    for fn in os.listdir(run):
        if fn.endswith('.olean') or fn.endswith('.ilean'):
            os.remove(os.path.join(run, fn))
    return res

if __name__ == '__main__':
    jobs = [('BASE', None, None)] + [(f'{s}__{f}', s, f) for s in PROP_FIELDS for f in PROP_FIELDS[s]]
    if len(sys.argv) > 1:
        jobs = [j for j in jobs if j[0] in sys.argv[1:]]
    os.makedirs(RUNS, exist_ok=True)
    out = []
    prog = open(os.path.join(HERE, 'progresso.txt'), 'w', encoding='utf-8')
    with ThreadPoolExecutor(max_workers=int(os.environ.get('W', '4'))) as ex:
        for r in ex.map(lambda j: one(*j), jobs):
            out.append(r)
            prog.write('%s core_rc=%s stage2=%s kt=%s\n' % (r['name'], r[CORE]['rc'], r.get('stage2'),
                                                           r['kernel_newer_than_R2_start']))
            prog.flush()
    prog.write('FIM\n'); prog.close()
    fn = 'resultado_mutacao.json' if len(sys.argv) == 1 else 'resultado_parcial.json'
    json.dump(out, open(os.path.join(HERE, fn), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
