"""Record completed adapter/mesh controls and the freshly observed live run."""
from datetime import datetime,timezone
import argparse
import json
from record_source_evidence_start import ROOT,RUN,safe,sha


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--live-session',type=int,required=True)
    args=parser.parse_args()
    receipt=ROOT/'C5_NATIVE_MESH_AND_BALANCED_START.json'
    handoff=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_malha_interna_e_amostragem_balanceada.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once record')
    read=lambda p:json.loads(p.read_bytes())
    adapter=read(RUN/'native_seob_phase_validation/RESULT.json')
    mesh=read(RUN/'native_internal_mesh_refinement/RESULT.json')
    diagnostic=read(RUN/'balanced_proposal_diagnostic/RESULT.json')
    proposal=read(RUN/'phase_ringdown_balanced/PROPOSAL.json')
    oracle=read(RUN/'phase_ringdown_balanced/PROPOSAL_ORACLE.json')
    folder=RUN/'phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384'
    start=read(folder/'START.json'); progress=read(folder/'PROGRESS.json')
    if (folder/'RESULT.json').exists():
        raise ValueError('Run already complete; do not record a stale live state')
    assert adapter['failures']==0 and mesh['adapter_pass']
    assert oracle['status']=='PASS_TRANSPORT_PROPOSAL_MOMENTS'
    paths=[ROOT/'record_native_mesh_and_balanced_start.py']
    names=['native_seob_phase_source.py','validate_native_seob_phase.py','refine_native_internal_mesh.py',
        'diagnose_proposal_efficiency.py','diagnose_balanced_proposal.py','refine_balanced_source_proposal.py',
        'direct_seob_modes.py','native_seob_phase_validation/REGISTRATION.json','native_seob_phase_validation/RESULT.json',
        'native_internal_mesh_refinement/REGISTRATION.json','native_internal_mesh_refinement/RESULT.json',
        'proposal_efficiency_diagnostic/REGISTRATION.json','proposal_efficiency_diagnostic/RESULT.json',
        'balanced_proposal_diagnostic/REGISTRATION.json','balanced_proposal_diagnostic/RESULT.json',
        'phase_ringdown_balanced/PROPOSAL.json','phase_ringdown_balanced/REGISTRATION.json','phase_ringdown_balanced/PROPOSAL_ORACLE.json']
    paths += [RUN/n for n in names]+[folder/'START.json',folder/'PROPOSALS.npz']
    paths += list((RUN/'native_internal_mesh_refinement').glob('*.npz'))
    for relative in ('native_seob_phase_validation/REGISTRATION.json','native_internal_mesh_refinement/REGISTRATION.json',
                     'phase_ringdown_balanced/REGISTRATION.json'):
        for name,h in read(RUN/relative)['hashes'].items():
            if sha(RUN/name)!=h:
                raise ValueError('Custody mismatch: '+name)
    hashes={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in paths}
    now=datetime.now(timezone.utc).isoformat()
    live=dict(tool='write_stdin',session_id=args.live_session,status='LIVE_OBSERVED_BEFORE_RECORD',
        folder=str(folder.relative_to(ROOT)).replace('\\','/'),last_progress=progress,
        observation='Tool returned live session and progressing output immediately before this record; revalidate next turn')
    measured=dict(status='NUMERICAL_CONTROLS_COMPLETE_SOURCE_INTEGRATION_RUNNING',date_utc=now,
        previous_goal_turn='PROGRESS:8192 integration/audits,504 phase tests,native source reconstruction; side reply about prompt did not change goal state',
        this_goal_turn='PROGRESS:180 native-adapter tests; actual internal-grid refinement; cross-fit proposal diagnostics; normalization oracle; fresh16384 draw integration launched',
        adapter={k:adapter[k] for k in ('status','count','failures','max_relative_error','max_logL_errors_SNR40_600','max_peak_difference_s')},
        mesh={k:mesh[k] for k in ('status','internal_step_ratios','adapter_pass','adapter_check_count','all_rate_pass','comparisons')},
        proposal=dict(selected=proposal['selected_candidate'],training_weight_ESS=proposal['training_weight_ESS'],
            df=proposal['df'],components=proposal['count'],normalization_mean=oracle['means'][0],
            normalization_MC_error=oracle['MC_standard_errors'][0],moment_max_standardized_error=oracle['max_standardized_error'],
            density_error=oracle['direct_density_error']),
        active_processes=[live],scientific_acceptance=False,physical_prior_changed=False,C6_changed=False,hashes=hashes)
    table='\n'.join(f"| {r['low']}→{r['high']} | {r['psd']} | "+' | '.join(f'{v:.8g}' for v in r['max_logL_integral_change_SNR40_200_600'])+' |' for r in mesh['comparisons'])
    text=f'''[REAL — controles numéricos; OPEN — evidência integrada e calibração científica]

# ORDEM 013 — Malha interna medida e nova amostragem

Registro: {now}. Axiomas: N/A — sem Lean.

**PAGO:** o adaptador de modos nativos reproduziu a API anterior em{adapter['count']}
controles: três fontes de referência e dois pontos de prior,8192/16384Hz,
deslocamentos de pico de ambos os sinais, três fases externas ao banco,
a=0/0,37/1, O4/O5. Erro relativo máximo={adapter['max_relative_error']:.17g};
erro de logL máximo em SNR40/600={adapter['max_logL_errors_SNR40_600']}.
O pico é exatamente o da API anterior nos casos testados. Não houve troca
de família SEOB, perda de modos nem alteração do prior.

**PAGO:** na fonte90, a malha interna foi de fato refinada com taxas de saída
131072/262144/524288Hz. Razões dos passos medidos={mesh['internal_step_ratios']}.
Doze controles adicionais da API de alta taxa passaram. O banco131072 também
reproduziu os16 pontos de fase anteriores, erro relativo
{mesh['rates'][0]['original_bank_relative_error']:.17g}.

**NÃO PAGO:** convergência suficiente em alta SNR. A mudança da log-likelihood
integrada sobre fase/amplitudes, neste ponto de fonte, foi:

| taxas (Hz) | PSD | SNR40 | SNR200 | SNR600 |
|---|---|---:|---:|---:|
{table}

O limite registrado é0,1. SNR40 passa neste controle;200/600 falham.
A malha interna fixa explicava a ausência de refinamento anterior, mas refiná-la
não resolveu a precisão: não é demonstração de causa única nem justificativa
para continuar dobrando taxas cegamente. As injeções continuam congeladas
em8192Hz; este ensaio não valida sua precisão intrínseca em alta SNR.

**PAGO COMO DIAGNÓSTICO:** a rodada8192 anterior é terminal e permanece
não aceita. Usamos suas likelihoods para comparar propostas, sem recalculá-las.
Primeiro:36 alternativas em duas metades. Depois: treinamento pela média e
pela raiz da média quadrática das densidades-alvo, com3/6/12 componentes.
Pela desigualdade de Cauchy-Schwarz, a segunda forma é a proposta ideal para
reduzir o segundo momento médio se as densidades-alvo forem conhecidas.
Aqui elas são estimadas com baixa ESS: a motivação não é prova de eficiência.

Selecionada:{proposal['selected_candidate']['id']}, pelo maior ganho previsto
no décimo percentil, no pior dos dois grupos de validação. Esse ganho ainda é
{proposal['selected_candidate']['min_fold_gain10']:.8g}<1; nenhuma melhora
uniforme foi demonstrada. Ganho mediano mínimo previsto:
{proposal['selected_candidate']['min_fold_median_gain']:.8g}, diagnóstico apenas.
Proposta:seis componentes Student-t,df30,mais10% do prior completo.
As sete coordenadas físicas continuam integradas; fase por quadratura,
distância/polarização comuns por integral analítica.

**PAGO:** teste independente de normalização/momentos32768draws:
integral={oracle['means'][0]:.8g} ±{oracle['MC_standard_errors'][0]:.8g};
maior desvio padronizado={oracle['max_standardized_error']:.8g}; erro da
densidade por fórmula independente={oracle['direct_density_error']:.17g}.
Normalização aprovada não é precisão dos fatores de Bayes.

**EM EXECUÇÃO:** sessão{args.live_session},16384propostas,seed130892,
{progress['done']}/{progress['valid_draws']}avaliações no suporte no último
registro observado. Fora do suporte:integrando zero, contado no denominador.
Não há resultado final desta rodada. O modelo/likelihood congelado não mudou;
a nova extração SEOB é instrumento de controle e não foi injetada na rodada Phenom.

**CONTINUAR:** revalidar a sessão{args.live_session}; não reiniciar por timeout.
Depois de RESULT:auditar todas as densidades com `audit_registered_transport.py
--stage phase_ringdown_balanced`, auditar pesos e taxa com `audit_phase_source.py
../phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384 --rate --processes 6`,
comparar com a rodada8192. Repetição independente continua necessária, assim
como recuperação SEOB integrada, outras leituras/SNR, posterior contínuo de a,
viés/cobertura e pacote para reprodução. C6 preservada; nenhuma confirmação ou5σ.

Reprodução dos novos controles:create-once `validate_native_seob_phase.py`,
`refine_native_internal_mesh.py`, `diagnose_proposal_efficiency.py`,
`diagnose_balanced_proposal.py`. Proposta:`refine_balanced_source_proposal.py`
nas etapas fit,oracle,run --draws 16384 --seed 130892 --processes 6.
Para repetir resultados concluídos, usar diretório separado; não sobrescrever.

## Custódia medida

| arquivo relativo à bancada | SHA256 |
|---|---|
'''+''.join(f'| {p} | {h} |\n' for p,h in hashes.items())
    safe(receipt,(json.dumps(measured,indent=2,ensure_ascii=False)+'\n').encode())
    safe(handoff,text.encode())
    p=ROOT/'STATUS_ORDEM_013.json'; status=read(p)
    status.update(date_utc=now,previous_goal_turn=measured['previous_goal_turn'],this_goal_turn=measured['this_goal_turn'],active_processes=[live])
    status['verified']['C5_native_mesh_balanced_start']={k:v for k,v in measured.items() if k!='hashes'}
    status['hashes'].update(hashes)
    status['next_action']=f'Revalidar sessão{args.live_session}:16384propostas phase_ringdown_balanced. Após RESULT, auditar densidade/rate e repetir independentemente. 93398,17680,10814,87367,5127 encerrados. Adaptador SEOB passou180+12controles; refinamento real ainda falhaSNR200/600. Não declarar precisão/evidência científica a partir dos diagnósticos.'
    status['requirements_remaining'][0]=status['next_action']
    safe(p,(json.dumps(status,indent=2,ensure_ascii=False)+'\n').encode())
    p=ROOT/'PROGRESSO.md'; safe(p,p.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps(dict(status=measured['status'],active=live,handoff=str(handoff)),ensure_ascii=False))


if __name__=='__main__':
    main()
