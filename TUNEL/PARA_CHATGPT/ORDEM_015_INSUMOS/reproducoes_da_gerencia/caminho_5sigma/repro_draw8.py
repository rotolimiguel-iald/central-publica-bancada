"""Reproducao independente (auditoria) do aborto nativo DRAW8_2048 da bancada.
Chama lalsimulation diretamente (sem codigo da bancada). Cada caso roda em subprocesso
para que um SIGSEGV/abort nao derrube o supervisor. Nada e escrito fora deste diretorio."""
import json, subprocess, sys, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
DRAW8 = dict(mass_1=40.70912464765123, mass_2=20.237781889510657, chi_1=0.9196233876975504, chi_2=0.2055129322455731,
             luminosity_distance=103.3345570969183, theta_jn=1.560261620994438, phase=4.252515165901328,
             dtau220=-0.6157519631492032, dtau440=1.7780455359890353, domega220=-0.42647193412015016, domega440=0.7808349673597068)
TGL = dict(DRAW8, dtau220=-0.0199, dtau440=-0.082, domega220=0.0, domega440=0.0)   # escala da leitura R-B (GW250114)
GR  = dict(DRAW8, dtau220=0.0, dtau440=0.0, domega220=0.0, domega440=0.0)
CHILD = r'''
import sys, json, resource
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
import lal, lalsimulation as ls
p=json.loads(sys.argv[1]); fmax=float(sys.argv[2])
d=lal.CreateDict()
ls.SimInspiralWaveformParamsInsertDTau220(d,p['dtau220']); ls.SimInspiralWaveformParamsInsertDTau440(d,p['dtau440'])
ls.SimInspiralWaveformParamsInsertDOmega220(d,p['domega220']); ls.SimInspiralWaveformParamsInsertDOmega440(d,p['domega440'])
try:
    hp,hc=ls.SimInspiralFD(p['mass_1']*lal.MSUN_SI,p['mass_2']*lal.MSUN_SI,0,0,p['chi_1'],0,0,p['chi_2'],
        p['luminosity_distance']*1e6*lal.PC_SI,p['theta_jn'],p['phase'],0.,0.,0.,1/16.,20.,fmax,20.,d,ls.pSEOBNRv4HM_PA)
    print(json.dumps({"status":"FINITE" if (abs(hp.data.data).max()>0) else "ZERO","n":len(hp.data.data)}))
except RuntimeError as e:
    print(json.dumps({"status":"LAL_ERROR","msg":str(e)[:200]}))
'''
def run(label, p, fmax):
    t=time.perf_counter()
    r=subprocess.run([sys.executable,'-c',CHILD,json.dumps(p),str(fmax)],capture_output=True,text=True,timeout=300)
    return dict(label=label,fmax=fmax,returncode=r.returncode,wall_s=round(time.perf_counter()-t,3),
                stdout=r.stdout.strip()[-300:],stderr_tail=r.stderr.strip()[-300:])
out=[]
for fmax in (1024,2048,4096,8192):
    out.append(run('DRAW8',DRAW8,fmax)); print(out[-1],flush=True)
for fmax in (1024,2048,4096):
    out.append(run('TGL_scale',TGL,fmax)); print(out[-1],flush=True)
    out.append(run('GR',GR,fmax)); print(out[-1],flush=True)
json.dump(out,open(os.path.join(HERE,'repro_draw8_result.json'),'w'),indent=1)
