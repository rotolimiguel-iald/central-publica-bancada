"""Record the failed original run, verified numerical repair and live continuations."""
from datetime import datetime, timezone
import argparse
import json
from record_source_evidence_start import ROOT, RUN, safe, sha


def read(path):
    return json.loads(path.read_bytes())


def main(rate_done):
    receipt = ROOT/'C5_REAL_PHASE_RECOVERY.json'
    handoff = ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_recuperacao_da_interpolacao_real.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once record')
    validation = read(RUN/'real_phase_adapter_validation_corrected/RESULT.json')
    diagnosis = read(RUN/'real_phase_adapter_validation/ORACLE_FAILURE_DIAGNOSIS.json')
    continuation = RUN/'phase_ringdown_real_continuation'
    reg = read(continuation/'REGISTRATION.json')
    folder = continuation/'IMRPhenomXPHM_seed130892_N16384'
    repeat = RUN/'phase_native_repeat/SEOBNRv4HM_seed130942_N16384'
    if validation['status'] != 'PASS_REAL_PHASE_ADAPTER':
        raise ValueError('Real phase adapter has not passed')
    for name, expected in reg['hashes'].items():
        if sha(RUN/name) != expected:
            raise ValueError('Changed continuation input: '+name)
    for name, expected in reg['copied_npz_hashes'].items():
        if sha(folder/name) != expected:
            raise ValueError('Changed continuation custody copy: '+name)
    if (RUN/'phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/RESULT.json').exists():
        raise ValueError('Original failed run unexpectedly has a result')
    if sha(ROOT/'REGISTRO_C6.json') != sha(RUN/'REGISTRO_C6.json'):
        raise ValueError('Frozen C6 changed')
    now = datetime.now(timezone.utc).isoformat()
    live = [
        dict(session_id=54722, kind='real_phase_continuation', family='IMRPhenomXPHM',
             folder=str(folder.relative_to(ROOT)), last_progress=read(folder/'PROGRESS.json')),
        dict(session_id=40860, kind='independent_native_repeat', family='SEOBNRv4HM',
             folder=str(repeat.relative_to(ROOT)), last_progress=read(repeat/'PROGRESS.json')),
        dict(session_id=15254, kind='original_generator_rate_audit', family='SEOBNRv4HM',
             last_progress=dict(rate_done=rate_done,total=196))]
    for entry in live:
        entry['observation'] = 'Specific write_stdin handle returned live and advancing in this turn; revalidate next turn. Files alone are not process liveness.'
    names = ['diagnose_failed_phase_reconstruction.py','failed_phenom_phase_diagnostic/REGISTRATION.json',
        'failed_phenom_phase_diagnostic/RESULT.json','failed_phenom_phase_diagnostic/point_15627.json',
        'real_fourier_phase.py','phase_marginal_real_source.py','REAL_PHASE_ADAPTER_PROVENANCE.json',
        'validate_real_phase_adapter.py','real_phase_adapter_validation/REGISTRATION.json',
        'diagnose_real_phase_oracle.py','real_phase_adapter_validation/ORACLE_FAILURE_DIAGNOSIS.json',
        'build_real_phase_validation_corrected.py','validate_real_phase_adapter_corrected.py',
        'REAL_PHASE_VALIDATION_CORRECTION.json','real_phase_adapter_validation_corrected/REGISTRATION.json',
        'real_phase_adapter_validation_corrected/RESULT.json','continue_real_phase_source.py',
        'phase_ringdown_real_continuation/REGISTRATION.json','phase_ringdown_real_continuation/PROPOSAL.json',
        'phase_ringdown_real_continuation/PROPOSAL_ORACLE.json','audit_real_phase_continuation.py',
        'prepare_continuation_family_mixture.py','combine_continuation_families.py',
        'CONTINUATION_FAMILY_MIXTURE_PROVENANCE.json','source_family_combination_real_repeat/REGISTRATION.json']
    hashes = {'cache/source_evidence/'+name:sha(RUN/name) for name in names}
    hashes['record_real_phase_recovery.py'] = sha(ROOT/'record_real_phase_recovery.py')
    measurement = dict(status='REAL_FOURIER_CORRECTION_VALIDATED_CONTINUATION_RUNNING', date_utc=now,
        previous_goal_turn='PROGRESS: Phenom terminal failure localized and reproduced; independent SEOB repeat started; proposed correction first failed an auxiliary oracle.',
        previous_visible_nonresearch_turn='Answered the short prompt request; no scientific result or goal completion claimed.',
        this_goal_turn='PROGRESS: diagnosed oracle broadcasting error without changing failed artifacts; independent real trigonometric and full-wave checks passed; recovered all32 diagnostic points; resumed394 remaining draws in separate custody; registered new two-family input paths.',
        original_phenom_handle=62818, original_exit_code=1, diagnostic_handle=80765, diagnostic_exit_code=0,
        corrected_validation_handle=58463, corrected_validation_exit_code=0,
        failed_source_index=15627, original_saved=reg['original_preserved_evaluations'],
        replay_recovered=reg['recovered_evaluations'], remaining_at_start=reg['remaining_evaluations'],
        total_proposals=reg['draws'], valid_proposals=reg['total_valid_evaluations'],
        oracle_diagnosis=diagnosis, validation=validation,
        metadata_limitation=reg['metadata_limitation'],
        incomplete_result_reader='audit_real_phase_continuation.py correctly refused absent RESULT.json with exit1; no partial arithmetic output.',
        active_processes=live, scientific_acceptance=False, C6_changed=False,
        original_sources_changed=False, physical_clock_selected=False, hashes=hashes)
    failed = next(row for row in validation['source_rows'] if row['index'] == 15627)
    error = max(row['direct_amplitude_integral_error'] for row in validation['algebra']['rows'])
    text = f'''[REAL — correção numérica verificada; OPEN — convergência científica]

# ORDEM 013 — Recuperação da interpolação real

Registro: {now}. N/A — sem alteração de Lean, um.py, Atlas ou C6.

O processo Phenom62818 terminou com código1. Foram preservados8128 vetores
completos em508 blocos;426 avaliações ainda faltavam. O diagnóstico80765
reproduziu a falha somente no índice15627 entre32 pontos: os outros31 passaram.
Os arquivos da rodada original continuam intactos e sem RESULT.json.

## Causa e correção verificadas

Para dados reais com N par, o coeficiente de Nyquist real deve multiplicar
cos(Nφ/2). O leitor antigo usava a exponencial complexa isolada e recusava
sua parte imaginária, embora devolvesse apenas a parte real. Substituir
essa exponencial pelo cosseno preserva a interpolação real anterior.
O novo leitor verifica dados/coeficientes, simetria conjugada e resíduo
imaginário. Os limites contra a forma de onda completa e a quadratura
permaneceram1e-6 relativo,0.001 em logL e1e-5 na integração de fase.

O primeiro teste da correção falhou por um erro próprio de broadcasting:
comparou matrizes(34,1,9) e(34,9), cruzando fases diferentes. Ele e seu
registro foram preservados. O teste corrigido compara formatos iguais;
erro máximo da integral gaussiana independente={error:.12g}.
Oráculos cardinais N16/N17 e cosseno puro passaram; três entradas adulteradas
foram recusadas. Em dois pontos já aprovados, diferença da integral=0.
No ponto15627: erro relativo de forma de onda
{failed['controls']['max_relative_waveform_interpolation_error']:.12g};
erro máximo logL={failed['controls']['max_logL_interpolation_error']:.12g};
erro de quadratura={failed['controls']['max_phase_quadrature_error']:.12g}.
Os bancos16/32/64 concordaram dentro de0.001. Validador58463 terminou código0.

## Continuação sem apagar o ponto difícil

`phase_ringdown_real_continuation`: cópia byte a byte das16384 propostas e
dos8128 resultados anteriores, mais32 pontos recuperados;394 avaliações
novas. Denominador16384 preservado, inclusive integrandos zero fora do suporte.
As novas avaliações guardam os controles em arquivos junto aos blocos.
**Limitação:** os valores exatos dos controles dos8128 pontos antigos estavam
somente na RAM; não foram recuperados. O caminho original só escrevia um
resultado depois de seus controles passarem, mas isso não recupera seus máximos.

Ativos conferidos nesta sessão:54722(continuação Phenom,2 trabalhadores),
40860(repetição SEOB16384,4 trabalhadores),15254(auditoria SEOB original,
2 trabalhadores,{rate_done}/196 na consulta). Revalidar os três handles.
O auditor da continuação recusou corretamente a ausência do resultado final.

## Sequência necessária

1. Quando54722 terminar: `audit_registered_transport.py IMRPhenomXPHM_seed130892_N16384 --stage phase_ringdown_real_continuation`;
   `audit_real_phase_continuation.py --rate --processes 2`;
   `compare_phase_runs.py phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192 phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384`.
2. Quando40860 terminar: auditar densidade/taxa e comparar com o piloto SEOB2048.
   Não duplicar o processo enquanto seu handle estiver vivo.
3. A nova combinação já está registrada em `source_family_combination_real_repeat`:
   `combine_continuation_families.py run` espera ambos RESULT e DENSITY_AUDIT.
   Ela utiliza a continuação Phenom e a repetição SEOB16384, com os mesmos pesos
   das famílias e fórmulas verificadas. O registro anterior não foi alterado.
4. Precisão componente a componente, repetição independente e viés/cobertura
   de intensidade contínua ainda são necessários. Nenhum resultado desta
   correção estabelece significância física ou seleciona relógio/partição.
'''
    safe(receipt, (json.dumps(measurement,indent=2,ensure_ascii=False)+'\n').encode())
    safe(handoff,text.encode())
    path = ROOT/'STATUS_ORDEM_013.json'; status = read(path)
    status.update(date_utc=now, active_processes=live,
        previous_goal_turn=measurement['previous_goal_turn'], this_goal_turn=measurement['this_goal_turn'])
    status['verified']['C5_real_phase_recovery'] = {k:v for k,v in measurement.items() if k != 'hashes'}
    status['registered_not_started'] = [dict(status='REGISTERED_WAITING_SOURCE_RESULTS',
        stage='cache/source_evidence/source_family_combination_real_repeat',
        command='combine_continuation_families.py run')]
    status['preserved_failures'] += [
        'Phenom62818 exit1: non-real Nyquist interpolation at index15627; all508 saved chunks preserved.',
        'Original real-phase correction validator failed due to broadcasting(34,1,9)-(34,9); failed source and registration retained; corrected separate validator passed.',
        'Continuation audit refused missing RESULT.json before run completion; exit1, no partial evidence accepted.']
    status['hashes'].update(hashes)
    status['next_action'] = 'Revalidar54722(cont.Ph),40860(repeatSEOB),15254(rateSEOB).62818 terminou código1. Depois dos resultados: auditar densidade/taxa, comparar repetições e executar combine_continuation_families.py run. Não repetir registros nem alterar o antigo source_family_combination. Metadados numéricos dos8128 pontos originais indisponíveis, declarados.'
    status['requirements_remaining'][0] = status['next_action']
    safe(path,(json.dumps(status,indent=2,ensure_ascii=False)+'\n').encode())
    path = ROOT/'PROGRESSO.md'; safe(path,path.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps(dict(status=measurement['status'],handoff=str(handoff),active_handles=[p['session_id'] for p in live]),ensure_ascii=False))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--rate-done',type=int,required=True)
    main(parser.parse_args().rate_done)
