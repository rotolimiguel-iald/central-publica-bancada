"""Secondary GW250114 TEOB posterior robustness; never multiply by pSEOB.

Uses the two inspected numerical remnant functions in pinned pyRingGW 2.7.0
source. Only their elementary arithmetic AST is allowed to execute. The full
package, its CLI, and the release's notebooks are never executed. LAL's more
precise UIB2016 coefficients provide a distinct remnant-fit control.
"""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
from pathlib import Path
import ast
import hashlib
import inspect
import json
import math
import re
import sys
ROOT = Path(__file__).resolve().parent
os.environ['NUMBA_CACHE_DIR'] = str(ROOT/'cache/numba')
os.environ['QNMCACHEDIR'] = str(ROOT/'cache/qnm')
sys.path.insert(0, str(ROOT/'cache/vendor'))
import numpy as np
import qnm
from scipy.interpolate import CubicSpline
from scipy.optimize import fsolve
from scipy.stats import gaussian_kde
from lalinference.imrtgr import nrutils
from fetch_public import atomic_json
from posterior_220_readout import ratio_pair
from catalog_220_readout import local_support
from tgl_ringdown_prediction import prediction

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def checked_selected(manifest, suffix, directory):
    rows = manifest.get('sources', manifest.get('files'))
    row, = [r for r in rows if r['member'].endswith(suffix)]
    filename = re.split(r'[/\\]', row['path'])[-1]
    path = directory / filename
    if sha(path) != row['sha256']:
        raise ValueError('Changed pinned source: ' + str(path))
    return path, row

def numerical_remnant_functions(path):
    """Transcribe exactly two reviewed Cython arithmetic bodies, retaining coefficients."""
    text = path.read_text()
    names = ('_JimenezFortezaRemnantMass', '_JimenezFortezaRemnantSpin')
    pieces = []
    for name in names:
        match = re.search(r'^cdef double ' + name + r'\(([^\n]+)\) nogil:\n(.*?)(?=^cdef |\Z)',
                          text, re.M | re.S)
        if not match:
            raise ValueError('Missing named arithmetic function')
        body = re.sub(r'""".*?"""', '', match[2], flags=re.S)
        args = [v.strip().removeprefix('double ') for v in match[1].split(',')]
        lines = ['def ' + name + '(' + ', '.join(args) + '):']
        for line in body.splitlines():
            clean = line.split('#', 1)[0].strip()
            if not clean:
                continue
            if clean.startswith('cdef double '):
                clean = clean.removeprefix('cdef double ')
                if '=' not in clean:
                    continue
                # These inspected declarations contain only scalar arithmetic, no calls with commas.
                lines.extend('    ' + v.strip() for v in clean.split(','))
            else:
                lines.append('    ' + clean)
        pieces.append('\n'.join(lines))
    generated = '\n\n'.join(pieces) + '\n'
    tree = ast.parse(generated)
    allowed = (ast.Module, ast.FunctionDef, ast.arguments, ast.arg, ast.Assign,
               ast.Name, ast.Load, ast.Store, ast.BinOp, ast.UnaryOp, ast.Constant,
               ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.UAdd, ast.USub,
               ast.Call, ast.Return)
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            raise ValueError('Unexpected arithmetic AST: ' + type(node).__name__)
        if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name) and node.func.id == 'sqrt'):
            raise ValueError('Unexpected numerical function call')
    namespace = {'__builtins__': {}, 'sqrt': np.sqrt}
    exec(compile(tree, str(path) + ':two_reviewed_functions', 'exec'), namespace)
    return [namespace[n] for n in names], generated

def main():
    regpath = ROOT / 'REGISTRO_C4.json'
    reg = json.loads(regpath.read_bytes())
    receipt = ROOT.parent / 'TUNEL/DO_CHATGPT/ENTREGA_013_C4a_REGISTRO_POSTERIORES.md'
    if sha(regpath) not in receipt.read_text():
        raise ValueError('C4 registration differs from receipt')
    source_dir = ROOT / 'cache/source_distributions'
    sm = json.loads((source_dir / 'source_index.json').read_bytes())
    fitpath, fitrow = checked_selected(sm, '/eob_utils.pyx', source_dir / 'selected')
    priorpath, priorrow = checked_selected(sm, '/pyRing.py', source_dir / 'selected')
    wavepath, waverow = checked_selected(sm, '/waveform.pyx', source_dir / 'selected')
    # Pin the actual prior and fractional-time convention, rather than relying on names.
    prior_text = priorpath.read_text().split('class TEOBPMModel', 1)[1].split('def log_prior', 1)[0]
    if prior_text.count('bound = [-1.0,1.0]') != 2:
        raise ValueError('Inspected TEOB deformation priors changed')
    if 'alph1  = alph1 * (1.0/(1.0+dtau1))' not in wavepath.read_text():
        raise ValueError('Inspected fractional damping-time convention changed')
    release_dir = ROOT / 'cache/public/17018009'
    em = json.loads((release_dir / 'extraction_receipt.json').read_bytes())
    suffix = 'TEOB_22_21_33_44_55_domega_dtau_220_domega_dtau_440_0M_weighted_posterior/Nested_sampler/posterior.dat'
    path, row = checked_selected(em, suffix, release_dir / 'selected')
    s = np.genfromtxt(path, names=True)
    if any('weight' in n.lower() for n in s.dtype.names):
        raise ValueError('Explicit weights require a different estimator')
    functions, generated = numerical_remnant_functions(fitpath)
    mass1, mass2, chi1, chi2 = [s[k].copy() for k in ('m1', 'm2', 'chi1', 'chi2')]
    swap = mass1 < mass2
    mass1, mass2 = np.where(swap, mass2, mass1), np.where(swap, mass1, mass2)
    chi1, chi2 = np.where(swap, chi2, chi1), np.where(swap, chi1, chi2)
    total = mass1 + mass2
    x1, x2 = mass1 / total, mass2 / total
    nu = x1 * x2
    mass = functions[0](nu, x1, x2, chi1, chi2, total)
    spin = functions[1](nu, x1, x2, chi1, chi2)
    mass_lal = nrutils.bbh_final_mass_non_precessing_UIB2016(mass1, mass2, chi1, chi2)
    spin_lal = nrutils.bbh_final_spin_non_precessing_UIB2016(mass1, mass2, chi1, chi2)
    mass_equal = float(functions[0](.25, .5, .5, 0., 0., 1.))
    spin_equal = float(functions[1](.25, .5, .5, 0., 0.))
    # At equal mass and zero spin all unequal-spin and spin rational terms vanish.
    # Check against that independently simplified expression, not a guessed tolerance
    # between two different coefficient tables.
    equal_mass_oracle = 1 - (3.145/256 - .847/64 + .5610/16 + (1-2*math.sqrt(2)/3)/4)
    equal_spin_oracle = (1.3*(-9.49)/64 + 5.24*3.833/16 + 2*math.sqrt(3)/4)/(2.88*2.513/4+1)
    assert abs(mass_equal-equal_mass_oracle) < 1e-14
    assert abs(spin_equal-equal_spin_oracle) < 1e-14
    data = np.vstack([s['domega_220'], s['dtau_220']])
    if not np.all(np.isfinite(data)) or np.any(abs(data) >= 1.):
        raise ValueError('Posterior outside verified broad prior')
    grid = json.loads((ROOT / 'QNM_GRID.json').read_bytes())['modes']['220']
    interp = CubicSpline(grid['spins'], np.array(grid['real']) + 1j*np.array(grid['imag']), extrapolate=False)
    # Keep all samples. Under reversal of the spin axis, m also reverses.
    # For negative signed spin in the fixed m=+2 frame, qnm uses |a| and m=-2.
    # Independently check the frequency using the existing fixed-m Leaver solver
    # at signed a. Load only its four numerical definitions, never its file-writing loop.
    leaver_path = ROOT/'refeito/leaver_kerr.py'
    definitions = [n for n in ast.parse(leaver_path.read_text()).body
                   if isinstance(n, ast.FunctionDef) and n.name in ('cf','angular','radial','solve')]
    if len(definitions) != 4:
        raise ValueError('Leaver oracle definitions changed')
    oracle = dict(np=np, fsolve=fsolve, s=-2, l=2, m=2)
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(leaver_path), 'exec'), oracle)
    negative_checks = []
    def signed_modes(spins):
        values = interp(spins)
        negative_mode = qnm.modes_cache(s=-2, l=2, m=-2, n=0) if np.any(spins<0) else None
        for i in np.flatnonzero(spins<0):
            a = float(spins[i]); w = negative_mode(a=-a)[0]
            independent, _, residual = oracle['solve'](a/2, 2*w, 4.+0j)
            err = abs(independent/2-w)/abs(w)
            if err>1e-8 or residual>1e-8:
                raise ValueError('Negative-spin mode failed independent continued-fraction oracle')
            values[i] = w
            negative_checks.append(dict(index=int(i),spin=a,omega_real=float(w.real),
                                       omega_imag=float(w.imag),relative_error=float(err),residual=float(residual)))
        return values
    exact, exact_lal = signed_modes(spin), signed_modes(spin_lal)
    if not np.all(np.isfinite(exact)) or not np.all(np.isfinite(exact_lal)):
        raise ValueError('Remnant spins outside validated exact-QNM grid')
    rng = np.random.default_rng(13042100)
    test = rng.choice(len(s), min(5000, len(s)//5), replace=False)
    train = np.setdiff1d(np.arange(len(s)), test)
    kde = gaussian_kde(data[:, train])
    hpd = float(np.mean(kde.logpdf(data[:, test]) >= kde.logpdf([0, 0])[0]))
    support = local_support(data)
    rows = []
    for reading in ('R-B', 'R-RAIZ-0', 'R-LIN', 'R-MOD'):
        def shifts(masses, spins, modes, force_exact=False):
            return np.array([prediction(float(m), float(a), reading,
                              qnm_dimensionless=complex(w) if reading == 'R-MOD' or force_exact or a<0 else None)
                             ['delta_tau_ensemble_exact'] for m, a, w in zip(masses, spins, modes)])
        shift = shifts(mass, spin, exact)
        control = shifts(mass_lal, spin_lal, exact_lal)
        exact_shift = shifts(mass, spin, exact, True)
        if np.any(abs(shift) >= 1.):
            raise ValueError('Curve outside verified prior support')
        central, marginal = ratio_pair(data, shift)
        robust = [ratio_pair(data, shift, bw)[0] for bw in reg['KDE']['bandwidth_robustness_multipliers']]
        boot = []
        for _ in range(reg['KDE']['bootstrap_replicates']):
            ix = rng.integers(0, len(s), len(s))
            boot.append(ratio_pair(data[:, ix], shift[ix])[0])
        moved = data.copy(); moved[1] -= shift
        alt_support = local_support(moved)
        resolved = min(support['kernel_effective_samples'], alt_support['kernel_effective_samples']) >= 100
        verdict = 'NOT_EXCLUDED'
        if all(v <= -math.log(100) for v in robust) and hpd <= .95:
            verdict = 'EXCLUDED_IN_READING'
        if not resolved:
            verdict = 'INCONCLUSIVE_DENSITY_SUPPORT'
        if hpd > .95:
            verdict = 'INCONCLUSIVE_SYSTEMATICS'
        result = dict(reading=reading, lnB=central, lnB_tau_marginal=marginal,
             lnB_bandwidth=robust, lnB_bootstrap_025_50_975=np.quantile(boot, [.025,.5,.975]).tolist(),
             lnB_LAL_remnant_control=ratio_pair(data, control)[0],
             lnB_exact_QNM_control=ratio_pair(data, exact_shift)[0],
             shift_05_50_95=np.quantile(shift, [.05,.5,.95]).tolist(),
             support=alt_support, verdict=verdict,
             scope='SECONDARY_TEOB_220__440_FREE_IN_BOTH__NOT_INDEPENDENT_FROM_PSEOB')
        rows.append(result)
        print(json.dumps(result), flush=True)
    out = dict(status='SECONDARY_MODEL_ROBUSTNESS_CONDITIONAL_ON_PINNED_FIGURE_ENVIRONMENT',
        event='GW250114', N=len(s), registration_sha256=sha(regpath), posterior=row,
        posterior_weighting='Equal sample mass: released posterior.dat has no weight column; do not reweight by logL. Merger/resampling provenance is not reconstructed.',
        version_scope='pyRingGW 2.7.0 in released figure uv.lock; exact inference binary version not independently recorded',
        prior='Independent Uniform[-1,1] for all four deviations, verified in pinned TEOBPMModel',
        point_prior_density_ratio=1., no_duplicate_event=True, GR_HPD_content=hpd,
        signed_spin=dict(N_negative=int(np.sum(spin<0)),discarded=0,checks=negative_checks,
                         qnm_version=qnm.__version__,oracle_sha256=sha(leaver_path)),
        GR_HPD_test_N=len(test), GR_support=support,
        remnant_fit=dict(name='JimenezForteza pyRing 2.7.0 rounded active coefficients',
             source=fitrow, prior_source=priorrow, waveform_source=waverow,
             generated_arithmetic_sha256=hashlib.sha256(generated.encode()).hexdigest(),
             LAL_source_sha256=sha(Path(inspect.getfile(nrutils))),
             mass_relative_max_LAL=float(np.max(abs(mass/mass_lal-1))),
             spin_absolute_max_LAL=float(np.max(abs(spin-spin_lal))),
             equal_mass_nonspinning=dict(mass_fraction=mass_equal,spin=spin_equal)),
        quantiles={k:np.quantile(v,[.05,.5,.95]).tolist() for k,v in
                   [('Mf_detector',mass),('spin',spin),('df220',data[0]),('dtau220',data[1])]},
        rows=rows, code_sha256=sha(Path(__file__)),
        not_done=['Full 220+440 physical hypothesis', 'pyRing comparison at five late start times',
                  'Independent audit of weighted-posterior merging and original inference binary'],
        preserved_failures=['Initial guessed 1e-4 rounded-versus-LAL spin tolerance failed: 0.6864792261527318 vs 0.686369879389307. Replaced by an analytic equal-mass arithmetic oracle; coefficient differences propagated as controls.',
                            'Positive-only QNM grid refused three negative-spin samples. All retained with m-reversed exact QNM checked against signed-spin Leaver; BCW never extrapolated to negative spins.'])
    atomic_json(ROOT/'C4_PYRING.json', out)
    print(json.dumps({k:out[k] for k in ('N','GR_HPD_content','GR_support','quantiles','remnant_fit')}),flush=True)

if __name__ == '__main__':
    main()
