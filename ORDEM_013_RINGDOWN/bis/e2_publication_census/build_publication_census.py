"""Freeze publication existence only; do not access posterior or strain products."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
CAT = BASE.parent / 'TUNEL/PARA_CHATGPT/ORDEM_013BIS_INSUMOS/medicao_da_ampliacao/B_catalogos'
INPUT = BASE / 'bis/e1_selection/CALIBRATION_AND_CANDIDATE_CENSUS.json'
INPUT_MD = INPUT.with_suffix('.md')
PINS = {}

def read_source(path):
    raw = path.read_bytes()
    PINS[str(path.resolve())] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    return raw

def atomic_new(name, raw):
    target = OUT / name
    if target.exists():
        raise FileExistsError('Frozen output already exists: ' + str(target))
    temp = OUT / (name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.stat().st_size == len(raw) and len(raw) > 0
    temp.replace(target)
    assert target.read_bytes() == raw

def save_json(name, obj):
    atomic_new(name, (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

e1 = json.loads(read_source(INPUT))
read_source(INPUT_MD)
research = json.loads(read_source(OUT / 'SEARCH_METADATA.json'))
events = e1['counts_by_run']['O4_public_total']['candidate_events']
assert len(events) == 23 and len(set(events)) == 23
assert events == research['target_events']
tgr4_path = CAT / 'gwtc4_tgr3.txt'
tgr5_path = CAT / 'gwtc5_tgr.txt'
tgr4 = read_source(tgr4_path).decode('utf-8').splitlines()
tgr5 = read_source(tgr5_path).decode('utf-8').splitlines()
flags_path = CAT / 'gwtc5_tgr_table2_3_parsed.json'
flags = {r['event']: r for r in json.loads(read_source(flags_path))}

# Extract ONLY event identifiers from the table, never parameter values.
assert 'Table 2. Results from the PYRING analysis' in tgr4[1831]
table2_names = []
table2_lines = {}
for number in range(1847, 2176):
    for match in re.finditer(r'GW\d{6}[ _]\d{6}', tgr4[number-1]):
        name = match.group().replace(' ', '_')
        table2_names.append(name)
        table2_lines[name] = number
assert len(table2_names) == len(set(table2_names)) == 22
assert 'Parametrized tests' in tgr4[2473]
assert 'deviations in the frequency and damping time' in tgr4[2475]
assert 'We hierarchically combine the deviation measurements' in tgr4[2500]
assert 'from all O4a events analyzed, listed in Table 2.' in tgr4[2501]
published_tgr4 = sorted(set(events) & set(table2_names))
assert len(published_tgr4) == 8
found = set(published_tgr4) | {'GW231123_135430'}
glitch_events = {'GW240515_005301', 'GW240615_160735', 'GW240930_035959', 'GW241102_144729'}

def selection_symbols(lines, event, lower, upper):
    indexes = [i for i in range(lower-1, upper) if re.search(re.escape(event).replace('_', '[ _]'), lines[i])]
    assert len(indexes) == 1, (event, indexes)
    start = indexes[0]
    end = next((i for i in range(start+1, upper) if re.match(r'GW\d{6}[ _]\d{6}', lines[i])), upper)
    return start+1, [s.strip() for s in lines[start+1:end] if re.fullmatch(r'[✓+· .–−—-]+', s.strip()) and s.strip()]

rows = []
for event in events:
    is_found = event in found
    batches = [s for s in research['searches'] if event in s['events']]
    assert len(batches) == 6, (event, len(batches))
    run = 'O4a' if event in e1['counts_by_run']['O4a']['candidate_events'] else 'O4b'
    local = None
    if event in published_tgr4:
        source_ids = ['TGR4', 'TGR4_RELEASE']
        reason = 'Nome na Tabela 2; método parametrizado vincula os eventos dessa tabela a medidas de delta_f220 e delta_tau220.'
        local = {'path': str(tgr4_path.resolve()), 'table': 2, 'event_name_line': table2_lines[event], 'method_lines': [2474, 2502], 'scope': 'Nomes e existência da análise; valores da tabela/contornos não extraídos.'}
    elif event == 'GW231123_135430':
        source_ids = ['GW231123_SIEGEL', 'GW231123_ZENODO', 'GW231123_WANG', 'GW231123_IDENTITY']
        reason = 'Resumo primário declara busca de desvios do espectro de Kerr; release TGR própria existe. Não é mera estimativa Kerr/GR.'
    elif run == 'O4a':
        source_ids = ['TGR4']
        line, symbols = selection_symbols(tgr4, event, 83, 1536)
        assert symbols == ['· · ·']*3 + ['✓']*4
        local = {'path': str(tgr4_path.resolve()), 'table': 1, 'event_name_line': line, 'ringdown_columns': ['pyRing', 'pSEOBNR', 'QNMRF'], 'ringdown_selected': [False]*3, 'echo_selected': [True]*4, 'legend_lines': [1528,1536]}
        reason = 'Não localizado no escopo. TGR4 Tabela 1 marca apenas testes de ecos, sem seleção pyRing/pSEOBNR/QNMRF; ecos não são delta_f/delta_tau QNM.'
    else:
        source_ids = ['TGR5', 'TGR5_RELEASE']
        f = flags[event]
        assert f['RT'] and f['POL'] and not any(f[k] for k in ['TIGER','FTI','RD','pSEOBNR','QNMRF'])
        line, symbols = selection_symbols(tgr5, event, 334, 1745)
        assert symbols.count('✓') == 2
        local = {'path': str(tgr5_path.resolve()), 'table': 2, 'event_name_line': line, 'selection_flags_source': str(flags_path.resolve()), 'tests_selected': {k:f[k] for k in ['RT','POL','TIGER','FTI','RD','pSEOBNR','QNMRF']}, 'raw_checkmark_count': 2}
        reason = 'Não localizado no escopo. TGR5 seleciona RT/POL; não seleciona RD/pSEOBNR/QNMRF para este evento. Metadados GR não contam como deformação.'
    if event in glitch_events:
        source_ids.append('O4B_GLITCH')
    direct_hits = []
    for b in batches:
        for hit in b['results']:
            if hit['primary_domain'] and event in hit['title'] + hit['url']:
                if hit['url'] not in direct_hits: direct_hits.append(hit['url'])
    sources = [s for s in research['supplemental_sources'] if s['id'] in source_ids]
    rows.append({
        'event': event, 'run': run, 'statute': 'REAL_PUBLICATION_EXISTENCE' if is_found else 'OPEN_SCOPED_NOT_FOUND',
        'eventknown_delta_publication': 'FOUND' if is_found else 'NOT_FOUND_IN_SCOPE',
        'known_delta_publication': True if is_found else None,
        'publication_universally_absent': None,
        'prior_exposure_reported': False, 'prior_exposure_statute': 'DECLARADO_E1_NO_CANDIDATE_POSTERIOR_ACCESS; NOT_GLOBAL_AUDIT',
        'prior_exposure_verified': None,
        'newly_found_relative_to_pSEOB33_plus18_census': is_found,
        'exclude_even_if_prior_exposure_false': is_found,
        'incidental_numeric_exposure_in_this_session': event == 'GW231123_135430',
        'blindness_certified': False,
        'disposition': 'EXCLUDE_PUBLISHED_NONBLIND_CALIBRATION_CANDIDATE' if is_found else ('HOLD_DATA_QUALITY_METHODS_BEFORE_BLIND_PE' if event in glitch_events else 'PROVISIONAL_NOT_FOUND_SCOPE_ONLY'),
        'reason': reason, 'source_ids': source_ids,
        'sources': [{'id':s['id'],'url':s['url'],'publication_date':s.get('publication_date'),'version':s.get('version')} for s in sources],
        'local_source_pin_locator': local, 'direct_primary_search_hits': direct_hits,
        'search_batch_ids': [b['id'] for b in batches],
        'queries': [q for b in batches for q in b['request']['search_query'] if event in q['q'] or event.replace('_',' ') in q['q'] or ('"'+event.split('_')[0]+'"') in q['q']],
        'domain_census_coverage': {'arxiv':'exact-ID domain search plus short alias discovery; direct known-publication abstract checks and local TGR4/5; index failures explicit', 'zenodo':'exact-ID search; GR release metadata not classified as deformation; direct GW231123 record if applicable', 'LVK_DCC_GWOSC':'domain-filtered targeted search, exact-name metadata and TGR4/5 local selection coverage', 'broader_web':'short and full-space-name queries; nonprimary hits discovery only', 'not_covered':'exhaustive all-version full-text crawl, private/unindexed studies, posterior contents, strain, all theses'},
        'data_quality_warning': {'status':'REAL_LVK_GLITCH_SUBTRACTION_METADATA', 'detector':'LLO', 'source_id':'O4B_GLITCH', 'required_before_PE':'Fixar produto/subtração usados, canais, máscara, PSD e controle de sensibilidade a glitch sem consultar os deltas do evento. Este censo não executou essas ações.'} if event in glitch_events else None
    })

now = datetime.now(timezone.utc).isoformat()
result = {
    'schema_version':1, 'order':'ORDEM013BIS',
    'status':'FROZEN_SCOPED_PUBLICATION_INVENTORY__NOT_E2_REGISTRATION',
    'started_utc':research['started_utc'], 'frozen_utc':now,
    'publication_cutoff_utc':now,
    'statutes':['REAL — existência e metadados conferidos','DERIVED — cruzamento nominal das tabelas','INPUT — exclusão por publicação independentemente de exposição','OPEN — ausência universal, cegamento e validação de PE'],
    'definition':'FOUND exige evidência de análise publicada que admite desvios QNM de frequência/tempo de amortecimento (ou espectro equivalente), com vínculo ao evento; detecção multimodo, estimativa Kerr/GR, teste de ecos ou outro teste GR não bastam.',
    'summary': {'events':23,'found_publication':len(found),'not_found_in_scope':23-len(found),'published_via_TGR4_pyRing_KerrPostmerger':len(published_tgr4),'GW231123_external_publication':1,'data_quality_holds_among_not_found':len(glitch_events),'provisional_without_this_specific_warning':23-len(found)-len(glitch_events),'targeted_search_batches':len(research['searches']),'targeted_search_queries':sum(len(s['request']['search_query']) for s in research['searches'])},
    'published_exclusions': sorted(found),
    'not_found_scope_events': [e for e in events if e not in found],
    'data_quality_holds':sorted(glitch_events),
    'tgr4_table2_name_only_membership':table2_names,
    'events':rows, 'sources':research['supplemental_sources'],
    'source_pins':PINS,
    'pin_scope':'SHA256 dos bytes locais lidos. SEARCH_METADATA.json fixa títulos/URLs/datas retornados e consultas, não hash dos artigos remotos nem dos produtos científicos. Textos locais históricos não presumidos idênticos à versão web atual.',
    'limitations':research['limitations'], 'incidental_exposure':research['incidental_exposure'],
    'policy': {'universal_absence_asserted':False,'E2_registered':False,'E2_PE_run':False,'blindness_certified':False,'posterior_or_strain_files_downloaded':False,'numerical_posterior_values_intentionally_extracted':False,'no_numeric_exposure_claim_permitted':False,'canonical_files_modified':False,'write_scope':str(OUT),'memory_updates':'Não executadas: ordem expressa restringe escrita a esta pasta.'},
    'next_gate':'Aplicar nove exclusões independentemente de exposição; registrar formalmente escopo temporal/publicações no E2; resolver controles de qualidade dos quatro avisos antes de qualquer PE. Os demais continuam provisórios, sem certificado universal de ineditismo.'
}
save_json('PUBLICATION_CENSUS.json', result)

md = ['# ORDEM013BIS — inventário de publicações antes de E2','',
      '[REAL — existência documental e metadados] · [DERIVED — cruzamento nominal] · [INPUT — seleção] · [OPEN — ausência universal e cegamento]', '',
      f'Congelado em **{now}**. **23 eventos; 9 exclusões por publicação; 14 não localizados no escopo, dos quais 4 com pendência de qualidade de dados.** E2 não registrado nem executado.', '',
      '## Achados prioritários', '',
      'Os oito nomes O4a abaixo estão na Tabela 2 do [TGR4 III](https://arxiv.org/abs/2603.19021) (19/03/2026). O parágrafo metodológico “Parametrized tests” vincula os eventos dessa tabela às medidas de desvios de frequência e amortecimento com pyRing/KerrPostmerger. Foram extraídos somente nomes e a existência da análise. A tabela GR isolada não sustentaria essa conclusão.', '',
      '**GW231123_135430** tem publicação externa de teste do espectro de Kerr: [Siegel et al.](https://arxiv.org/abs/2511.02691v1), 04/11/2025, e [release Zenodo v1](https://zenodo.org/records/17518767), mesma data. [Wang et al.](https://arxiv.org/abs/2509.02047v1), 02/09/2025, corrobora a existência de teste no-hair. Não se presume igualdade de modos ou parametrizações entre estudos. A âncora do nome abreviado é a [documentação GWOSC](https://gwosc.org/o4_eventdata_docs/).', '',
      '**Publicação localizada exclui mesmo quando `prior_exposure_reported=false`.** Esse campo preserva a declaração de E1; exposição histórica global não foi auditada. Calibração aqui é classificação de uso, sem incorporação de likelihood ou posterior.', '',
      '## Disposição por evento', '',
      '| Evento | Publicação de desvios | Disposição | Fonte e data |',
      '|---|---|---|---|']
for r in rows:
    event = r['event']
    if event in published_tgr4:
        citation='[TGR4 III](https://arxiv.org/abs/2603.19021), 19/03/2026; Tabela 2 + método'
    elif event == 'GW231123_135430':
        citation='[Siegel](https://arxiv.org/abs/2511.02691v1), 04/11/2025; [Zenodo](https://zenodo.org/records/17518767)'
    elif r['run']=='O4a':
        citation='[TGR4 III](https://arxiv.org/abs/2603.19021), 19/03/2026; Tabela 1 + buscas'
    else:
        citation='[TGR5](https://arxiv.org/abs/2607.19293), 21/07/2026; seleção + buscas'
    disposition='EXCLUIR do cego' if event in found else ('PENDÊNCIA glitch/PE' if event in glitch_events else 'PROVISÓRIO')
    md.append(f'| {event} | {"LOCALIZADA" if event in found else "NÃO LOCALIZADA NO ESCOPO"} | {disposition} | {citation} |')
md += ['', '## Aviso LVK de qualidade dos dados', '',
       'O artigo primário [Open Data O4b](https://arxiv.org/abs/2605.27090), submetido em 26/05/2026 e revisado em 17/06/2026, contém tabela de subtração de glitches. Os metadados da [cópia primária MPG](https://pure.mpg.de/rest/items/item_3712777_1/component/file_3712778/content) listam **GW240515_005301, GW240615_160735, GW240930_035959 e GW241102_144729**, todos em **Livingston (LLO)**. Não foi presumida identidade entre versões do espelho e arXiv.', '',
       'Antes de PE cega, fixar o produto e a subtração adotados, canais, máscara, PSD e controles de sensibilidade. Nada disso foi executado aqui. O aviso de GW240930 foi confrontado com LVK; o blog Gravity Spy não foi usado sozinho. Glitch não prova deformação QNM e não é exclusão por publicação de delta.', '',
       '## Cobertura e limites', '',
       f'Foram realizadas **{result["summary"]["targeted_search_queries"]} consultas dirigidas em {len(research["searches"])} lotes**, com os 23 nomes completos, variantes com espaço e prefixos de data; filtros arXiv/Zenodo/LVK/GWOSC e busca web ampla. Consultas suplementares verificaram os achados prioritários. O JSON conserva consultas e cobertura por evento; SEARCH_METADATA.json guarda os resultados bibliográficos dos lotes. Resultados de lote não são atribuídos indiscriminadamente a cada evento.', '',
       'O índice arXiv retornou vazio para consultas exatas inclusive do positivo GW231123. Logo, zero hits não prova ausência. Prefixos com a mesma data podem designar eventos distintos. A busca não cobre exaustivamente toda versão, tese, estudo privado ou não indexado.', '',
       'GW230919_215712: TGR4 marca testes de ecos, sem seleção das três análises de ringdown. Os treze O4b: metadados TGR5 marcam RT/POL, sem RD/pSEOBNR/QNMRF. Nenhuma dessas ausências locais prova ausência em outros trabalhos. Estimativas GR e releases gerais de parâmetros não foram promovidas a publicação de deformação.', '',
       '## Integridade do cegamento e custódia', '',
       '**Incidente declarado:** a primeira busca devolveu trechos quantitativos sobre GW231123 antes da ativação do filtro, além de números GR. Portanto, esta sessão não pode certificar “nenhuma exposição numérica”. Os valores não são reproduzidos, não foram usados na seleção e não integram estes arquivos. GW231123 já é excluído pela existência da publicação. As buscas seguintes tiveram supressão antes da apresentação; os artefatos conservam apenas metadados.', '',
       'Nenhum arquivo de posterior/strain foi baixado ou aberto; nenhum PE foi executado. Os textos TGR4/5 existentes foram consultados apenas para métodos, seleção e nomes. Não houve operação em arquivos canônicos. A ordem limita a escrita a esta pasta; não se atualizaram memórias externas.', '',
       'Os SHA256 em PUBLICATION_CENSUS.json foram calculados dos arquivos locais nesta execução. Pins web identificam o snapshot bibliográfico, não bytes de artigos remotos. FREEZE_RECEIPT.json sela JSON, Markdown, metadados e script, com nova conferência das entradas. Este inventário é utilizável para o próximo registro E2, mas não o substitui.', '']
atomic_new('PUBLICATION_CENSUS.md', ('\n'.join(md)).encode('utf-8'))
for name, pin in PINS.items():
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == pin['sha256'], name
assert sum(r['known_delta_publication'] is True for r in rows)==9
assert sum(r['eventknown_delta_publication']=='NOT_FOUND_IN_SCOPE' for r in rows)==14
receipt={'status':'PASS_SCOPED_INVENTORY_INTEGRITY__BLINDNESS_NOT_CERTIFIED','utc':datetime.now(timezone.utc).isoformat(),'inputs_unchanged':True,'counts':result['summary'],'outputs':{}}
for name in ['PUBLICATION_CENSUS.json','PUBLICATION_CENSUS.md','SEARCH_METADATA.json','build_publication_census.py']:
    raw=(OUT/name).read_bytes();receipt['outputs'][name]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
save_json('FREEZE_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
