"""Record passing rate controls, fresh draws and the repaired continuous API."""
from datetime import datetime, timezone
import json
import numpy as np
from record_source_evidence_start import ROOT, RUN, safe, sha


def read(path):
    return json.loads(path.read_bytes())


def main():
    receipt=ROOT/'C5_REAL_REFINEMENT_START.json'
    handoff=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_refinamento_iniciado_e_api_continua.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once record')
    pilot=RUN/'phase_ringdown_real_continuation/IMRPhenomXPHM_seed130892_N16384'
    rate=read(pilot/'real_rate_control/RESULT.json')
    rate_reg=read(pilot/'real_rate_control/REGISTRATION.json')
    if (rate['status']!='PASS_DOMINANT_RATE_CONTROL' or
            rate['registration_sha256']!=sha(pilot/'real_rate_control/REGISTRATION.json') or
            rate_reg['result_sha256']!=sha(pilot/'RESULT.json')):
        raise ValueError('Missing matched Phenom rate result')
    for name,expected in rate['point_hashes'].items():
        if sha(pilot/'real_rate_control'/name)!=expected:
            raise ValueError('Rate control checkpoint changed')
    validation=read(RUN/'continuous_real_phase_validation/RESULT.json')
    if validation['status']!='PASS_REAL_CONTINUOUS_PHASE_API':
        raise ValueError('Continuous API not validated')
    validation_reg=read(RUN/'continuous_real_phase_validation/REGISTRATION.json')
    for name,expected in validation_reg['hashes'].items():
        if sha(RUN/name)!=expected:
            raise ValueError('Changed continuous API input')
    endpoints={family:read(RUN/f'continuous_real_phase_validation/{family}_endpoints.json') for family in ('IMRPhenomXPHM','SEOBNRv4HM')}
    refined=RUN/'phase_real_refined/IMRPhenomXPHM_seed130972_N32768'
    registration=read(refined.parent/'REGISTRATION.json')
    for name,expected in registration['hashes'].items():
        if sha(RUN/name)!=expected:
            raise ValueError('Changed fresh-run registration input')
    start=read(refined/'START.json')
    if start['transport_registration_sha256']!=sha(refined.parent/'REGISTRATION.json'):
        raise ValueError('Fresh run uses wrong registration')
    # Snapshot immutable, already completed chunks only; writers use atomic rename.
    checkpoint_rows=[]
    for path in sorted(refined.glob('chunk_*.npz')):
        with np.load(path) as archive:
            controls=json.loads(str(archive['controls_json']))
            ids=archive['indices'].tolist()
            if ids!=[row['index'] for row in controls] or archive['components'].shape!=(len(ids),2400):
                raise ValueError('Checkpoint controls or components do not match')
            if not np.all(np.isfinite(archive['components'])):
                raise ValueError('Nonfinite completed checkpoint')
            for row in controls:
                if (row['max_relative_waveform_interpolation_error']>1e-6 or
                        row['max_logL_interpolation_error']>.001 or row['max_phase_quadrature_error']>1e-5):
                    raise ValueError('Checkpoint contains failed numerical controls')
            checkpoint_rows.append(dict(file=path.name,points=len(ids),sha256=sha(path)))
    if not checkpoint_rows:
        raise ValueError('Fresh source run has not written complete checkpoints')
    if sha(ROOT/'REGISTRO_C6.json')!=sha(RUN/'REGISTRO_C6.json'):
        raise ValueError('Frozen C6 changed')
    repeat=RUN/'phase_native_repeat/SEOBNRv4HM_seed130942_N16384'
    now=datetime.now(timezone.utc).isoformat()
    live=[dict(session_id=34860,kind='fresh_real_phase_refinement',family='IMRPhenomXPHM',workers=4,
               folder=str(refined.relative_to(ROOT)),last_progress=read(refined/'PROGRESS.json')),
          dict(session_id=40860,kind='independent_native_repeat',family='SEOBNRv4HM',workers=4,
               folder=str(repeat.relative_to(ROOT)),last_progress=read(repeat/'PROGRESS.json'))]
    for entry in live:
        entry['observation']='Specific write_stdin handle returned live and advancing during this turn; revalidate on continuation.'
    names=['build_real_continuous_api.py','real_continuous_phase_source.py','REAL_CONTINUOUS_API_PROVENANCE.json',
        'validate_real_continuous_api.py','continuous_real_phase_validation/REGISTRATION.json',
        'continuous_real_phase_validation/RESULT.json','continuous_real_phase_validation/IMRPhenomXPHM_endpoints.json',
        'continuous_real_phase_validation/SEOBNRv4HM_endpoints.json',
        str((pilot/'real_rate_control/RESULT.json').relative_to(RUN)),
        str((pilot/'real_rate_control/REGISTRATION.json').relative_to(RUN)),
        str((refined/'START.json').relative_to(RUN)),str((refined/'PROPOSALS.npz').relative_to(RUN))]
    hashes={'cache/source_evidence/'+name:sha(RUN/name) for name in names}
    hashes['record_real_refinement_start.py']=sha(ROOT/'record_real_refinement_start.py')
    measured=dict(status='PHENOM_RATE_PASS_FRESH_REFINEMENT_RUNNING_CONTINUOUS_API_PASS',date_utc=now,
        previous_goal_turn='PROGRESS: completed Phenom draws and independent audits; measured512/1200 local precision and120 unstable comparisons; selected and normalized prospective numerical refinement; SEOB rate control passed.',
        this_goal_turn='PROGRESS: Phenom rate control completed and passed; registered32768-draw refinement started; continuous-strength real-reader API passed60 full-wave controls and exact binary-endpoint comparisons.',
        terminal_processes=[dict(session_id=57200,exit_code=0),dict(session_id=67888,exit_code=0)],
        phenom_rate_points=len(rate['rows']),phenom_rate_max_logL_change=rate['max_active_logL_change'],
        continuous_API=validation,binary_endpoint_checks=endpoints,
        fresh_run_draws=start['draws'],fresh_run_seed=start['seed'],
        control_checkpoint_snapshot=checkpoint_rows,checkpoint_points_verified=sum(v['points'] for v in checkpoint_rows),
        active_processes=live,physical_prior_changed=False,continuous_strength_prior_selected=False,
        continuous_source_integration_completed=False,coverage_completed=False,scientific_acceptance=False,
        C6_changed=False,hashes=hashes)
    text=f'''[REAL — controles numéricos passaram; OPEN — precisão integral e calibração]

# ORDEM 013 — Refinamento iniciado e API contínua verificada

Registro: {now}. N/A — sem alteração do cânone, Lean, Atlas ou C6.

**Controle de resolução Phenom:**57200 terminou código0;347 pontos dominantes,
8192→16384Hz. Maior |ΔlogL|={rate['max_active_logL_change']:.12g}<0.1.
O controle SEOB196 pontos já havia passado. São controles pontuais, não limites
globais de erro do posterior nem provas de precisão da integração de fonte.

**Nova rodada começou:**34860,quatro trabalhadores;32768 propostas,seed130972,
`phase_real_refined/IMRPhenomXPHM_seed130972_N32768`. Mesmos priors e likelihood;
a proposta numérica foi ajustada e registrada na etapa anterior. O instantâneo
de{len(checkpoint_rows)} blocos conferiu{measured['checkpoint_points_verified']} vetores completos
e seus controles guardados atomicamente dentro dos NPZ. Não reiniciar o processo.
A repetição SEOB16384/seed130942 continua no handle40860,quatro trabalhadores.

**API contínua:** a função de integração de fase já existente recebeu somente
o leitor real de Nyquist, em cópia separada. Foram examinados os pontos reais
Phenom15627(o que havia interrompido a rodada) e SEOB1002(dominante no piloto),
com intensidades[-2,0,0.37,1,4],três fases fora da grade e O4/O5.
São{validation['direct_full_wave_controls']} controles diretos: máximo erro relativo
{validation['max_relative_wave_error']:.12g}; máximo erro logL
{validation['max_direct_logL_error']:.12g}. Os extremos a=0/1 concordaram
exatamente nas duas famílias. Intensidade negativa é extensão diagnóstica,
não afirmação de dinâmica GKLS física. Nenhum prior sobre a foi escolhido.

**O que continua faltando:** as curvas de fonte marginalizadas Z(a), além dos
dois extremos, e a calibração por injeções. Esta validação de API não entrega
viés/cobertura. Reutilizar os leitores de intervalos existentes quando houver
curvas completas; dois pontos não determinam um máximo ou um intervalo.
Intervalo truncado pelo domínio, curva sem identificação ou integração sem
precisão devem permanecer falhas visíveis, sem fabricar erro/sigma.

**Sequência:** revalidar34860 e40860. Quando terminarem, auditar densidades e
somas, conferir controles completos e comparar com as rodadas anteriores.
O controle de resolução da nova proposta deve abranger seus próprios pontos
dominantes; não herda automaticamente a aprovação dos pontos antigos.
`combine_continuation_families.py run` mantém os caminhos já registrados
(Phenom16384 + SEOB16384); não trocar pelo novo32768 sem registro separado.
A rodada Phenom16384 segue512/1200 em precisão local e120 diferençaslnB>0.2.
Não anunciar nova significância física. Restam convergência e viés/cobertura
da intensidade contínua no escopo completo.
'''
    safe(receipt,(json.dumps(measured,indent=2,ensure_ascii=False)+'\n').encode())
    safe(handoff,text.encode())
    path=ROOT/'STATUS_ORDEM_013.json';status=read(path)
    status.update(date_utc=now,previous_goal_turn=measured['previous_goal_turn'],this_goal_turn=measured['this_goal_turn'],active_processes=live)
    status['verified']['C5_real_refinement_started']={k:v for k,v in measured.items() if k!='hashes'}
    status['hashes'].update(hashes)
    status['registered_not_started']=[dict(status='REGISTERED_WAITING_SEOB_RESULT',
        stage='cache/source_evidence/source_family_combination_real_repeat',command='combine_continuation_families.py run')]
    status['next_action']='Revalidar34860(Phenom32768/seed130972) e40860(SEOB16384).57200 terminou código0:347 controles, máximo0.013669652097632934<0.1.67888 API contínua passou60 controles, extremos idênticos. Auditar/comparar os novos resultados quando concluírem; depois mistura registrada e integração contínua/calibração. Não reiniciar jobs nem repetir fit/oracle.'
    status['requirements_remaining'][0]=status['next_action']
    safe(path,(json.dumps(status,indent=2,ensure_ascii=False)+'\n').encode())
    path=ROOT/'PROGRESSO.md';safe(path,path.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps(dict(status=measured['status'],active_handles=[v['session_id'] for v in live],
        checkpoint_points=measured['checkpoint_points_verified'],handoff=str(handoff)),ensure_ascii=False))


if __name__=='__main__':
    main()
