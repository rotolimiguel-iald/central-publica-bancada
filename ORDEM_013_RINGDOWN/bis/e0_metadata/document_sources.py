"""Document audited excerpts and metadata counts, without running scientific builders."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math
from lxml import html
from pypdf import PdfReader

B = Path(__file__).resolve().parents[2]
C = B/'cache/e0_metadata'
O = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name, text):
    with (O/name).open('xb') as f: f.write(text.encode('utf-8'))
def emit(name, data): write(name, json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
def text(name): return ' '.join(html.fromstring((C/name).read_text(encoding='utf-8',errors='replace')).text_content().split())

inventory=json.loads((O/'GWOSC_INVENTORY.json').read_bytes())
fisher=json.loads((B/'C5_FISHER_v3.json').read_bytes())
ratio=next(r for r in fisher['same_source_R_B'] if r['psd']=='O5')['snr_ratio_to_O4']
budget=json.loads((B/'bis/PART_B_BUDGET_START.json').read_bytes())
now=datetime.now(timezone.utc).isoformat()
sources=[]
for p in sorted(C.glob('*.receipt.json')):
    r=json.loads(p.read_bytes()); raw=C/p.name.removesuffix('.receipt.json')
    if sha(raw)!=r['sha256'] or raw.stat().st_size!=r['bytes']: raise ValueError(str(raw))
    r.update(receipt_sha256=sha(p), usable_document=r['status']==200)
    if raw.name=='ce_whitepaper_v1.pdf':
        r.update(usable_document=False, availability_note='HTTP 200 but PDF is incomplete (1048576 bytes, no EOF, PdfReader failure); not used to substantiate timeline.')
    if raw.name=='ce_whitepaper_v3.html':
        r.update(usable_document=False, availability_note='HTTP 406; attempted version not present in arXiv submission history. No claim supported by this response.')
    if raw.name=='ce_update_2026.html':
        r['availability_note']='URL redirected to PDF; raw cache basename ends .html, but MIME and signature are PDF. Title + page 5 timeline inspected; not whole-deck reading.'
    sources.append(r)
emit('SOURCE_LEDGER.json',dict(status='REAL_BYTE_ARCHIVE_AND_AVAILABILITY_CHECK',generated_utc=now,sources=sources,
    no_posterior_or_strain_downloads=True, reading_scope='Selected excerpts only; archive of full document does not mean full reading'))

# Small derived excerpts are navigation aids. The cached original bytes remain authoritative.
read_scopes={
 'igwn_observing_plan.html':'Dated 3 September 2026 update and timeline paragraphs',
 'igwn_capabilities.html':'O5 sensitivity and schedule context; older update than observing plan',
 'et_overview.html':'Preparatory phase, early 40s and site decision 2027',
 'et_italy_questions.html':'Operational date optimistic 2035; construction/funding conditions',
 'o5_psd_projections_v2.html':'Abstract: epochs O5a/b/c and replaced A+ test masses',
 'gwtc5_release.html':'Catalog scope, cumulative link and release note 26 May 2026',
 'berti_2505_23895v3.html':'Section 7.1/7.1.1, Figure 76, reference 1184',
 'bhagwat_2304_02283v2.html':'Section II (window and degeneracy), IV/V, Tables 2 and 3',
 'observing_scenarios_v55.pdf':'Table 2, printed page 10; document landing-page/version metadata',
 'ce_update_2026.html':'Title page and page 5 image (visual inspection) only'}
emit('READING_SCOPE.json',read_scopes)
pdf=PdfReader(C/'observing_scenarios_v55.pdf')
write('observing_scenarios_table2_extracted.txt',pdf.pages[9].extract_text())
berti=html.fromstring((C/'berti_2505_23895v3.html').read_text(encoding='utf-8'))
sec=berti.xpath('//*[@id="S7.SS1"]')[0]
write('berti_section_7_1_extracted.txt',' '.join(sec.text_content().split()))
emit('SCENARIOS_AND_SCHEDULES.json',dict(status='DOCUMENTARY_SCENARIOS_NOT_MEASURED_FORECAST',as_of_utc=now,
    part_b_budget=budget,
    o5_gain=dict(bbh_range_ratio=[2500/1600,2500/1400],bns_range_ratio=[330/190,330/160],bns_upper_only=330/160,
        range_source='LIGO-P1200087-v55, Table 2, printed p10, archived 2019-09-04 PDF',
        range_scope='Historical projected orientation-averaged range for single detector threshold SNR8, BBH30+30 solar masses. Not a universal network/ringdown SNR multiplier.',
        c5_ratio=ratio,c5_status='DECLARED_LOCAL_C5_RESULT_READ_AND_HASHED_NOT_REMEASURED_HERE',c5_sha256=sha(B/'C5_FISHER_v3.json'),
        c5_scope=fisher['parameters'], c5_limit='Same source/projection and individual reference PSD; not network or cosmological population. No Fisher rerun.',
        current_o5_scope='T2500310-v2 distinguishes O5a/b/c; terminal A+ sensitivity is not guaranteed at O5 start'),
    timelines=[
        dict(project='O5',source='https://observing.docs.ligo.org/plan/',document_date='2026-09-03',status='PLANNED_START_OPEN',
             statement='O5 plans/timeline under discussion/refinement. Six-month IR1 planned early/mid-November 2026; IR1 is not O5.'),
        dict(project='ET',source='https://einsteintelescope.eu/about-et/overview/',document_date=None,status='PLANNING_NOT_COMMITTED',
             statement='Official overview: observations by early 2040s; site decision foreseen 2027. Page publication date not displayed; retrieval dated.'),
        dict(project='ET optimistic alternative',source='https://www.einstein-telescope.it/en/questions-answers/',document_date=None,status='OPTIMISTIC_CONDITIONAL',
             statement='Around 2035 in the most optimistic case, conditional on construction (~10 years) and funding; not reconciled into a fixed date.'),
        dict(project='CE',source='https://dcc.cosmicexplorer.org/CE-G2600054/public',document_date='2026-09-03',figure_date='2026-03-10',status='ILLUSTRATIVE_PROJECT_TIMELINE',
             statement='Slide 5: construction 2035-2039, commissioning into 2040, Run from 2041. Title/date and graphic inspected. No funded/delivered commitment inferred.'),
        dict(project='GWTC-6',source='https://gwosc.org/api/v2/catalogs',document_date=None,status='NO_RELEASE_OR_OFFICIAL_DATE_FOUND_IN_CHECKED_SOURCES',
             statement='Not in 18-catalog API snapshot; May/June 2027 in prior input is an analogy, not an official release date. Negative search does not prove nonexistence everywhere.')],
    ringdown_basis=dict(berti='arXiv:2505.23895v3 section7.1/Figure76, 10 August2026',bhagwat='arXiv:2304.02283v2, 25 September2023',
        snr_window='About 10M after strain peak, amplitude/phase fits and SNR integration consistent (Bhagwat section II). Upper time endpoint not explicitly established in this read scope.',
        window_mass_convention='Do not silently equate paper symbol M to local final-mass tM convention; exact conversion not certified here',
        rates_per_year=[dict(network='ET triangle10km',rho_ge50=28,error50=7,rho_ge100=3,error100=1),
            dict(network='ET twoL15km',rho_ge50=70,error50=9,rho_ge100=7,error100=3),
            dict(network='ET triangle10km+CE',rho_ge50=161,error50=14,rho_ge100=13,error100=5),
            dict(network='ET twoL15km+CE',rho_ge50=246,error50=16,rho_ge100=18,error100=7)],
        status='KNOWN_CONDITIONAL_POPULATION_FORECAST_NOT_OBSERVED_COUNTS',
        applicability='Berti order100/year at RD>=50 is configuration/population dependent. Multi-mode Fisher forecast, not delta_tau220 identifiability or 5-sigma evidence.',
        uncertainty='Quoted errors belong to source simulation; not a new confidence interval on astrophysical rate'),
    deferred=['sigma(SNR) fit until A standard deviations and exact event join are supplied',
        'Mass/final-spin selection: final spin absent from metadata default summary',
        'O5 counts/rates/Poisson bands require definition of selected population and exposure; calendar duration is not live time',
        'No reading chosen; no sigma scaling, PE, source population simulation, posterior or strain acquisition performed']))

table=['| Corrida | únicos no inventário | ≥12 | ≥30 | ≥53 | ≥78 | ≥95 |','|---|---:|---:|---:|---:|---:|---:|']
for run,g in inventory['by_run'].items():
    table.append('| '+run+' | '+str(g['n_unique'])+' | '+' | '.join(str(g['thresholds'][str(t)]['count']) for t in [12,30,53,78,95])+' |')
source_table=['| Fonte/cache | HTTP | utilizável | SHA256 |','|---|---:|---|---|']
for r in sources: source_table.append(f"| [{Path(r['path']).name}]({r['requested_url']}) | {r['status']} | {r['usable_document']} | `{r['sha256']}` |")
high='\n'.join(f"- {r['event']} — {r['run']}, SNR {r['network_matched_filter_snr']}" for r in inventory['events'] if r['network_matched_filter_snr'] is not None and r['network_matched_filter_snr']>=30)
report=f'''# E0.3/E0.7 — metadados e bases documentais

[REAL documental/contagem de metadados; NÃO-CEGO; nenhuma nova inferência física]

Gerado {now}. Relógio da Parte B preservado em `SCENARIOS_AND_SCHEDULES.json`; fonte `bis/PART_B_BUDGET_START.json`, SHA256 `{sha(B/'bis/PART_B_BUDGET_START.json')}`. Trabalho leve e sequencial, um processo de cálculo por vez. Instantes inicial/final e duração de cada aquisição constam de SOURCE_LEDGER; o snapshot entre endpoints não é atômico. A duração de download não é exposição observacional.

## Convenção e inventário

Uma convenção: **network_matched_filter_snr preferencial/default publicado pelo GWOSC**, com cortes inclusivos sobre o valor arredondado. Cumulativo oficial confident é a base; acrescenta-se a última versão de discovery ausente desse cumulativo. Deduplicação por commonName. Isso não torna os pipelines de origem idênticos. Não misturamos SNR TGR, SNR de ringdown ou um valor recalculado. [API documentada](https://gwosc.org/api/v1/docs/), [cumulativo](https://gwosc.org/eventapi/jsonfull/GWTC/), [API v2](https://gwosc.org/api/v2/).

{chr(10).join(table)}

São 391 eventos cumulativos + GW250207_115645 = 392. O inventário inclui CBCs de diferentes classes, **não é amostra BBH pura**: por exemplo GW170817 explica o evento O2 ≥30. Catálogos marginais/terceiros e alertas sem publicação não entram. Os 433 latest da API ampla e 671 versões não são 433/671 eventos elegíveis deste recorte. GWTC4.0 não é somado a GWTC4.1. Todas as listas completas por corrida/corte constam em `GWOSC_INVENTORY.json`; `GWOSC_EVENTS.csv` carrega os campos por evento. Contagem foi cruzada com o mesmo campo da API v2 em 361 versões coincidentes; as demais são escolhas diferentes do endpoint latest, não equivalência presumida.

O4 público tem 302 eventos nominais e 74 ≥12; os 74 têm links de strain anunciados, **nenhum baixado ou validado aqui**. Entre esses 74, 69 têm massa final de fonte e spin efetivo; zero têm **spin final** no resumo default. `chi_eff` não é `chi_f`. Não derivamos massa detector multiplicando medianas, não cortamos M/spin e não certificamos que PE GR resumida seja inspiral-only. Esses campos são anteriores à futura seleção por δτ, mas a certificação mais forte permanece OPEN. Há parâmetros/links em GWOSC; isso não certifica posterior δτ disponível. O4c é apenas uma discovery publicada, não cobertura integral da corrida. [Corridas da API](https://gwosc.org/api/v2/runs).

Eventos ≥30:

{high}

GW250114 usa 78,6 nesta convenção, não 76,9 de outra análise. GW250207 usa 68,91. Não há evento ≥95 neste universo público consultado. Incertezas de SNR e de classificação não foram propagadas às contagens nominais; eventos próximos do corte podem mudar com nova versão. Isso não é uma declaração sobre eventos não publicados.

`SNR_JOIN_FOR_A.json` entrega chaves/GPS/SNR/Mfonte/z/chi_eff e ausência explícita de spin final para a bancada A. **σ(SNR) não foi ajustada**, aguardando os stds e a conciliação de conjuntos de A. Não foi escolhida leitura científica.

## Comparação com insumos

`HISTORICAL_COMPARISON.json` compara a nova resposta byte-arquivada ao antigo `E_instrumento/gwosc_catalogs_raw.json` por catálogo/evento/SNR. GWTC4.0 (129), 4.1 (140), 5.0 (161) e discovery (8): nenhum acréscimo, remoção ou mudança de SNR. Isto verifica estabilidade entre arquivos; os números antigos não foram copiados como medição nova. Reobtivemos GWTC5 ≥30 = 5, ≥78 = 1, ≥95 = 0. A diferença 45 GWTC5 versus 74 O4 ≥12 é cobertura de corridas, não melhora de sensibilidade. Nenhuma ausência de δτ pública ou contagem de eventos “cegos” foi inferida só destes metadados.

## O5: fatores com escopos distintos

[KNOWN/DERIVED] Releitura da **Tabela 2, página impressa 10**, [Observing Scenarios v55](https://dcc.ligo.org/LIGO-P1200087-v55/public), PDF arquivado com Last-Modified 04/09/2019: BBH30+30 aLIGO O4 1400–1600 Mpc e O5 2500 Mpc. Divisão independente: **{2500/1600:.4f}–{2500/1400:.7f}**. São alcances projetados de detector individual com limiar 8 e média de orientação/volume; não um fator universal de SNR da rede ou do ringdown. A tabela BNS dá 330/(160–190); **{330/160:.4f} é apenas o teto desse cenário BNS**, não ganho BBH autorizado.

[DECLARADO — artefato local conferido] C5_FISHER_v3 fornece **{ratio:.12f}**, SHA256 `{sha(B/'C5_FISHER_v3.json')}`. Fonte ilustrativa de massa detector 68,1 Msol, spin 0,68, banda 20–2048 Hz, passo 0,125 Hz, mesma fonte/projeção e PSD individual de referência. O código define o fator como razão das normas espectrais; nesta frente lemos a implementação e o resultado, **não repetimos C5**. Não é contagem medida, ganho da rede ou calibração do estimador pSEOB. O ganho não pode ser aplicado duas vezes.

[KNOWN atual] [T2500310-v2](https://dcc.ligo.org/T2500310-v2/public) distingue O5a/b/c e associa O5 à troca por massas A+; O5c corresponde à sensibilidade final projetada. Isso impede rotular a curva antiga como sensibilidade garantida desde o começo de O5. Não baixamos novas PSDs nem calculamos novos forecasts.

## Datas e disponibilidade

- **O5:** [plano IGWN, atualização 03/09/2026](https://observing.docs.ligo.org/plan/): cronograma em discussão/refinamento. IR1 previsto para início/meados de novembro de 2026, por seis meses; não confundir IR1 com O5. Data firme de O5 permanece OPEN. Datas antigas do insumo não se tornam promessa atual.
- **ET:** [overview oficial](https://einsteintelescope.eu/about-et/overview/) prevê início dos anos 2040 e escolha do sítio em 2027. [FAQ italiana](https://www.einstein-telescope.it/en/questions-answers/) mantém 2035 no caso mais otimista, condicionado a construção/financiamento. As páginas não exibem data editorial verificada; registramos acesso, não inventamos publicação. Não combinamos cenários em uma data firme.
- **CE:** [apresentação CE-G2600054 de 03/09/2026](https://dcc.cosmicexplorer.org/CE-G2600054/public), slide 5, gráfico atualizado em 10/03/2026: construção 2035–2039, commissioning até 2040, “Run” em 2041. Imagem extraída arquivada e inspecionada. É linha de planejamento, não compromisso entregue/financiado. A referência histórica a meados dos anos 2030 não foi promovida a cronograma atual. O PDF do white paper de 2023 retornou incompleto e não sustenta nenhuma conclusão aqui.
- **GWTC6:** não aparece nos 18 catálogos da [API consultada](https://gwosc.org/api/v2/catalogs); a busca primária não encontrou data oficial. Maio/junho de 2027 permanece analogia do insumo, não anúncio. O GWTC5 registra publicação em [26/05/2026](https://gwosc.org/GWTC-5.0/). Ausência nas fontes consultadas não é prova de inexistência de toda comunicação futura.

## Base 3G e janela

[KNOWN — forecast condicional] [Berti et al., v3, §7.1/Fig.76](https://arxiv.org/html/2505.23895v3) dá ordem de 100 eventos/ano com SNR_RD ≳50 e ordem de 10 com ≳100 na população/rede ilustrada. Não são observações ou precisão garantida de δτ220.

A origem [Bhagwat et al., v2, §II/Tabelas 2–3](https://arxiv.org/html/2304.02283v2) fixa os ajustes de amplitudes/fases e a integração da SNR a aproximadamente **10M depois do pico do strain**. Releitura das tabelas: ET triangular 10km: 28±7/3±1 por ano acima de 50/100; ET dois L de 15km: 70±9/7±3; acrescentando CE: 161±14/13±5 e 246±16/18±7. São resultados de população sintética e Fisher multimodo, não taxas medidas. Preservamos os erros publicados, sem chamar isso de novo IC Poisson. A fonte explicita degenerescência do 220 com massa/spin sem informação adicional.

Não está certificada aqui a equivalência exata do símbolo M da fonte ao tM de massa final usado localmente, nem o endpoint temporal superior. Não se transporta SNR_IMR→SNR_RD, janela no pico→10M, ET isolado→ET+CE ou previsão multimodo→δτ220 por igualdade nominal. O número de eventos úteis depende da população, configuração e critérios.

## Limites e próximos insumos

Esta frente fecha **inventário e base documental** de E0.3/E0.7, não seus forecasts completos. Permanecem a calibração σ(SNR) por A, seleção admissível por M/chi_f, população/exposição e bandas de contagem/tempo. Um intervalo-calendário não é live time; catálogo selecionado não fornece sozinho taxa Poisson completa. Fontes foram lidas nos trechos discriminados em `READING_SCOPE.json`; arquivamento integral não equivale a leitura integral.

## Custódia

{chr(10).join(source_table)}

SOURCE_LEDGER contém URL final, tipo, bytes, datas HTTP e de aquisição e flags. A tentativa HTML v3 do white paper CE retornou 406; a versão v1 PDF retornou HTTP200 com truncamento e falha de parse. Ambas ficam visíveis e inutilizáveis para sustentar afirmações. Nenhum posterior/strain novo, PE ou alteração de produção/canônico/memória.
'''
write('REPORT.md',report)
print(json.dumps(dict(report_sha256=sha(O/'REPORT.md'),sources=len(sources),usable=sum(r['usable_document'] for r in sources),ratio_declared=ratio)))
