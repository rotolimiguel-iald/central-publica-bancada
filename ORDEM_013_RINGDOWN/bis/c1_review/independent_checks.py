"""Read-only C1/F1 audit. No import of production modules, qnm, or um.py.

Outputs are exclusively under this script's directory; existing files are refused.
Independent Decimal formulas and a fresh spectral/angular + radial residual check.
The standard radial recurrence is shared physics, not a novel method.
"""
from pathlib import Path
from decimal import Decimal as D, localcontext
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
import math
import os
import sys

os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ALPHA_FINE_CODATA_2018 = D('7.2973525693e-3')
PI = D('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651')
READINGS = {'R-A', 'R-B', 'R-MOD', 'R-RAIZ-0', 'R-RAIZ-EP4', 'R-RAIZ-REST', 'R-LIN', 'R-GLOBAL'}


def load(name):
    return json.loads((ROOT / name).read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dec(value):
    return D(str(value))


def error(got, expected):
    if expected == 0:
        return abs(float(got))
    return float(abs(dec(got) / dec(expected) - 1))


def quantities(mass, spin, redshift, reading, profile='modern', mode=None):
    """120-digit direct root differences, not production rationalization."""
    with localcontext() as ctx:
        ctx.prec = 120
        mass, spin, z = map(dec, (mass, spin, redshift))
        beta = ALPHA_FINE_CODATA_2018 * (D(1) / 2).exp()
        c = D(299792458)
        if profile == 'legacy':
            g, hbar, gm_sun = D('6.674e-11'), D('1.054571817e-34'), D('6.674e-11') * D('1.98892e30')
        else:
            g, hbar, gm_sun = D('6.67430e-11'), D('6.62607015e-34') / (2 * PI), D('1.3271244e20')
        tm = mass * gm_sun / c**3
        tp = (hbar * g / c**5).sqrt()
        if mode is None:
            wr = D('1.5251') - D('1.1568') * (1-spin)**D('0.1292')
            quality = D('.7') + D('1.4187') * (1-spin)**D('-.4990')
            wi = wr / (2 * quality)
        else:
            wr, wi = dec(mode[0]), -dec(mode[1])
        omega = wr / tm
        tau = tm / wi
        # First compute the dimensionless rate gamma * tM.
        if reading == 'R-A':
            star = tp * (1 if profile == 'legacy' else 1+z)
            rate_mass = beta * star / tm * wr**2 / 2
        elif reading == 'R-B':
            rate_mass = beta * wr**2 / 2
        elif reading == 'R-RAIZ-0':
            rate_mass = beta * wr / 2
        elif reading in ('R-RAIZ-EP4', 'R-RAIZ-REST'):
            if reading == 'R-RAIZ-EP4':
                omega0 = 1 / (4 * tp * (1+z))
            else:
                source_mass = mass * gm_sun / (g * (1+z))
                omega0 = source_mass * c**2 / (hbar * (1+z))
            gap = (omega0 + omega).sqrt() - omega0.sqrt()
            rate_mass = beta * gap**2 * tm / 2
        elif reading == 'R-LIN':
            rate_mass = beta * wr
        elif reading == 'R-MOD':
            root = (1-spin**2).sqrt()
            kappa_mass = root / (2*(1+root))
            nu_mass = wr - spin / (1+root)  # m=2
            if nu_mass <= 0:
                raise ValueError('Nonpositive corotating gap')
            rate_mass = PI * beta * nu_mass**2 / kappa_mass
        elif reading == 'R-GLOBAL':
            rate_mass = D(0)
        else:
            raise ValueError(reading)
        x = rate_mass / wi
        return {'Gamma_per_second': float(rate_mass/tm), 'Gamma_over_omega': float(rate_mass/wr),
                'delta_tau': float(-x/(1+x)), 't_mass': float(tm), 't_planck': float(tp),
                'tau': float(tau), 'omega': float(omega), 'x': float(x)}


def angular_eigenvalue(spin, frequency, max_l):
    """Matrix of cos(theta) in spin-weighted spherical harmonics, s=-2,m=2.

    qnm.angular documents the same spectral equation; no qnm code is imported.
    Building a larger cosine matrix before truncation retains the upper C^2 edge.
    """
    s, m = -2, 2
    ls = np.arange(2, max_l+2)
    cosine = np.diag(-m*s/(ls*(ls+1))).astype(complex)
    for j, ell in enumerate(ls[:-1]):
        k = ell + 1
        coeff = math.sqrt((k*k-m*m)*(k*k-s*s)/(k*k*(4*k*k-1)))
        cosine[j, j+1] = cosine[j+1, j] = coeff
    aw = spin * frequency
    mat = np.diag(ls*(ls+1)-s*(s+1)) + 2*aw*s*cosine - aw*aw*(cosine @ cosine)
    vals = np.linalg.eigvals(mat[:-1, :-1])
    return min(vals, key=lambda z: abs(z-4))


def radial_residual(spin, frequency, eigenvalue, depth):
    """Leaver recurrence, 2M=1 convention, evaluated bottom-up.

    Recurrence cross-checked against local refeito/leaver_kerr.py (read only)
    and qnm.radial public documentation. No root is fitted to the input value.
    """
    a, w = spin/2, 2*frequency
    s, m = -2, 2
    b = math.sqrt(1-4*a*a)
    x = w/2-a*m
    c0 = 1-s-1j*w-2j*x/b
    c1 = -4+2j*w*(2+b)+4j*x/b
    c2 = s+3-3j*w-2j*x/b
    c3 = w*w*(4+2*b-a*a)-2*a*m*w-s-1+(2+b)*1j*w-eigenvalue+(4*w+2j)*x/b
    c4 = s+1-2*w*w-(2*s+3)*1j*w-(4*w+2j)*x/b
    def coefficients(n):
        return (n*n+(c0+1)*n+c0, -2*n*n+(c1+2)*n+c3, n*n+(c2-3)*n+c4-c2+2)
    value = coefficients(depth)[1]
    for n in range(depth-1, -1, -1):
        al, be, _ = coefficients(n)
        value = be-al*coefficients(n+1)[2]/value
    return value


def mode_check(spin, pair):
    w = complex(*pair)
    a16 = angular_eigenvalue(spin, w, 16)
    a24 = angular_eigenvalue(spin, w, 24)
    return {'spin': spin, 'omega': pair,
            'angular_16_vs_24_abs': float(abs(a16-a24)),
            'radial_abs_depth400': float(abs(radial_residual(spin, w, a24, 400))),
            'radial_abs_depth800': float(abs(radial_residual(spin, w, a24, 800))),
            'perturbed_omega_residual': float(abs(radial_residual(spin, w+1e-4, angular_eigenvalue(spin,w+1e-4,24),800)))}


def main():
    output = HERE / 'independent_results.json'
    if output.exists():
        raise FileExistsError(output)
    num = load('bis/C1_NUMERICAL_CONTROLS.json')
    v1, v2 = load('C1_LEITURAS.json'), load('C1_LEITURAS_v2.json')
    primary = load('bis/C1_PRIMARY_RETRIEVALS.json')
    inputs = set(num['dependencies']) | {
        'C1_LEITURAS_v2.json','C1_ADENDO_CORRECOES_013BIS.md','REAPROVEITAMENTO_C1.md',
        'refeito/record_c1_013bis.py','bis/C1_NUMERICAL_CONTROLS.json','bis/C1_PRIMARY_RETRIEVALS.json',
        'QNM_GRID.json','C1_TABLES.json','complete_c1_contract.py','refeito/leaver_kerr.py',
        'cache/literature/013bis/bisognano_wichmann_1975.txt',
        'cache/literature/013bis/bisognano_wichmann_1976.txt',
    }
    inputs.update('cache/literature/013bis/'+row['name'] for row in primary if row.get('sha256'))
    for row in v2['rows']:
        inputs.update(item['path'] for item in row.get('sources', []))
    inputs.update(item['path'] for item in v2['source_references'].values())
    before = {name: digest(ROOT/name) for name in sorted(inputs)}
    integrity = [{'path': name, 'expected': value, 'actual': before[name], 'match': value==before[name]}
                 for name, value in num['dependencies'].items()]
    for row in primary:
        if row.get('sha256'):
            path = 'cache/literature/013bis/'+row['name']
            integrity.append({'path': path, 'expected': row['sha256'], 'actual': before[path],
                              'match': row['sha256']==before[path], 'bytes_match': (ROOT/path).stat().st_size==row['bytes']})
    for key in ('numerical_controls','primary_retrievals','clock_evidence','numerical_source'):
        item=v2[key]; path=Path(item['path'])
        path=path if path.is_absolute() else ROOT/path
        integrity.append({'path': str(path), 'match': digest(path)==item['sha256']})
    integrity.append({'path': 'C1_LEITURAS.json', 'match': before['C1_LEITURAS.json']==v2['supersedes_sha256']})
    core = load('cache/casa/um_absoluto.json')['core']['clock_test_result_v369']
    flags = {'P1': core['P1']['verdict'], 'P2': core['P2']['verdict'],
             'R_MOD_unruh_g': core['tau_star_alternatives']['unruh_g_excluded'],
             'P2_bound_stored': core['P2']['tau_star_bound_if_reading_in_tP'],
             'P2_bound_recomputed': core['P2']['gamma_upper_bound_s_median_with_cal']/core['gamma_s'],
             'P2_bound_note': core['P2']['gamma_upper_bound_note']}
    for name in ('R-A','R-RAIZ-EP4'):
        row=next(x for x in v2['rows'] if x['reading']==name)
        assert row['excluded_if_universal_P1_matter'] is False
        assert row['excluded_if_universal_P2_independent_arm_light_modes'] is True
        assert row['P2_tau_star_bound_in_tP']==flags['P2_bound_stored']
    assert flags['P1']=='P1_NOT_FALSIFIED_UNDERPOWERED' and flags['P2']=='P2_EXCLUDED_IN_READING'
    assert next(x for x in v2['rows'] if x['reading']=='R-MOD')['excluded_if_universal'] is flags['R_MOD_unruh_g'] is True
    assert v2['hypothesis_selected'] is False
    assert all(row['physical_selection'] is None and row['relation_to_operator_16Sep'] is None for row in v2['rows'])
    cat = load('C4_CATALOG_220.json')
    with (ROOT/'C7_INDEPENDENT/tables/event_reading_predictions.csv').open(encoding='utf-8-sig',newline='') as f:
        table=list(csv.DictReader(f))
    keys=[(r['event'],r['reading']) for r in table]
    events=[e['event'] for e in cat['rows']]
    assert len(events)==len(set(events))==33
    assert len(keys)==len(set(keys))==264
    assert set(keys)=={(event,reading) for event in events for reading in READINGS}
    by_key={k:r for k,r in zip(keys,table)}
    checks=[]; catalog_modes=[]
    for event in cat['rows']:
        mass,spin,z=[event['quantiles'][k][1] for k in ('mass_detector','spin','redshift')]
        assert {row['reading'] for row in event['rows']}==READINGS
        for row in event['rows']:
            name=row['reading']; mode=None
            if name=='R-MOD':
                p=row['median_prediction']
                mode=[p['omega_mass'],-p['t_mass_s']/p['tau_gr_s']]
                catalog_modes.append({'event':event['event'],**mode_check(spin,mode)})
            fresh=quantities(mass,spin,z,name,mode=mode)
            public=by_key[event['event'],name]
            errors={key:error(fresh[key],float(public[key])) for key in ('Gamma_per_second','Gamma_over_omega','delta_tau')}
            assert all(math.isfinite(float(public[key])) for key in errors)
            checks.append({'event':event['event'],'reading':name,'independent':{key:fresh[key] for key in errors},
                           'relative_errors':errors,'sub_resolution':abs(fresh['delta_tau'])<1e-6})
    spin_results=[]
    for row in num['spin_comparison']:
        spin=row['spin']; mode=row['exact_qnm']
        mod=quantities(68.287,spin,0,'R-MOD',mode=mode)
        root=quantities(68.287,spin,0,'R-RAIZ-0',mode=mode)
        wr=1.5251-1.1568*(1-spin)**.1292
        quality=.7+1.4187*(1-spin)**(-.499)
        bcw=quantities(68.287,spin,0,'R-MOD',mode=[wr,-wr/(2*quality)])
        measured={'delta_mod':mod['delta_tau'],'delta_root_zero':root['delta_tau'],
                  'delta_mod_bcw_control':bcw['delta_tau'],
                  'mod_bcw_relative_error':bcw['delta_tau']/mod['delta_tau']-1}
        spin_results.append({**mode_check(spin,mode),**measured,
                             'max_absolute_difference_recorded':max(abs(value-row[key]) for key,value in measured.items())})
    profiles=[]
    for row in num['profile_comparison']:
        legacy=quantities(68.287,.6785,0,row['reading'],'legacy')
        modern=quantities(68.287,.6785,0,row['reading'])
        values={key:legacy[col]/modern[col]-1 for key,col in (
            ('gamma_legacy_over_modern_minus_one','Gamma_per_second'),
            ('delta_legacy_over_modern_minus_one','delta_tau'))}
        profiles.append({'reading':row['reading'],**values,
                         'max_absolute_difference_recorded':max(abs(value-row[key]) for key,value in values.items())})
    # Independent SI rescaling: length u, mass v, time t; constants transform accordingly.
    # Numeric homogeneity tests exercise complete expressions with Planck/rest offsets.
    beta=float(ALPHA_FINE_CODATA_2018)*math.sqrt(math.e)
    def dimension_samples(mass_scale,length_scale,time_scale):
        g=6.67430e-11*length_scale**3/mass_scale/time_scale**2
        c=299792458*length_scale/time_scale
        hb=6.62607015e-34/(2*math.pi)*mass_scale*length_scale**2/time_scale
        mass=1.35e32*mass_scale; omega=1600/time_scale
        tm=g*mass/c**3; tp=math.sqrt(hb*g/c**5)
        oh=.2/tm; kap=.1/tm; nu=omega-2*oh
        offset_ep=1/(4*tp); offset_rest=mass*c*c/hb
        root_rate=lambda base: beta*omega*omega/(2*(math.sqrt(base+omega)+math.sqrt(base))**2)
        return {'R-A':beta*tp*omega**2/2,'R-B':beta*tm*omega**2/2,
                'R-MOD':math.pi*beta*nu**2/kap,'R-RAIZ-0':beta*omega/2,
                'R-RAIZ-EP4':root_rate(offset_ep),'R-RAIZ-REST':root_rate(offset_rest),
                'R-RAIZ-COHERENT':beta*omega/(8*1e8),'R-LIN':beta*omega,
                'R-PROP':beta*tp*omega**2/2*(.1/(2.2e-18/time_scale))}
    dim_base=dimension_samples(1,1,1); dimensional=[]
    for m,l,t in ((3,5,7),(.2,13,.7),(11,.4,19)):
        changed=dimension_samples(m,l,t)
        dimensional.append({'scales_mass_length_time':[m,l,t],
            'errors':{name:error(value,dim_base[name]*(1 if name=='R-PROP' else 1/t)) for name,value in changed.items()}})
    # Finite conditional modular generator: adjacent coherence and Gibbs positivity.
    kappa,nu=.17,.29
    eigenvalues=2*math.pi*nu/kappa*np.arange(4)
    K=np.diag(eigenvalues); rho=np.zeros((4,4)); rho[1,2]=1
    comm=K@rho-rho@K
    derivative=-beta/2*(K@comm-comm@K)*kappa/(2*math.pi)
    modular={'adjacent_rate':float(-derivative[1,2]),'analytic_rate':math.pi*beta*nu**2/kappa,
             'finite_matrix_residual':float(abs(derivative[1,2]+math.pi*beta*nu**2/kappa)),
             'gibbs_ratio_positive_zero_negative':[math.exp(-2*math.pi*v/kappa) for v in (nu,0,-nu)],
             'scope':'CONDITIONAL_EFFECTIVE_OSCILLATOR__NOT_QNM_QUANTIZATION_OR_KERR_STATE'}
    counts=Counter(row['reading'] for row in checks if row['sub_resolution'])
    report={'status':'INDEPENDENT_NUMERICAL_REVIEW__SCOPE_C1_F1',
            'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'numpy':np.__version__,
            'method':'No production import. Decimal 120-digit formulas, independent QNM residuals, SI rescalings.',
            'script_sha256':digest(Path(__file__)),'inputs_before':before,'integrity':integrity,'flags':flags,
            'csv':{'checked':len(checks),'unique_events':len(events),'unique_keys':len(set(keys)),
                   'sub_resolution_by_reading':dict(counts),'sub_resolution_total':sum(counts.values()),
                   'nonzero_sub_resolution':sum(n for k,n in counts.items() if k!='R-GLOBAL'),
                   'max_relative_error':max(max(row['relative_errors'].values()) for row in checks),'rows':checks},
            'spin':spin_results,'catalog_mode_residuals':catalog_modes,'profiles':profiles,
            'dimensions':dimensional,'modular':modular,
            'external_formula_sources':['https://qnm.readthedocs.io/en/latest/_modules/qnm/angular.html',
                                        'https://qnm.readthedocs.io/en/latest/_modules/qnm/radial.html'],
            'limitations':['Catalog QNM inputs are the archived/interpolated medians; residuals are independently evaluated.',
                           'Residual smallness is a consistency test, not a rigorous error bound or a quantum-state construction.',
                           'No posterior, likelihood, PE, injections, um.py execution, kernel build, or memory update.']}
    after={name:digest(ROOT/name) for name in sorted(inputs)}
    report['inputs_unchanged']=before==after
    report['input_changes']={name:[before[name],after[name]] for name in before if before[name]!=after[name]}
    report['all_integrity_matches']=all(row['match'] and row.get('bytes_match',True) for row in integrity)
    report['numeric_acceptance']=(report['csv']['max_relative_error']<1e-12
        and all(row['radial_abs_depth800']<1e-9 for row in spin_results)
        and all(row['max_absolute_difference_recorded']<1e-12 for row in profiles)
        and all(max(row['errors'].values())<1e-12 for row in dimensional))
    raw=(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    temp=output.with_suffix('.json.tmp')
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes()==raw and len(raw)>0
    if output.exists():
        raise FileExistsError(output)
    temp.rename(output)
    print(json.dumps({k:report[k] for k in ('status','all_integrity_matches','numeric_acceptance','inputs_unchanged')},indent=2))
    print('CSV',len(checks),report['csv']['max_relative_error'],dict(counts))
    print('QNM max residual: spin',max(x['radial_abs_depth800'] for x in spin_results),
          'catalog',max(x['radial_abs_depth800'] for x in catalog_modes))
    print('RESULT_SHA256',digest(output))


if __name__=='__main__':
    main()
