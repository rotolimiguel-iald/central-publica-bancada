"""Join admitted event metadata to observed archive headers; no member-body reads."""
import ast
import bisect
from collections import Counter
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import datetime as dt

BASE=Path(__file__).resolve().parent
CHECKS=[]

def check(name,value):
    CHECKS.append({'name':name,'passed':bool(value)})
    if not value:raise AssertionError(name)

def hash_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(262144),b''):h.update(chunk)
    return h.hexdigest()

def pin(p):return {'path':str(p.relative_to(BASE)),'bytes':p.stat().st_size,'sha256':hash_file(p)}

def read(name):return json.loads((BASE/name).read_bytes())

def write_new(name,data):
    if not isinstance(data,str):data=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    raw=data.encode('utf-8');p=BASE/name;tmp=p.with_name(p.name+'.tmp')
    if p.exists() or tmp.exists():raise FileExistsError(p)
    with tmp.open('xb') as f:f.write(raw)
    if tmp.stat().st_size!=len(raw):raise RuntimeError('Incomplete write')
    os.replace(tmp,p)

def main():
    request=read('sources_local/D_CALIBRATION_MEMBER_INVENTORY_REQUEST.json')
    discovery=read('DISCOVERY.json');download=read('DOWNLOAD_RECEIPT.json');receipt=read('INVENTORY_RECEIPT.json')
    meta=read('sources_local/PROPOSTA_MANIFESTO_METADATA_D.json')
    p=BASE/'sources_local'/Path(request['source_receipt']['path']).name
    check('ROOT receipt identity',p.stat().st_size==request['source_receipt']['bytes'] and hash_file(p)==request['source_receipt']['sha256'])
    check('two complete downloads',download['status']=='COMPLETE' and len(download['archives'])==2)
    check('total within authorized cap',download['total_bytes_written']<=request['limits']['max_total_archive_bytes'])
    check('no retry',download['automatic_retries']==request['limits']['automatic_retries']==0)
    check('header inventory completed',receipt['status']=='COMPLETE_HEADER_INVENTORY_ONLY' and receipt['extracted_members']==0 and receipt['numerical_rows_parsed'] is False)
    check('original14events',len(meta['events'])==14 and [e['event'] for e in meta['events']]==meta['original_candidate_order'])
    check('source proposal unratified',meta['ratified'] is False and meta['V1_unchanged'] is True and meta['gate_changed'] is False)
    code=ast.parse((BASE/'public_archive_inventory.py').read_text(encoding='utf-8'))
    attrs={node.func.attr for node in ast.walk(code) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute)}
    check('no extraction/body-reader API in collector',not attrs.intersection({'extract','extractall','extractfile','readline','readlines'}))
    imports={node.name for n in ast.walk(code) if isinstance(n,ast.Import) for node in n.names}
    check('no science/library/execution imports',not imports.intersection({'numpy','h5py','scipy','bilby','subprocess'}))
    summary=[];index={};sources=[]
    for a in download['archives']:
        path=Path(a['path']);d=next(r for r in discovery['archives'] if r['archive']==a['archive'])
        check('official URL retained '+a['archive'],a['url_as_published']==d['url_as_published'])
        check('archive byte limit '+a['archive'],a['bytes']<=request['limits']['max_archive_bytes_each'])
        check('archive length '+a['archive'],path.stat().st_size==a['bytes']==d['declared_bytes'])
        check('archive pin '+a['archive'],hash_file(path)==a['sha256'])
        hp=BASE/(a['archive']+'.members.json');headers=json.loads(hp.read_bytes())
        check('header/archive binding '+a['archive'],headers['archive_sha256']==a['sha256'])
        members=headers['members'];names=[m['name'] for m in members]
        check('unique member paths '+a['archive'],len(names)==len(set(names)))
        check('member count '+a['archive'],len(members)==headers['header_count']<=100000)
        check('expanded size cap '+a['archive'],headers['expanded_bytes_traversed']<=8*1024**3)
        check('no member body interpreted '+a['archive'],all(not m['member_body_read_via_extractfile'] and not m['numerical_rows_parsed'] for m in members))
        check('no unsafe names '+a['archive'],all(not n.startswith(('/','\\')) and '..' not in n.replace('\\','/').split('/') for n in names))
        check('no links or special members '+a['archive'],all(m['is_regular_file'] or m['is_directory'] for m in members))
        check('all files match documentary name pattern '+a['archive'],all(m['detector_from_name'] in ('H1','L1') and m['GPS_from_name'] is not None for m in members if m['is_regular_file']))
        run=re.fullmatch(r'LIGO_(O4[ab])_cal_uncertainty\.tgz',a['archive']).group(1)
        detectors=[]
        for detector in ('H1','L1'):
            files=sorted([m for m in members if m['detector_from_name']==detector],key=lambda m:m['GPS_from_name'])
            epochs=[m['GPS_from_name'] for m in files]
            check('unique named epochs '+run+detector,len(epochs)==len(set(epochs)))
            check('matching directory detector '+run+detector,all(m['name'].split('/')[0]==detector+'_'+run for m in files))
            index[(run,detector)]={'files':files,'epochs':epochs,'archive':a,'header_pin':pin(hp)}
            gaps=[b-a for a,b in zip(epochs,epochs[1:])]
            detectors.append({'detector':detector,'regular_members':len(files),'min_GPS_in_name':min(epochs),'max_GPS_in_name':max(epochs),
                'spacing_seconds_counts':dict(sorted(Counter(gaps).items())),'is_validity_interval':False})
        summary.append({'archive':a['archive'],'sha256':a['sha256'],'bytes':a['bytes'],'url':a['url_as_published'],
            'header_count':len(members),'regular_file_count':sum(m['is_regular_file'] for m in members),
            'directory_count':sum(m['is_directory'] for m in members),'detectors':detectors,
            'expanded_bytes_traversed_without_parsing_bodies':headers['expanded_bytes_traversed']})
        sources.append({'archive':pin(path),'headers':pin(hp)})
    rows=[]
    for event in meta['events']:
        check('two detector descriptors '+event['event'],len(event['series'])==2 and {s['detector'] for s in event['series']}=={'H1','L1'})
        t=Decimal(event['GPS_text_as_catalog'])
        check('GPS text consistent with existing proposal '+event['event'],t==Decimal(str(event['GPS_proposed'])))
        for series in event['series']:
            run=re.search(r'/data/(O4[ab])_4KHZ_R1/',series['official_url']).group(1)
            det=series['detector'];data=index[(run,det)];files=data['files'];epochs=data['epochs']
            minimum=min(abs(Decimal(g)-t) for g in epochs)
            matches=[f for f in files if abs(Decimal(f['GPS_from_name'])-t)==minimum]
            pos=bisect.bisect_left(epochs,t)
            neighbor_epochs=[epochs[j] for j in (pos-1,pos) if 0<=j<len(epochs)]
            check('nearest verified by independent neighbor search '+event['event']+det,minimum==min(abs(Decimal(g)-t) for g in neighbor_epochs))
            before=max((g for g in epochs if g<=t),default=None)
            after=min((g for g in epochs if g>=t),default=None)
            spacing=None if before is None or after is None else after-before
            def descriptor(f):
                return {'member_name':f['name'],'GPS_from_filename':f['GPS_from_name'],
                    'member_size_header':f['size_from_header'],'member_mtime_header':f['mtime_from_header'],
                    'signed_epoch_minus_event_seconds':str(Decimal(f['GPS_from_name'])-t),
                    'member_content_sha256':None,'member_columns_verified':False,'calibration_version_effective':None,'frequency_validity_verified':False}
            rows.append({'event':event['event'],'detector':det,'release_group_from_admitted_URL':run,
                'event_GPS_text_reused':event['GPS_text_as_catalog'],'GPS_status_reused':event['GPS_status'],
                'GPS_source_field':'events[].GPS_text_as_catalog; existing GPS_proposed checked for agreement only',
                'source_manifest_pin':pin(BASE/'sources_local/PROPOSTA_MANIFESTO_METADATA_D.json'),
                'prior_hold_preserved':event['event'] in meta['four_holds'],'scientifically_selected':False,
                'archive':data['archive']['archive'],'archive_sha256':data['archive']['sha256'],
                'official_archive_url':data['archive']['url_as_published'],'header_inventory_pin':data['header_pin'],
                'nearest_distance_seconds':str(minimum),'nearest_candidates':list(map(descriptor,matches)),
                'nearest_is_unique':len(matches)==1,'epoch_at_or_before':before,'epoch_at_or_after':after,
                'bracket_spacing_seconds':spacing,'bracket_spacing_exceeds_one_hour':spacing is not None and spacing>3600,
                'spacing_is_documentary_not_veto':True,'local_validity_status':'OPEN_NO_NUMERICAL_CONTENT_READ',
                'C00_C01_equivalence_inferred':False,'chosen_calibration_for_PE':None})
    check('28 detector associations',len(rows)==28)
    check('14 event associations',len({r['event'] for r in rows})==14)
    check('no calibration chosen',all(r['chosen_calibration_for_PE'] is None and not r['scientifically_selected'] for r in rows))
    holds=[e for e in meta['original_candidate_order'] if any(r['event']==e and r['prior_hold_preserved'] for r in rows)]
    check('all holds retained',holds==meta['four_holds'])
    association={'request_id':request['request_id'],'status':'NAME_ONLY_CANDIDATES_NOT_CALIBRATION_POLICY',
        'rule':'Nearest absolute GPS difference within same run/detector, by filename only. Preserve ties and neighboring epochs; no validity threshold inferred.',
        'GPS_reconciliation_repeated':False,'four_holds_preserved':holds,'rows':rows,
        'calibration_payloads_parsed':False,'strain_PE_posteriors_read':False,'CAL_B_ratified':False,'D_opened':False}
    write_new('ASSOCIACAO_14_EVENTOS_28_DETECTORES.json',association)
    spacing_rows=[r for r in rows if r['bracket_spacing_exceeds_one_hour']]
    epoch_differences=[]
    for event in meta['original_candidate_order']:
        er=[r for r in rows if r['event']==event]
        if all(r['nearest_is_unique'] for r in er) and er[0]['nearest_candidates'][0]['GPS_from_filename']!=er[1]['nearest_candidates'][0]['GPS_from_filename']:
            epoch_differences.append(event)
    overview={'request_id':request['request_id'],'status':'HEADER_INVENTORY_COMPLETE_LOCAL_CALIBRATION_VALIDITY_OPEN',
        'archive_summaries':summary,'total_archive_bytes':sum(a['bytes'] for a in summary),
        'total_headers':sum(a['header_count'] for a in summary),'total_regular_files':sum(a['regular_file_count'] for a in summary),
        'associations':len(rows),'unique_nearest_candidates':sum(r['nearest_is_unique'] for r in rows),
        'max_nearest_distance_seconds':str(max(Decimal(r['nearest_distance_seconds']) for r in rows)),
        'bracket_spacing_over_one_hour':[{'event':r['event'],'detector':r['detector'],'spacing_s':r['bracket_spacing_seconds'],'nearest_distance_s':r['nearest_distance_seconds']} for r in spacing_rows],
        'events_with_different_detector_candidate_epochs':epoch_differences,
        'not_inferred':['Actual numerical columns/units','Frequency grid/validity','Coverage between named epochs','C00/C01 compatibility per member','PSD, science, posterior centers or significance'],
        'bytes_accessed_scope':'Compressed archives downloaded and hashed. Gzip traversal discards member bodies; only TAR headers recorded. No member extraction or numeric interpretation.',
        'calibration_archive_inventory_authorized':True,'science_data_opening_authorized':False,'models_called':0,'INIT003_repeated':False,
        'contracts_holds_V1_edited':False,'shared_memories_edited':False,'automatic_download_retries':0}
    write_new('RESUMO_INVENTARIO.json',overview)
    sourcepins=[pin(p) for p in sorted((BASE/'sources_local').glob('*'))]+[pin(BASE/'sources_public/DCC_T2500288_v5.html')]
    write_new('FONTES_E_PINS.json',{'textual_sources':sourcepins,'archives_and_headers':sources,'hashes_calculated_from_bytes':True,
        'member_payload_hashes_calculated':False,'source_page_hash_scope':'Raw HTTP body downloaded in this unit; distinct from previous web-tool excerpt hashes.'})

    report=['# D — inventário documental dos membros de calibração','',
        'Pedido `'+request['request_id']+'` — 06/10/2026. Entrega para revisão ROOT.','',
        '**[REAL — nomes/cabeçalhos]** Foram obtidos uma vez os dois pacotes oficiais e enumerados seus cabeçalhos. Nenhum membro foi extraído; nenhuma linha numérica de calibração foi interpretada. Não houve abertura de strain/PE/posteriors, execução de ciência, nova chamada a modelos ou retry INIT003.','',
        '## Resultado medido','',
        '| Pacote | Bytes comprimidos | Cabeçalhos | Arquivos regulares | H1 | L1 |','|---|---:|---:|---:|---:|---:|']
    for a in summary:
        report.append(f"| {a['archive']} | {a['bytes']} | {a['header_count']} | {a['regular_file_count']} | {a['detectors'][0]['regular_members']} | {a['detectors'][1]['regular_members']} |")
    report+=['',f"Total: **{overview['total_archive_bytes']} bytes**, abaixo de100MiB; cada arquivo abaixo de50MiB. Os **{overview['total_regular_files']}** arquivos regulares seguem o padrão de nome documentado. Os outros quatro membros são diretórios. Não apareceram links ou membros especiais. Os nomes são únicos dentro de cada pacote e as épocas são únicas por detector/run.",'',
        'Os hrefs foram extraídos da [página oficial DCC T2500288-v5](https://dcc.ligo-wa.caltech.edu/LIGO-T2500288/public); tamanho HEAD, GET, arquivo local e ETag foram confrontados. `DISCOVERY.json` e `DOWNLOAD_RECEIPT.json` preservam URLs efetivos e recibos. Os SHA256 são calculados dos arquivos comprimidos locais. Nenhuma URL de pacote foi construída por adivinhação.','',
        '## Identidade dos pacotes','']
    for a in summary:report += [f"- `{a['archive']}`: `{a['sha256']}` — [arquivo publicado]({a['url']})."]
    report+=['','## Associação aos eventos — candidatos, não escolha científica','',
        'Reutilizamos somente o GPS textual do manifesto de metadados já admitido, mantendo sua condição de proposta não ratificada. Não reabrimos catálogos nem refizemos a reconciliação GPS. Para cada run/detector, encontramos a época nominal mais próxima e preservamos os vizinhos. Os nomes completos estão no JSON de associação.','',
        '| Evento | GPS candidato H1 | Distância H1(s) | GPS candidato L1 | Distância L1(s) | Hold anterior |','|---|---:|---:|---:|---:|---|']
    for e in meta['original_candidate_order']:
        bydet={r['detector']:r for r in rows if r['event']==e};h=bydet['H1'];l=bydet['L1']
        def epochs(r):return ', '.join(str(x['GPS_from_filename']) for x in r['nearest_candidates'])
        report.append(f"| {e} | {epochs(h)} | {h['nearest_distance_seconds']} | {epochs(l)} | {l['nearest_distance_seconds']} | {'Preservado' if h['prior_hold_preserved'] else 'Sem hold anterior; não liberado'} |")
    report+=['',f"**[DERIVED — metadados]** Há {overview['unique_nearest_candidates']} candidatos temporais únicos para os28pares. A maior distância nominal é {overview['max_nearest_distance_seconds']}s. Essa proximidade não comprova validade do envelope nem constitui um corte de seleção.",'',
        '## Lacunas temporais observadas nos nomes','',
        'O intervalo abaixo é a diferença entre as épocas de membros imediatamente anterior/posterior ao GPS do evento. Não é duração de dados ruins, lacuna de strain, validade de calibração ou diagnóstico do instrumento. A cadência horária nominal não garante uma grade sem lacunas.','',
        '| Evento | Detector | Espaçamento entre vizinhos(s) | Distância ao mais próximo(s) |','|---|---|---:|---:|']
    for r in spacing_rows:report.append(f"| {r['event']} | {r['detector']} | {r['bracket_spacing_seconds']} | {r['nearest_distance_seconds']} |")
    report+=['', 'Eventos com épocas candidatas H1/L1 diferentes: '+', '.join(epoch_differences)+'. Não impor uma única época aos dois detectores. Um evento exatamente sobre uma época tem espaçamento inclusivo zero no JSON; isso também não prova continuidade ao redor dele.','',
        '## Alcance e alternativas','',
        'Antes da obtenção, foram comparadas duas rotas: índice remoto oficial versus enumeração limitada dos pacotes. A página consultada e as duas buscas oficiais não forneceram um índice de membros; isso não é prova universal de inexistência. A enumeração dos pacotes foi realizada no mandato específico, com limites de stream e recibos sem repetição automática. `PREPARACAO_E_ALTERNATIVAS.md` conserva a comparação anterior ao download.','',
        'A identidade externa ficou concreta: pacote pinado + caminho exato do membro + detector/época extraídos do nome + cabeçalho. **Continuam [OPEN]** colunas, unidades efetivas, grade de frequência, intervalo de validade, correlações, tratamento estatístico e compatibilidade C00/C01 de cada membro. Nada disso foi inferido do nome, diretório ou calendário. Hashes individuais do conteúdo dos membros permanecem nulos; o hash do pacote fixa indiretamente o conjunto de bytes sem interpretar esse conteúdo.','',
        'Para avançar depois desta revisão, há duas alternativas de proveniência: (1) qualificação segregada dos envelopes DCC candidatos, mantendo ciência fechada e definindo o tratamento apenas após examinar suas convenções; (2) inventário autorizado de cabeçalhos PE para vincular o produto ao label exato publicado. A segunda aumenta a proximidade com a proveniência PE, mas exige impedir leitura de posteriors. Nenhuma foi executada ou adotada por este inventário.','',
        '## O que exatamente foi lido','',
        'A transferência e o SHA256 leram os bytes comprimidos. O percurso gzip/TAR necessariamente descomprime e descarta bytes para chegar aos próximos cabeçalhos. O código não chama extract, extractall ou extractfile, não interpreta linhas numéricas e não grava membros separados. A enumeração respeitou também limites adicionais de100000membros/8GiB descomprimidos por pacote. Não afirmar que os bytes comprimidos nunca foram acessados.','',
        'Somente cópias textuais admitidas foram usadas para relacionar eventos. Não tocaram contratos, V1, holds, memórias compartilhadas ou resultados do piloto. CAL_B não foi ratificado e D permanece fechado. O inventário facilita a próxima verificação; não fornece resultado físico, posterior ou significância.','',
        '## Arquivos de revisão','',
        '- `ASSOCIACAO_14_EVENTOS_28_DETECTORES.json`: nomes completos, candidatos, distâncias, vizinhos, pins e campos não observados.',
        '- `LIGO_O4a_cal_uncertainty.tgz.members.json` e `LIGO_O4b_cal_uncertainty.tgz.members.json`: todos os cabeçalhos observados.',
        '- `RESUMO_INVENTARIO.json`, `FONTES_E_PINS.json`, `VALIDACAO_DOCUMENTAL.json`: resultados e limites.',
        '- `MANIFESTO_ENTREGA.json`: identidade por bytes de todos os artefatos da entrega, incluindo pacotes fechados.',
        '- `public_archive_inventory.py` e `build_inventory_delivery.py`: procedimentos auditáveis; não reexecutar fases já iniciadas para repetir downloads.','']
    write_new('NOTA_INVENTARIO_MEMBROS_CALIBRACAO_D.md','\n'.join(report))
    for name in ('ASSOCIACAO_14_EVENTOS_28_DETECTORES.json','RESUMO_INVENTARIO.json','FONTES_E_PINS.json'):
        json.loads((BASE/name).read_bytes());check('output parses '+name,True)
    write_new('VALIDACAO_DOCUMENTAL.json',{'status':'PASS_HEADER_AND_METADATA_ONLY','checks_passed':len(CHECKS),'checks':CHECKS,
        'scope':'Archive transfer integrity, header counts/identity, source pins and name-only metadata association; not calibration contents or scientific validation.'})
    files=[pin(p) for p in sorted(BASE.rglob('*')) if p.is_file() and p.name!='MANIFESTO_ENTREGA.json']
    write_new('MANIFESTO_ENTREGA.json',{'request_id':request['request_id'],'created_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'status':'HEADER_INVENTORY_COMPLETE_WITH_EXPLICIT_SCIENTIFIC_GAPS','files':files,
        'calibration_archive_headers_opened':True,'calibration_numeric_content_interpreted':False,'science_data_opened':False,
        'holds_contracts_V1_modified':False,'CAL_B_ratified':False,'models_called':0,'shared_memories_edited':False})
    print(json.dumps({'status':'COMPLETE_HEADER_INVENTORY_ONLY','checks_passed':len(CHECKS),'manifest_files':len(files),
        'total_headers':overview['total_headers'],'regular_members':overview['total_regular_files'],'candidate_pairs':len(rows),
        'unique_nearest_candidates':overview['unique_nearest_candidates'],'bracket_gaps_over_one_hour':len(spacing_rows),
        'note':pin(BASE/'NOTA_INVENTARIO_MEMBROS_CALIBRACAO_D.md'),'manifest':pin(BASE/'MANIFESTO_ENTREGA.json')},ensure_ascii=False))

if __name__=='__main__':main()
