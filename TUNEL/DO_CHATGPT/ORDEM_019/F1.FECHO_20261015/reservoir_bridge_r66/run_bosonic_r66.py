"""One preregistered check of compatible excitation cuts; no original imports."""
from pathlib import Path
import ast
import datetime as dt
import hashlib
import json
import math
import os
import sys
import time

ROOT = Path(__file__).resolve().parent

def pin(p):
    p = Path(p).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def put(name, data):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n'); f.flush(); os.fsync(f.fileno())

def main():
    plan_path = ROOT / 'PLAN_BOSONIC_R66.json'
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    review = json.loads((ROOT / 'PREEXEC_REVIEW_BOSONIC_R66.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS') and review['reviewer'] != 'codex-gerente-tgl'
    assert pin(plan_path) in review['evidence'] and pin(__file__) in review['evidence']
    for row in review['evidence'] + plan['evidence']:
        assert pin(row['path']) == row, 'Pin mismatch before any execution'
    for name in ['FREEZE_BOSONIC_R66.json', 'START_BOSONIC_R66.json', 'RESULT_BOSONIC_R66.json']:
        assert not (ROOT / name).exists(), 'Run already initiated; do not repeat'
    import support_r66 as s
    s.preflight('R5', 'EXEC_BOSONIC_R66')
    put('FREEZE_BOSONIC_R66.json', {'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'plan': pin(plan_path), 'runner': pin(__file__), 'review': pin(ROOT/'PREEXEC_REVIEW_BOSONIC_R66.json')})
    started = dt.datetime.now(dt.timezone.utc).isoformat(); tick = time.perf_counter()
    put('START_BOSONIC_R66.json', {'utc': started, 'command': [sys.executable, '-B', '-X', 'utf8', __file__]})
    try:
        import numpy as np
        import scipy
        from scipy import sparse as sp
        from scipy.sparse.linalg import expm_multiply
        original = json.loads(Path(plan['r62_plan']).read_text(encoding='utf-8'))
        for row in original['source_pins']:
            assert pin(row['path'])['sha256'] == row['sha256']
        alpha_path = next(row['path'] for row in original['source_pins'] if 'ALPHA_FINE_CODATA_2018' in row['role'])
        constants = {}
        for node in ast.parse(Path(alpha_path).read_text(encoding='utf-8')).body:
            if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in {'ALPHA_FINE_CODATA_2018','_SEALED_ALPHA_CODATA_2018'}:
                    constants[node.targets[0].id] = ast.literal_eval(node.value)
        assert constants['ALPHA_FINE_CODATA_2018'] == constants['_SEALED_ALPHA_CODATA_2018']
        beta = constants['ALPHA_FINE_CODATA_2018'] * math.sqrt(math.e)
        p = original['model']['parameters']; lam = beta * original['model']['gamma_Lambda']
        checks = []; states = []; residuals = []
        def check(name, value, limit, negative=False):
            value = float(value); assert math.isfinite(value)
            checks.append({'id': name, 'value': value, 'limit': limit,
                           'pass': value > limit if negative else value <= limit})
        def norm(x):
            return float(np.linalg.norm(x.toarray() if sp.issparse(x) else x))
        def liou(h, jumps):
            d = len(h); eye = sp.eye(d, format='csr')
            h = sp.csr_matrix(h)
            out = -1j*(sp.kron(eye,h)-sp.kron(h.T,eye))
            for l in jumps:
                l=sp.csr_matrix(l); q=l.conj().T@l
                out += sp.kron(l.conj(),l)-.5*sp.kron(eye,q)-.5*sp.kron(q.T,eye)
            return out.tocsr()
        def model(m):
            basis=[(i,o,e) for i in range(m+1) for o in range(m+1-i) for e in (0,1) if i+o+e<=m]
            d=len(basis); index={b:k for k,b in enumerate(basis)}
            ai=np.zeros((d,d),complex); ao=ai.copy(); sm=ai.copy()
            for col,(i,o,e) in enumerate(basis):
                if i: ai[index[(i-1,o,e)],col]=math.sqrt(i)
                if o: ao[index[(i,o-1,e)],col]=math.sqrt(o)
                if e: sm[index[(i,o,0)],col]=1
            plus=sm.conj().T
            n_i=np.diag([b[0] for b in basis]); n_o=np.diag([b[1] for b in basis]); n_e=np.diag([b[2] for b in basis])
            N=n_i+n_o+n_e; Z=np.eye(d)-2*n_e
            h0=p['omega_c']*(n_i+n_o)+p['omega_OH']*n_e+p['g_JC']*(ai.conj().T@sm+plus@ai)
            drive=p['Omega']*(plus+sm)
            A=ao.conj().T@sm; B=plus@ai; J=A+B
            jumps=[math.sqrt(p['kappa_in'])*ai,math.sqrt(p['kappa_out'])*ao,
                   math.sqrt(p['gamma_OH'])*sm,math.sqrt(p['gamma_dephasing'])*Z,math.sqrt(lam)*J]
            return {'basis':basis,'index':index,'ai':ai,'N':N,'J':J,'A':A,'B':B,'h0':h0,
                    'g0':liou(h0,jumps),'g':liou(h0+drive,jumps),'jumps':jumps,'drive':drive}
        def include(a,b):
            v=np.zeros((len(b['basis']),len(a['basis'])),complex)
            for k,x in enumerate(a['basis']): v[b['index'][x],k]=1
            return v
        models={m:model(m) for m in plan['cuts']}
        for m,mod in models.items():
            check(f'dimension_{m}',abs(len(mod['basis'])-(m+1)**2),0)
            for key in ['J','h0']:
                check(f'N_commutes_{key}_{m}',norm(mod['N']@mod[key]-mod[key]@mod['N']),plan['algebra_tol'])
        for m,n in plan['compatible_pairs']:
            a,b=models[m],models[n]; v=include(a,b); E=sp.kron(v.conj(),v,format='csr')
            check(f'all_matrix_units_unpumped_{m}_{n}',norm(b['g0']@E-E@a['g0']),plan['algebra_tol'])
            check(f'negative_pumped_cut_not_invariant_{m}_{n}',norm(b['g']@E-E@a['g']),plan['negative_threshold'],True)
        base=models[2]; v0=np.zeros(len(base['basis']),complex)
        v0[base['index'][(2,0,0)]]=1/math.sqrt(2); v0[base['index'][(1,0,1)]]=1j/math.sqrt(2)
        rho0=np.outer(v0,v0.conj()); n0=float(np.trace(rho0@base['N']).real)
        evolved={}
        for m in plan['evolution_cuts']:
            mod=models[m]; v=include(base,mod); rho=v@rho0@v.conj().T
            for t in plan['times']:
                final=expm_multiply(mod['g']*t,rho.reshape(-1,order='F')).reshape(rho.shape,order='F')
                evolved[m,t]=final
                tr=complex(np.trace(final)); min_eig=float(np.linalg.eigvalsh((final+final.conj().T)/2).min())
                moment=float(np.trace(final@mod['N']).real)
                check(f'finite_{m}_{t}',0 if np.isfinite(final).all() else 1,0)
                check(f'trace_{m}_{t}',abs(tr-1),plan['state_tol'])
                check(f'hermitian_{m}_{t}',norm(final-final.conj().T),plan['state_tol'])
                check(f'positive_{m}_{t}',max(0,-min_eig),plan['state_tol'])
                check(f'energy_bound_{m}_{t}',max(0,moment-n0-abs(p['Omega'])*t),plan['state_tol'])
                states.append({'cut':m,'t':t,'min_eigenvalue':min_eig,'mean_N':moment,'trace':[tr.real,tr.imag]})
        high=plan['evolution_cuts'][-1]
        for m in plan['evolution_cuts'][:-1]:
            v=include(models[m],models[high])
            for t in plan['times']:
                delta=evolved[high,t]-v@evolved[m,t]@v.conj().T
                error=float(np.linalg.svd(delta,compute_uv=False).sum())
                x=2*abs(p['Omega'])*t; first=m-plan['initial_max_N']+1
                # Positive tail sum avoids subtractive cancellation near zero.
                bound=2*sum(x**k/math.factorial(k) for k in range(first,70))
                check(f'dyson_tail_cut_{m}_{high}_{t}',error,bound+plan['state_tol'])
                residuals.append({'cut':m,'reference_cut':high,'t':t,'trace_norm_difference':error,'analytic_bound':bound})
        mod=models[2]
        amp=abs(mod['ai'][mod['index'][(1,0,0)],mod['index'][(2,0,0)]])
        check('bosonic_sqrt_two',abs(amp-math.sqrt(2)),plan['algebra_tol'])
        check('negative_hardcore_cannot_lower_two',amp,plan['negative_threshold'],True)
        split=liou(mod['h0']+mod['drive'],mod['jumps'][:-1]+[math.sqrt(lam)*mod['A'],math.sqrt(lam)*mod['B']])
        check('negative_independent_reservoir_changes_generator',norm(split-mod['g']),plan['negative_threshold'],True)
        result={'status':'PASS_BOSONIC_COMPATIBILITY_AND_CONTROLLED_CUTOFF' if all(c['pass'] for c in checks) else 'FAIL',
                'checks':checks,'states':states,'cutoff_comparisons':residuals,'beta_runtime':beta,
                'parameters':p,'gamma_Lambda_input':original['model']['gamma_Lambda'],
                'started_utc':started,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
                'seconds':time.perf_counter()-tick,'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,
                'new_measured_data':False,'infinite_theorem':'Analytical proof in BOSONIC_CONTINUUM_R66.txt; not inferred from finite tests.'}
        put('RESULT_BOSONIC_R66.json',result)
        print(json.dumps({'status':result['status'],'checks':len(checks),'passed':sum(c['pass'] for c in checks),'seconds':result['seconds'],'cutoff_comparisons':residuals}))
        return 0 if all(c['pass'] for c in checks) else 1
    except Exception as exc:
        put('RESULT_BOSONIC_R66.json',{'status':'ERROR','error':repr(exc),'started_utc':started,
            'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'seconds':time.perf_counter()-tick})
        raise

if __name__=='__main__':
    raise SystemExit(main())
