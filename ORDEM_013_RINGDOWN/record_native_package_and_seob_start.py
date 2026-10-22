"""Record portable waveform replay and live second-family source inference."""
from datetime import datetime,timezone
import argparse
import json
from record_source_evidence_start import ROOT,RUN,safe,sha


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--phenom-session',type=int,required=True)
    parser.add_argument('--seob-session',type=int,required=True)
    args=parser.parse_args()
    read=lambda p:json.loads(p.read_bytes())
    receipt=ROOT/'C5_NATIVE_SOURCE_AND_C7_PORTABLE.json'
    handoff=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C7_forma_onda_nativa_e_C5_segunda_familia.md'
    replay_receipt=ROOT/'C7_NATIVE_SEOB_REPLAY_VALIDATION.json'
    if any(p.exists() for p in (receipt,handoff,replay_receipt)):
        raise FileExistsError('Create-once record')
    package_info=read(ROOT/'C7_NATIVE_SEOB_WAVEFORM_PACKAGE.json'); package=ROOT/package_info['package']
    manifest=read(package/'MANIFEST.json')
    for row in manifest['files']:
        if sha(package/row['path'])!=row['sha256']:
            raise ValueError('Portable package changed:'+row['path'])
    matches=list((package/'cache').glob('replay_*/RESULT.json'))
    if len(matches)!=1:
        raise ValueError('Ambiguous or missing isolated replay result')
    replay_path=matches[0]; replay=read(replay_path)
    integrity=read(ROOT/'C7_NATIVE_SEOB_INTEGRITY_VALIDATION.json')
    integral=read(RUN/'native_source_integral_validation/RESULT.json')
    oracle=read(RUN/'phase_native_seob/PROPOSAL_ORACLE.json')
    if replay['status']!='PASS_PORTABLE_NATIVE_WAVEFORM' or not all(replay['guards']):
        raise ValueError('Portable replay failed')
    if integrity['status']!='PASS_ARCHIVE_AND_TAMPER_REJECTION' or not integrity['original_package_unchanged']:
        raise ValueError('Portable archive integrity failed')
    if integral['status']!='PASS_NATIVE_SOURCE_INTEGRAL' or oracle['status']!='PASS_TRANSPORT_PROPOSAL_MOMENTS':
        raise ValueError('Second-family source input checks failed')
    for directory in ('native_source_integral_validation','phase_native_seob'):
        for name,h in read(RUN/directory/'REGISTRATION.json')['hashes'].items():
            if sha(RUN/name)!=h:
                raise ValueError('Native source custody changed:'+name)
    live=[]
    for family,session,relative in (
        ('IMRPhenomXPHM',args.phenom_session,'phase_ringdown_balanced/IMRPhenomXPHM_seed130892_N16384'),
        ('SEOBNRv4HM',args.seob_session,'phase_native_seob/SEOBNRv4HM_seed130901_N2048')):
        folder=RUN/relative
        if (folder/'RESULT.json').exists():
            raise ValueError('Run already complete: update terminal state instead of recording live')
        progress=read(folder/'PROGRESS.json')
        live.append(dict(tool='write_stdin',session_id=session,family=family,
            status='LIVE_OBSERVED_BEFORE_RECORD',folder=str(folder.relative_to(ROOT)).replace('\\','/'),
            last_progress=progress,observation='Live tool handle and progressing output verified immediately before record; revalidate next turn'))
    now=datetime.now(timezone.utc).isoformat()
    replay_summary=dict(status='PASS_ISOLATED_PORTABLE_REPLAY_AND_TAMPER_REJECTION',date_utc=now,
        command='python -I -B C7_NATIVE_SEOB_WAVEFORM/reproduce.py',count=replay['count'],
        max_relative_error=replay['max_relative_error'],guards=replay['guards'],
        result=str(replay_path.relative_to(ROOT)).replace('\\','/'),result_sha256=sha(replay_path),
        archive=package_info['archive'],archive_sha256=sha(ROOT/package_info['archive']),
        tamper_rejected=integrity['tamper_rejected'],scientific_acceptance=False,
        scope='Standalone model consumer and real waveform regeneration; not independent external review or calibrated physical evidence')
    safe(replay_receipt,(json.dumps(replay_summary,indent=2)+'\n').encode())
    paths=[ROOT/'record_native_package_and_seob_start.py',ROOT/'build_native_waveform_package.py',
        ROOT/'verify_native_package_integrity.py',ROOT/'C7_NATIVE_SEOB_WAVEFORM_PACKAGE.json',
        ROOT/'C7_NATIVE_SEOB_INTEGRITY_VALIDATION.json',replay_receipt,replay_path,
        ROOT/package_info['archive'],package/'MANIFEST.json']
    names=['native_seob_source_likelihood.py','validate_native_source_integral.py','run_native_seob_source.py',
        'native_source_integral_validation/REGISTRATION.json','native_source_integral_validation/RESULT.json',
        'phase_native_seob/REGISTRATION.json','phase_native_seob/PROPOSAL.json','phase_native_seob/PROPOSAL_ORACLE.json',
        'phase_native_seob/SEOBNRv4HM_seed130901_N2048/START.json','phase_native_seob/SEOBNRv4HM_seed130901_N2048/PROPOSALS.npz']
    paths += [RUN/n for n in names]
    hashes={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in paths}
    measured=dict(status='PORTABLE_WAVEFORM_VERIFIED_TWO_SOURCE_FAMILIES_RUNNING',date_utc=now,
        previous_goal_turn='PROGRESS: native modes/mesh controls; sampling diagnostics and balanced16384 proposal launched',
        this_goal_turn='PROGRESS: independent original-vs-native SEOB phase-integral validation; second-family prior oracle and2048 pilot launched; portable waveform regenerated in isolated Python; corrupted-copy rejection verified',
        native_integral_max_error=integral['max_logL_integral_error'],native_integral_components_per_point=2400,
        native_integral_points=len(integral['rows']),
        timing_caveat='Validation native timing benefits from original held-out waveform cache; not a clean benchmark',
        seob_prior_oracle_mean=oracle['mean'][0],seob_prior_oracle_standard_error=oracle['MC_standard_errors'][0],
        seob_prior_oracle_max_standardized_error=oracle['max_standardized_error'],
        portable_replay=replay_summary,active_processes=live,scientific_acceptance=False,C6_changed=False,hashes=hashes)
    replay_rel=str(replay_path.relative_to(ROOT)).replace('\\','/')
    live_text='\n'.join(f"- {v['family']}:sessão{v['session_id']}, {v['last_progress']['done']}/{v['last_progress']['valid_draws']}avaliações no suporte, `{v['folder']}`." for v in live)
    text=f'''[REAL — forma de onda reproduzida; OPEN — evidência integrada e calibração]

# ORDEM 013 — Forma de onda portátil e recuperação da segunda família

Registro: {now}. Axiomas: N/A — sem Lean.

**PAGO:** a integral de fase/amplitudes via modos nativos SEOB reproduz a
implementação original em quatro pontos fonte/taxa,2400 componentes por ponto,
erro máximo |ΔlogL|={integral['max_logL_integral_error']:.17g}, abaixo de0,001.
Os tempos do teste têm cache aquecido: não são benchmark independente de velocidade.
Cada ponto da nova inferência continua comparado com o gerador COMPLETO original
em três fases externas à malha, sem dispensar os critérios anteriores.

**PAGO:** proposta SEOB usa mapa de remanescente e jacobiano próprios; o aprendizado
Phenom fornece apenas uma distribuição computacional inicial. Não foi usado como
prior físico. As sete coordenadas da fonte, a fase inteira e as amplitudes comuns
continuam integradas. Normalização em32768 amostras:
{oracle['mean'][0]:.8g} ±{oracle['MC_standard_errors'][0]:.8g}; maior desvio dos13
momentos={oracle['max_standardized_error']:.8g}. A eficiência para SEOB ainda não é conhecida.

**PAGO — C7:** pacote standalone `{package_info['archive']}`, {package_info['bytes']}bytes,
{package_info['files']}arquivos de conteúdo e manifesto. Dispensa memória/contexto da
bancada e dados privados. `prepare_ringdown` gera todos os modos SEOB41;
`polarizations` aplica a leitura condicional explícita, intensidade, distância e
polarização comuns, retornando strain adimensional. Não escolhe relógio físico.
As demais harmônicas ficam preservadas. β vem do cálculo em runtime.

Reprodução real em `python -I -B`:{replay['count']} comparações passaram,
erro relativo máximo={replay['max_relative_error']:.17g}. Três fontes, duas taxas,
quatro leituras condicionais, três intensidades, duas escolhas de distância/rotação.
Seis entradas inválidas foram recusadas. A leitura de estado coerente é recusada
como exponencial completa porque só fornece a inclinação inicial nessa API.

**PAGO:** arquivo ZIP conferido byte a byte contra o pacote testado. Uma cópia
descartável adulterada foi recusada pelo consumidor antes dos imports científicos.
Os originais continuam intactos. Isso é controle de integridade, não aprovação
externa independente da teoria. Resultado do replay:`{replay_rel}`.

**EM EXECUÇÃO, observado antes deste registro:**
{live_text}

Não há resultado final dessas rodadas. A primeira integra16384 propostas; a
segunda é piloto2048. Propostas fora do suporte têm integrando zero e continuam
no denominador. Os50 intervalos de ruído são reutilizados/pareados; não são1200
eventos independentes.

**NÃO PAGO:** convergência/replicação das duas famílias, viés/cobertura da intensidade
contínua, demais leituras/SNR e aceitação científica dos fatores de Bayes. Os
controles prévios de alta SNR continuam falhando; a entrega portátil não os apaga.
Dados/C6/cânone preservados. Nenhuma declaração de confirmação ou5σ.

**PRÓXIMA AÇÃO:** revalidar os dois handles acima. Só após RESULT, executar
`audit_registered_transport.py <nome_da_rodada> --stage <fase>`; a fase é
`phase_ringdown_balanced` ou `phase_native_seob`. `audit_phase_source.py
../<fase>/<nome_da_rodada> --rate --processes 2` usa o gerador original para
controle independente de taxa (SEOB é mais caro). Comparação de Phenom contra
8192 em `compare_phase_runs.py`; não comparar famílias como se fossem repetições
do mesmo estimador. Repetições por seed da mesma família permanecem necessárias.

Comandos da etapa: `run_native_seob_source.py register`, `oracle`, `run --draws
2048 --seed 130901 --processes 2`. Artefatos concluídos são create-once; reproduzir
em cópia separada, nunca sobrescrever resultados. Pacote: `python -I -B
C7_NATIVE_SEOB_WAVEFORM/reproduce.py` cria diretório de replay próprio.

## Custódia medida

| arquivo relativo | SHA256 |
|---|---|
'''+''.join(f'| {p} | {h} |\n' for p,h in hashes.items())
    safe(receipt,(json.dumps(measured,indent=2,ensure_ascii=False)+'\n').encode())
    safe(handoff,text.encode())
    path=ROOT/'STATUS_ORDEM_013.json'; status=read(path)
    status.update(date_utc=now,previous_goal_turn=measured['previous_goal_turn'],this_goal_turn=measured['this_goal_turn'],active_processes=live)
    status['verified']['C5_native_source_C7_portable']={k:v for k,v in measured.items() if k!='hashes'}
    status['hashes'].update(hashes)
    status['next_action']=f'Revalidar Phenom{args.phenom_session} e SEOB{args.seob_session}. Ambas integrações ativas; após RESULT auditar densidade, aritmética, taxa e repetição. Pacote C7_NATIVE_SEOB_WAVEFORM passou144 controles em modo isolado e recusa adulteração.71560/49180 concluídos. Precisão/calibração científica continua aberta.'
    status['requirements_remaining'][0]=status['next_action']
    safe(path,(json.dumps(status,indent=2,ensure_ascii=False)+'\n').encode())
    path=ROOT/'PROGRESSO.md';safe(path,path.read_bytes()+('\n\n---\n'+text).encode())
    path=ROOT/'C7_DELIVERY_OVERVIEW.md'
    addition=f'''\n\n## Native SEOB waveform supplement — {now}\n\n[REAL — portable numerical reproduction; OPEN — calibrated physical evidence]\n\n`{package_info['archive']}` provides an independent consumer API for the full\nSEOB41 waveform with conditional22/44 dephasing. Isolated Python replay passed\n{replay['count']} checks, maximum relative error{replay['max_relative_error']:.17g};\nsix input guards and corrupted-copy rejection passed. Read\n`C7_NATIVE_SEOB_WAVEFORM/README.md` and `C7_NATIVE_SEOB_REPLAY_VALIDATION.json`.\nThe package receipt marked PACKAGED_REPLAY_PENDING is historical; the separate\nreplay validation above records completion. Source integration/calibration and\nhigh-SNR precision remain open; this supplement does not replace prior packages\nor promote their scientific status. Archive SHA256: {sha(ROOT/package_info['archive'])}.\n'''
    safe(path,path.read_bytes()+addition.encode())
    print(json.dumps(dict(status=measured['status'],active_processes=live,portable_replay=replay_summary,handoff=str(handoff)),ensure_ascii=False))


if __name__=='__main__':main()
