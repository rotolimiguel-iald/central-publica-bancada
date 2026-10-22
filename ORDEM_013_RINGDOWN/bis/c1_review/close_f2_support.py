"""Verify support correction without rerunning production or a full curve."""
from f2_light_checks import R,get,sha,need,put,density
import numpy as np,h5py,json,math
from pathlib import Path
from datetime import datetime,timezone
out=R/'bis/c1_review/f2_closing_results.json';report=R/'bis/F2_CLOSING_REVIEW.md'
need(not out.exists() and not report.exists(),'Output exists')
old=get('bis/F2_FREE_CLOCK_EXTENDED.json');new=get('bis/F2_FREE_CLOCK_EXTENDED_v2.json')
names=['bis/F2_FREE_CLOCK_EXTENDED.json','bis/F2_FREE_CLOCK_EXTENDED_v2.json','refeito/correct_f2_clock_support_013bis.py','bis/F2_DENSITY_CLOCK_REVIEW.md']
before={n:sha(R/n) for n in names}
need(before[names[0]]==get('bis/c1_review/f2_light_results.json')['input_hashes'][names[0]],'Old artifact changed')
need(new['supersedes']==names[0] and new['supersedes_sha256']==before[names[0]],'Supersedes')
cor=new['support_correction'];need(cor['finding']=='F2-R1' and cor['builder_sha256']==before[names[2]] and cor['review_sha256']==before[names[3]] and cor['review_path']==names[3],'Provenance')
topskip={'curves','status','supersedes','supersedes_sha256','support_correction'}
need({k:v for k,v in old.items() if k not in topskip}=={k:v for k,v in new.items() if k not in topskip},'Unexpected top-level change')
source=R/'cache/public/17018009/extracted/TGR_companion_S250114ax_results/gw250114_pseobnr/posterior_samples.h5'
need(sha(source)==new['source_sha256'],'Source hash')
with h5py.File(source,'r') as h:s=h['pSEOBNRv5PHM/posterior_samples'][()]
x=np.vstack([s['domega220'],s['dtau220']]);a=s['final_spin_non_evolved'];beta=7.2973525693e-3*math.sqrt(math.e)
xb=beta*(1.5251-1.1568*(1-a)**.1292)*(.7+1.4187*(1-a)**(-.499))
point_checks=[];masses=[]
for oc,c in zip(old['curves'],new['curves']):
    need({k:c[k] for k in oc if k!='conditional_posteriors'}=={k:v for k,v in oc.items() if k!='conditional_posteriors'},'Curve or cutoff changed')
    q=np.asarray(c['q']);ess=np.asarray(c['ESS_restricted_grid']);bw=c['bandwidth_multiplier']
    need(ess.shape==(801,) and np.isfinite(ess).all() and np.all((ess>=1-1e-10)&(ess<=len(s))),'ESS schema')
    need(c['data_supported_cut'] is None,'Unsupported cut promoted')
    null=density(x,bw)[1]
    points=c['support_reported_points']+[c['raw_KDE_diagnostic_crossing']]
    need({p['q'] for p in c['support_reported_points']}=={float(k) for k in c['reported_points']},'Reported-point coverage')
    for op,p in zip(oc['conditional_posteriors'],c['conditional_posteriors']):
        need({k:p[k] for k in op}==op,'Prior or quantile changed')
        need(p['quadrature_converged']==op['converged'] and p['density_validation_status']=='INCONCLUSIVE_DENSITY_SUPPORT_IN_NORMALIZATION_TAIL','Convergence/support conflated')
        need(set(p['quantile_support'])==set(p['q_quantiles']),'Quantile coverage')
        for quant,point in p['quantile_support'].items():need(point['q']==p['q_quantiles'][quant],'Quantile point differs')
        points+=list(p['quantile_support'].values())
        ix=q<=p['ceiling_in_tM'];qq=q[ix];w=np.exp(np.asarray(c['lnB'])[ix]);indicator=(ess[ix]<100)
        numerator=math.fsum((w[j]*indicator[j]+w[j+1]*indicator[j+1])*(qq[j+1]-qq[j])/2 for j in range(len(qq)-1))
        denominator=math.fsum((w[j]+w[j+1])*(qq[j+1]-qq[j])/2 for j in range(len(qq)-1))
        fraction=numerator/denominator
        need(abs(fraction-p['raw_KDE_posterior_mass_in_low_support_grid'])<1e-12,'Low-support mass differs')
        masses.append(dict(bandwidth=bw,ceiling=p['ceiling_in_tM'],low_support_mass=fraction))
    for p in points:
        v=p['q'];moved=x.copy();moved[1]+=v*xb/(1+v*xb);ind=density(moved,bw)[1]
        error=abs(ind/p['ESS_restricted']-1)
        need(error<1e-11 and abs(null/p['ESS_GR']-1)<1e-11,'Independent ESS mismatch')
        need(p['ESS_threshold']==100 and p['status']==('SUPPORTED_LOCAL_KERNEL_COUNT' if min(null,ind)>=100 else 'INCONCLUSIVE_DENSITY_SUPPORT'),'ESS status differs')
        if abs(v*20-round(v*20))<1e-12:need(abs(ess[round(v*20)]/ind-1)<1e-11,'Grid/report mismatch')
        point_checks.append(dict(bandwidth=bw,q=v,ESS=ind,relative_error=error))
    need(c['raw_KDE_diagnostic_crossing']['q']==oc['first_lnB_minus_log100_crossing_q'],'Raw cutoff lost')
need(before=={n:sha(R/n) for n in names},'Inputs changed')
r=dict(status='F2_R1_CLOSED__DENSITY_SUPPORT_REMAINS_INCONCLUSIVE',utc=datetime.now(timezone.utc).isoformat(),hashes=before,source_sha256=sha(source),script_sha256=sha(Path(__file__)),ESS_checks=point_checks,grid_values_structurally_checked=2403,low_support_masses=masses,raw_curves_and_priors_unchanged=True)
put(out,(json.dumps(r,indent=2)+'\n').encode())
table='\n'.join(f"| {v['bandwidth']} | {100*v['low_support_mass']:.8f}% |" for v in masses if v['ceiling']==20)
hashes='\n'.join(f'| `{n}` | `{h}` |' for n,h in before.items())
text=f'''[REAL — fechamento somente de F2-R1; suporte da cauda permanece inconclusivo]

# Fechamento F2-R1

{r['utc']}. **Achado encerrado.** A v2 transporta o ESS e distingue estabilidade da quadratura de validade da densidade. Não há bloqueante remanescente da omissão nomeada; isso não transforma a cauda em suporte suficiente nem aprova limites físicos.

Conferi os 2.403 valores da grade quanto a dimensão, finitude e faixa [1,N]; reavaliei independentemente {len(point_checks)} pontos reportados/quantis/cruzamentos com scipy KDE e whitening por Cholesky, sem chamar o corretor. Maior diferença relativa de ESS: {max(v['relative_error'] for v in point_checks):.6g}. As entradas coincidentes na grade concordam. Não recalculei a grade inteira nem a curva de densidade.

As nove frações de massa KDE em regiões de baixo suporte conferem por soma própria de trapézios. No teto 20:

| Banda | Massa KDE na grade com ESS < 100 |
|---|---:|
{table}

Essas frações são diagnósticos da aproximação KDE na grade, não probabilidades calibradas de erro. O limiar descontínuo não ganhou controle próprio de convergência; não se deve atribuir precisão física aos decimais impressos.

Os três cruzamentos brutos foram preservados e marcados INCONCLUSIVE_DENSITY_SUPPORT; data_supported_cut é null. Os quantis têm seu ESS; os nove posteriores mantêm quadrature_converged separado de density_validation_status, que explicita a cauda da normalização. Não houve recorte, renormalização em teto menor, apagamento de cauda ou mudança de prior: curvas, quantis, integrais, dois priors originais e demais campos antigos permanecem iguais.

Hashes de supersedes, builder e parecer conferem; original preservado. O status global é NONBLIND_RAW_CLOCK_DENSITY__INCONCLUSIVE_DENSITY_SUPPORT_FOR_CUT. Continua aberta a sustentação estatística da cauda, agora honestamente registrada.

Controle: `bis/c1_review/close_f2_support.py`, executado com `/opt/lal_env/bin/python -B` em WSL. Evidência: `bis/c1_review/f2_closing_results.json`, SHA256 `{sha(out)}`; script SHA256 `{sha(Path(__file__))}`. Reprodução em cópia isolada, pois as saídas recusam sobrescrita. Sem PE, novos posteriores, strain, C5 ou código de produção executado. Insumos intactos. Axiomas: N/A — sem Lean.

| Caminho relativo a ORDEM_013_RINGDOWN | SHA256 lido |
|---|---|
{hashes}
'''
put(report,text.encode());print(json.dumps(dict(status=r['status'],points=len(point_checks),max_ESS_relative_error=max(v['relative_error'] for v in point_checks),report_sha256=sha(report))))
