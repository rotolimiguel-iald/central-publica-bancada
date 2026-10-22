"""Record completed SEOB pilot, rejected adaptation and primary-source scope."""
from datetime import datetime, timezone
import json
import numpy as np
from record_source_evidence_start import ROOT, RUN, safe, sha


def read(path):
    return json.loads(path.read_bytes())


def main():
    receipt = ROOT/'C5_SEOB_PILOT_AND_REPEAT_REGISTRATION.json'
    handoff = ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_piloto_SEOB_e_repeticao_registrada.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once receipt')
    folder = RUN/'phase_native_seob/SEOBNRv4HM_seed130901_N2048'
    result = read(folder/'RESULT.json'); density = read(folder/'DENSITY_AUDIT.json')
    if density['hashes']['RESULT.json'] != sha(folder/'RESULT.json'):
        raise ValueError('Source-density audit is stale')
    for n, h in result['hashes'].items():
        if sha(folder/n) != h:
            raise ValueError('Pilot result input changed: '+n)
    with np.load(folder/'RESULT_ARRAYS.npz') as f:
        quantiles = {k: np.quantile(f[k], [0, .1, .5, .9, 1]).tolist()
                     for k in ('ESS', 'max_weight', 'lnB_MC_sd')}
    full = read(RUN/'native_proposal_crossfit/RESULT.json')
    product = read(RUN/'native_product_proposal_diagnostic/RESULT.json')
    if full['prospective_refinement_allowed'] or product['prospective_refinement_allowed']:
        raise ValueError('Adaptation decision changed')
    repeat = read(RUN/'phase_native_repeat/REGISTRATION.json')
    for n, h in repeat['hashes'].items():
        if sha(RUN/n) != h:
            raise ValueError('Repeat registration changed: '+n)
    archive = ROOT/'cache/literature_milburn_followup'
    literature = read(archive/'PROVENANCE.json')
    if literature['sha256'] != sha(archive/'milburn_grqc0308021.html'):
        raise ValueError('Primary-source archive changed')
    if sha(ROOT/'REGISTRO_C6.json') != sha(RUN/'REGISTRO_C6.json'):
        raise ValueError('Frozen C6 changed')
    now = datetime.now(timezone.utc).isoformat()
    phenom = RUN/'phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384'
    live = [dict(session_id=62818, kind='source_integration', family='IMRPhenomXPHM',
            folder=str(phenom.relative_to(ROOT)).replace('\\','/'), last_progress=read(phenom/'PROGRESS.json'),
            observation='Live write_stdin handle verified immediately before this record; revalidate next turn'),
        dict(session_id=15254, kind='original_generator_rate_audit', family='SEOBNRv4HM',
            folder=str(folder.relative_to(ROOT)).replace('\\','/'), last_progress=dict(rate_done=33, total=196),
            observation='Live write_stdin handle returned rate_done33/196 in this turn. No AUDIT_RATE result yet; revalidate handle, not files alone.')]
    names = ['adapt_native_source_proposal.py', 'diagnose_native_product_proposal.py', 'repeat_native_source.py',
        'phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT.json',
        'phase_native_seob/SEOBNRv4HM_seed130901_N2048/RESULT_ARRAYS.npz',
        'phase_native_seob/SEOBNRv4HM_seed130901_N2048/DENSITY_AUDIT.json',
        'native_proposal_crossfit/REGISTRATION.json', 'native_proposal_crossfit/RESULT.json',
        'native_product_proposal_diagnostic/REGISTRATION.json', 'native_product_proposal_diagnostic/RESULT.json',
        'phase_native_repeat/REGISTRATION.json', 'phase_native_repeat/PROPOSAL.json', 'phase_native_repeat/PROPOSAL_ORACLE.json']
    hashes = {'cache/source_evidence/'+n: sha(RUN/n) for n in names}
    for n in ('fetch_milburn_followup.py', 'C0_MILBURN_FONTE_COMPLEMENTAR.md',
              'cache/literature_milburn_followup/PROVENANCE.json',
              'cache/literature_milburn_followup/milburn_grqc0308021.html',
              'record_seob_pilot_and_followup.py'):
        hashes[n] = sha(ROOT/n)
    measurement = dict(status='SEOB_PILOT_AUDITED_NO_PRECISION_ACCEPTANCE', date_utc=now,
        previous_goal_turn='PROGRESS: family mixture derived, tested and preregistered; incomplete-run consumer refused',
        this_goal_turn='PROGRESS: native SEOB pilot completed and source-density audit passed; full6D and product adaptations failed held-out criteria; independent higher-count repeat registered; Milburn follow-up primary text consulted and archived',
        seob_process_61984_exit_code=0, source_result_status=result['status'],
        pilot_draws=result['draws'], pilot_valid=result['evaluations'], passing_datasets=result['draws_passing_precision'],
        quantiles_00_10_50_90_100=quantiles, density_audit=density,
        full6D_best_gain10=full['ranking'][0]['min_fold_gain10'],
        product_best_gain10=product['ranking'][0]['min_fold_gain10'],
        rejected_adaptive_proposals=len(full['ranking'])+len(product['ranking']),
        active_processes=live,
        repeat=dict(status='REGISTERED_NOT_STARTED', seed=repeat['seed'], draws=repeat['draws'],
            stage='cache/source_evidence/phase_native_repeat', proposal_changed=False,
            original_proposal_oracle_reused=True, new_oracle_claimed=False),
        literature_access=literature, scientific_acceptance=False, C6_changed=False, hashes=hashes)
    text = f'''[REAL — piloto concluído e auditado; OPEN — precisão e calibração]

# ORDEM 013 — Piloto SEOB, adaptações recusadas e repetição registrada

Registro: {now}. N/A — sem Lean novo.

**O piloto terminou:** processo61984, código0; {result['draws']} propostas,
{result['evaluations']} avaliações dentro do suporte. As propostas restantes
têm integrando zero e permanecem no denominador. A auditoria independente
da densidade/suporte/jacobiano e aritmética passou. Erro logarítmico da
densidade={density['direct_density_log_error']:.10g}; discrepância das somas
={density['direct_integral_arithmetic_error']:.10g}.

**A precisão não passou:** {result['draws_passing_precision']}/1200 conjuntos.
ESS mínimo/mediano/máximo={quantiles['ESS'][0]:.8g}/{quantiles['ESS'][2]:.8g}/{quantiles['ESS'][4]:.8g}.
Maior peso normalizado={quantiles['max_weight'][-1]:.8g}. A pequena incerteza
delta de certos quocientes não vence essa reprovação. Os ln B do arquivo são
pilotos, não resultados aceitos nem significância física.

**Diagnóstico que mudou a próxima ação:** treinar no próprio piloto SEOB não
melhorou a generalização. Melhor ganho no décimo percentil, pior metade:
{measurement['full6D_best_gain10']:.8g} em seis dimensões e
{measurement['product_best_gain10']:.8g} no produto espectral. Ambos abaixo
de1. Foram recusadas {measurement['rejected_adaptive_proposals']} alternativas;
nenhuma rodada física usa esses ajustes. Os diagnósticos reutilizam amostras
do piloto e não são validação científica independente.

**Repetição registrada, ainda não iniciada:**16384 propostas, seed130942,
`phase_native_repeat`. A proposta é cópia byte a byte da anterior. Seu oráculo
de normalização foi reutilizado com proveniência explícita; não foi anunciado
um teste novo. `repeat_native_source.py run --processes 4` usa novas amostras
e os mesmos critérios. Iniciar quando a rodada Phenom liberar os trabalhadores.

**Ativos, confirmados via handles:**62818 (Phenom16384) e15254 (controle SEOB
com gerador original a16384Hz,196 pontos dominantes;33 tinham sido conferidos
na observação desta sessão). Não duplicar. Revalidar na próxima continuação.
O controle de taxa completo ainda não produziu resultado.

**Bibliografia:** o texto HTML posterior do próprio Milburn foi lido e
arquivado; ver `C0_MILBURN_FONTE_COMPLEMENTAR.md`. O acesso ao artigo original
de1991 e a Kay–Wald continua limitado como antes. Esse registro não altera
a partição física ou os templates em execução.

**Próxima sequência:** após Phenom terminar, auditoria da densidade e da taxa;
comparação com sua rodada8192; `combine_source_families.py run` sobre os dois
pilotos originais. A mistura continuará não aceita enquanto os componentes
falharem. A repetição SEOB nova deverá ser auditada e comparada ao piloto; não
substituir silenciosamente os caminhos já congelados no registro da mistura.
Viés/cobertura da intensidade contínua continuam pendentes. C6 e cânone intactos.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
'''+''.join(f'| {n} | {h} |\n' for n, h in hashes.items())
    safe(receipt, (json.dumps(measurement, indent=2, ensure_ascii=False)+'\n').encode())
    safe(handoff, text.encode())
    path = ROOT/'STATUS_ORDEM_013.json'; status = read(path)
    status.update(date_utc=now, previous_goal_turn=measurement['previous_goal_turn'],
        this_goal_turn=measurement['this_goal_turn'], active_processes=live)
    status['verified']['C5_SEOB_pilot_followup'] = {k: v for k, v in measurement.items() if k != 'hashes'}
    status['registered_not_started'] = [measurement['repeat']]
    status['hashes'].update(hashes)
    status['next_action'] = 'Revalidar Phenom62818 e auditoria SEOB15254.61984 terminou código0. Ao terminar Phenom: auditar densidade/taxa, comparar8192 e combinar pilotos. Depois lançar repeat_native_source.py run --processes4 (16384/seed130942), ainda não iniciado; proposta idêntica, adaptações recusadas. Não repetir register.'
    status['requirements_remaining'][0] = status['next_action']
    status['requirements_remaining'][-1] = 'Partição/relógio/desenrolamento físicos não selecionados. Milburn2003 HTML lido/arquivado com limites explícitos; Milburn1991 e Kay-Wald1991 continuam no escopo anterior. Não refazer as cadeias C1-C4/C6/C7 já reproduzidas.'
    safe(path, (json.dumps(status, indent=2, ensure_ascii=False)+'\n').encode())
    path = ROOT/'PROGRESSO.md'; safe(path, path.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps(dict(status=measurement['status'], pilot_precision=result['draws_passing_precision'],
        active_processes=live, repeat=measurement['repeat'], handoff=str(handoff)), ensure_ascii=False))


if __name__ == '__main__':
    main()
