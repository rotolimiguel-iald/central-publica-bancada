"""Record measured continuous-curve controls and the actual running integral."""
from datetime import datetime, timezone
import json
import numpy as np
from record_source_evidence_start import ROOT, RUN, safe, sha


def read(path):
    return json.loads(path.read_bytes())


def main():
    receipt = ROOT/'C5_CONTINUOUS_CURVE_START.json'
    handoff = ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C5_curvas_continuas_iniciadas.md'
    if receipt.exists() or handoff.exists():
        raise FileExistsError('Create-once progress record')
    arithmetic = read(RUN/'continuous_calibration_validation/RESULT.json')
    fullwave = read(RUN/'controlled_continuous_validation/RESULT.json')
    if (arithmetic['status'] != 'PASS_CONTINUOUS_CALIBRATION_ARITHMETIC' or
            fullwave['status'] != 'PASS_CONTROLLED_CONTINUOUS_SOURCE_EVALUATOR'):
        raise ValueError('Missing completed continuous validation')
    for stage, result in [('continuous_calibration_validation', arithmetic),
                          ('controlled_continuous_validation', fullwave)]:
        regpath = RUN/stage/'REGISTRATION.json'
        if sha(regpath) != result['registration_sha256']:
            raise ValueError('Validation custody changed')
        for name, digest in read(regpath)['hashes'].items():
            if sha(RUN/name) != digest:
                raise ValueError('Validated input changed: ' + name)
    binary_ph = RUN/'phase_real_refined/IMRPhenomXPHM_seed130972_N32768'
    binary_se = RUN/'phase_native_repeat/SEOBNRv4HM_seed130942_N16384'
    curves = RUN/'continuous_source_curves/SEOBNRv4HM_seed130942_N16384'
    registered_ph = RUN/'continuous_source_curves/IMRPhenomXPHM_seed130972_N32768'
    for path in (curves, registered_ph):
        for name, digest in read(path/'REGISTRATION.json')['hashes'].items():
            if sha(RUN/name) != digest:
                raise ValueError('Continuous source registration changed: ' + name)
    if read(curves/'START.json')['registration_sha256'] != sha(curves/'REGISTRATION.json'):
        raise ValueError('Live continuous run uses wrong registration')
    checkpoint = []
    for path in sorted(curves.glob('chunk_*.npz')):
        with np.load(path) as archive:
            data, ids = archive['components'], archive['indices']
            controls = json.loads(str(archive['controls_json']))
            if (data.shape != (len(ids), 17, 1200) or not np.isfinite(data).all() or
                    ids.tolist() != [v['index'] for v in controls]):
                raise ValueError('Invalid continuous checkpoint')
            for point in controls:
                for row in point['controls']:
                    if (row['max_relative_wave_error'] > 1e-6 or row['max_logL_error'] > .001 or
                            len(row['phase_quadrature']) != 17 or
                            any(q['error'] > 1e-5 for q in row['phase_quadrature'])):
                        raise ValueError('Failed continuous numerical control')
            checkpoint.append(dict(file=path.name, points=len(ids), sha256=sha(path)))
    if not checkpoint:
        raise ValueError('No completed continuous checkpoint yet')
    now = datetime.now(timezone.utc).isoformat()
    live = [dict(session_id=34860, kind='binary_source', workers=4, folder=str(binary_ph.relative_to(ROOT)),
                 last_progress=read(binary_ph/'PROGRESS.json')),
            dict(session_id=40860, kind='binary_source', workers=4, folder=str(binary_se.relative_to(ROOT)),
                 last_progress=read(binary_se/'PROGRESS.json')),
            dict(session_id=19681, kind='continuous_source', workers=2, folder=str(curves.relative_to(ROOT)),
                 last_progress=read(curves/'PROGRESS.json'))]
    for entry in live:
        entry['observation'] = 'Specific write_stdin handle returned live during this turn; revalidate on continuation.'
    controls = [c for row in fullwave['rows'] for c in row['controls']]
    summary = dict(points=len(fullwave['rows']), full_wave_checks=sum(c['full_wave_checks'] for c in controls),
        max_relative_wave_error=max(c['max_relative_wave_error'] for c in controls),
        max_logL_error=max(c['max_logL_error'] for c in controls),
        max_quadrature_error=max(q['error'] for c in controls for q in c['phase_quadrature']),
        max_binary_endpoint_error=max(row['endpoint_error'] for row in fullwave['rows']))
    names = ['continuous_source_calibration.py', 'validate_continuous_calibration.py',
        'controlled_continuous_source.py', 'validate_controlled_continuous_source.py',
        'run_continuous_source_curves.py', 'continuous_calibration_validation/REGISTRATION.json',
        'continuous_calibration_validation/RESULT.json', 'controlled_continuous_validation/REGISTRATION.json',
        'controlled_continuous_validation/RESULT.json']
    names += [str((path/'REGISTRATION.json').relative_to(RUN)) for path in (curves, registered_ph)]
    names += [str((curves/'START.json').relative_to(RUN))]
    hashes = {'cache/source_evidence/'+n:sha(RUN/n) for n in names}
    hashes['record_continuous_curve_start.py'] = sha(ROOT/'record_continuous_curve_start.py')
    measured = dict(status='CONTINUOUS_CALIBRATION_READER_VALIDATED_SOURCE_CURVES_RUNNING',date_utc=now,
        previous_goal_turn='PROGRESS: Phenom rate passed;32768 fresh source draws launched;real continuous API checked.',
        this_goal_turn='PROGRESS: paired continuous integration and interval reader passed independent oracles and nine refusal controls;complete strength evaluator passed306 direct-wave checks;full SEOB source curves started.',
        arithmetic=arithmetic, waveform_summary=summary, checkpoints_verified=checkpoint,
        checkpoint_points=sum(c['points'] for c in checkpoint), active_processes=live,
        registered_not_started=str(registered_ph.relative_to(ROOT)),
        physical_bias_coverage_complete=False, scientific_acceptance=False,
        strength_prior_selected=False, physical_prior_changed=False, C6_changed=False,hashes=hashes)
    text = f'''[REAL — leitor e avaliador contínuos verificados; OPEN — integral/calibração físicas]

# ORDEM 013 — Curvas contínuas iniciadas

Registro:{now}. N/A — sem Lean. Cânone, Atlas e C6 preservados.

## Critérios e evidências

- **PAGO, aritmética:** `continuous_source_calibration.py` reutiliza a função
  de importância pareada existente. O erro máximo contra quadratura de
  Gauss–Legendre foi {arithmetic['max_integral_error_in_MC_sd']:.9g} erros MC;
  a covariância foi conferida por somas independentes em long double, erro
  {arithmetic['paired_covariance_absolute_error']:.9g}. Propostas de integrando
  zero continuam no denominador. Não se multiplicam mocks.
- **PAGO, geometria do leitor:** reutiliza `profile_intervals`. No oráculo
  gaussiano, erro MLE={arithmetic['gaussian_MLE_error']:.9g} e erro de limites
  ={arithmetic['gaussian_interval_error']:.9g}. Os nove controles recusados
  incluem curva plana, borda, ilhas desconexas, fonte dominante, NaN e ruído
  duplicado. Mock com falha não é removido para melhorar a cobertura.
- **PAGO, avaliador de forma de onda:** {summary['points']} pontos reais,
  {summary['full_wave_checks']} comparações diretas, 17 intensidades de −4 a4
  com passo0,5. Máximo erro relativo={summary['max_relative_wave_error']:.9g},
  logL={summary['max_logL_error']:.9g}, quadratura de fase
  ={summary['max_quadrature_error']:.9g}. Os extremos a=0/1 reproduzem os
  checkpoints anteriores com erro {summary['max_binary_endpoint_error']:.9g}.
  Os dois critérios de seleção SEOB apontaram ao mesmo ponto1002: por isso
  são TRÊS pontos distintos, não quatro. Não extrapolar este controle pontual
  para todo o domínio; cada ponto novo enfrenta os controles completos.
- **INICIADO, ainda NÃO PAGO:** curvas SEOB para16384 propostas,8520 válidas,
  handle19681,dois trabalhadores. Primeiros{measured['checkpoint_points']} pontos
  completos conferidos com seus controles embutidos. O conjunto inclui todos
  os1200 mocks congelados; reutiliza as mesmas coordenadas de fonte da rodada
  binária. São novas intensidades, não novas observações independentes.
- **REGISTRADO, NÃO INICIADO:** extensão Phenom32768/22384 válidas. A rodada
  binária Phenom34860 e a SEOB40860 continuam com quatro trabalhadores cada.
- **NÃO PAGO:** viés/cobertura físicos, repetição independente das curvas,
  controle de resolução nos pontos dominantes dessas novas curvas, mistura
  das famílias e demais leituras/SNR exigidos no objetivo completo.

## Tipagem estatística

Não foi escolhido prior para a, nem alterado β. O leitor calcula intervalos
de razão de verossimilhança sobre Z(a) marginalizado nos parâmetros da fonte.
Não os chama de intervalos bayesianos nem presume cobertura por Wilks: a
cobertura precisa ser medida nas injeções. Curva plana, ilha desconexa,
intervalo truncado, grade sem resolução ou fonte sem precisão deixam a
cobertura calibrada como nula/indisponível; diagnósticos brutos permanecem.
Intensidade negativa é controle numérico, não dinâmica GKLS física.
Uma comparação passo0,5/1,0 é necessária, mas não prova resolução final:
domínio/grade maiores podem ser exigidos. O máximo deslocamento aceito do
MLE e das duas bordas nessa comparação foi registrado em0,05unidades de a.

## Continuação e reprodução

Em `cache/source_evidence`, no Python WSL `/opt/pycbc_env/bin/python -B`:

1. Revalidar os handles34860,40860,19681. Não duplicar execução viva.
2. Quando19681 terminar, conferir `EVALUATIONS_COMPLETE.json` e rodar
   `run_continuous_source_curves.py analyze --family SEOBNRv4HM`.
3. Para Phenom, registro pronto; iniciar
   `run_continuous_source_curves.py run --family IMRPhenomXPHM --workers 2`
   quando houver capacidade, e depois seu `analyze`.
4. Comparar os extremos integrados das curvas às integrais binárias respectivas
   (mesmas propostas) e fazer auditoria independente; preservam-se as exigências
   de densidade, repetição e resolução. O runner emite diagnóstico, nunca
   aceitação científica automática.
5. A mistura binária já registrada continua Phenom16384+SEOB16384. Não trocar
   silenciosamente o primeiro pelo novo32768.

Nenhum teste de natureza moveu gate; nenhum resultado novo em sigma.
Tentativas anteriores e registros congelados mantidos. Ficha de aproveitamento:
reutilizados estimador de importância, leitor de intervalos, geradores completos,
adaptador SEOB nativo, leitor Fourier real, priors, propostas e ruídos existentes.
Acrescentadas apenas a ligação para curvas contínuas, controles e execução.

## Custódia

Hashes SHA256 lidos por script:

'''
    text += '\n'.join(f'- `{name}`: `{value}`' for name,value in hashes.items()) + '\n'
    safe(receipt, (json.dumps(measured,ensure_ascii=False,indent=2)+'\n').encode())
    safe(handoff, text.encode())
    status_path=ROOT/'STATUS_ORDEM_013.json'; status=read(status_path)
    status.update(date_utc=now,previous_goal_turn=measured['previous_goal_turn'],
        this_goal_turn=measured['this_goal_turn'],active_processes=live)
    status['verified']['C5_continuous_curves_started']={k:v for k,v in measured.items() if k!='hashes'}
    status['hashes'].update(hashes)
    status['registered_not_started'].append(dict(status='REGISTERED_NOT_STARTED',
        stage=str(registered_ph.relative_to(ROOT)),
        command='run_continuous_source_curves.py run --family IMRPhenomXPHM --workers 2'))
    status['next_action']='Revalidar34860,40860,19681. Curvas SEOB completas em andamento;Phenom contínuo registrado ainda não iniciado. Após término,analyze+auditoria dos extremos e densidade/repetição/resolução;preservar a mistura binária registrada. Calibração física permanece aberta.'
    status['requirements_remaining'][0]=status['next_action']
    safe(status_path,(json.dumps(status,ensure_ascii=False,indent=2)+'\n').encode())
    progress=ROOT/'PROGRESSO.md'; safe(progress,progress.read_bytes()+('\n\n---\n'+text).encode())
    print(json.dumps(dict(status=measured['status'],checkpoint_points=measured['checkpoint_points'],
        active_handles=[p['session_id'] for p in live],handoff=str(handoff)),ensure_ascii=False))


if __name__=='__main__':
    main()
