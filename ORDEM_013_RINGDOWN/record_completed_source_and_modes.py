"""Close stale live state using terminal artifacts, keeping every pilot result."""
from datetime import datetime, timezone
import json
from record_source_evidence_start import ROOT, RUN, safe, sha


def main():
    receipt = ROOT/'C5_SOURCE_8192_AND_NATIVE_MODES.json'
    handoff = ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_fonte8192_e_modos_nativos.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once record')
    folder = RUN/'phase_ringdown_regularized/IMRPhenomXPHM_seed130861_N8192'
    read = lambda p: json.loads(p.read_bytes())
    result, density, rate, comparison = [read(folder/n) for n in
        ('RESULT.json','DENSITY_AUDIT.json','AUDIT_RATE.json','PROPOSAL_COMPARISON.json')]
    phase = read(RUN/'stable_phase_prior_controls/RESULT.json')
    native = read(RUN/'DIRECT_SEOB_MODES_CORRECTED_VALIDATION.json')
    mesh = read(RUN/'LAL_INTERNAL_MESH_AUDIT.json')
    assert result['draws'] == 8192 and result['evaluations'] == 4299
    assert comparison['new_passing'] == 0 and phase['failures'] == 0
    assert native['status'] == 'PASS_DIRECT_SEOB_MODES'
    assert sha(RUN/'direct_seob_modes.py') == native['source_sha256']
    assert sha(RUN/'lal_generator_source_gitlab/LALSimIMRSpinAlignedEOB.c') == mesh['source_sha256']
    paths = [folder/n for n in ('RESULT.json','RESULT_ARRAYS.npz','PROPOSALS.npz','DENSITY_AUDIT.json','AUDIT_RATE.json','PROPOSAL_COMPARISON.json')]
    paths += [RUN/n for n in ('stable_phase_prior_controls/REGISTRATION.json','stable_phase_prior_controls/RESULT.json',
        'DIRECT_SEOB_MODES_VALIDATION.json','DIRECT_SEOB_MODES_CORRECTED_VALIDATION.json','direct_seob_modes.py',
        'LAL_INTERNAL_MESH_AUDIT.json','lal_generator_source_gitlab/LALSimIMRSpinAlignedEOB.c',
        'lal_generator_source_gitlab_LALSimInspiralGeneratorLegacy/LALSimInspiralGeneratorLegacy.c')]
    paths.append(ROOT/'record_completed_source_and_modes.py')
    hashes = {str(p.relative_to(ROOT)).replace('\\','/'): sha(p) for p in paths}
    now = datetime.now(timezone.utc).isoformat()
    measured = dict(status='NUMERICAL_PROGRESS_SOURCE_EVIDENCE_NOT_ACCEPTED', date_utc=now,
        previous_goal_turn='PROGRESS: completed 8192-source integration, audits, 504 phase controls and native-mode verification; intervening short-prompt reply was not goal work',
        this_goal_turn='PROGRESS: verified terminal artifacts and removed stale live handle41895; preparing actual internal-mesh refinement',
        active_processes=[], handle_observation='write_stdin41895 returned Unknown process id on this turn; complete RESULT and all audits exist',
        draws=result['draws'], evaluations=result['evaluations'], zero_integrand_draws=result['draws']-result['evaluations'],
        precision_pass=comparison['new_passing'], ESS_quantiles=comparison['new_ESS_quantiles'],
        efficiency_old=comparison['old_median_ESS_per_draw'], efficiency_new=comparison['new_median_ESS_per_draw'],
        changed_lnB_over_point2=comparison['changes_over_point2'], max_lnB_change=comparison['max_abs_lnB_change'],
        density_audit_status=density['status'], rate_audit_status=rate['status'],
        max_active_rate_difference=rate['max_active_rate_difference'], rate_control_pass=rate['rate_control_pass'],
        phase_controls={k:phase[k] for k in ('status','count','failures','max_logL_errors_SNR40_600','max_relative_waveform_error')},
        native_modes={k:native[k] for k in ('status','count','max_relative_error','dynamics','scope')},
        mesh_status=mesh['status'], physical_prior_changed=False, scientific_acceptance=False, C6_changed=False, hashes=hashes)
    text = f'''[REAL — resultados e implementação conferidos; OPEN — precisão da evidência integrada]

# ORDEM 013 — Encerramento da rodada8192 e modos nativos

Registro: {now}. Axiomas: N/A — sem Lean.

**PAGO:** rodada8192 concluída, {result['evaluations']} avaliações no suporte; as demais
propostas têm integrando zero e continuam no denominador. Auditorias de densidade e
aritmética concluídas. O controle8192→16384Hz em pontos dominantes deu máximo
|ΔlogL|={rate['max_active_rate_difference']:.17g}; não é cota uniforme do posterior.

**NÃO PAGO:** zero das1200 razões atinge a precisão registrada. Quantis ESS:
{comparison['new_ESS_quantiles']}. A eficiência mediana por proposta passou de
{comparison['old_median_ESS_per_draw']:.8g} para {comparison['new_median_ESS_per_draw']:.8g}.
Portanto a mistura de três componentes não resolveu a eficiência. Em
{comparison['changes_over_point2']} casos |ΔlnB|>0,2 contra o piloto2048;
máximo={comparison['max_abs_lnB_change']:.8g}. Erros Monte Carlo de baixa ESS
podem ser subestimados; não promover médias/quantis a resultado científico.

**PAGO:** correção do pico comum testada em{phase['count']} controles, zero falhas;
erro máximo de logL em SNR40/600={phase['max_logL_errors_SNR40_600']}.
São três fontes de referência e quatro pontos do prior, não prova uniforme.

**PAGO:** reconstrução direta dos modos SEOB verificada em{native['count']} casos,
erro relativo máximo={native['max_relative_error']:.17g}, fonte90/8192Hz.
A tentativa anterior falhou e está preservada. A cópia corrigida usa a rotação
de polarização explícita no LAL e as mesmas conversões SI do PyCBC.

**DIAGNÓSTICO:** fonte oficial da versão instalada mostra que, para fonte90,
8192 até131072Hz mantêm a mesma malha interna. A taxa262144 realmente a refina.
Isso motiva o próximo controle, mas ainda não demonstra a causa única do erro.
Código consultado: {mesh['source_url']} (commit e SHA conferidos).

**CONTINUAR:** validar um adaptador de banco de fase via modos nativos contra a
API original; então testar131072/262144/524288Hz com malha interna medida.
Não repetir a mistura8192 sem diagnóstico/adaptação. Faltam precisão/repetições,
recuperação SEOB integrada, demais leituras/SNR, viés/cobertura de intensidade
contínua e atualização do pacote. C6 e fontes canônicas preservados.

O identificador41895 deixou de existir; não há processo vivo registrado aqui.
Comandos já concluídos: refine_ringdown_proposal.py; audit_registered_transport.py
--stage phase_ringdown_regularized; audit_phase_source.py com --rate;
compare_phase_runs.py; validate_stable_phase_prior.py; direct_seob_modes.py.
Arquivos/resultados são create-once; reprodução deve usar diretório separado.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
'''+''.join(f'| {p} | {h} |\n' for p,h in hashes.items())
    safe(receipt,(json.dumps(measured,indent=2,ensure_ascii=False)+'\n').encode())
    safe(handoff,text.encode())
    p=ROOT/'STATUS_ORDEM_013.json'; status=read(p)
    status.update(date_utc=now, previous_goal_turn=measured['previous_goal_turn'],this_goal_turn=measured['this_goal_turn'],active_processes=[])
    status['verified']['C5_source8192_native_modes']={k:v for k,v in measured.items() if k!='hashes'}
    status['hashes'].update(hashes)
    status['next_action']='Validar adaptador nativo de modos SEOB; medir refinamento real da malha interna. Rodada8192 e auditorias concluídas, não aceitas por baixa ESS. Não repetir sem melhorar proposta. Nenhum processo conhecido vivo.'
    status['requirements_remaining'][0]=status['next_action']
    safe(p,(json.dumps(status,indent=2,ensure_ascii=False)+'\n').encode())
    p=ROOT/'PROGRESSO.md'; safe(p,p.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps({k:measured[k] for k in ('status','draws','precision_pass','ESS_quantiles','active_processes')}))


if __name__=='__main__':
    main()
