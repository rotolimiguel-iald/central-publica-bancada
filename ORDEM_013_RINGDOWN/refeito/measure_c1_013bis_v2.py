"""Recompute F1 C1 controls without modifying a previously delivered artifact."""
import os
import sys
from pathlib import Path
import json
import math
import csv
import hashlib
from datetime import datetime, timezone
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
                  NUMBA_CACHE_DIR=str(ROOT/'cache/numba'),QNMCACHEDIR=str(ROOT/'cache/qnm'))
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'cache/vendor'))
import numpy as np
import qnm
from c1_evidence_guards import require, finite, validate_inputs, validate_clock
from tgl_ringdown_prediction import prediction, kerr_mode, beta_tgl

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class Dim:
    """Rational SI exponents (mass, length, time)."""
    def __init__(self,*v): self.v=tuple(Fraction(x) for x in v)
    def __mul__(self,other): return Dim(*(a+b for a,b in zip(self.v,other.v)))
    def __truediv__(self,other): return Dim(*(a-b for a,b in zip(self.v,other.v)))
    def __pow__(self,k): return Dim(*(x*k for x in self.v))
    def __add__(self,other):
        if self.v!=other.v: raise ValueError('Dimensionally invalid sum')
        return self
    __sub__=__add__
    def text(self): return [str(x) for x in self.v]

def main():
    oldpath=ROOT/'C1_LEITURAS.json'
    old=oldpath.read_bytes()
    obj=json.loads(old)
    core=json.loads((ROOT/'cache/casa/um_absoluto.json').read_bytes())['core']['clock_test_result_v369']
    clock_flags=validate_clock(core)
    tau_bound=core['P2']['tau_star_bound_if_reading_in_tP']
    seq=qnm.modes_cache(s=-2,l=2,m=2,n=0)
    spin_rows=[]
    for a in [0.,.3,.5,.6785,.8,.9,.95]:
        mode=seq(a=a)[0]
        mod=prediction(68.287,a,'R-MOD',qnm_dimensionless=mode)
        root=prediction(68.287,a,'R-RAIZ-0',qnm_dimensionless=mode)
        b=kerr_mode(68.287,a)
        bcwmode=complex(b['omega_mass'],-b['t_mass_s']/b['tau_gr_s'])
        control=prediction(68.287,a,'R-MOD',qnm_dimensionless=bcwmode)
        spin_rows.append(dict(spin=a,exact_qnm=[mode.real,mode.imag],
             delta_mod=mod['delta_tau'],delta_root_zero=root['delta_tau'],
             delta_mod_bcw_control=control['delta_tau'],
             mod_bcw_relative_error=(control['delta_tau']/mod['delta_tau']-1)))
    # Derive dimensions from physical expressions rather than annotating outputs.
    mass,length,time=Dim(1,0,0),Dim(0,1,0),Dim(0,0,1)
    one=Dim(0,0,0); G=length**3/mass/time**2; c=length/time
    hbar=mass*length**2/time
    tP=(hbar*G/c**5)**Fraction(1,2); tM=G*mass/c**3
    w=one/time; kappa=one/time; energy=mass*c**2
    w0=energy/hbar
    squared_root_gap=w**2/((w0+w)**Fraction(1,2)+w0**Fraction(1,2))**2
    dims={'R-A':tP*w**2,'R-B':tM*w**2,'R-MOD':(w-w)**2/kappa,
          'R-RAIZ-0':w,'R-RAIZ-EP4':squared_root_gap,
          'R-RAIZ-REST':squared_root_gap,'R-RAIZ-COHERENT':w/one,
          'R-LIN':w,'R-GLOBAL':w*one,
          'R-PROP':tP*w**2*(one/w)}
    require(all(v.v==(one if k=='R-PROP' else w).v for k,v in dims.items()), 'Derived units differ')
    try: w+tM
    except ValueError: rejects_mixed=True
    else: raise AssertionError('Invalid units accepted')
    cat=json.loads((ROOT/'C4_CATALOG_220.json').read_bytes())
    csvpath=ROOT/'C7_INDEPENDENT/tables/event_reading_predictions.csv'
    with csvpath.open(encoding='utf-8-sig') as f:
        raw_rows=list(csv.DictReader(f))
    saved=validate_inputs(raw_rows,cat)
    checks=[]
    for ev in cat['rows']:
        m,a,z=[ev['quantiles'][key][1] for key in ('mass_detector','spin','redshift')]
        for row in ev['rows']:
            reference=row['median_prediction']; reading=row['reading']
            mode=complex(reference['omega_mass'],-reference['t_mass_s']/reference['tau_gr_s'])
            fresh=prediction(m,a,reading,redshift=z,
                             qnm_dimensionless=mode if reading=='R-MOD' else None)
            public=saved[ev['event'],reading]
            errors={}
            for newkey,oldkey in [('gamma_per_s','Gamma_per_second'),
                                  ('gamma_over_omega','Gamma_over_omega'),('delta_tau','delta_tau')]:
                actual=finite(fresh[newkey],newkey); baseline=finite(public[oldkey],oldkey)
                errors[newkey]=abs(actual-baseline)/max(abs(baseline),1e-300)
            require(all(math.isfinite(v) and 0<=v<1e-12 for v in errors.values()), str((ev['event'],reading,errors)))
            checks.append(dict(event=ev['event'],reading=reading,relative_errors=errors,
                               sub_resolution=abs(fresh['delta_tau'])<1e-6))
    profile_rows=[]
    for reading in ('R-A','R-B','R-RAIZ-EP4','R-RAIZ-REST','R-LIN'):
        legacy=prediction(68.287,.6785,reading,profile='LEGACY_V346')
        modern=prediction(68.287,.6785,reading,profile='CODATA2018_IAU2015')
        profile_rows.append(dict(reading=reading,comparison_redshift=0,
             gamma_legacy_over_modern_minus_one=legacy['gamma_per_s']/modern['gamma_per_s']-1,
             delta_legacy_over_modern_minus_one=legacy['delta_tau']/modern['delta_tau']-1))
    report=dict(status='PASS_NUMERICAL_C1_CONTROLS__KERR_KMS_BRIDGE_STILL_CONDITIONAL',
        utc=datetime.now(timezone.utc).isoformat(),beta_runtime=beta_tgl(),
        qnm_version=qnm.__version__,spin_comparison=spin_rows,
        dimensions={k:v.text() for k,v in dims.items()},unit_guard_rejected_mixed_dimensions=rejects_mixed,
        csv_checks=checks,checked=len(checks),sub_resolution_checked=sum(x['sub_resolution'] for x in checks),
        profile_comparison=profile_rows,P2_tau_star_bound_tP=tau_bound,
        dependencies={str(p.relative_to(ROOT)):sha(p) for p in
           [oldpath,ROOT/'tgl_ringdown_prediction.py',ROOT/'C4_CATALOG_220.json',csvpath,
            ROOT/'cache/casa/um_absoluto.json',Path(__file__),ROOT/'refeito/c1_evidence_guards.py']})
    target=ROOT/'bis/C1_NUMERICAL_CONTROLS_v2.json'
    require(not target.exists(),'Output already exists')
    raw=(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    tmp=target.with_suffix('.tmp')
    with tmp.open('xb') as f:f.write(raw)
    require(tmp.read_bytes()==raw,'Output bytes differ')
    tmp.replace(target)
    require(oldpath.read_bytes()==old,'Historical v1 changed')
    print(json.dumps({k:report[k] for k in ('status','checked','sub_resolution_checked','P2_tau_star_bound_tP','spin_comparison','profile_comparison')},indent=2))
    print('sha256',sha(target))

if __name__=='__main__': main()
