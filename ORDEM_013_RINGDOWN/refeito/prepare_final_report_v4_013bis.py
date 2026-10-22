"""Build a reviewable final report from completed stage receipts, without new science."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, re, shlex

B = Path(__file__).resolve().parents[1]
R = B.parent
D = R / 'TUNEL/DO_CHATGPT'
LIMIT = 25_000_000
READ_SNAPSHOTS = {}

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for x in iter(lambda:f.read(1048576), b''): h.update(x)
    return h.hexdigest()

def load(p):
    p=Path(p).resolve()
    with p.open('rb') as stream:raw=stream.read(LIMIT+1)
    if len(raw)>LIMIT:raise ValueError('Report input must be compact metadata: '+str(p))
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    def finite(x):
        n=float(x)
        if not math.isfinite(n):raise ValueError('Nonfinite metadata')
        return n
    def invalid(x):raise ValueError('Invalid JSON constant '+x)
    value=json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=invalid)
    READ_SNAPSHOTS[p]=hashlib.sha256(raw).hexdigest()
    return value

def require(value,message):
    if not value:raise ValueError(message)

def artifact_path(name):
    raw=str(name).replace('\\','/')
    if re.match(r'^[A-Za-z]:/',raw):
        prefix='C:/IALD/Central de Patentes/Chatgpt/'
        require(raw.lower().startswith(prefix.lower()),'Reference outside Chatgpt')
        raw=raw[len(prefix):]
    p=Path(raw);p=(p if p.is_absolute() else R/p).resolve()
    require(p.is_relative_to(R.resolve()),'Reference outside Chatgpt')
    require(p.name.lower() not in ('.env','iald_stack_v7.py','iald_psion_state.json')
        and not any('PRIVATE' in s.upper() for s in p.parts),'Private input excluded')
    return p

def pin(p):return dict(path=Path(p).resolve().relative_to(R.resolve()).as_posix(),sha256=sha(p))

def safe(value):return str(value).replace('|','\\|').replace('\n',' ')

def link(p,label=None):return f'[{label or Path(p).name}](<{Path(p).resolve().as_posix()}>)'

def historical_ratio_cell(prediction,ratio):
    """An inherited C4 zero is not a prediction for an undefined reading."""
    if type(prediction) not in (int,float) or not math.isfinite(prediction):return 'OPEN'
    return number(ratio)

def load_b2_costs():
    manifest=load(B/'bis/B2_DELIVERY_MANIFEST.json')
    specs=(
        ('Nulos MC E2','bis/RESULT_E2_NULL_CAMPAIGN.json','wall_seconds',None,
         'Campanha de nulos sintéticos; não calibração física'),
        ('E4/E5 produtor','bis/e4_e5_prepare/runs/authorized_001/RESULT_RECEIPT.json',
         'wall_seconds_through_result_hash','process_CPU_seconds_through_result_hash',
         'Entrada no main até gravação/hash do resultado; exclui gravação do recibo'),
        ('Revisão independente E4/E5','bis/e4_indep_review/runs/authorized_001/INDEPENDENT_REVIEW.json',
         'wall_seconds',None,'Revisão aritmética condicional; não nova ciência'),
        ('Controlador E4/E5','bis/E4_E5_EXECUTION_V1.json','wall_seconds',None,
         'Envelope do lançamento; sobrepõe o tempo do produtor, não somar'))
    rows=[]
    for label,relative,field,cpu_field,scope in specs:
        path=B/relative;entry=manifest['files'][relative]
        require(sha(path)==entry['sha256'] and path.stat().st_size==entry['bytes'],'B2 cost receipt pin differs: '+relative)
        receipt=load(path);seconds=receipt[field];cpu=receipt[cpu_field] if cpu_field else None
        require(type(seconds) in (int,float) and math.isfinite(seconds) and seconds>=0,'Invalid observed wall time')
        require(cpu is None or type(cpu) in (int,float) and math.isfinite(cpu) and cpu>=0,'Invalid observed CPU time')
        rows.append(dict(label=label,path=path,sha256=entry['sha256'],pointer='/'+field,wall_seconds=seconds,
            cpu_seconds=cpu,cpu_pointer='/'+cpu_field if cpu_field else None,scope=scope))
    return rows

def validate_integrity(receipt):
    require(receipt['status']=='PASS_FROZEN_INPUTS_DELIVERED_A_AND_SIZE_LAYOUT','Integrity receipt reports differences')
    require(receipt['oversized_outside_cache']==[],'Unresolved oversized files')
    rows=receipt['checks'];require(isinstance(rows,list) and rows,'Empty integrity checks')
    require(all(x['matches'] is True and x['expected_sha256']==x['actual_sha256']
        and re.fullmatch('[0-9a-f]{64}',x['actual_sha256']) for x in rows),'Integrity rows do not support PASS')
    baseline=B/'bis/INPUT_INTEGRITY_013BIS_retry.json'
    require(sha(baseline)==receipt['baseline_sha256'],'Integrity baseline changed')
    original=load(baseline)
    key=lambda x:str(x).replace('\\','/').casefold()
    for category in ('inputs','sources'):
        expected={(key(x['path']),x['sha256']) for x in original[category]}
        actual=[(key(x['path']),x['actual_sha256']) for x in rows if x['category']==category]
        require(len(actual)==len(expected) and set(actual)==expected,'Integrity inventory coverage differs: '+category)
    delivered=load(B/'bis/M6_MA_DELIVERY_MANIFEST.json')['files']
    expected={(key(p),h) for p,h in delivered.items()}
    actual=[(key(x['path']),x['actual_sha256']) for x in rows if x['category']=='delivered_part_A']
    require(len(actual)==len(expected) and set(actual)==expected,'Part A integrity coverage differs')
    require(isinstance(receipt['metadata_exceptions'],list),'Metadata exceptions must be explicit')
    return {c:sum(x['category']==c for x in rows) for c in ('inputs','sources','delivered_part_A')}

def verify_extra(extra,execution):
    require(extra['status']=='DELIVERED_B3_B4_TEST_B5_HASHES_RECHECKED','Closure status not accepted')
    require(extra['checks'] and all(x['matches'] is True for x in extra['checks']),'Closure contains failed checks')
    result={}
    for name,entry in extra['files'].items():
        p=artifact_path(name);require(re.fullmatch('[0-9a-f]{64}',entry['sha256']),'Invalid extra pin')
        require(p.stat().st_size==entry['bytes'],'Extra size differs: '+name)
        # The final report never opens sample arrays/HDF. Their byte custody was
        # checked by the execution/review/closure, not by this documentary renderer.
        payload=p.suffix.lower() in ('.h5','.hdf5','.gz','.npz','.npy') or p.name.startswith('POSTERIORES_PSEOB_')
        if payload:
            product=execution['products'].get(p.name)
            require(product is not None and product['sha256']==entry['sha256'] and product['bytes']==entry['bytes'],
                'Payload pin lacks exact execution-receipt support: '+name)
            method='EXECUTION_AND_CLOSURE_PIN_SIZE_ONLY_NO_SAMPLE_READ'
        else:
            require(sha(p)==entry['sha256'],'Extra pin mismatch: '+name);method='BYTES_REHASHED'
        result[p]=dict(sha256=entry['sha256'],bytes=entry['bytes'],verification=method)
    return result

def documentary_sections(e6,e6_md,e6_review_path,e7,allocation,execution,integrity,counts,b2_costs):
    readings=e6['readings'];routes=e6['routes'];groups=e6['data_groups']
    require(len(readings)==10 and len(set(readings))==10 and len(routes)==3 and len(groups)==6,'E6 axes differ')
    keys=[(c['route'],c['reading'],c['data_group']) for c in e6['cells']]
    require(len(keys)==180 and set(keys)=={(r,l,g) for r in routes for l in readings for g in groups},'E6 cell coverage differs')
    statutes={}
    for cell in e6['cells']:
        prior=statutes.setdefault(cell['reading'],cell['reading_statute'])
        require(prior==cell['reading_statute'],'Conflicting reading statute')
    lines=['','## Quadro de alcance aprovado — anexo integrante','',
        f'Quadro integral: {link(e6_md)} — SHA256 `{sha(e6_md)}`. '
        f'Revisão documental: {link(e6_review_path)} — `{sha(e6_review_path)}`. '
        'O JSON pareado, também pinado neste relatório, contém unidades, origens e motivos OPEN de cada campo. '
        'Este anexo integra o relatório; não foi recalculado pelo gerador.','',
        'Grupos: '+', '.join(groups)+'. Todas as dez leituras, sem seleção. '
        'As contagens abaixo descrevem cobertura documental, não eventos científicos ou poder.','',
        '| Rota | Células | Cenários já produzidos | Unidade da informação-alvo | Estado do TESTE |',
        '|---|---:|---:|---|---|']
    units={'TAU220_POPULATION':'Σ1/σ²(dtau220)','TAU440_FIXED_SOURCE_FISHER':'Σ1/σ²(dtau440), fonte fixa',
        'DF220_POPULATION_WIDTH_IV':'informação local da variância df220; pesos 1/σ⁴'}
    for route in routes:
        cells=[c for c in e6['cells'] if c['route']==route]
        tests=[s for c in cells for s in c['scenarios'] if s['id'].startswith('TEST:')]
        require(len(tests)==60 and all(s['verdict']=='AWAITING_DATA' and s['physical_test_present'] is False for s in tests),'Unexpected TEST state')
        lines.append(f'| {route} | {len(cells)} | {sum(len(c["scenarios"]) for c in cells)} | {units[route]} | AWAITING_DATA; físico null |')
    lines+=['','O anexo preserva z esperado **condicional**, N90 em informação, equivalentes GW250114 do canal próprio, '
        'IC de taxa e correção/σ por cenário. Fisher440 não paga PE multimodo; IV permanece limite inferior enquanto transferência/σsys estão OPEN. '
        'Taxas e bandas O5/ET/CE não são promessa de data.','',
        '## Leituras e variantes E7 — estados efetivos','',
        '| Leitura | Estatuto C1/E6 | Variante | Veredito | Dados/modos | Alvo | Motivo físico OPEN |',
        '|---|---|---|---|---|---|---|']
    rows=e7['matrix']
    require(len(rows)==20 and {(x['reading'],x['mode_variant']) for x in rows}==
        {(r,m) for r in readings for m in ('220_only','220_plus_440_INPUT')},'E7 matrix coverage differs')
    require(e7['test_events_added']==0,'This final wall report requires absent test data')
    for row in rows:
        require(row['statute']==statutes[row['reading']],'E7/C1 statute differs')
        require(row['verdict']=='AWAITING_DATA' and all(row[n] is None for n in ('lnB','z_physical','correction_over_sigma_physical')),'Unexpected physical result')
        lines.append('| '+' | '.join(safe(x) for x in (row['reading'],row['statute'],row['mode_variant'],row['verdict'],
            row['mode_data_status'],row['target_status'],row['reason']))+' |')
    lines+=['','OPEN por leitura nos diagnósticos condicionais (copiado de estados/motivos; sem ler amostras):','']
    for reading in readings:
        diagnostic=e7['conditional_readings'][reading]
        reasons=sorted({str(x.get('reason',x['status'])) for x in diagnostic['events'] if x['status']=='OPEN'})
        reasons.append(diagnostic['mode_440']['status']+': '+diagnostic['mode_440']['reason'])
        lines.append('- '+reading+' ['+statutes[reading]+']: '+safe('; '.join(reasons)))
    lines+=['','## Custos observados por campanha — não somar ao ledger contínuo','',
        'Transcrição dos recibos/orçamento. CPU de filhos, soma de paredes de filhos e intervalo controlador têm escopos diferentes. '
        'Nenhuma destas linhas é acrescentada ao contador contínuo. Outros trabalhos não itemizados permanecem incluídos nele; não se inventa custo isolado.','',
        '| Item / origem e ponteiro | Parede ou intervalo (s) | CPU (s) | Escopo |','|---|---:|---:|---|']
    for x in b2_costs:
        origin=x['label']+' — '+link(x['path'])+' `'+x['pointer']+'`; SHA256 `'+x['sha256']+'`'
        cpu='OPEN' if x['cpu_seconds'] is None else format(x['cpu_seconds'],'.9f')+' `'+x['cpu_pointer']+'`'
        lines.append('| '+' | '.join((origin,format(x['wall_seconds'],'.9f'),cpu,safe(x['scope'])))+' |')
    costs=allocation['measured_costs']
    for key in ('Kerr_V1','Kerr_V2'):
        x=costs[key];lines.append(f'| /measured_costs/{key} | {number(x["wall_seconds"])} | {number(x["children_cpu_seconds"])} | {safe(x["cost_scope"])} |')
    x=costs['Kerr_Welch_separate_diagnostic']
    lines.append(f'| /measured_costs/Kerr_Welch_separate_diagnostic | {number(x["wall_seconds_through_checks"])} | {number(x["process_cpu_seconds_through_checks"])} | {safe(x["cost_scope"])} |')
    x=costs['IMR_pilot_failed_controller']
    lines.append(f'| /measured_costs/IMR_pilot_failed_controller | {number(x["wall_seconds"])} | usuário {number(x["children_user_cpu_seconds"])}; sistema {number(x["children_system_cpu_seconds"])} | Tentativa falha; não custo por posterior |')
    x=costs['IMR_native_diagnostic']
    lines.append(f'| /measured_costs/IMR_native_diagnostic | soma filhos {number(x["sum_child_wall_seconds"])}; plano→último fim {number(x["plan_to_last_child_finish_seconds"])} | soma filhos {number(x["sum_child_CPU_seconds"])} | Medidas sobrepostas; não somar entre si |')
    lines.append(f'| E7_FINAL_EXECUTION_V1 /wall_seconds | {number(execution["wall_seconds"])} | OPEN | Extração/consumo documental de calibração existente; sem PE nova |')
    lines+=['','| Alternativa não paga | Custo estimado qualificado (s) | Alocação nova (s) | Motivo |','|---|---:|---:|---|']
    for x in allocation['alternatives']:
        lines.append('| '+' | '.join(safe(v) for v in (x['id']+' — '+x['description'],number(x['estimated_wall_seconds_for_qualified_program']),
            number(x['allocated_wall_seconds']),x['reason']))+' |')
    lines+=['',f'Custo por posterior IMR convergido: {number(allocation["cost_per_converged_IMR_posterior_seconds"])}. '
        'Zero alocado não é custo estimado zero. Os tempos B2 acima foram copiados dos campos dos recibos pinados, '
        'não dos arredondamentos da nota nem inferidos por diferença. O controlador E4/E5 engloba o produtor: não somar suas durações.','',
        '## Integridade efetivamente conferida no recibo','',
        f'Recibo em `{integrity["measured_utc"]}`: inventário com {counts["inputs"]} insumos, {counts["sources"]} fontes '
        f'e {counts["delivered_part_A"]} artefatos entregues da Parte A; cobertura e pares de hashes conferidos pelo gerador. '
        'Não é uma nova auditoria de outras casas nem varredura de segredos. O conteúdo do cache não foi varrido pelo recibo; '
        'o gerador não abre JSON de amostras ou HDF. Pins desses payloads são transportados do recibo E7 e closure, com tamanho conferido.','',
        'Exceções de metadados registradas (não ocultadas pelo status PASS):']
    lines += ['- '+safe(json.dumps(x,ensure_ascii=False)) for x in integrity['metadata_exceptions']] or ['- Nenhuma exceção registrada.']
    return lines,statutes
def number(x): return 'OPEN' if x is None else format(x, '.6g')
def new(p, raw):
    if isinstance(raw,str): raw=raw.encode()
    require(len(raw)<=LIMIT,'Report artifact exceeds 25 MB')
    tmp=p.with_name(p.name+'.pending')
    with tmp.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.stat().st_size!=len(raw): raise OSError('Short staged write')
    os.link(tmp,p); tmp.unlink()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--e6-result',type=Path,required=True)
    ap.add_argument('--e7-review',type=Path,required=True)
    ap.add_argument('--integrity-receipt',type=Path,required=True)
    ap.add_argument('--extra-manifest',type=Path,required=True)
    ap.add_argument('--e6-review',type=Path,default=B/'bis/e6_actual_review/E6_ACTUAL_RESULT_REVIEW_002.json',
                    help='Independent review binding E6 JSON and markdown (default: approved review 002)')
    ap.add_argument('--output-dir',type=Path,default=B/'bis/final_report_v4_001',help='Successor draft directory; default bis/final_report_v4_001, no replay required')
    ap.add_argument('--replay',action='store_true',help='Documentary replay only, requires a fresh isolated output directory; no budget activation/publication')
    a=ap.parse_args()
    for name in ('e6_result','e7_review','integrity_receipt','extra_manifest','e6_review'):
        setattr(a,name,artifact_path(getattr(a,name)))
    output=a.output_dir.resolve()
    require(output.is_relative_to(B.resolve()),'Output must remain in the work package')
    if a.replay:require(output!=(B/'bis').resolve() and not output.exists(),'Replay requires new isolated output directory')
    for name in ('FINAL_REVIEW_DRAFT.md','FINAL_REVIEW_DRAFT_MANIFEST.json'):
        p=output/name
        require(not p.exists() and not p.with_name(p.name+'.pending').exists(),'Preserve existing draft/manifest')
    e7=load(B/'bis/E7_FULLSAMPLE_RESULT_V1.json')
    execution=load(B/'bis/E7_FINAL_EXECUTION_V1.json')
    review=load(a.e7_review)
    if execution['failure'] is not None or review.get('approved') is not True:
        raise ValueError('E7 must pass before final drafting')
    if review.get('e7_result_sha256')!=sha(B/'bis/E7_FULLSAMPLE_RESULT_V1.json'):
        raise ValueError('E7 independent review does not bind result')
    require(not review.get('blocking_findings',[]),'E7 review has blockers')
    require(execution['products']['E7_FULLSAMPLE_RESULT_V1.json']['sha256']==sha(B/'bis/E7_FULLSAMPLE_RESULT_V1.json')
        and all(x['returncode']==0 and x['error'] is None for x in execution['commands']),'E7 execution/result differs')
    e6=load(a.e6_result); e0=load(B/'PORTAO_DA_AMPLIACAO_V1.json')
    e6_review=load(a.e6_review)
    require(e6_review['approved'] is True and e6_review['blocking_findings']==[] and e6_review['all_checks'] is True
        and e6_review['failed_checks']==[] and e6_review['e6_result_sha256']==sha(a.e6_result),'E6 review not bound/accepted')
    b5_review_path=B/'bis/e6_actual_review/B5_ACTUAL_DELIVERY_REVIEW.json'
    b5_review=load(b5_review_path)
    require(b5_review['approved'] is True and b5_review['blocking_findings']==[]
        and b5_review['delivery_sha256']==sha(D/'ENTREGA_013BIS_B5_quadro_e_modulo.md')
        and b5_review['manifest_sha256']==sha(B/'bis/B5_DELIVERY_MANIFEST.json')
        and b5_review['e6_review_sha256']==sha(a.e6_review)
        and b5_review['e7_review_sha256']==sha(a.e7_review),'B5 review does not bind current delivery/reviews')
    e6_md=a.e6_result.with_suffix('.md')
    reviewed_pins={artifact_path(k):v for k,v in e6_review['verified_input_hashes'].items()}
    require(reviewed_pins.get(e6_md)==sha(e6_md),'E6 markdown not bound by accepted review')
    for ref in e6['source_pins'].values():
        if ref['path'].endswith('C1_LEITURAS_v4.json'):
            require(sha(artifact_path(ref['path']))==ref['sha256'],'C1 source changed')
    integrity=load(a.integrity_receipt);integrity_counts=validate_integrity(integrity)
    allocation=load(B/'ORCAMENTO_40H.json')
    extra=load(a.extra_manifest);extra_files=verify_extra(extra,execution)
    b2_costs=load_b2_costs()
    extra_lines,reading_statutes=documentary_sections(e6,e6_md,a.e6_review,e7,allocation,execution,integrity,integrity_counts,b2_costs)
    budget=load(B/'bis/PART_B_BUDGET_START.json')
    native=load(B/'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json')
    if native['status']!='BOUNDED_DIAGNOSIS_CLOSED_TECHNICAL_WALL_NO_SUPPORTED_PE_ADAPTER':
        raise ValueError('Technical wall not reviewed')
    expected_notes=['ENTREGA_013BIS_ABERTURA_operador.md','ENTREGA_013BIS_MA_fechamento.md',
        'ENTREGA_013_M1_fechamento.md','ENTREGA_013_M2_C4_fechamento.md','ENTREGA_013_M3_C3_2_C2_RMOD.md',
        'ENTREGA_013_M4_C5_parede_e_portao.md','ENTREGA_013_M5_C6pre.md','ENTREGA_013_M6_C7_final.md',
        'ENTREGA_013_ERRATA_contrato.md','ENTREGA_013BIS_B1_portao_e_nuisance.md',
        'ENTREGA_013BIS_E2_REGISTRO_V1.md','ENTREGA_013BIS_B2_registro_e_440.md',
        'ENTREGA_013BIS_B3_piloto_e_orcamento.md','ENTREGA_013BIS_B4_calibracao_e_cegos.md',
        'ENTREGA_013BIS_TESTE_O4_cegos.md','ENTREGA_013BIS_B5_quadro_e_modulo.md']
    paths=[D/n for n in expected_notes]+[a.e6_result,e6_md,a.e6_review,a.e7_review,a.integrity_receipt,a.extra_manifest,
        b5_review_path,B/'bis/B5_DELIVERY_MANIFEST.json',
        B/'ORCAMENTO_40H.json',B/'RINGDOWN_5SIGMA_V1.json',B/'NUISANCE_V1.json',
        B/'PORTAO_DA_AMPLIACAO_V1.json',B/'bis/E7_FULLSAMPLE_RESULT_V1.json',
        B/'bis/E7_FINAL_EXECUTION_V1.json',B/'bis/e3_pilot_review/PILOT_NATIVE_DIAGNOSIS_CLOSING_REVIEW.json',
        B/'bis/e3_pilot_failure_diagnostic/MANIFEST.json',
        B/'bis/e3_pyring_review/KERR_V2_POST_RESULT_REVIEW.json',
        B/'bis/M6_MA_DELIVERY_MANIFEST.json',B/'bis/B2_DELIVERY_MANIFEST.json',
        B/'bis/PART_B_BUDGET_START.json',B/'bis/B1_DELIVERY_MANIFEST.json',
        B/'bis/E3_WALL_BUDGET_ACTIVATION_V1.json',B/'bis/INPUT_INTEGRITY_013BIS_retry.json',
        B/'C1_LEITURAS_v4.json',Path(__file__).resolve(),
        B/'refeito/REAPROVEITAMENTO_FINAL_REPORT_V4.md',B/'refeito/FINAL_REPORT_V4_IMPLEMENTATION_MANIFEST.json',
        B/'bis/e3_budget_wall_review/SYMLINK_CLASSIFICATION.json']
    paths += [x['path'] for x in b2_costs]
    paths=list(dict.fromkeys(p.resolve() for p in paths))
    if any(not p.is_relative_to(R) for p in paths): raise ValueError('Output reference outside Chatgpt')
    files={p.relative_to(R).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size,verification='BYTES_REHASHED') for p in paths}
    for p,entry in extra_files.items():
        name=p.relative_to(R).as_posix()
        require(name not in files or files[name]['sha256']==entry['sha256'],'Closure/direct pin conflict')
        files[name]=entry
    now=datetime.now(timezone.utc)
    elapsed=(now-datetime.fromisoformat(budget['started_utc'])).total_seconds()/3600
    if not a.replay and (not 0<=elapsed<40 or now>=datetime.fromisoformat(allocation['wall_accounting']['finalization_stop_utc'])):
        raise TimeoutError('Allocated budget envelope expired')
    opening=sha(D/expected_notes[0])
    boundaries=[('E0/E1, preparo e revisão B1', load(B/'bis/B1_DELIVERY_MANIFEST.json')['utc']),
        ('E2/E4/E5, registro e revisão B2',load(B/'bis/B2_DELIVERY_MANIFEST.json')['created_utc']),
        ('E3.1/E3.2, Kerr, piloto, diagnóstico e orçamento',load(B/'bis/E3_WALL_BUDGET_ACTIVATION_V1.json')['finished_utc']),
        ('Paredes E3.3/TEST, E6/E7 e integração final',now.isoformat())]
    wall_ledger=[]; previous=datetime.fromisoformat(budget['started_utc'])
    for label, stamp in boundaries:
        finish=datetime.fromisoformat(stamp)
        if finish<previous:raise ValueError('Nonmonotonic delivered-stage accounting')
        wall_ledger.append(dict(item=label,started_utc=previous.isoformat(),finished_utc=finish.isoformat(),
            continuous_wall_hours=(finish-previous).total_seconds()/3600))
        previous=finish
    lines=['[REAL — relatório final da bancada; encerramento por resultados e paredes medidas. Calibração física e teste cego NÃO PAGOS.]','',
        '# ORDEM 013BIS — relatório final','',
        'O trabalho entrega o registro, os resultados condicionais, o quadro de alcance e o módulo de leitura. '
        'Não produziu um novo posterior pSEOB válido nem demonstrou 5σ físico. O piloto IMR terminou em falha nativa; '
        'a revisão do diagnóstico não encontrou um reparo validado que preservasse a região de parâmetros registrada. '
        'Por isso a ampliação por PE foi encerrada como parede técnica nesta configuração, e não como falta de tempo ou impossibilidade geral da rota.','',
        f'Abertura do operador: `{opening}`. Os recibos encadeiam as etapas realizadas pela bancada até este relatório. '
        'A incorporação no programa canônico e a ratificação continuam com a gerência/operador.','',
        '## Cumprimento por alvo','',
        '| Alvo | PAGO | NÃO PAGO / limite |','|---|---|---|',
        '| F0 | Encerramento conferido dos trabalhos antigos antes do piloto; recibo próprio. | Seus resultados não entram para mudar vereditos. |',
        '| F1 | Entrega M1, correções e portão medido. | Não promove diagnóstico em prova física. |',
        '| F2 | Entrega M2, catálogos, controles e correções ao lado. | C4 permanece INCONCLUSIVE_SYSTEMATICS, NÃO-CEGA. |',
        '| F3 | Entrega M3, template/oráculo e leituras com escopo. | Pontes/identificações abertas não são escolhidas. |',
        '| F4 | Entrega M4, parede C5 e portão do poder. | Calibração livre de massa/spin da C5. |',
        '| F5 | Entrega M5, C6 reclassificada e inícios realizados. | C6 permanece diagnóstico anterior ao portão. |',
        '| F6 | Entrega M6, pacote e reproduções documentadas. | Não converte entrega em evidência física. |',
        '| F7 | Fichas, licenças documentais, arquivos grandes em cache e conferência de integridade. | Custódia/publicação externa não realizadas. |',
        '| F8 | Parte A fechada por resultado/falsificador/parede; MA entregue. | Paredes físicas explicitadas. |',
        '| E0 | Portão refeito, dez leituras, alvos em informação e cenários. | N90 condicionado não garante poder com sistemática real. |',
        '| E1 | Nuisance condicional, seleção documentada e controles existentes. | Eficiência de seleção, normalização e covariância físicas. |',
        '| E2 | Registro com testemunha, hashes, guardas e nulos sintéticos. | Cauda física da pipeline e autorização estatística de descegamento. |',
        '| E3.1 | Comparação Kerr e custo da tentativa IMR; diagnóstico independente. | Reprodução exatamente equivalente do pyRing; posterior pSEOB convergido e custo por evento válido. |',
        '| E3.2 | Orçamento registrado, cinco alternativas, pesos esperados e custo observado separados. | Custo calibrado por posterior/injeção e ganho por hora desconhecidos. |',
        '| E3.3 | Parede, alocação sem novos jobs e estado do gate registrados. | Novas injeções RG/TGL, c(SNR), sigma_sys, cobertura e PE cega. |',
        '| E4 | Fisher440 condicionado, sensibilidade 2D e leituras/modos separados. | Comparação de PE multimodo equivalente e lnB físico normalizado. |',
        '| E5 | Nulo LRT sintético e informação 1/sigma^4. | Transferência browniana na recuperação e sigma_sys físicos. |',
        '| TESTE | Parede/estado AWAITING_DATA registrado sob E2. | TESTE observacional não executado; nenhum evento novo admitido ou descego. |',
        '| E6 | Quadro gerado por script com origens e revisão. | Projeções futuras não são observações nem promessa de datas. |',
        '| E7 | Extrator e consumidor congelados, amostras pareadas completas e revisão. | Likelihood restrita normalizada, seleção e teste físico não implementados/pagos. |','',
        '## O portão e as dez leituras','',
        'Bases distintas nas colunas: delta e piso são a referência GW250114 sob cada leitura, com seu estatuto C1/E6; '
        'N90/informação-alvo e correção/sigma são populacionais, GWTC5_31, com a mistura de precisões preservada. '
        'N90 abaixo é o cenário de média gaussiana sem sistemática, não um N garantido para a análise física. '
        'O piso é |delta|/5; |delta|/15 permanece sensibilidade. Sigma(c) físico é OPEN em todas as leituras. '
        'Na leitura INPUT R-GLOBAL o efeito local é zero por construção; zero não é um piso positivo atendido. '
        'Cada estatuto de leitura permanece no quadro completo, sem promoção de INPUT a medição. '
        'Correção/sigma é diagnóstico condicional, nunca significância física com gate vermelho.','',
        '| Leitura / estatuto | delta de referência | Piso primário INPUT | N90 mistura (arredondado acima) | Informação-alvo N90 | Correção/sigma condicional dos31 | Estado do teste novo |',
        '|---|---:|---:|---:|---:|---:|---|']
    targets={r['reading']:r for r in e0['planning_targets'] if r['population']=='GWTC5_31'}
    old={r['reading']:r for r in e0['inherited_C4_nonblind'] if r['dataset']=='GWTC5_31'}
    for row in e0['systematic_conditions']:
        t=targets[row['reading']]; n=t['N90_mixture_illustration_not_selection']
        lines.append('| '+ ' | '.join([row['reading']+' ['+reading_statutes[row['reading']]+']',number(row['delta_GW250114']),number(row['floor5_INPUT']),
            'OPEN' if n is None else str(math.ceil(n)),number(t['I_tau_expected_target90']),
            historical_ratio_cell(row['delta_GW250114'],old[row['reading']]['correction_over_sigma']),'AWAITING_DATA; gate vermelho'])+' |')
    lines+=['','Onde a predição de referência não é numérica, correção/σ fica OPEN. '
        'Os zeros herdados da C4 para R-PROP e R-RAIZ-COHERENT são marcadores históricos, não predições físicas nulas. '
        'O zero numérico de R-GLOBAL, sob sua partição INPUT, é preservado como zero por construção; não paga um piso positivo.']
    lines+=['','Todas as leituras foram preservadas; nenhuma partição, relógio, deformação440 ou realização estocástica foi escolhida. '
        'A RG é o limite clássico/controle. Os escores históricos da C4 ficam nas entregas M2/B1, com seu escopo220 condicional e o veto da cláusula relativa.','',
        '## Resultados que não se confundem','',
        'O controle Kerr do evento conhecido convergiu nos critérios registrados para a variante com PSD pública. '
        'A diferença contra o posterior publicado é descritiva, com famílias/configurações e equivalência incompleta explicitadas em B3. '
        'A variante Welch foi recusada por condicionamento; o primeiro resultado com PSD pública parou parcial. Ambos foram preservados.','',
        'O piloto IMR sofreu SIGSEGV antes de produzir posterior aceito. No diagnóstico isolado, aumentar a frequência de geração '
        'produziu também um aborto de alocação de memória num ponto do prior. A hipótese de capacidade do buffer é CONJECTURE; '
        'a causa exata do SIGSEGV original continua OPEN. Recusar numericamente pontos do prior, remover modos ou estreitar priors '
        'não foi tratado como reparo científico.','',
        'Os nulos sintéticos, o Fisher440 e as razões de densidade foram medidos e revisados. '
        'A cauda t5 excede muito a referência gaussiana5σ; zero excedências em uma simulação finita é apenas um limite superior de probabilidade. '
        'O modo440 não é observação independente do220 no mesmo evento. A rotaIV mantém a dependência da realização estocástica e da transferência ainda aberta.','',
        'As candidatas foram classificadas por metadados anteriores à PE: 14 sem publicação encontrada no escopo, dez sem hold e quatro com hold. '
        'Os pesos esperados são projeções do ajuste em SNR; nenhum desses pesos é informação observada de uma PE nova. '
        'Na execução desta bancada registrada nos recibos, não houve download de strain novo para teste, posterior novo de teste ou descegamento.','',
        f'E7 processou {e7["calibration_events"]} produtos de calibração. O consumidor devolveu {len(e7["matrix"])} linhas '
        '(dez leituras × duas variantes de modos), sem eventos de teste acrescentados. z físico, lnB físico e correção/sigma física permanecem null.','',
        '## Custo e itens não pagos','',
        f'Contador conservador contínuo até a emissão deste documento: {elapsed:.6f}h desde o início; saldo nominal {max(0,40-elapsed):.6f}h de40. '
        f'Início `{budget["started_utc"]}`; deadline inalterado `{budget["hard_deadline_utc"]}`. '
        'Orquestração e revisão contam; trabalhos simultâneos não são somados em dobro. O contador final da publicação será atualizado no recibo final.','',
        'Os custos medidos de cada campanha e da tentativa falha estão no orçamento/B3; 11 segundos até um crash não são custo por evento convergido. '
        'As contagens necessárias para calibrar os pisos e as cinco alternativas estão explicitadas, com custo em horas OPEN quando falta medição válida. '
        'Saldo não utilizado não significa que a condição sistemática foi satisfeita. Não se gastou o restante repetindo uma pipeline inválida.','',
        '## Reprodução, incidentes e custódia','',
        'As entregas intermediárias contêm os comandos e fichas por alvo; a ficha própria e o comando documental estão abaixo. Execuções recusam destinos existentes: '
        'reprodução exige cópia isolada e novo registro quando altera o instrumento. O extrator usa h5py no runtime pinado; '
        'o consumidor usa NumPy, valida os hashes e preserva amostras completas. N/A — sem Lean; nenhum teorema/gate formal movido.','',
        'Foram conservados os abortos, resultados parciais, correções documentais de hashes, revisões recusadas e versões substituídas. '
        'A custódia da semente é procedural no mesmo host; não representa separação de administradores. '
        'A bancada declara não ter divulgado conteúdo de semente ou offset em seus artefatos desta ordem; isto não é auditoria global do host. '
        'O detalhamento das tentativas de selagem, permissões e do código de preparação permanece em B2/B3/B5 e nos manifestos.','',
        'A conferência final dos insumos/fontes/ParteA está no recibo de integridade: qualquer exceção de leitura de metadados é explícita. '
        'No escopo declarado desta bancada, as escritas foram limitadas à pasta Chatgpt; os pares de hashes e a cobertura do recibo de integridade foram validados antes da emissão. '
        'Não se executou commit/push/publicação nesta ordem; essa declaração não equivale a auditar ações de outras sessões. '
        'O pacote da bancada aguarda auditoria externa da gerência e ratificação do operador, como determina a ordem.','',
        ]
    lines+=extra_lines
    replay_dir=B/'bis'/('final_report_replay_'+now.strftime('%Y%m%dT%H%M%SZ'))
    command=['python','-B',str(Path(__file__).resolve()),'--e6-result',str(a.e6_result),'--e7-review',str(a.e7_review),
        '--integrity-receipt',str(a.integrity_receipt),'--extra-manifest',str(a.extra_manifest),
        '--e6-review',str(a.e6_review),'--output-dir',str(replay_dir),'--replay']
    quote=(lambda s:"'"+s.replace("'","''")+"'") if os.name=='nt' else shlex.quote
    replay_command=' '.join(quote(x) for x in command)
    if os.name=='nt':replay_command='& '+replay_command
    lines+=['','## Reprodução documental isolada','',
        'Executar no mesmo ambiente Python do comando abaixo. Não executa ciência, não publica no túnel e não abre arrays de posterior/HDF. '
        'Requer novo destino; o horário do replay será novo e não é reprodução byte a byte nem consumo científico adicional. '
        'O replay não reabre o orçamento e não substitui o draft aprovado.','',
        '```'+('powershell' if os.name=='nt' else 'sh'),replay_command,'```','',
        'Ficha: '+link(B/'refeito/REAPROVEITAMENTO_FINAL_REPORT_V4.md')+'; SHA256 `'+sha(B/'refeito/REAPROVEITAMENTO_FINAL_REPORT_V4.md')+'`.','',
        '## Arquivos, hashes e portas de auditoria','']
    for name,entry in files.items():
        lines.append(f'- [{name}](<{(R/name).as_posix()}>) — `{entry["sha256"]}` ({entry["bytes"]} B).')
    lines+=['','## Contabilidade contínua por etapa','',
        'Intervalos não sobrepostos entre recibos, incluindo revisão e orquestração. Não são CPU-h nem duração isolada do algoritmo. '
        'Os custos de campanhas dentro desses intervalos estão nas entregas; somá-los outra vez duplicaria consumo. '
        'Em E3.3 e TEST, novas execuções científicas tiveram duração0 porque não foram lançadas; documentação continua consumindo parede.','',
        '| Etapa | Início UTC | Fim UTC | Parede h |','|---|---|---|---:|']
    for row in wall_ledger:
        lines.append(f'| {row["item"]} | {row["started_utc"]} | {row["finished_utc"]} | {row["continuous_wall_hours"]:.6f} |')
    if a.replay:
        lines[0]='[REAL — replay documental em destino isolado; não é nova entrega final nem autorização de ciência.]'
        lines.insert(2,'REPLAY: os intervalos até este instante são informação temporal do replay, não novo débito/autorização das 40 h originais.')
    for p,digest in READ_SNAPSHOTS.items():require(sha(p)==digest,'Metadata changed during rendering: '+str(p))
    for name,entry in files.items():
        p=artifact_path(name)
        if entry['verification']=='BYTES_REHASHED':require(sha(p)==entry['sha256'],'Artifact changed during rendering: '+name)
        else:require(p.stat().st_size==entry['bytes'],'Payload size changed')
    output.mkdir(parents=True,exist_ok=not a.replay)
    draft=output/'FINAL_REVIEW_DRAFT.md'
    new(draft,'\n'.join(lines)+'\n')
    manifest=dict(status='DRAFT_FOR_INDEPENDENT_FINAL_REVIEW',created_utc=now.isoformat(),
        draft_sha256=sha(draft),files=files,elapsed_wall_hours=elapsed,opening_sha256=opening,
        wall_ledger=wall_ledger,script_sha256=sha(Path(__file__)),replay=a.replay,
        integrity_validation=dict(counts=integrity_counts,metadata_exceptions=integrity['metadata_exceptions']),
        no_scientific_computation=True,no_sample_arrays_read=True,E6_rerun=False)
    out=output/'FINAL_REVIEW_DRAFT_MANIFEST.json'
    new(out,json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(draft=str(draft),sha256=sha(draft),manifest_sha256=sha(out))))

if __name__=='__main__':main()
