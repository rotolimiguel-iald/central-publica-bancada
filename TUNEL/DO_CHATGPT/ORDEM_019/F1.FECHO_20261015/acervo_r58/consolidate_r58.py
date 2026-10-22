"""Verify source bytes, consolidate documentary reuse, and register a scoped survey."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess
import sys
import survey_r58 as s

REPORTS = ['dispositivos/SURVEY_DISPOSITIVOS_R58.json',
           'rede/REDE_CONTINUO_REPORT_R1.json',
           'gravidade/GRAVIDADE_H3_COMPLETUDE_INVENTORY_R58.json']

def pin(p):
    return {k:v for k,v in s.pin(p).items() if k in ('path','sha256')}

def prepare():
    unique={}; rows=[]; references=[]
    for name in REPORTS:
        p=s.ROOT/name;d=json.loads(p.read_text(encoding='utf-8'))
        references.append(pin(p))
        for k,x in d['sources'].items():
            path=x['path']; expected=x['sha256']
            if path in unique:
                assert unique[path]['sha256']==expected, path
            else:
                actual=s.pin(path)
                assert actual['sha256']==expected,path
                unique[path]=actual
        for finding in d['findings']:
            rows.append({'area':name.split('/')[0],'report':pin(p),'finding':finding,
                         'source_definitions':'See sources in the pinned area report.'})
    s.new('SOURCE_INTEGRITY_R58.json',{'status':'PASS_BYTES','unique_source_paths':len(unique),
        'sources':list(unique.values()),'reports':references,'finding_count':len(rows),
        'scope':'Bytes and provenance verified. This is not recompilation or reproof of every mathematical claim.'})
    s.new('MATRIZ_DE_REAPROVEITAMENTO_R58.json',{'schema':'iald.reuse.survey.v1',
        'unit':'F1.FECHO_20261015','reference':str(s.REF),'report':pin(s.ROOT/'APANHADO_GERAL_R58.txt'),
        'canonical_baseline':pin(s.ROOT/'CANONICAL_BASELINE_R58.json'),
        'findings':rows,'open_mission_requirements':['R4','R5','R3','R10'],
        'next_step':'Compare already-written pair/quadrature observables and their covariance to the same OH preparation and the existing continuous realizations; prove identifications before consumers.',
        'full_mission_satisfied':False,'new_scientific_builds':0,'new_provider_calls':0})
    s.new('PRECISAO_DE_ESCOPO_R58.txt',
        'Em nome de codex-gerente-tgl: a referência ampla a Ward/renormalização na seção4C não declara ausentes a identidade clássica de gauge, Bianchi ou a naturalidade curva. Essas construções já existem, como registra G09/G10 do inventário gravidade. A pendência de alcance ampliado é a construção quântica/interagente que não pode ser obtida por homonímia de certificados. Nenhum teorema de alcance menor é invalidado por isso.\n')
    print(json.dumps({'sources':len(unique),'findings':len(rows)}))

def run_once(label,args):
    s.new(label+'_INTENT.json',{'command':args,'utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp=subprocess.run(args,capture_output=True,encoding='utf-8')
    p=s.new(label+'_RESULT.json',{'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode:raise RuntimeError(str(p))
    print(cp.stdout[:1200]);return p

def finish():
    m=s.cli('mission_cli.py',{'operation':'project','reference':str(s.REF),'max_chars':400000},'DELIVERY_PROJECT')
    t=next(t for t in m['projection']['active'] if t['id']=='R5')
    s.cli('mission_cli.py',{'operation':'check','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':m['receipt']['revision'],'projection_sha256':m['projection_sha256'],
        'task_id':'R5','lease_id':t['lease']['id']},'DELIVERY_PREFLIGHT')
    review=json.loads((s.ROOT/'REVIEW_REPORT_R58.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS')
    assert review['report']==pin(s.ROOT/'APANHADO_GERAL_R58.txt')
    assert review['reviewer']!=s.ACTOR['id']
    files=['APANHADO_GERAL_R58.txt','MATRIZ_DE_REAPROVEITAMENTO_R58.json',
        'PRECISAO_DE_ESCOPO_R58.txt','SOURCE_INTEGRITY_R58.json','CANONICAL_BASELINE_R58.json',
        'INVENTORY_RESULT.json','CORPUS_SEARCH_RESULT.json','CURRENT_SEARCH_RESULT.json',
        'REVIEW_REPORT_R58.json','MEMORY_APPLIED_R58.json','MEMORY_REVIEW_R58.json',*REPORTS]
    evidence=[pin(s.ROOT/n) for n in files]
    source=json.loads((s.ROOT/'SOURCE_INTEGRITY_R58.json').read_text(encoding='utf-8'))
    current=json.loads((s.ROOT/'CURRENT_SEARCH_RESULT.json').read_text(encoding='utf-8'))
    delivery=s.new('DELIVERY_CONSOLIDATED_R58.json',{'status':'SURVEY_DELIVERED_WITH_SCOPE',
        'unit':'F1.FECHO_20261015','claim':939,'author':s.ACTOR['id'],
        'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reference':pin(s.REF),'evidence':evidence,
        'findings':source['finding_count'],'unique_sources_verified':source['unique_source_paths'],
        'current_search_counts':current['counts'],'scientific_builds':0,'provider_calls':0,
        'full_R4_satisfied':False,'full_R5_satisfied':False,'gate_changed':False,
        'conclusion':'Existing receivers, phase reading, pair states, Hadamard/067/073, Fock/Takesaki/Maxwell and curved Einstein recovered. Remaining work is explicit physical/model correspondence and universal-H3 scope, not reconstruction of all ingredients.'})
    entry=s.new('MAP_ENTRY_R58.json',{'tipo':'RESULTADO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics',
        'dominio':'FORMAL','titulo':'R58: reexame de C:\\IALD recupera receptores, pares, Hadamard e consumidores QG',
        'metodo':'Inventário mecânico, busca textual histórica/atual, três leituras dirigidas, verificação de hashes e revisão de alcance.',
        'resultado':f"{source['finding_count']} achados; {source['unique_source_paths']} fontes únicas conferidas. Oito memórias acrescentadas com backups. R4/R5 não aceitos integralmente.",
        'veredito':'PASS_DOCUMENTARY_SURVEY_WITH_SCOPE','estatuto':'REAL','status':'EM_CURSO','olhou_dados':False,
        'defeito':'Localização de peças não demonstra identidade entre dispositivo, Maxwell H1 e Einstein-sigma; H3 universal segue antecedente.',
        'nao_refazer':'Não reconstruir receptor, RelativePhaseCharacter, estados067/073, rede/Fock, traço nem liganteEinstein.',
        'proximo_passo':'Comparar observáveis de pares/quadraturas, preparação e covariâncias; provar mapas físicos e entrelaçamento no mesmo modelo.',
        'artefatos':[str(delivery),*[str(s.ROOT/n) for n in files]],'onde':str(s.ROOT)})
    map_result=run_once('MAP_REGISTER_R58',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(entry),'--quem',s.ACTOR['id']])
    board_result=run_once('BOARD_REGISTER_R58',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',
        'avancar','F1.FECHO_20261015','--quem',s.ACTOR['id'],'--status','EM_CURSO','--evidencia',str(delivery),
        '--nota','R58: acervo reexaminado, peças anteriores recuperadas e pinos conferidos; relatório e oito memórias com revisão. R4/R5 ainda abertos, sem rito novo, provedor ou gate.'])
    registration=s.new('REGISTRATION_R58.json',{'delivery':pin(delivery),'map':pin(map_result),'board':pin(board_result)})
    state=s.cli('session_memory.py',{'operation':'get','reference':str(s.REF)},'FINAL_GET')
    handles=state['p']['handles']
    reports_by_id=dict(zip(['r58-survey-dispositivos','r58-survey-rede','r58-survey-gravidade'],REPORTS))
    for h in handles:
        if h.get('id') in reports_by_id:
            h['status']='completed';h['result']=pin(s.ROOT/reports_by_id[h['id']])
    s.cli('session_memory.py',{'operation':'transition','reference':str(s.REF),'actor':s.ACTOR,
        'expected_revision':state['revision'],'event_id':'r58-corpus-survey-delivered-20261017',
        'changes':{'records':[{'id':'r58-corpus-reuse-findings','kind':'fact','statute':'REAL',
            'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [delivery,registration]],
            'text':'R58 localiza receptores, leitura relativa, estados de pares e construçãoHadamard067/073; confirma rede/core/Maxwell e Einstein condicional já existentes. Presença e hashes verificados; alcance matemático separado por fonte. R4/R5 continuam abertos: identidade dos objetos, covariância e dinâmica entre realizações. Sem novo build/provedor/gate.'}],
            'flow':{'phase':'r58_corpus_reuse_delivered','next_action':'Reaproveitar pares/quadraturas e covariâncias existentes; provar identificação com preparação e dinâmicaOH e comparar às realizações contínuas. H3 universal separado; R3/R10 aguardam composição.','handles':handles}}},'FINAL_TRANSITION')
    print(delivery)

if __name__=='__main__':
    {'prepare':prepare,'finish':finish}[sys.argv[1]]()
