"""Independent density formulas and sparse clock controls; never import builders."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json,math,hashlib,bisect
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import h5py
from scipy.interpolate import make_interp_spline
from scipy.stats import gaussian_kde
R=Path(__file__).resolve().parents[2]
def need(ok,msg):
    if not ok:raise ValueError(msg)
def get(name):return json.loads((R/name).read_bytes())
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def put(p,data):
    need(not p.exists(),'Output exists');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    need(t.read_bytes()==data,'Write differs');need(not p.exists(),'Output appeared');t.rename(p)
def gaussian_zero(data):
    n=data.shape[1];means=[math.fsum(v)/n for v in data]
    d=data-np.asarray(means)[:,None]
    v0=math.fsum(d[0]**2)/(n-1);v1=math.fsum(d[1]**2)/(n-1);c=math.fsum(d[0]*d[1])/(n-1)
    det=v0*v1-c*c;need(det>0,'Bad covariance')
    quadratic=(v1*means[0]**2-2*c*means[0]*means[1]+v0*means[1]**2)/det
    logpdf=-math.log(2*math.pi)-math.log(det)/2-quadratic/2
    return logpdf,means,[[v0,c],[c,v1]]
def density(data,bw):
    kde=gaussian_kde(data,bw_method=lambda k:k.scotts_factor()*bw)
    white=np.linalg.solve(np.linalg.cholesky(kde.covariance),data)
    lp=-np.sum(white*white,axis=0)/2;weights=np.exp(lp-np.max(lp))
    ess=float(np.sum(weights)**2/np.sum(weights**2))
    return float(kde.logpdf(np.zeros(2))[0]),ess
def trap_quantile(q,y,prob):
    areas=[(y[i]+y[i+1])*(q[i+1]-q[i])/2 for i in range(len(q)-1)]
    total=math.fsum(areas);acc=0.;target=prob*total
    for i,area in enumerate(areas):
        if acc+area>=target:
            return total,q[i]+(q[i+1]-q[i])*(target-acc)/area
        acc+=area
    raise ValueError('Quantile missing')
def main():
    output=R/'bis/c1_review/f2_light_results.json';need(not output.exists(),'Output exists')
    a=get('bis/REGISTRO_C4_EMENDA_013BIS.json');g=get('bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json');c=get('bis/F2_FREE_CLOCK_EXTENDED.json')
    source='cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
    names=list(g['dependencies'])+[source,'bis/REGISTRO_C4_EMENDA_013BIS.json','C4_EMENDA_TECNICA_013BIS.md','refeito/measure_f2_density_clock_013bis.py','refeito/register_f2_amendment_013bis.py','REGISTRO_C4.json','C4_SCHEMA.json','bis/F2_INDEPENDENT_GAUSSIAN_DENSITY.json','bis/F2_FREE_CLOCK_EXTENDED.json']
    before={n:sha(R/n) for n in names}
    for obj in (g,c):
        need(obj['source_sha256']==before[source]==get('C4_SCHEMA.json')['h5_sha256'],'Source hash mismatch')
        need(obj['amendment_sha256']==before['bis/REGISTRO_C4_EMENDA_013BIS.json'],'Amendment hash')
        need(obj['code_sha256']==before['refeito/measure_f2_density_clock_013bis.py'],'Builder hash')
        for n,h in obj['dependencies'].items():need(before[n]==h,'Dependency hash '+n)
    need(a['original_registration']['sha256']==before['REGISTRO_C4.json'],'Original registration')
    need(a['code_sha256']==before['refeito/register_f2_amendment_013bis.py'],'Amendment builder')
    need(a['opening_sha256']==sha(R.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'),'Opening hash')
    witness=(R/'C4_EMENDA_TECNICA_013BIS.md').read_text(encoding='utf-8')
    need(before['bis/REGISTRO_C4_EMENDA_013BIS.json'] in witness and a['opening_sha256'] in witness and before['REGISTRO_C4.json'] in witness,'Witness hashes')
    with h5py.File(R/source,'r') as h:
        group=h['pSEOBNRv5PHM'];s=group['posterior_samples'][()]
        priors={k:group['priors/analytic/'+k][0].decode() for k in ['domega220','dtau220','domega440','dtau440']}
    need(len(s)==g['N']==c['N']==40776,'Sample count')
    need([priors[k] for k in ['domega220','dtau220']]==g['priors']==c['priors'],'Prior texts')
    need(all('Uniform(minimum=-0.8, maximum=2.0,' in priors[k] for k in ['domega220','dtau220']),'Not stated Uniform prior')
    x=np.vstack([s['domega220'],s['dtau220']]);spin=s['final_spin_non_evolved']
    need(np.isfinite(x).all() and np.isfinite(spin).all() and np.all((spin>=0)&(spin<1)),'Bad samples')
    beta=7.2973525693e-3*math.sqrt(math.e)
    wr=1.5251-1.1568*(1-spin)**.1292;Q=.7+1.4187*(1-spin)**(-.499)
    grid=get('QNM_GRID.json')['modes']['220'];need(spin.min()>=min(grid['spins']) and spin.max()<=max(grid['spins']),'Spline extrapolation')
    w=make_interp_spline(grid['spins'],np.asarray(grid['real'])+1j*np.asarray(grid['imag']))(spin)
    root=np.sqrt(1-spin*spin);kh=root/(2*(1+root));nu=w.real-spin/(1+root)
    need(np.all(nu>0) and np.all(w.imag<0),'Bad corotating QNM')
    xs={'R-B':beta*wr*Q,'R-RAIZ-0':beta*Q,'R-LIN':2*beta*Q,'R-MOD':beta*math.pi*nu**2/(kh*(-w.imag))}
    base=gaussian_zero(x);checks=[]
    for row in g['rows']:
        v=xs[row['reading']];shift=-v/(1+v);need(np.all((shift>-.8)&(shift<2)),'Curve outside prior')
        moved=x.copy();moved[1]-=shift;z=gaussian_zero(moved)
        err=abs(z[0]-base[0]-row['lnB_gaussian2D'])
        need(err<1e-11,'Independent Gaussian differs')
        checks.append(dict(reading=row['reading'],lnB=z[0]-base[0],absolute_error=err,
                           mean_max_error=float(np.max(abs(np.asarray(z[1])-row['density']['mean']))),
                           covariance_max_error=float(np.max(abs(np.asarray(z[2])-row['density']['covariance'])))))
    need({r['reading'] for r in checks}==set(a['independent_density']['readings']),'Reading coverage')
    old=get('C4_FREE_CLOCK.json')
    oldcopy=[{k:r[k] for k in ['prior','quantiles','ln_evidence_free_clock_over_GR','bandwidth_controls']} for r in old['rows']]
    need(c['original_priors']==oldcopy,'Original priors not preserved')
    tp=math.sqrt((6.62607015e-34/(2*math.pi))*6.67430e-11/299792458.**5)
    tm=s['final_mass_non_evolved']*1.3271244e20/299792458.**3/(1+s['redshift'])
    qmin=float(np.max(tp/tm));need(math.isclose(qmin,c['lower_endpoint_approximation']['exact_q_lower_max'],rel_tol=1e-14),'Source clock lower endpoint')
    pointchecks=[];integrals=[];crossings=[]
    for curve in c['curves']:
        bw=curve['bandwidth_multiplier'];q=np.asarray(curve['q']);ln=np.asarray(curve['lnB'])
        need(len(q)==801 and np.isfinite(ln).all() and np.allclose(q,np.arange(801)/20,rtol=0,atol=1e-14),'Grid')
        null,ess0=density(x,bw)
        for point in [0.,1.,10.,20.,40.,curve['first_lnB_minus_log100_crossing_q']]:
            shift=-xs['R-B']*point/(1+xs['R-B']*point);moved=x.copy();moved[1]-=shift
            need(np.all((shift>-.8)&(shift<2)),'Clock support')
            value,ess=density(moved,bw);value-=null
            stored=float(np.interp(point,q,ln));err=abs(value-stored)
            need(err < (0.002 if point not in [0.,1.,10.,20.,40.] else 1e-10),'Sparse KDE control differs')
            pointchecks.append(dict(bandwidth=bw,q=point,lnB=value,stored_or_interpolated=stored,absolute_error=err,ESS_GR=ess0,ESS_shifted=ess,ESS_100_pass=min(ess0,ess)>=100))
        for p in curve['conditional_posteriors']:
            L=p['ceiling_in_tM'];sel=q<=L;qq=q[sel].tolist();yy=np.exp(ln[sel]).tolist()
            z,q95=trap_quantile(qq,yy,.95);z2,q95coarse=trap_quantile(qq[::2],yy[::2],.95)
            logB=math.log(z/L);qerr=abs(q95/q95coarse-1);zerr=abs(math.log(z/z2))
            need(abs(logB-p['lnB_integrated'])<1e-12 and abs(q95-p['q_quantiles']['0.95'])<1e-12,'Prior integral differs')
            need(abs(qerr-p['q95_relative_grid_change'])<1e-12 and abs(zerr-p['ln_integral_grid_change'])<1e-12,'Grid error differs')
            need(p['converged']==(qerr<.005 and zerr<.001),'Convergence label')
            integrals.append(dict(bandwidth=bw,ceiling=L,q95=q95,lnB=logB,q95_grid_error=qerr,log_integral_error=zerr))
        cross=next(i for i in range(len(q)) if ln[i]<=-math.log(100));need(cross>0,'Crossing not bracketed')
        value=q[cross-1]+(-math.log(100)-ln[cross-1])*(q[cross]-q[cross-1])/(ln[cross]-ln[cross-1])
        need(abs(value-curve['first_lnB_minus_log100_crossing_q'])<1e-12,'Crossing interpolation')
        crossings.append(dict(bandwidth=bw,q=float(value)))
    need(before=={n:sha(R/n) for n in before},'Inputs changed')
    result=dict(utc=datetime.now(timezone.utc).isoformat(),status='LIGHT_NUMERICAL_CHECKS_PASS__DENSITY_SUPPORT_QUALIFICATION_REQUIRED',
       input_hashes=before,script_sha256=sha(Path(__file__)),N=len(s),priors=priors,
       weight_fields=[n for n in s.dtype.names if 'weight' in n.lower()],gaussian=checks,
       sparse_KDE_controls=pointchecks,integrals=integrals,crossings=crossings,
       max_q_lower=qmin,hashes_witnessed=True,inputs_unchanged=True,
       scope='No production imports, PE or full curve rerun. Gaussian independently recalculated for four readings; sparse scipy KDE evaluations; integration of archived curve nodes.')
    put(output,(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
    print(json.dumps({k:result[k] for k in ['status','gaussian','sparse_KDE_controls','integrals','weight_fields']},indent=2))
if __name__=='__main__':main()
