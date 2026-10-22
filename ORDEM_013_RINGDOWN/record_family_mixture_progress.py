"""Preserve the verified mixture preparation without claiming source results."""
from datetime import datetime, timezone
import json
from record_source_evidence_start import ROOT, RUN, safe, sha


def read(path):
    return json.loads(path.read_bytes())


def main():
    receipt = ROOT/'C5_FAMILY_MIXTURE_PREPARATION.json'
    handoff = ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_mistura_das_familias_preparada.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once progress receipt')
    validation = read(RUN/'source_family_mixture_validation/RESULT.json')
    if validation['status'] != 'PASS_FAMILY_MIXTURE_ARITHMETIC':
        raise ValueError('Mixture control failed')
    for directory in ('source_family_mixture_validation', 'source_family_combination'):
        reg = read(RUN/directory/'REGISTRATION.json')
        for name, expected in reg['hashes'].items():
            if sha(RUN/name) != expected:
                raise ValueError('Registered file changed: '+name)
    if (RUN/'source_family_combination/RESULT.json').exists():
        raise ValueError('Preparation-only receipt would be stale')
    if sha(ROOT/'REGISTRO_C6.json') != sha(RUN/'REGISTRO_C6.json'):
        raise ValueError('Frozen strain registration changed')
    now = datetime.now(timezone.utc).isoformat()
    runs = read(RUN/'source_family_combination/REGISTRATION.json')['runs']
    live = []
    for (family, name), handle in zip(runs.items(), (62818, 61984)):
        live.append(dict(family=family, session_id=handle, folder='cache/source_evidence/'+name,
            last_progress=read(RUN/name/'PROGRESS.json'),
            live_observation='write_stdin returned this live session immediately before this record. Progress files alone are not liveness evidence; revalidate next turn.'))
    names = ['source_family_mixture.py', 'validate_source_family_mixture.py', 'combine_source_families.py',
             'FAMILY_MIXTURE_METHOD.md', 'source_family_mixture_validation/REGISTRATION.json',
             'source_family_mixture_validation/RESULT.json', 'source_family_mixture_validation/TOY_REPETITIONS.npz',
             'source_family_combination/REGISTRATION.json']
    hashes = {'cache/source_evidence/'+n: sha(RUN/n) for n in names}
    hashes['record_family_mixture_progress.py'] = sha(ROOT/'record_family_mixture_progress.py')
    measurement = dict(status='FAMILY_MIXTURE_VALIDATED_SOURCE_RUNS_STILL_ACTIVE', date_utc=now,
        previous_goal_turn='NO_GOAL_PROGRESS: answered the requested short prompt; active source jobs revalidated in this continuation',
        this_goal_turn='PROGRESS: derived centered mixture covariance; implemented and verified analytic/repeated-sampling controls; registered two-family combination; incomplete-run consumer refusal verified',
        oracle=validation, active_processes=live,
        incomplete_consumer_guard=dict(observed_exit_code=1,
            missing_file='phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384/RESULT.json',
            message='Mixture is not ready', result_written=False,
            evidence_scope='Observed tool execution of combine_source_families.py run, followed by inspection: only REGISTRATION.json exists'),
        scientific_acceptance=False, C6_changed=False, hashes=hashes)
    table = '\n'.join(f"- {v['family']}: sessão {v['session_id']}, {v['last_progress']['done']}/{v['last_progress']['valid_draws']} avaliações no suporte." for v in live)
    text = f'''[REAL — controle estatístico implementado; OPEN — precisão e calibração astrofísicas]

# ORDEM 013 — Combinação preparada das famílias de recuperação

Registro: {now}. N/A — sem Lean novo.

**Avanço:** a mistura de evidências das duas famílias está implementada e
registrada, com prior explícito 1/2 para cada família sob ambas as hipóteses.
As simulações permanecem separadas. A mistura não faz média de ln B nem
seleciona a família mais favorável a cada hipótese.

**Resultado do controle:** em 4000 repetições de integrais analíticas,
a razão entre variância observada e prevista foi
{validation['empirical_over_predicted_variance']:.12g}. O erro de Monte Carlo
preserva o pareamento das hipóteses dentro de cada família e centra sua
influência, pois as probabilidades posteriores das famílias podem mudar.
No controle com integrandos constantes, o erro correto foi
{validation['constant_likelihood_correct_MC_sd']:.8g}; omitir o centramento
produziria erro espúrio {validation['constant_likelihood_spurious_uncentered_MC_sd']:.8g}.
Isso é teste do estimador, não resultado de ondas gravitacionais.

**Recusas verificadas:** quatro entradas inválidas; componente com ESS baixo
mesmo com erro pareado cancelado; tentativa de consumir uma rodada incompleta.
Esta última terminou com código 1 e nenhum resultado da mistura foi gravado.

**Rodadas ainda ativas, observadas via handles antes deste registro:**
{table}

**O que falta:** terminar as integrações, auditar densidade/taxa, comparar
repetições e recuperar a intensidade contínua com viés/cobertura medidos.
A mistura não apaga falhas de precisão dos componentes. Não há resultado
aceito novo de ln B ou sigma nesta etapa. Os 50 intervalos de ruído continuam
reutilizados e pareados; O4/O5 estão normalizados separadamente a SNR40.

**Próximo passo:** após os RESULT.json, executar as auditorias existentes
`audit_registered_transport.py` com as respectivas fases, e então
`combine_source_families.py run`. O registro já existe: não repetir `register`.
Não reiniciar processos vivos. A nota `cache/source_evidence/FAMILY_MIXTURE_METHOD.md`
contém derivação, limitações e comandos exatos. C6 e originais preservados.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
'''+''.join(f'| {p} | {h} |\n' for p, h in hashes.items())
    safe(receipt, (json.dumps(measurement, indent=2, ensure_ascii=False)+'\n').encode())
    safe(handoff, text.encode())
    path = ROOT/'STATUS_ORDEM_013.json'
    status = read(path)
    status.update(date_utc=now, previous_goal_turn=measurement['previous_goal_turn'],
        this_goal_turn=measurement['this_goal_turn'], active_processes=live)
    status['verified']['C5_family_mixture_preparation'] = {k: v for k, v in measurement.items() if k != 'hashes'}
    status['hashes'].update(hashes)
    status['next_action'] = 'Revalidar 62818/61984. Após RESULT, auditar densidade/taxa/repetição. Combinação registrada em source_family_combination; run exige os dois resultados e DENSITY_AUDIT. Não repetir register nem testes já concluídos. Calibração contínua segue aberta.'
    status['requirements_remaining'][0] = status['next_action']
    safe(path, (json.dumps(status, indent=2, ensure_ascii=False)+'\n').encode())
    path = ROOT/'PROGRESSO.md'
    safe(path, path.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps(dict(status=measurement['status'], active_processes=live, handoff=str(handoff)), ensure_ascii=False))


if __name__ == '__main__':
    main()
