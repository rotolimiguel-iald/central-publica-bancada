"""Varredura da fronteira do aborto nativo: DRAW8 com dtau440 e dtau220 variando, fmax=2048. Subprocessos isolados."""
import json, subprocess, sys, time, os
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=dict(mass_1=40.70912464765123, mass_2=20.237781889510657, chi_1=0.9196233876975504, chi_2=0.2055129322455731,
          luminosity_distance=103.3345570969183, theta_jn=1.560261620994438, phase=4.252515165901328,
          dtau220=-0.6157519631492032, dtau440=1.7780455359890353, domega220=-0.42647193412015016, domega440=0.7808349673597068)
CHILD=open(os.path.join(HERE,'child.py')).read()
def run(label,p,fmax=2048):
    t=time.perf_counter(); r=subprocess.run([sys.executable,'-c',CHILD,json.dumps(p),str(fmax)],capture_output=True,text=True,timeout=300)
    return dict(label=label,dtau220=p['dtau220'],dtau440=p['dtau440'],domega220=p['domega220'],domega440=p['domega440'],rc=r.returncode,out=r.stdout.strip()[-80:],err=r.stderr.strip()[-60:])
out=[]
for d440 in (0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.78):
    out.append(run('vary_d440',dict(BASE,dtau440=d440))); print(out[-1],flush=True)
for d220 in (-0.62,-0.3,0.0,0.5,1.0,2.0):
    out.append(run('vary_d220_d440_1.78',dict(BASE,dtau220=d220))); print(out[-1],flush=True)
# domega zerados, so dtau
out.append(run('only_dtau_wide',dict(BASE,domega220=0.0,domega440=0.0))); print(out[-1],flush=True)
# ponto do prior LVK-like: dtau220=-0.9 dtau440=0
out.append(run('d220_-0.9_d440_0',dict(BASE,dtau220=-0.9,dtau440=0.0,domega220=0.0,domega440=0.0))); print(out[-1],flush=True)
json.dump(out,open(os.path.join(HERE,'scan_boundary_result.json'),'w'),indent=1)
