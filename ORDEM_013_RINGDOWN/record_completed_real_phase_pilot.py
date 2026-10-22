"""Record completed source draws and the next registered numerical refinement."""
from datetime import datetime, timezone
import argparse
import json
from record_source_evidence_start import ROOT, RUN, safe, sha


def read(path):
    return json.loads(path.read_bytes())


def main(seob_done, phenom_done):
    receipt=ROOT/'C5_COMPLETED_REAL_PHASE_PILOT.json'
    handoff=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_piloto_real_concluido_e_refinamento.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once record')
    pilot=RUN/'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384'
    result=read(pilot/'RESULT.json'); density=read(pilot/'DENSITY_AUDIT.json')
    arithmetic=read(pilot/'ARITHMETIC_AUDIT.json'); comparison=read(pilot/'PROPOSAL_COMPARISON.json')
    for report in (density,arithmetic):
        if report['hashes']['RESULT.json']!=sha(pilot/'RESULT.json'):
            raise ValueError('Unmatched completed-run audit')
    for name,expected in result['hashes'].items():
        if sha(pilot/name)!=expected:
            raise ValueError('Changed completed-run data')
    if comparison['hashes']['new_result']!=sha(pilot/'RESULT.json'):
        raise ValueError('Unmatched repetition comparison')
    diagnostic=read(RUN/'continuation_proposal_crossfit/RESULT.json')
    reg=read(RUN/'phase_real_refined/REGISTRATION.json'); oracle=read(RUN/'phase_real_refined/PROPOSAL_ORACLE.json')
    for name,expected in reg['hashes'].items():
        if sha(RUN/name)!=expected:
            raise ValueError('Changed refined-proposal input: '+name)
    if oracle['registration_sha256']!=sha(RUN/'phase_real_refined/REGISTRATION.json'):
        raise ValueError('Proposal oracle has wrong registration')
    if sha(ROOT/'REGISTRO_C6.json')!=sha(RUN/'REGISTRO_C6.json'):
        raise ValueError('Frozen C6 changed')
    now=datetime.now(timezone.utc).isoformat()
    repeat=RUN/'phase_native_repeat/SEOBNRv4HM_seed130942_N16384'
    live=[dict(session_id=40860,kind='independent_native_repeat',family='SEOBNRv4HM',last_progress=read(repeat/'PROGRESS.json')),
          dict(session_id=15254,kind='original_generator_rate_audit',family='SEOBNRv4HM',last_progress=dict(rate_done=seob_done,total=196)),
          dict(session_id=57200,kind='real_phase_rate_audit',family='IMRPhenomXPHM',last_progress=dict(rate_done=phenom_done,total=347))]
    for entry in live:
        entry['observation']='Specific handle confirmed live by write_stdin in this turn; revalidate before action, do not use files alone as liveness.'
    pending=dict(status='REGISTERED_AND_PROPOSAL_ORACLE_PASSED_NOT_STARTED',
        stage='cache/source_evidence/phase_real_refined',draws=reg['draws'],seed=reg['seed'],
        command='run_real_phase_importance.py --processes 4',
        start_condition='After pending waveform-rate controls are read and pass; then use available workers, preserving all ongoing handles.')
    names=['diagnose_continuation_proposal.py','continuation_proposal_crossfit/REGISTRATION.json',
        'continuation_proposal_crossfit/RESULT.json','build_real_importance_runner.py','run_real_phase_importance.py',
        'REAL_IMPORTANCE_RUNNER_PROVENANCE.json','fit_real_source_refinement.py','phase_real_refined/REGISTRATION.json',
        'phase_real_refined/PROPOSAL.json','phase_real_refined/PROPOSAL_ORACLE.json']
    names += [str((pilot/name).relative_to(RUN)) for name in ('RESULT.json','RESULT_ARRAYS.npz','DENSITY_AUDIT.json',
        'ARITHMETIC_AUDIT.json','PROPOSAL_COMPARISON.json','real_rate_control/REGISTRATION.json')]
    hashes={'cache/source_evidence/'+name:sha(RUN/name) for name in names}
    hashes['record_completed_real_phase_pilot.py']=sha(ROOT/'record_completed_real_phase_pilot.py')
    measured=dict(status='PHENOM_COMPLETE_PARTIAL_LOCAL_PRECISION_NO_SCIENTIFIC_ACCEPTANCE',date_utc=now,
        previous_goal_turn='PROGRESS: real-Nyquist interpolation repaired and validated; failed oracle comparison corrected; preserved samples resumed with custody.',
        this_goal_turn='PROGRESS: Phenom54722 completed; independent density/arithmetic audits passed; inter-run instability measured; held-out numerical proposal refinement passed prospective criterion and normalization oracle.',
        completed_handles=[dict(session_id=54722,exit_code=0),dict(session_id=50600,exit_code=0),
            dict(session_id=78475,exit_code=0),dict(session_id=39755,exit_code=0),dict(session_id=41792,exit_code=0)],
        draws=result['draws'],evaluations=result['evaluations'],local_precision_pass=result['draws_passing_precision'],
        required_datasets=1200,old_local_precision_pass=comparison['old_passing'],
        ESS_quantiles_00_10_50_90_100=arithmetic['ESS_quantiles'],
        max_weight_quantiles=arithmetic['max_weight_quantiles'],
        lnB_MC_sd_quantiles=arithmetic['lnB_MC_sd_quantiles'],
        changes_over_point2=comparison['changes_over_point2'],max_abs_lnB_change=comparison['max_abs_lnB_change'],
        density_audit=density,arithmetic_error_max=max(arithmetic['independent_arithmetic_errors'].values()),
        control_metadata_coverage=result['control_metadata_coverage'],
        crossfit_selected=diagnostic['ranking'][0],proposal_oracle=oracle,
        registered_not_started=pending,active_processes=live,scientific_acceptance=False,C6_changed=False,hashes=hashes)
    text=f'''[REAL — rodada e auditorias aritméticas concluídas; OPEN — convergência e calibração]

# ORDEM 013 — Piloto Phenom completo, precisão parcial e próxima proposta

Registro: {now}. N/A — sem mudança no cânone, no Lean ou em C6.

**Terminou:**54722,código0. Foram contabilizadas todas as16384 propostas:
8554 vetores válidos e7830 integrandos zero fora do suporte. Nenhum ponto
difícil foi descartado. O original62818 permanece falho e preservado.

**Auditorias passaram:** densidade logarítmica com erro
{density['direct_density_log_error']:.12g}; jacobiano relativo
{density['max_independent_Jacobian_relative_error']:.12g}; erro máximo de
soma independente (inclui ESS)={measured['arithmetic_error_max']:.12g}.
Erro no próprio lnB={arithmetic['independent_arithmetic_errors']['lnB']:.12g}.

**Precisão local:**{result['draws_passing_precision']}/1200 conjuntos,
contra{comparison['old_passing']}/1200 na rodada8192. ESS mínimo/mediano/máximo:
{arithmetic['ESS_quantiles'][0]:.9g}/{arithmetic['ESS_quantiles'][2]:.9g}/{arithmetic['ESS_quantiles'][-1]:.9g}.
Isso não é aceitação física nem calibração:688 conjuntos continuam falhando,
e{comparison['changes_over_point2']} mudaram mais de0.2 em lnB na comparação
com8192. Maior mudança={comparison['max_abs_lnB_change']:.10g}.
Não combinar as simulações como eventos nem converter esses lnB em sigma.

**Controles antigos:** máximos numéricos disponíveis para426 pontos; para8128
somente o fato de terem atravessado os testes antes da gravação, conforme
implementação preservada. Essa limitação segue explícita. Os próximos blocos
guardam os controles dentro do mesmo NPZ, junto com os vetores.

**Diagnóstico da próxima amostragem:**12 candidatos comparados em duas metades,
com seleção pela eficiência prevista, nunca pelo sinal da evidência.
Venceu `{reg['selected']['id']}`: pior-metade, décimo percentil de ganho
{reg['selected']['min_fold_gain10']:.9g}; ganho mediano
{reg['selected']['min_fold_median_gain']:.9g}. É previsão incerta, não precisão
conquistada. A hipótese de envelope foi testada e não venceu.

**Registrada, ainda não iniciada:**32768 propostas,seed130972,
`phase_real_refined`. Mesmos priors físicos e likelihood;70% mistura ajustada,
20% mistura anterior e10% prior completo. Oráculo independente32768/seed130850:
normalização{oracle['mean'][0]:.9g} ±{oracle['MC_standard_errors'][0]:.9g};
maior desvio padronizado dos13 momentos={oracle['max_standardized_error']:.9g}.
O novo amostrador reaproveita o código existente, altera o leitor já validado
e acrescenta apenas a persistência dos controles aos blocos.

**Ativos:**40860(SEOB16384);15254(controle de resolução SEOB,{seob_done}/196);
57200(controle de resolução Phenom,{phenom_done}/347). Revalidar os handles.
Os controles de resolução são nos pontos dominantes, não um limite global
de erro do posterior. Antes de lançar `run_real_phase_importance.py --processes 4`,
ler seus resultados; se algum reprovar, tratar a falha primeiro.

**Demais próximos passos:** concluir/auditar/comparar SEOB; executar a combinação
já registrada `combine_continuation_families.py run` somente após os dois
resultados e auditorias de densidade. Esse registro usa a continuação Phenom
16384 e SEOB16384; a nova proposta32768 não substitui esse caminho em silêncio.
Precisão integral, repetição, posterior contínuo e viés/cobertura continuam abertos.
Não repetir as cadeias C1-C4/C6/C7 já verificadas.
'''
    safe(receipt,(json.dumps(measured,indent=2,ensure_ascii=False)+'\n').encode())
    safe(handoff,text.encode())
    path=ROOT/'STATUS_ORDEM_013.json'; status=read(path)
    status.update(date_utc=now,active_processes=live,previous_goal_turn=measured['previous_goal_turn'],
        this_goal_turn=measured['this_goal_turn'])
    status['verified']['C5_completed_real_phase_pilot']={k:v for k,v in measured.items() if k!='hashes'}
    status['registered_not_started']=[pending,dict(status='REGISTERED_WAITING_SEOB_RESULT',
        stage='cache/source_evidence/source_family_combination_real_repeat',command='combine_continuation_families.py run')]
    status['hashes'].update(hashes)
    status['next_action']='Revalidar40860(SEOB repeat),15254(rateSEOB),57200(ratePhenom).54722 concluiu código0:512/1200 precisão local;120 mudançaslnB>.2. Ler controles de taxa antes de iniciar run_real_phase_importance.py --processes4 (32768,seed130972;fit/oracle já feitos). Após SEOB terminar, auditar/comparar e executar combine_continuation_families.py run. Não substituir os caminhos registrados.'
    status['requirements_remaining'][0]=status['next_action']
    safe(path,(json.dumps(status,indent=2,ensure_ascii=False)+'\n').encode())
    path=ROOT/'PROGRESSO.md'; safe(path,path.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps(dict(status=measured['status'],local_precision_pass=result['draws_passing_precision'],
        active_handles=[p['session_id'] for p in live],handoff=str(handoff)),ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--seob-rate-done',type=int,required=True)
    parser.add_argument('--phenom-rate-done',type=int,required=True);args=parser.parse_args()
    main(args.seob_rate_done,args.phenom_rate_done)
