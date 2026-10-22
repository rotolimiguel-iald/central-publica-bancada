"""Assemble the reviewed nonblind E0 planning gate, never a physical test."""
import json,hashlib,math,os
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((B/n).read_text(encoding='utf-8'))
def create(p,raw):
    if p.exists():raise FileExistsError(p)
    if not isinstance(raw,bytes):raw=(json.dumps(raw,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>25000000:raise ValueError('Large files belong in cache')
    t=p.with_suffix(p.suffix+'.tmp')
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise IOError('Incomplete temporary')
    try:os.link(t,p)
    finally:t.unlink()
def main():
    names=['bis/e0_core/E0_CORE.json','bis/e0_core/DATASET.json','bis/e0_core/SYSTEMATICS_ADENDO.json',
      'bis/E0_SYSTEMATICS_REVIEW.json','bis/E0_CORE_SCALAR_REVIEW.json','bis/E0_SNR_INFORMATION_FIT.json',
      'bis/E0_SNR_FIT_REVIEW.md','bis/E0_ROUTE_IV_POWER_v2.json','bis/E0_ROUTE_IV_VALIDATION.json',
      'bis/E0_ROUTE_IV_VALIDATION_PLAN.json','bis/E0_ROUTE_IV_PROVENANCE.json','bis/E0_MC_GUARD_CLOSURE.json',
      'bis/E0_ROUTE_IV_INDEPENDENT_REVIEW.md','bis/e0_metadata/GWOSC_INVENTORY.json',
      'bis/e0_metadata/GR_METADATA_DRAFT_REVIEW.json','bis/e0_metadata/GR_METADATA_DRAFT_REVIEW.md',
      'bis/e0_metadata/SCENARIOS_AND_SCHEDULES.json','bis/e0_metadata/SOURCE_LEDGER.json',
      'bis/E0_RATE_O5_SCENARIOS.json','bis/E0_RATE_O5_INDEPENDENT_REVIEW.md','bis/PART_B_BUDGET_START.json','C1_LEITURAS_v4.json']
    files={n:{'sha256':sha(B/n),'bytes':(B/n).stat().st_size} for n in names}
    core=read(names[0]);dataset=read(names[1]);sys=read(names[2]);fit=read('bis/E0_SNR_INFORMATION_FIT.json')
    inv=read('bis/e0_metadata/GWOSC_INVENTORY.json');gr=read('bis/e0_metadata/GR_METADATA_DRAFT_REVIEW.json')
    val=read('bis/E0_ROUTE_IV_VALIDATION.json');rate=read('bis/E0_RATE_O5_SCENARIOS.json')
    anchor=next(r for r in dataset['rows'] if r['product_id']=='GWTC5:GW250114_082203')
    readings=list(anchor['predictions'])
    if len(readings)!=10:raise ValueError('Expected ten parallel readings')
    targets=[]
    for pop,variants in core['combinations'].items():
        for rd in readings:
            r=variants['std_ddof1'][rd];delta=r.get('delta_weighted');resolved=delta is not None and abs(delta)>=1e-12
            targets.append({'population':pop,'reading':rd,'status':'CONDITIONAL_PLANNING_ONLY' if resolved else 'OPEN_OR_ZERO_OR_SUBRESOLUTION',
              'I_tau_expected_target90':r['I_tau_target90'] if resolved else None,
              'GW250114_equivalents_reference_sigma_0p058':r['GW250114_equivalents_target90'] if resolved else None,
              'N90_mixture_illustration_not_selection':r['N90'] if resolved else None,
              'N50_mixture_illustration_not_selection':r['N50'] if resolved else None,
              'z_signal_planning_offset_zero':r['z_comb'],'z_slope_free_intercept':r['z_slope'],
              'N90_slope_illustration':r['N90_slope'] if resolved else None,
              'N_spurious_offset_zero50':r['N_spurious50_median'],
              'operational_target_paid':False,'systematic_gate_green':False,
              'status_offset_zero':'PROIBIDA_COMO_TESTE','analytic_tiny_numbers_source':names[0] if not resolved else None})
    all_published={r['event'] for r in dataset['rows']}
    event_quality=[];a,b=fit['fits'][0]['coefficients_log_intercept_slope'];sd=fit['fits'][0]['residual_sigma_ln_ddof_Nminus2']
    for e in gr['events']:
        row={k:e[k] for k in ['event','run','network_snr','gr_metadata','gr_metadata_status']}
        snr=e['network_snr'];known=e['gr_metadata'] is not None
        eligible=False if snr is not None and snr<12 else e['proposed_input_would_pass'] if known else None
        row.update(eligible_INPUT_rule=eligible,status='ELIGIBLE_PREANALYSIS_INPUT' if eligible else 'BELOW_REGISTERED_INPUT_CUT' if eligible is False else 'AWAITING_GR_METADATA',
          priority_snr30=bool(snr is not None and snr>=30),posterior_published_in_archived_census=e['event'] in all_published,
          strain_download_verified=False,
          expected_I_tau_from_SNR=math.exp(-2*(a+b*math.log(snr))+2*sd*sd) if snr is not None and snr>0 else None)
        event_quality.append(row)
    condition=[{'reading':rd,**sys['floors'][rd],
      'condition_today':'FALSA_PARA_ADMISSAO__CALIBRACAO_NAO_PAGA' if sys['floors'][rd]['floor5_INPUT'] not in (None,0) else 'SEM_EFEITO_OU_OBSERVAVEL_LOCAL_ABERTO',
      'sigma_c_calibrated':None,'gate_green':False,'reason':'Archived conditional estimators do not calibrate full pSEOB free mass/spin residual uncertainty'} for rd in readings]
    doc={'status':'NONBLIND_E0_REGISTERED_PLANNING_GATE__NO_TEST_DATA','registered_utc':datetime.now(timezone.utc).isoformat(),
      'scope':'E0 completed as numerical planning/falsifier wall. This is not E2 preregistration or a physical significance result.',
      'readings':readings,'reading_statutes_source':read('C1_LEITURAS_v4.json'),'beta_runtime':dataset['beta_runtime'],'primary_convention':core['primary_prediction_convention'],
      'formula':{'z':'sqrt(sum((delta_i/sigma_i)^2))','I':'sum(1/sigma_i^2)','N90_factor':core['N90_factor'],
        'target':'(5+Phi^-1(0.90))^2 / mean(delta_i^2/sigma_i^2); I90=N90*mean(1/sigma_i^2)',
        'scope':'Fixed calibration joint distribution of delta and sigma. Information alone is insufficient when signal varies with spin; mixture counts illustrative, never a posterior-width cut.'},
      'all_calibration_combinations':core['combinations'],'planning_targets':targets,
      'quality_INPUT':{'network_snr_min_inclusive':12,'Mf_detector_median_min_solar_inclusive':40,
        'chi_final_median_min_inclusive':0,'chi_final_median_max_exclusive':.98,'priority_snr_min':30,
        'source':'GWOSC preferred/default network_matched_filter_snr plus standard GR IMR remnant medians published before deformation analysis',
        'scope':'GR full-IMR, not inspiral-only or independent of strain. Default SNR may be PE or loudest search. No posterior-width or measured deformation cut.',
        'missing':'AWAITING_GR_METADATA; not failure or acceptance. Table availability is administrative pendingness, not physical selection.',
        'uncertainty':'Point-median INPUT, intervals not propagated into eligibility. Future metadata fill applies exactly the same rule before test posterior.',
        'authority':'Implementation choice within order E0.3; no human approval inferred. Draft waiting-user wording superseded here by principal agent adoption.'},
      'quality_counts_current':gr['by_run'],'events_preanalysis':event_quality,'snr_counts_by_run':inv['by_run'],
      'snr_fit':fit,'snr_fit_convention_addendum':'sigma_fit_performed=false is inherited inventory-stage metadata; this sealed artifact embeds the completed nonblind fit and independent review.',
      'systematic_conditions':condition,'systematic_matrix_file':names[2],
      'route_IV':{'statistic':'Common-mean-profiled Gaussian intrinsic variance LRT >25','sigma_sys_assumed':0,
        'validated_grid_targets':val['selected'],'confidence':'Independent draws; one-sided Clopper-Pearson alpha .05/27; smallest approved of three candidates, not minimum integer.',
        'status':'OPTIMISTIC_PLANNING_UNTIL_JITTER_TRANSFER_AND_SYSTEMATICS','null_5sigma_calibrated':False,
        'implementation_guard_addendum':'Original MC values unchanged. Provenance frozen posthoc and nine negative tests under -O; never retroactive preregistration.'},
      'conditional_rates_scenarios':rate,'threeG_source_scenarios':read('bis/e0_metadata/SCENARIOS_AND_SCHEDULES.json'),
      'threeG_fixed_anchor_calculations':core['threeG_GW250114_anchor_scenarios'],
      'inherited_C4_nonblind':core['inherited_C4_rows'],'C4_scope':core['inherited_C4_scope'],
      'differences_management':['SNR fit changes both estimator of width (std not q90-equivalent) and SNR source (GWOSC not TGR); controlled 2x2 comparison in review.',
        'N90 Monte Carlo includes free mean and simultaneous confidence validation; differs from point estimates in management.',
        'O4b GR metadata impact gives 27 median-Mf>=40 candidates, not inherited 25; direct source medians and one SNR convention used.',
        'Rare-event Poisson interval corrected with exact central 90% and explicitly conditional exposure; archive calendar is not observing live time.',
        'O5 gain-plus-volume assumes retained fixed-source quality; rate-only control shown. No assertion of actual O5 sigma reach.',
        'ET/CE timing uses current primary planning sources rather than universal 2035 start; start remains conditional.'],
      'not_paid':['Selection efficiency normalization E1/E3','Residual nuisance full pSEOB calibration','Physical route IV transfer and systematic variance','E2 null 5sigma tail','E3 new PE','Any test event or physical 5sigma'],
      'source_files':files,'code_sha256':sha(Path(__file__))}
    create(B/'PORTAO_DA_AMPLIACAO_V1.json',doc)
    lines=['[NÃO-CEGO — E0 PAGO como portão de planejamento; calibração sistemática NÃO PAGA; nenhum teste físico]',
      '', '# Portão da ampliação V1', '',
      'Todos os números abaixo são cálculos condicionais de planejamento. Offset fixo em zero: **PROIBIDA_COMO_TESTE**. Dez leituras em paralelo; nenhuma escolhida. RG permanece limite clássico.', '',
      'Fonte de largura: DP dos posteriores completos, ddof=1. Previsão E0 em medianas separadas; a marginalização conjunta pertence a E1. Controle q90 e QNM exato preservado no JSON.', '',
      f"N90/N50 = {core['N90_factor']:.12g}; I = Σ1/σ². I90 depende da distribuição conjunta de δ e σ. A referência 1/0,058² é unidade fixa de informação, não corte de seleção.", '',
      '| Leitura | z de sinal, 31, calibração | I90 condicional | N90 mistura ilustrativa | z tendência, intercepto livre |',
      '|---|---:|---:|---:|---:|']
    def fmt(v):return 'OPEN/nulo/subresolução' if v is None else f'{v:.6g}'
    for r in targets:
        if r['population']=='GWTC5_31':lines.append('| '+r['reading']+' | '+' | '.join(fmt(r[k]) for k in ['z_signal_planning_offset_zero','I_tau_expected_target90','N90_mixture_illustration_not_selection','z_slope_free_intercept'])+' |')
    lines+=['', 'Os conjuntos 33, 39 únicos e GWTC3 18/10, o falsificador espúrio inclusive RG e os controles constam integralmente do JSON. N astronômicos de efeitos subresolvidos ficam como aritmética histórica; alvos operacionais permanecem null.', '',
      '**Qualidade [INPUT adotado nesta etapa]:** SNR de rede GWOSC ≥12, mediana GR Mf,det ≥40 M☉ e 0≤χf<0,98; prioridade SNR≥30. Nenhuma largura de posterior decide admissão. GR full-IMR é anterior ao teste de deformação, não inspiral-only. χ_eff não substitui χf. Ausências aguardam metadados sob a mesma regra.', '',
      'Na cobertura atual, O4b: 45 com SNR≥12; 44 têm Mf/χf na tabela GR; 27 passam o INPUT, 17 ficam abaixo, um aguarda. O4a e O4c precisam completar metadados. Não se afirma que todos são elegíveis nem que strain foi baixado.', '',
      f"Ajuste: mediana σ = {math.exp(a):.9g} SNR^({b:.9g}); dispersão ln={sd:.9g}. E[1/σ²]=exp(−2μ+2s²), diferente do inverso da mediana². As diferenças contra 3,03/−0,86 vêm de fonte do SNR **e** definição de largura; tabela 2×2 no parecer independente.", '',
      '**Condição sistemática:** FALSA para admissão em todas as leituras com efeito definido: σ(c_calibrado) ainda não medido na pipeline exigida. Pisos |δ|/5 e |δ|/15 separados; null não é zero. A matriz recalculada de controles C5 e a revisão independente estão vinculadas por hash.', '',
      '**Rota IV:** poder condicional ≥90% nos candidatos aprovados por IC simultâneo: N=61/39/22 para largura GW250114; 1588/996/524 na mistura31; 1696/1144/594 na mistura33, para jitter 0,019/0,0228/0,030. Menor aprovado de três candidatos, não mínimo inteiro. As duas tentativas falhas da mistura33 sobrevivem. Cauda nula de 5σ, transferência e σ_sys continuam OPEN.', '',
      '**Taxas/cenários:** Poisson central90 condicionado ao universo publicado e à exposição declarada. SNR≥78 é proxy de metadado, não precisão garantida. O5 tem bandas históricas BBH, controle de PSD e teto BNS distinto. Ganho de qualidade mais volume é hipótese otimista; controle de qualidade invariante separado. ET/CE são cronogramas e populações projetadas, não promessa de anos.', '',
      'C4 permanece herdada, NÃO-CEGA, com correção/σ e veto relativo à RG. Nenhum número de planejamento muda seu veredito ou o gate. E0 não é o registro E2, e nenhum posterior de teste foi lido.', '',
      'Reprodução: executar os produtores documentados em cada recibo apenas em novo destino; este assemblador recusa substituir arquivos. N/A — sem Lean; zero teoremas. Tentativas e revisões preservadas.', '',
      '## Fontes e recibos', '',f"JSON desta entrega: `{sha(B/'PORTAO_DA_AMPLIACAO_V1.json')}`."]
    for n,h in files.items():lines.append(f"- `{n}` — `{h['sha256']}` ({h['bytes']} B)")
    create(B/'PORTAO_DA_AMPLIACAO_V1.md',('\n'.join(lines)+'\n').encode())
    print(json.dumps({'status':doc['status'],'json_sha256':sha(B/'PORTAO_DA_AMPLIACAO_V1.json'),'md_sha256':sha(B/'PORTAO_DA_AMPLIACAO_V1.md'),'readings':len(readings),'targets':len(targets)},ensure_ascii=False))
if __name__=='__main__':main()
