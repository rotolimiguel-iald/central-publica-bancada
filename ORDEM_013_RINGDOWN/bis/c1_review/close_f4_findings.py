"""Read-only targeted F4 closure; write review and private audit receipt."""
import hashlib,json,math
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[2]
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def get(p):return json.loads((R/p).read_bytes())
def need(ok,msg):
    if not ok:raise ValueError(msg)
def put(p,data):
    p=R/p;need(not p.exists(),'Output exists');t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    need(t.read_bytes()==data and len(data)>0,'Write differs');need(not p.exists(),'Output appeared');t.rename(p)
names=['C5_FISHER_v2.json','C5_FISHER_v3.json','PORTAO_DO_PODER_013.json','PORTAO_DO_PODER_013_v2.json','refeito/correct_f4_review_013bis.py','bis/F4_POWER_GATE_REVIEW.md']
before={n:sha(R/n) for n in names}
old=get(names[0]);new=get(names[1]);g0=get(names[2]);g=get(names[3]);prior=get('bis/c1_review/f4_independent_results.json')
for n in names[:1]+names[2:3]:need(before[n]==prior['input_hashes'][n],'Old production changed')
need(new['same_source_R_B_linear_historical']==old['same_source_R_B'],'Historical table changed')
need(new['records']==old['records'],'Fisher records changed')
checks=[]
for row in new['same_source_R_B']:
    pts=[r for r in new['records'] if r['psd']==row['psd'] and r['reading']=='R-B' and r['snr_ringdown']==40 and r['scenario']=='FREQUENCY_FREE_TAU_GR_FIXED']
    need(len(pts)==1,'Nonunique reference');p=pts[0]
    z=math.log1p(p['x'])/p['sigma_delta_local']*row['snr_ratio_to_O4']
    for field,value in [('z_local',z),('lnB_mean_if_reading',z*z/2),('lnB_standard_deviation',z)]:need(math.isclose(row[field],value,rel_tol=1e-14),'Incorrect corrected table')
    need(row['convention']=='log1p(x)/sigma_log_decay; point hypotheses','Convention missing')
    checks.append(dict(psd=row['psd'],z=z,mean=z*z/2))
need(len(checks)==4 and {r['psd'] for r in checks}=={'O4','O5','ET','CE'},'Coverage differs')
fskip={'same_source_R_B','same_source_R_B_linear_historical','supersedes','supersedes_sha256','correction'}
need({k:v for k,v in old.items() if k not in fskip}=={k:v for k,v in new.items() if k not in fskip},'Unexpected Fisher change')
need(len(g['measured_psd_control'])==16,'PSD coverage')
rho=next(b['rho'] for b in g['bases'] if b['name']=='GW250114_MEASURED_NORM_10tM')
for a,b in zip(g0['measured_psd_control'],g['measured_psd_control']):
    need({k:b[k] for k in a}==a,'Original PSD numbers changed')
    need(b['rho_used']==rho and b['rho_kind']=='NETWORK_NORM_APPLIED_TO_EACH_PSD_SCENARIO','Rho scope differs')
    need(b['scope']=='Separate PSD-shape scenarios at common network rho; not detector-specific measured z or combined network Fisher','Scope missing')
gskip={'measured_psd_control','supersedes','supersedes_sha256','correction','current_fisher'}
need({k:v for k,v in g0.items() if k not in gskip}=={k:v for k,v in g.items() if k not in gskip},'Unexpected gate change')
for doc,origin,finding in [(new,names[0],'F4-R1'),(g,names[2],'F4-R2')]:
    need(doc['supersedes']==origin and doc['supersedes_sha256']==before[origin],'Origin hash')
    need(doc['correction']['finding']==finding and doc['correction']['builder_sha256']==before[names[4]] and doc['correction']['review_sha256']==before[names[5]],'Correction provenance')
need(g['current_fisher']['path']==names[1] and g['current_fisher']['sha256']==before[names[1]],'Current Fisher link')
need(before=={n:sha(R/n) for n in names},'Inputs changed')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='F4_R1_R2_CLOSED',checks=checks,PSD_controls=16,readings_unchanged=g['readings']==g0['readings'],hashes=before,script_sha256=sha(Path(__file__)))
put('bis/c1_review/f4_closing_results.json',(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode())
table='\n'.join(f"| {r['psd']} | {r['z']:.12g} | {r['mean']:.12g} |" for r in checks)
hashes='\n'.join(f'| `{n}` | `{v}` |' for n,v in before.items())
report=f'''[REAL — fechamento somente de F4-R1/F4-R2; sem mudança de gate]

# Fechamento dos achados F4

{result['utc']}. **APROVADOS os dois achados nomeados.** Não restou bloqueante de F4-R1/R2 nas versões examinadas. Esta aprovação não abrange toda F4, a calibração física nem novos artefatos F2.

F4-R1: `C5_FISHER_v3.json` recalcula cada linha de `same_source_R_B` usando a referência única PSD/R-B/SNR40/FREQUENCY_FREE_TAU_GR_FIXED. Recalculei independentemente `log1p(x)/sigma × snr_ratio_to_O4`, média z²/2 e desvio-padrão z. As quatro linhas conferem. A tabela antiga foi preservada integralmente em `same_source_R_B_linear_historical`; todos os 384 records permanecem iguais à v2. A convenção pontual está explícita.

| PSD | z e desvio-padrão corretos | média lnB correta |
|---|---:|---:|
{table}

F4-R2: `PORTAO_DO_PODER_013_v2.json` conserva os 16 valores de controle e acrescenta rho_used, rho_kind e scope com o significado pedido: cenários separados de forma de PSD, normalizados ao mesmo rho de rede; não são z medidos por detector nem Fisher combinado da rede. Bases, 50 readings e vereditos permanecem inalterados.

Os hashes de supersedes, builder e parecer anterior conferem. O ponteiro current_fisher identifica v3; a dependência histórica congelada continua íntegra. O builder foi lido, não executado/importado. Insumos antigos e novos permaneceram intactos durante os controles. A lista de mudanças estruturais foi comparada com a lista autorizada; nenhuma diferença inesperada.

Mantém-se a conclusão anterior: maior z condicional 0,713209021511; INCONCLUSIVE_SYSTEMATICS e FAILED_TWO_FAMILY_CALIBRATION. Nenhuma PE, injeção ou execução de um.py. Axiomas: N/A — sem Lean.

Reprodução: Python bundled, `-B -O bis/c1_review/close_f4_findings.py`, a partir de uma cópia isolada preservando a estrutura relativa, pois as saídas recusam sobrescrita. Evidência: `bis/c1_review/f4_closing_results.json`; SHA256 `{sha(R/'bis/c1_review/f4_closing_results.json')}`. Script SHA256 `{sha(Path(__file__))}`.

| Arquivo (relativo a ORDEM_013_RINGDOWN) | SHA256 lido |
|---|---|
{hashes}
'''
put('bis/F4_CLOSING_REVIEW.md',report.encode())
print(json.dumps(dict(status=result['status'],report_sha256=sha(R/'bis/F4_CLOSING_REVIEW.md'))))
