"""Create-once handoff and additive task memory for measured C3/C5/C7 work."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,defaultdict
import hashlib
import json
from fetch_public import atomic_json,digests
from c6_engine import checked_registration

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_bytes())
def sha(path):return digests(path)[1]
def append_bytes(path,addition):
    old=path.read_bytes();backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(old)
    temp=path.with_name(path.name+'.tmp');temp.write_bytes(old+addition)
    if temp.stat().st_size!=len(old)+len(addition):raise ValueError('Short memory append')
    temp.replace(path)
    if path.read_bytes()[:len(old)]!=backup.read_bytes():raise ValueError('Old memory changed')

def main():
    delivery=ROOT.parent/'TUNEL/DO_CHATGPT/ENTREGA_013_C3_C5_C7_recoloracao_e_pacote.md'
    if delivery.exists():raise FileExistsError('Do not repeat this progress registrar')
    _,registration=checked_registration()
    forecast=read('C5_RECOLORED_FORECAST.json');validation=read('C5_RECOLORED_VALIDATION.json')
    package=read('C7_PACKAGE_VALIDATION.json');api=read('C3_UNRAVELING_API.json')
    package['archive']=package['archive'].replace('\\','/')
    guard=read('C6_GUARD_TEST.json');noise=read('C5_RECOLORED_NOISE.json')
    if any(v['status']!='PASS' for v in (validation,package,api,guard)):raise ValueError('Unverified delivery')
    if package['registered_strain_reproduction']['registration_sha256']!=registration:raise ValueError('Different C6 registration')
    if sha(ROOT/package['archive'])!=package['archive_sha256']:raise ValueError('Archive changed')
    allcounts=dict(Counter(r['status'] for r in forecast['results']))
    realrows=[r for r in forecast['results'] if r['content']=='FULL_IMR']
    fullcounts=dict(Counter(r['status'] for r in realrows))
    groups=defaultdict(list)
    for r in realrows:groups[(r['psd'],r['recovery'],r['reading'],r['SNR'])].append(r)
    common=[k for k,v in groups.items() if len(v)==4 and all(r['status']=='CALIBRATED_CONDITIONAL_CELL' for r in v)]
    now=datetime.now(timezone.utc).isoformat()
    manifest=read('cache/MANIFESTO_DOWNLOADS.json');files={r['path'].replace('\\','/'):r for r in manifest['files']}
    for rel,row in files.items():
        if sha(ROOT/rel)!=row['sha256']:raise ValueError('Preserved cache changed: '+rel)
    for row in noise['scenarios']:
        p=ROOT/row['cache_path']
        if sha(p)!=row['cache_sha256']:raise ValueError('Recolored cache changed')
        files[p.relative_to(ROOT).as_posix()]=dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p),
            kind='derived_conditional_recolored_noise',origin='Public O4 held-out residuals and design curves; not future observations')
    for row in forecast['draws']:
        p=ROOT/row['path']
        if sha(p)!=row['sha256']:raise ValueError('Injection draw cache changed')
        files[p.relative_to(ROOT).as_posix()]=dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p),
            kind='conditional_injection_recovery_draws',origin='Two public waveform models; same 50 paired noise intervals')
    p=ROOT/package['archive'];files[p.relative_to(ROOT).as_posix()]=dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p),
        kind='internal_independent_research_package',origin='Own code and attributed public/derived data; no canonical program')
    manifest.update(at=now,files=list(files.values()));atomic_json(ROOT/'cache/MANIFESTO_DOWNLOADS.json',manifest)
    artifacts=['C5_BIAS_ABLATION.json','C5_EXTRA_QNMS.json','C5_OVERTONE_ABLATION.json',
        'C5_RECOLORED_NOISE.json','C5_RECOLORED_FORECAST.json','C5_RECOLORED_VALIDATION.json',
        'C3_UNRAVELING_API.json','C6_GUARD_TEST.json','C7_PACKAGE_VALIDATION.json',
        'tgl_ringdown_unravelings.py','prepare_recolored_noise.py','forecast_recolored_imr.py',
        'verify_recolored_forecast.py','verify_unravelings.py','verify_c6_guard.py',
        'build_independent_package.py','package_demo.py','package_reproduce_c6.py','verify_package_release.py',
        'C5_O5_DISTRIBUTIONS.png','C5_O5_DISTRIBUTIONS.svg','C7_INDEPENDENT/MANIFEST.json',
        'C7_INDEPENDENT/README.md','C7_INDEPENDENT/C6_REPRODUCTION_RESULT.json',package['archive'],
        'cache/MANIFESTO_DOWNLOADS.json']
    hashes={name:sha(ROOT/name) for name in artifacts}
    remaining=[
        'C0: três tentativas de leitura integral da literatura falharam (403/406); resolver por fontes primárias alternativas ou manter explicitamente a limitação na auditoria final.',
        'C4: conferir o release GWTC-3 e reconciliar eventos sem contagem dupla; a versão integral da inferência/fusão pyRing segue limitada ao que o release documenta.',
        'C5/C6: discrepância de modos e volume de prior agora medidos. Nenhum grupo PSD/modelo/leitura/SNR passou nas duas famílias e nas duas injeções simultaneamente. Não promover células isoladas ou maior SNR a calibração universal. Qualquer modelo novo para o strain exige adendo NÃO-CEGO, mantendo C6 intacto.',
        'C7: v1 independente entregue e C6 reproduzido a partir do strain; completar automação de regeneração dos posteriores/injeções e auditoria de cobertura do objetivo integral.',
        'Limite físico explícito: a seleção da partição, relógio, quantização/excitação e desenrolamento não foi determinada pelos dados. Não inventar uma escolha para encerrar o objetivo.'
    ]
    status=read('STATUS_ORDEM_013.json')
    status.update(date_utc=now,goal_status='ACTIVE_NOT_COMPLETE',
        previous_goal_turn='PROGRESS: ablações de harmônicos/overtones já em disco; turno de pergunta curta não fez trabalho científico',
        this_goal_turn='PROGRESS: 4608 células recoloridas, oráculo SVD, API Cauchy/Poisson com Bilby, teste adversarial C6 e pacote independente reproduzindo 75 linhas desde o strain',
        no_blocker_recurrence=True,active_processes=[],requirements_remaining=remaining,
        next_action='Reconciliar GWTC-3 e completar a regeneração portátil de posteriores/injeções; auditar o objetivo, sem tratar a falha de calibração como confirmação ou como obrigação de obter um resultado positivo.')
    status['verified'].update(C5_recolored=dict(cells=len(forecast['results']),N_per_cell=50,
        paired_noise_intervals_per_detector=50,all_status_counts=allcounts,full_IMR_status_counts=fullcounts,
        simultaneously_calibrated_two_families_two_injections=len(common),
        independent_SVD_lnB_max_error=max(r['independent_lnB_max_error'] for r in validation['independent_SVD_controls']),
        physical_scope=forecast['source_clock']),
        C3_optional_readouts=dict(status=api['status'],bilby_consumers=len(api['consumer']),exact_occupation_max=4096,
            finite_density_checks=[r['occupation'] for r in api['finite_occupation_controls'] if 'finite_density_error' in r]),
        C6_guard=dict(status=guard['status'],tests=len(guard['tests'])),
        C7=dict(archive=package['archive'],sha256=package['archive_sha256'],bytes=package['bytes'],
            manifest_members=package['archive_members'],reproduction=package['registered_strain_reproduction'],
            status='WORKING_V1_WITH_FULL_PIPELINE_AUTOMATION_PENDING'))
    status['hashes'].update(hashes);atomic_json(ROOT/'STATUS_ORDEM_013.json',status)
    rows=[r for r in realrows if r['reading']=='R-B' and r['psd']=='O5' and r['SNR']==40 and r['family']=='SEOBNRv4HM']
    example='\n'.join(f"| {r['recovery']} | {r['injected_a']:g} | {r['lnB']['mean']:.6f} | {r['lnB']['standard_deviation']:.6f} | {r['absolute_bias']:.4f} | {r['coverage_90']:.2f} | {r['boundary_hits']} |" for r in rows)
    md=f'''[REAL — medições e reprodução; DERIVED/INPUT/CONJECTURE nos modelos; não confirmação física]

# Ordem 013 — distribuição de evidência, interfaces e pacote independente

Data UTC: {now}. Axiomas: N/A — sem Lean. Nenhuma edição do um.py, do kernel,
de memórias canônicas ou do gate. Registro C6 conferido: `{registration}`.

## O que mudou

- **PAGO — diagnóstico da discrepância:** a falha já existe no harmônico 22 isolado.
  Overtones reduzem o resíduo, mas amplitudes livres absorvem informação sobre a.
  No ruído O4 medido, SNR40, família SEOB: resíduo² 41,6301 com 220+440, 0,12646
  com quatro modos e 0,001435 com oito; poder Fisher local otimista cai de 0,4039
  para 0,1346 e 0,0430. São controles em SNR fixo, não eventos diferentes.
- **PAGO — recoloração validada:** quatro curvas O4/O5/ET/CE, 256 resíduos disponíveis
  por detector; primeiras 50 janelas em cada célula. Projeção polinomial no intervalo,
  convenção Cholesky explícita e controles independentes de ruído Gaussiano.
  Continuação abaixo da tabela por f^(-4), controles f^(-2)/f^(-6); sensibilidade
  máxima do norm do filtro de aproximadamente 1,31%. Não são observações futuras.
- **PAGO — matriz C5:** {len(forecast['results'])} células, duas famílias, oito leituras,
  três modelos, seis SNRs e a=0/1; controles FULL_IMR e MATCHED_RINGDOWN separados.
  Contagens globais: `{allcounts}`; FULL_IMR: `{fullcounts}`.
  **Nenhum grupo passou simultaneamente nas duas famílias e nas duas injeções.**
  As 100 células FULL_IMR aprovadas isoladamente não permitem escolher a posteriori
  uma família favorável. Matriz completa e amostras preservadas.
- **PAGO — oráculo independente:** 96 células conferidas por SVD, maior diferença
  em ln B `{max(r['independent_lnB_max_error'] for r in validation['independent_SVD_controls']):.6g}`;
  refinamento contínuo do MLE mudou no máximo
  `{max(r['shift'] for r in validation['continuous_profile_refinement']):.6g}`.
- **PAGO — interfaces C3:** Cauchy de fase e Poisson coerente finito reutilizáveis,
  com sementes, controles de cauda, recusa de N macroscópico como soma exata,
  oráculo de matriz densidade N=4/64/256 e três consumidores Bilby reais.
  Template antigo e C6 congelado preservados.
- **PAGO — recusa adversarial C6:** cópias com registro, código ou QNM adulterados
  são recusadas; cópias íntegras passam. Nenhuma janela real lida neste teste.
- **PAGO — pacote independente v1:** {package['bytes']} bytes no ZIP, {package['archive_members']}
  membros. Manifesto e demo NumPy passaram numa extração limpa no Windows.
  A reprodução em nova pasta WSL recalculou todas as cinco janelas a partir do
  strain público, sem saídas existentes: 75 linhas, diferença máxima em ln B
  `{package['registered_strain_reproduction']['max_lnB_difference']}`.
- **NÃO PAGO — automação portátil de todo o acervo:** v1 inclui interfaces,
  evidências e reprodução C6; a regeneração completa de posteriores/injeções e a
  comparação separada GWTC-3 continuam por fazer. Objetivo continua ativo.

## Exemplo O5/A+ — ramo B, SNR40, família SEOBNRv4HM

| modelo de recuperação | a injetado | média ln B | dispersão ln B | viés absoluto | cobertura90 | intervalos na borda |
|---|---:|---:|---:|---:|---:|---:|
{example}

O modelo com oito modos tem ln B médio ~0,851 mesmo no **ruído sem sinal**.
O pequeno favorecimento não distingue a=0 de a=1: o volume do prior de amplitudes
explica o deslocamento. Não converter isso em sigma, nem chamar de dephasing.
As distribuições das mesmas 50 janelas são pareadas; não são milhares de eventos.
A figura `C5_O5_DISTRIBUTIONS.png` foi renderizada e inspecionada.

## Pacote e reprodução

[README em inglês](../../ORDEM_013_RINGDOWN/C7_INDEPENDENT/README.md)
· [ZIP verificado](../../ORDEM_013_RINGDOWN/{package['archive']})
· [validação do pacote](../../ORDEM_013_RINGDOWN/C7_PACKAGE_VALIDATION.json).

```sh
python -m pip install -r requirements-minimal.txt
python verify_manifest.py
python run_demo.py --output
python -m pip install -r requirements-reproduction.txt
python reproduce_c6.py --run --download
```

Para refazer a nova bancada no ambiente científico local, scripts principais:
`prepare_recolored_noise.py`, `forecast_recolored_imr.py`,
`verify_recolored_forecast.py`, `verify_unravelings.py`.
Os geradores recusam sobrescrever caches; usar cópia nova para repetir.
O pacote inclui tabela de 264 combinações evento/leitura, 33 eventos únicos.
Não combina múltiplas análises de GW250114 como observações independentes.

## Ficha de aproveitamento

Reutilizados: v369 congelada (não executada), `QNM_GRID.json`, dois IMRs já
construídos, 256 janelas fora da fonte por detector, `linear_statistics`,
`mode_basis` e registro/engine C6. Novos artefatos têm consumidores: ruído
recolorido → matriz → oráculo/figura; interfaces → Bilby/demo; engine congelado
→ reprodução independente. Nenhuma função adicionada ao programa canônico.
Não há nova execução do evento orientada pela escolha de modelos extras.

## Próximos itens e limites

'''+'\n'.join('- '+r for r in remaining)+'''

Falhas anteriores preservadas. Esta entrega não apaga os diagnósticos de matriz
de covariância ou do modelo fundamental. O viés/cobertura negativo é resultado;
não se exige obter um número favorável para concluir uma medição honesta.

## Custódia lida nesta rodada

| arquivo | SHA-256 |
|---|---|
'''+''.join(f'| `{name}` | `{digest}` |\n' for name,digest in hashes.items())
    raw=md.encode('utf-8');temp=delivery.with_name(delivery.name+'.tmp');temp.write_bytes(raw)
    if temp.stat().st_size!=len(raw):raise ValueError('Short handoff write')
    temp.replace(delivery)
    append_bytes(ROOT/'PROGRESSO.md',('\n\n---\n\n'+md).encode('utf-8'))
    print(json.dumps(dict(status='RECORDED_ACTIVE',delivery=str(delivery),delivery_sha256=sha(delivery),cache_manifest_files=len(files),simultaneously_calibrated_groups=len(common),active_processes=[])))

if __name__=='__main__':main()
