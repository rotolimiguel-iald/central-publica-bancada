"""Record the nonblind technical amendment before its extra calculations."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    if p.exists():raise FileExistsError(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
    tmp.replace(p)
opening=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013BIS_ABERTURA_operador.md'
record=dict(status='NONBLIND_TECHNICAL_AMENDMENT__NOT_NEW_BLIND_REGISTRATION',utc=datetime.now(timezone.utc).isoformat(),
 original_registration=dict(path='REGISTRO_C4.json',sha256=sha(ROOT/'REGISTRO_C4.json')),
 opening_sha256=sha(opening),code_sha256=sha(Path(__file__)),
 prior_knowledge='Published posteriors, original free-clock ceiling tM, and auditor approximate lnB at 5/8/10 tM already known. No blind status is claimed.',
 technical_statuses=['OPEN_PHYSICAL_MAPPING','INCONCLUSIVE_DENSITY_SUPPORT','PENDING_*','PRELIMINARY_*'],
 technical_status_rule='These are diagnostics/statuses, not physical verdicts or confirmation.',
 ESS=dict(threshold=100,creation='After original C4 registration; now explicitly documented NONBLIND',meaning='Minimum local effective kernel samples for both restricted and GR point; no universal error guarantee'),
 independent_density=dict(estimator='Full-covariance Gaussian in (df220, dtau220-g(spin))',
  scope='Independent density approximation, same released samples and physical curves; not statistically independent evidence',readings=['R-B','R-RAIZ-0','R-LIN','R-MOD'],
  checks=['Actual Uniform deformation priors and support','Finite samples and positive definite covariance','Direct formula versus scipy multivariate_normal at zero']),
 free_clock=dict(coordinate='q=tau_source/tM_source conditional on each nuisance sample',
  retained_priors=['uniform source tau in [tP,tM_source]','log-uniform source tau in [tP,tM_source]'],
  new_prior_INPUT='Uniform source tau in [tP,20*tM_source], conditional mass-normalization retained',
  ceiling_robustness_INPUT=[10,20,40],grid=dict(q_max=40,step=.05,coarse_step=.10),
  reported_points=[0,1,5,8,10,20,40],density_bandwidth_multipliers=[.7,1,1.4],
  curve_cut='First crossing of lnB=-log(100) on q in [0,40], if bracketed. Relative density diagnostic, not a prior-free credible bound or calibrated exclusion.',
  posterior='q quantiles conditional on each stated finite ceiling; original seconds bounds retained from original result',
  convergence='Compare q95 and log-integral on .05 versus .10 grids; target relative q95 change<0.005 and absolute log-integral change<0.001, otherwise unresolved',
  limitations=['No universal shared clock catalog inference','No injection calibration','No claim of genuinely prior-free posterior upper bound','No inference outside measured q range']))
p=ROOT/'bis/REGISTRO_C4_EMENDA_013BIS.json'
new(p,(json.dumps(record,indent=2,ensure_ascii=False)+'\n').encode())
note=('[REAL — emenda técnica NÃO-CEGA, registrada antes das contas adicionais]\n\n'
      'Abertura: SHA256 `'+sha(opening)+'`. Registro original preservado: `'+sha(ROOT/'REGISTRO_C4.json')+'`.\n\n'
      'Emenda: `bis/REGISTRO_C4_EMENDA_013BIS.json`, SHA256 `'+sha(p)+'`.\n\n'
      'O ESS ≥ 100 foi criado depois do registro original; fica declarado sem alegar pré-registro retroativo. Status técnicos não são vereditos físicos. '
      'O novo teto 20 tM e controles 10/40 tM são [INPUT], escolhidos conhecendo o diagnóstico do auditor. A curva de densidade será publicada separada dos limites condicionais ao prior. '
      'O estimador gaussiano é controle de aproximação da densidade, não evidência independente.\n\n'
      'Reprodução: Python refeito/register_f2_amendment_013bis.py em cópia isolada; recusa sobrescrita. Nenhuma PE ou strain lido. Axiomas: N/A — sem Lean.\n')
new(ROOT/'C4_EMENDA_TECNICA_013BIS.md',note.encode())
print(p,sha(p))
