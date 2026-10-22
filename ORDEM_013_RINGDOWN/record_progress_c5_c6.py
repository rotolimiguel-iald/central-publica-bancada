"""Record C4 joint modes, C5 empirical calibration, and registered C6 results.

Task-local memory and the authorized return tunnel only. Create-once delivery;
existing memories get byte backups and atomic replacements before any update.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
from collections import Counter
from fetch_public import atomic_json,digests
from c6_engine import checked_registration

ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_bytes())
def sha(path):return digests(path)[1]

def append_bytes(path,addition):
    old=path.read_bytes()
    backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(old)
    temp=path.with_name(path.name+'.tmp');temp.write_bytes(old+addition)
    if temp.stat().st_size!=len(old)+len(addition):raise ValueError('Short memory append')
    temp.replace(path)
    if path.read_bytes()[:len(old)]!=backup.read_bytes():raise ValueError('Old memory bytes changed')

def main():
    delivery=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C4c_C5_C6_strain_registrado.md'
    if delivery.exists():raise FileExistsError('Delivery already exists; do not repeat this registrar')
    reg,regsha=checked_registration()
    c6=read('C6_RESULTS.json');c5=read('C5_EMPIRICAL_IMR_STARTS.json')
    noise=read('C5_EMPIRICAL_NOISE.json');validation=read('C5_LIKELIHOOD_VALIDATION.json')
    joint=read('C4_JOINT_MODES.json');pyring=read('C6_PYRING_START_COMPARISON.json')
    if c6['registration_sha256']!=regsha:raise ValueError('C6 receipt mismatch')
    if not all(x['passed'] for x in c6['convergence']):raise ValueError('Unconverged C6 result')
    if validation['status']!='INDEPENDENT_LIKELIHOOD_ORACLES_PASS':raise ValueError('Likelihood oracle failed')
    current_time=datetime.now(timezone.utc).isoformat()
    c6primary=[r for r in c6['results'] if r['start_tM']==10 and abs(r['amplitude_prior_sd_strain']-1e-20)<1e-30]
    rb=next(r for r in c6primary if r['reading']=='R-B')
    counts=dict(Counter(r['status'] for r in c5['results']))
    # Rehash existing downloads, then add newly extracted products and GWOSC data.
    manifest=read('cache/MANIFESTO_DOWNLOADS.json')
    files={row['path'].replace('\\','/'):row for row in manifest['files']}
    for rel,row in files.items():
        if sha(ROOT/rel)!=row['sha256']:raise ValueError('Old downloaded artifact changed: '+rel)
    def add(path,kind,origin,expected=None):
        actual=sha(path)
        if expected and actual!=expected:raise ValueError('New cache custody mismatch')
        rel=path.relative_to(ROOT).as_posix()
        files[rel]=dict(path=rel,bytes=path.stat().st_size,sha256=actual,kind=kind,origin=origin)
    extraction=read('cache/public/17018009/extraction_receipt.json')
    for row in extraction['files']:
        name=row['path'].replace('\\','/').split('/')[-1]
        path=ROOT/'cache/public/17018009/selected'/name
        if path.exists():add(path,'selected_release_product',row['member'],row['sha256'])
    for folder in ('offsource','on_source'):
        for receipt in (ROOT/'cache/gwosc'/folder).glob('*.receipt.json'):
            row=json.loads(receipt.read_bytes());path=receipt.with_name(receipt.name.removesuffix('.receipt.json'))
            add(path,'GWOSC_'+folder,row['url'],row['sha256'])
    for path in (ROOT/'cache/gwosc').glob('*.json'):add(path,'GWOSC_metadata','Official GWOSC API, acquisition receipts retained')
    for row in noise['detectors']:
        path=ROOT/'cache/empirical_noise'/f"{row['detector']}_noise.npz"
        add(path,'derived_PSD_and_held_out_noise','Wholly off-source GWOSC',row['cache_sha256'])
    for row in read('C5_IMR_CONTROLS.json')['families']:
        path=ROOT/'cache/imr_controls'/f"{row['family']}.npz"
        add(path,'generated_IMR_control',row['family'],row['sha256'])
    manifest.update(at=current_time,files=list(files.values()),on_source_strain_read=True,
        on_source_registration_sha256=regsha,
        attribution='GWOSC and parameter-estimation releases: LIGO Scientific Collaboration, Virgo Collaboration and KAGRA Collaboration. Source licenses/DOIs remain in individual acquisition records.')
    atomic_json(ROOT/'cache/MANIFESTO_DOWNLOADS.json',manifest)
    artifacts=['C4_JOINT_MODES.json','C3_MULTIMODE_TEMPLATE.json','C3_BILBY_CONSUMER.json',
        'C2_TEMPLATE_CHECKS.json','C5_EMPIRICAL_NOISE.json','C5_IMR_CONTROLS.json',
        'C5_EMPIRICAL_IMR.json','C5_EMPIRICAL_IMR_STARTS.json','C5_LIKELIHOOD_VALIDATION.json',
        'C5_FISHER_EMPIRICAL.json','C6_RESULTS.json','REGISTRO_C6.json','C6_DOWNLOADS.json',
        'C6_PYRING_START_COMPARISON.json','C6_SYNTHETIC_GRID_0.json','C6_SYNTHETIC_GRID_1.json',
        'tgl_ringdown_prediction.py','tgl_ringdown_template.py','tgl_ringdown_likelihood.py',
        'prepare_empirical_noise.py','prepare_imr_controls.py','empirical_imr_recovery.py',
        'verify_likelihood_and_noise.py','c6_engine.py','run_c6_grid.py','cache/MANIFESTO_DOWNLOADS.json']
    hashes={name:sha(ROOT/name) for name in artifacts}
    remaining=[
        'C0: três fontes integrais continuam com falhas 403/406 documentadas; não anunciar leitura integral.',
        'C2/C3: finalizar interfaces reutilizáveis de Cauchy e Poisson coerente no pacote; escolha física de desenrolamento e partição continuam hipóteses explícitas.',
        'C4: conferir release GWTC-3 sem duplicar eventos; procedência integral da fusão de posteriores/binário pyRing permanece ressalva. A comparação de quatro tempos foi realizada; 10,5M não existe no índice do release.',
        'C5: completar injeções com outras PSDs (O5/ET/CE) por recoloração validada; medir distribuição calibrada de evidência, não apenas Fisher.',
        'C5/C6: modelo fundamental 220+440 falhou no critério de viés/cobertura para duas famílias IMR; localizar e tratar a discrepância de modos/overtones e de priors. Qualquer novo acesso orientado pelo resultado exige adendo NÃO-CEGO, preservando o registro C6 e seus resultados.',
        'C6: a rodada registrada em H1/L1 foi executada em cinco inícios e três priors, com massa/spin marginalizados e convergência. Ainda não é uma verossimilhança coerente completa nem uma réplica pyRing; não promover INCONCLUSIVE_SYSTEMATICS a exclusão.',
        'C7: concluir pacote independente em inglês, tabela de escopos, comandos e teste de reprodução; auditar objetivo integral antes de marcar completo.'
    ]
    status=read('STATUS_ORDEM_013.json')
    status.update(date_utc=current_time,goal_status='ACTIVE_NOT_COMPLETE',
        previous_goal_turn='PROGRESS: catálogo, pyRing, relógio e trajetórias',
        this_goal_turn='PROGRESS: hipótese conjunta 220+440, ruído empírico, dois modelos IMR, 480 células em cinco inícios, registro C6 e strain real com quadratura convergida',
        on_source_strain_read=True,active_processes=[],no_blocker_recurrence=True,
        requirements_remaining=remaining,
        next_action='Completar calibração fora da fonte (PSDs alternativas e discrepância de modos), mantendo o C6 registrado intacto; finalizar pacote e auditoria integral.')
    status['verified'].update(
        C4_joint_modes='C4_JOINT_MODES.json: 220+440 correlacionados; não multiplicar marginais nem análises do mesmo evento',
        C5_noise=dict(detectors=2,held_out_intervals_per_detector=256,off_source_end_before_event_s=317.2),
        C5_injections=dict(cells=len(c5['results']),evaluations=len(c5['results'])*50,
            noise_intervals_reused_per_detector=50,status_counts=counts,
            scope='São avaliações pareadas do mesmo ruído, não 24 mil eventos independentes; metade das células só mede razões de verossimilhança sub-resolução'),
        C5_independent_integral_error=validation['numerical_quadrature_error'],
        C6=dict(registration_sha256=regsha,starts=reg['start_times_tM'],amplitude_priors=3,
                max_quadrature_difference=max(r['max_abs_lnB_difference'] for r in c6['convergence']),
                primary_R_B_lnB=rb['lnB_vs_GR'],verdict=c6['status'],mass_spin_marginalized=True),
        pyRing_start_controls=dict(products=len(pyring['results']),missing_10_5M=True))
    status['hashes'].update(hashes)
    status['preserved_failures'].extend(noise['preserved_failures'])
    status['preserved_failures'].append('Forecast empírico inicial integrava até o rolloff quase nulo de Nyquist do arquivo 4096 Hz; backup preservado. Versão corrente usa 20-1024 Hz e PSD aliased da seleção stride-2, com aproximação contínua explicitada.')
    atomic_json(ROOT/'STATUS_ORDEM_013.json',status)
    lines=[f'# Ordem 013 — ruído empírico e primeira rodada registrada em strain\n\nUTC: {current_time}\n\n[REAL — análises computacionais condicionais; objetivo integral ATIVO]\n',
        'A C6 foi executada após o registro verificável no túnel. Foram lidos os arquivos públicos H1/L1 do evento, preservando as janelas e os três priors de amplitude registrados. Massa e spin foram integrados com priors próprios uniformes, sem usar o posterior do mesmo evento como prior.\n',
        f'Registro C6: `{regsha}`. O erro máximo entre grades nos log-fatores de Bayes foi {max(r["max_abs_lnB_difference"] for r in c6["convergence"]):.9g}.\n',
        '| Leitura | ln B na janela primária 10 tM |\n|---|---:|\n'+'\n'.join(f'| {r["reading"]} | {r["lnB_vs_GR"]:.9f} |' for r in c6primary)+'\n',
        'Esses números são razões condicionadas ao modelo 220+440 com amplitudes por detector. Todas as janelas recebem INCONCLUSIVE_SYSTEMATICS por regra registrada: os controles com duas famílias IMR não passaram o critério completo de viés/cobertura. Não há sigma de descoberta nem exclusão física.\n',
        'A integral analítica das amplitudes foi conferida por covariância gaussiana independente e quadratura numérica. O ruído simulado diretamente no domínio de Fourier reproduziu a covariância projetada. Ruído real: 256 intervalos por detector; flutuações dos filtros entre 0,94 e 1,07 da escala prevista. Foram preservadas três tentativas numericamente instáveis antes da seleção de amostras e projeção estável.\n',
        f'C5: {len(c5["results"])} células × 50 avaliações pareadas, cinco tempos, três SNRs, oito leituras e duas famílias (SEOBNRv4HM e IMRPhenomXPHM). Contagem: {counts}. O mesmo ruído é reutilizado entre hipóteses para controle; não somar como eventos independentes.\n',
        'A comparação com oito posteriores Kerr publicados em 6, 8, 10 e 12 tM foi realizada. Há diferenças de modos, priors, processamento e referência de tempo (0,0001095 s), explicitadas no JSON. Não existe posterior de 10,5 tM no índice inspecionado. Não foi declarada reprodução da análise pyRing.\n',
        'A análise conjunta anterior 220+440 permanece em C4_JOINT_MODES.json; não foi multiplicada por esta nova análise do mesmo evento. O consumidor Bilby e a extensão angular multimodo passaram controles independentes com LAL.\n',
        '**O que falta no objetivo integral**\n\n'+'\n'.join('- '+x for x in remaining)+'\n',
        '**Artefatos e hashes medidos**\n\n'+'\n'.join(f'- `{name}` — `{value}`' for name,value in hashes.items())+'\n',
        f'Manifesto atualizado: {len(files)} arquivos de aquisição/derivação conferidos. Não foram alterados um.py, kernel, Atlas ou memórias canônicas; a gerência recebe esta entrega para incorporação.\n']
    report='\n'.join(lines)
    append_bytes(ROOT/'PROGRESSO.md',('\n\n'+report).encode('utf-8'))
    raw=report.encode('utf-8');temp=delivery.with_suffix('.tmp');temp.write_bytes(raw)
    if temp.stat().st_size!=len(raw):raise ValueError('Short delivery')
    temp.replace(delivery)
    print(json.dumps(dict(delivery=str(delivery),primary_R_B_lnB=rb['lnB_vs_GR'],
        C6_status=c6['status'],manifest_files=len(files),remaining=len(remaining)),ensure_ascii=False))

if __name__=='__main__':main()
