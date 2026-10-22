"""Recompute T01(a-f) from existing receipts without changing cited artifacts."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import json, math, hashlib, time, uuid

B=Path(__file__).resolve().parents[2]
CHAT=B.parent
OUT=CHAT/'TUNEL/DO_CHATGPT'
D=Path(__file__).resolve().parent/'t01_core'
SOURCES={}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    SOURCES[str(p)]=sha(p)
    return json.loads(p.read_bytes())
def write(p,data):
    raw=data.encode('utf-8') if isinstance(data,str) else (json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw
    # Exclusive destination, so an already-cited file cannot be replaced.
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
    t.unlink()
def scalars(d):return {k:v for k,v in d.items() if not isinstance(v,(dict,list))}

def main():
    begin=time.perf_counter();cpu=time.process_time();now=datetime.now(timezone.utc)
    D.mkdir(exist_ok=False)
    op15=sha(OUT/'ENTREGA_015_ABERTURA_operador.md')
    op16=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    header=f'[REAL / DERIVED — NÃO-CEGO; errata documental, sem novo teste físico]\n\nAbertura015SHA256={op15}.\nAbertura016SHA256={op16}.\n\n'
    closed=B/'bis/F0_CLOSED_20260922T215825Z.json';c=read(closed)
    pre=B/'bis/F0_PRESTOP_20260922T215825Z.json';read(pre)
    snapshots=sorted((B/'bis').glob('F0_SNAPSHOT_*.json'))
    assert len(snapshots)==4
    snap=read(snapshots[-1]);groups={}
    for x in snap['records']:
        path=Path(x['path'])
        if path.name not in ('START.json','PROGRESS.json','AUDIT_RATE.json'):continue
        assert path.resolve().is_relative_to(B.resolve()) and 'E2_PRIVATE' not in path.parts
        rel=path.parent.relative_to(B).as_posix()
        groups.setdefault(rel,{})[path.name]=dict(path=str(path),sha256=sha(path),content=read(path))
    annex=[]
    for name,g in groups.items():
        pr=g['PROGRESS.json']['content'];done=pr.get('done',pr.get('completed'));valid=pr['valid_draws']
        assert type(done) is int and type(valid) is int and 0<=done<=valid
        annex.append(dict(group=name,start=g['START.json'],last_progress=g['PROGRESS.json'],
            done=done,valid_draws=valid,status='COMPLETO' if done==valid else 'INCOMPLETO',
            causa='não observada',cause_statute='DECLARADO',
            audit_rate=g.get('AUDIT_RATE.json')))
    for p in snapshots: SOURCES[str(p)]=sha(p)
    artifact=B/'C5_ANEXO_PROCESSOS.json'
    write(artifact,dict(status='REAL_METADATA_ANNEX_ONLY',at=now.isoformat(),groups=annex,
        statement='nenhum produto destes processos entra em veredito nem no portão',
        snapshots=[dict(path=str(p),sha256=sha(p)) for p in snapshots],
        closed_sha256=sha(closed),prestop_sha256=sha(pre),signals=c['signals'],
        no_processes_observed_at=c['utc'],VM_restart_cause='CONJECTURE_NOT_ESTABLISHED'))
    f0=header+'F0 corrigido ao lado: ausência conferida em '+c['utc']+'. Nenhum sinal enviado.\nOs últimos progressos são:\n\n'
    for g in annex:f0+=f'- {g["group"]}: {g["done"]}/{g["valid_draws"]}, {g["status"]}, {g["last_progress"]["content"]["date_utc"]}; causa não observada.\n'
    f0+=f'\nAnexoSHA256={sha(artifact)}; PRESTOPSHA256={sha(pre)}; CLOSEDSHA256={sha(closed)}.\nNenhum produto destes processos entra em veredito nem no portão. Não foram retomados.\n'
    write(OUT/'ENTREGA_015_ERRATA_F0.md',f0)

    reg=read(B/'RINGDOWN_5SIGMA_V1.json')
    core=read(B/'bis/e0_core/E0_CORE.json')
    e7=read(B/'bis/E7_FULLSAMPLE_RESULT_V1.json')['fullsample_diagnostics']
    centers={}
    for population in ['GWTC5_31','GWTC5_33']:
        row=core['combinations'][population]['std_ddof1']['R-B']
        fields=['N_events','observed_weighted_median_center','observed_weighted_mean_center_control',
            'sigma_combined','max_information_fraction','z_observed_vs_prediction_median']
        centers[population]={k:row[k] for k in fields}
    centers['E7_direct']=dict(mean=e7['descriptive_uncorrected_dtau_weighted_mean'],
        max_share=e7['tau_inverse_variance']['max_share'],
        IV_max_share=e7['IV_inverse_fourth']['max_share'],cap=e7['tau_inverse_variance']['cap_INPUT'])
    assert math.isclose(centers['GWTC5_33']['observed_weighted_mean_center_control'],centers['E7_direct']['mean'],abs_tol=1e-10)
    write(D/'centers.json',dict(status='NONBLIND_DESCRIPTIVE_INCONCLUSIVE_SYSTEMATICS',values=centers))

    census=read(B/'bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.json')
    candidates=reg['test_candidates']; counts=Counter(str(v['eligible']) for v in candidates.values())
    inp=census['counts_by_run']['O4_public_total']
    assert len(candidates)==44 and counts=={'True':14,'False':22,'None':8}
    assert inp['SNR_ge12']==inp['eligible_INPUT']+inp['awaiting_GR']+counts['False']
    assert inp['eligible_INPUT']==inp['eligible_with_archived_220']+inp['eligible_absent_from_audited_corpus']
    removed=inp['eligible_absent_from_audited_corpus']-counts['True']
    holds=Counter(v['data_quality_hold'] for v in candidates.values() if v['eligible'] is True)
    reconciliation=dict(total_census=inp['SNR_ge12'],eligible_census=inp['eligible_INPUT'],
        awaiting_GR=inp['awaiting_GR'],failed_INPUT=counts['False'],
        eligible_with_archived_220=inp['eligible_with_archived_220'],
        eligible_absent=inp['eligible_absent_from_audited_corpus'],
        published_outside_old_corpus_removed=removed,registered_candidates=len(candidates),
        candidate_eligibility_counts=dict(counts),eligible_holds={str(k):v for k,v in holds.items()},
        statement='Os44test_candidates e os44elegíveisINPUT são conjuntos diferentes.')
    write(D/'candidate_reconciliation.json',reconciliation)

    info=read(B/'bis/e3_blind_prepare/EXPECTED_INFORMATION.json')
    fit=next(v for v in info['fits_preserved'] if v['population']=='GWTC5_31')
    a,b=fit['coefficients_log_intercept_slope'];resid=fit['residual_sigma_ln_ddof_Nminus2']
    weights={event:math.exp(-2*(a+b*math.log(v['SNR_network_GWOSC']))+2*resid**2) for event,v in candidates.items()}
    for v in info['rows']:
        if v['fit_population']=='GWTC5_31':assert math.isclose(weights[v['event']],v['expected_inverse_variance_lognormal_s_fixed'],rel_tol=1e-12)
    # Delta at the same GW250114 reference used by the management planning ledger.
    sysad=read(B/'bis/e0_core/SYSTEMATICS_ADENDO.json')
    refs={}
    for row in sysad['empirical_QNM_recovery_by_window']+sysad['full_IMR_family_recovery']:
        reading=row['reading'];v=row['floors']['delta_GW250114']
        if reading in refs:assert refs[reading]==v
        refs[reading]=v
    subsets={'eligible14':[e for e,v in candidates.items() if v['eligible'] is True],
             'registered44_including_failed_INPUT':list(candidates)}
    current=core['combinations']['GWTC5_31']['std_ddof1']['R-B']['I_tau_current']
    ledger={}
    for label,events in subsets.items():
        total=math.fsum(weights[e] for e in events)
        ledger[label]=dict(N=len(events),expected_information=total,current_information=current,
            z_planning={k:abs(v)*math.sqrt(total+current) for k,v in refs.items()},
            events=[dict(event=e,expected_information=weights[e],eligible=candidates[e]['eligible']) for e in events])
    write(D/'information_ledger.json',dict(status='DERIVED_PLANNING_OFFSET_ZERO_PROIBIDA_COMO_TESTE',
        formula='E[I]=exp(-2*(a+b*ln(SNR))+2*s^2); z=abs(delta_GW250114)*sqrt(sum(E[I])+I31)',
        parameters=fit,reference_effects=refs,groups=ledger,
        caveat='Teto otimista; inclui22INPUTreprovados no conjunto44. Transferência e sistemáticas não calibradas.'))

    nuisance=read(B/'NUISANCE_V1.json')['conditional_diagnostics']
    fits=[]
    for row in nuisance['fits']:
        if row['group'] in ('GWTC5_31','GWTC5_33'):
            res=row['result']
            fits.append(dict(group=row['group'],reading=row['reading'],bandwidth_factor=row['bandwidth_factor'],
                covariate=row['covariate'],c0=res.get('c0'),stderr=res.get('stderr'),
                local_wald=res.get('c0_local_wald_to_zero'),status=res['status']))
    write(D/'nuisance_scope.json',dict(status='NONBLIND_LOCAL_CURVATURE_NOT_CALIBRATED',fits=fits,
        comparisons=nuisance['descriptive_comparisons'],
        caveat='c0 não distingue0de delta_X nas leituras operacionais; distâncias locais não são significância calibrada.'))

    report=header+'T01(a-f) executados; (g,h) seguem pendentes para integração dos rascunhos externos.\n\n'
    report+='| Conjunto | Centro mediana | SE | Média controle | Maior fração I | Distância descritiva R-B |\n|---|---:|---:|---:|---:|---:|\n'
    for k in ['GWTC5_31','GWTC5_33']:
        v=centers[k];report+=f'|{k}|{v["observed_weighted_median_center"]:.8f}|{v["sigma_combined"]:.8f}|{v["observed_weighted_mean_center_control"]:.8f}|{v["max_information_fraction"]:.8f}|{v["z_observed_vs_prediction_median"]:.6f}|\n'
    report+=f'\nE7: participação máximaIV={centers["E7_direct"]["IV_max_share"]:.8f}; cap={centers["E7_direct"]["cap"]}.\n'
    report+='\nCenso:74=44elegíveis+8pendentes+22reprovados;44elegíveis=21arquivados+23ausentes;23−9publicados=14candidatos. Registro:44test_candidates=14elegíveis+22reprovados+8pendentes.\n\n'
    report+='| Planejamento | E[I] adicional | R-B | R-MOD | R-RAIZ-0 | R-LIN |\n|---|---:|---:|---:|---:|---:|\n'
    for k,v in ledger.items():report+='|'+k+'|'+f'{v["expected_information"]:.6f}'+'|'+ '|'.join(f'{v["z_planning"][q]:.6f}' for q in ['R-B','R-MOD','R-RAIZ-0','R-LIN'])+'|\n'
    report+='\n[DERIVED] Fórmula offset-zero PROIBIDA_COMO_TESTE; efeito de referênciaGW250114 e I31 preservados. A PE dos cegosO4 compra c(SNR), sigma_sys, o440 e custo por posterior — não N. Nenhum desses números é significância física.\n'
    report+='\n[DECLARADO] A camada v1 de E0_CORE conserva magnitudes-proxy históricas; SYSTEMATICS_ADENDO é o adendo específico. Não foram recalculadas as campanhasC5.\n\n'
    report+='Nuisance nominal, conjunto31, covariávelsigma: SE de curvatura local, não calibrado.\n\n| Leitura | c0 | SEc0 | c0/SE descritivo |\n|---|---:|---:|---:|\n'
    for v in fits:
        if v['group']=='GWTC5_31' and v['covariate']=='sigma' and v['bandwidth_factor']==1 and v['reading'] in ('GR','R-A','R-B','R-MOD','R-RAIZ-0','R-LIN'):
            report+=f'|{v["reading"]}|{v["c0"]:.8f}|{v["stderr"][0]:.8f}|{v["local_wald"]:.6f}|\n'
    report+='\nBandas0,7/1,4, outras covariáveis e conjunto33 preservados em nuisance_scope.json.\nA RG é o limite clássico; NOT_FALSIFIED nunca é CONFIRMED.\n'
    write(D/'RELATORIO_PARCIAL.md',report)
    write(OUT/'ENTREGA_015_T01_a_f_parcial.md',report)
    elapsed=time.perf_counter()-begin
    receipt=dict(at=now.isoformat(),status='T01_A_F_DONE_G_H_PENDING',
        wall_seconds=elapsed,cpu_seconds=time.process_time()-cpu,heavy_machine_hours=0,
        sources=SOURCES,outputs=[dict(path=str(p),sha256=sha(p)) for p in sorted(D.iterdir())],
        F0_annex_sha256=sha(artifact),opening015_sha256=op15,opening016_sha256=op16,
        original_files_changed=False,new_empirical_data=False)
    write(D/'manifest.json',receipt)
    print(json.dumps(dict(status=receipt['status'],groups=[(g['group'],g['done'],g['valid_draws']) for g in annex],
        information={k:dict(N=v['N'],I=v['expected_information'],z={q:v['z_planning'][q] for q in ['R-B','R-MOD','R-RAIZ-0','R-LIN']}) for k,v in ledger.items()},
        wall_seconds=elapsed),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
