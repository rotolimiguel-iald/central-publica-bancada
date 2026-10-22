"""Deliver native-diagnostic reproduction with differences and uninstrumented values explicit."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,defaultdict
import json,hashlib,uuid
B=Path(__file__).resolve().parents[2];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT';R=ROOT/'ORDEM_016_QG'
LOG=B/'bis/015/t02/remainder_runs';S=ROOT/'TUNEL/PARA_CHATGPT/ORDEM_015_INSUMOS/reproducoes_da_gerencia'
D=B/'bis/015/t02/final_delivery';now=datetime.now(timezone.utc);sources={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):sources[str(p)]=sha(p);return json.loads(p.read_bytes())
def jsonl(p):sources[str(p)]=sha(p);return [json.loads(l) for l in p.read_text('utf-8-sig').splitlines() if l.strip()]
def write(p,raw,replace=False):
    if p.exists():
        assert replace
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with t.open('xb') as f:f.write(raw)
    assert t.read_bytes()==raw;t.replace(p)
def put(p,obj,replace=False):write(p,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode(),replace)
def normalized(rows):
    return [{**{k:v for k,v in r.items() if k!='status'},'status':'NATIVE_CRASH' if r['status'].startswith('CRASH_rc') else r['status']} for r in rows]
def main():
    remainder=load(LOG/'RESULT.json');assert remainder['status']=='COMPLETE'
    D.mkdir(exist_ok=False)
    checkpoint=load(B/'bis/015/t02/checkpoint_dg14_dg02/RESULT.json')
    for name,h in checkpoint['sources'].items():assert sha(Path(name))==h
    cross=load(LOG/'crosscheck.json')['crosscheck_pred_vs_bilby_fmax1024'];assert cross['agree']==150 and cross['disagree']==0
    replay=jsonl(LOG/'front_replay.jsonl')[-1]
    scan=jsonl(LOG/'front_scan_registered.jsonl')[-1]
    grid=jsonl(LOG/'front_grid.jsonl')[-1]['rows'];fine=jsonl(LOG/'front_fine.jsonl')[-1]['rows']
    comparisons={}
    for tag,rows,name in [('grid',grid,'REPRO_grid.jsonl'),('fine',fine,'REPRO_fine.jsonl')]:
        ref=jsonl(S/'E3_piloto_orcamento_cegos'/name)[-1]['rows']
        comparisons[tag]={'own_rows':len(rows),'management_rows':len(ref),'same_outcomes_ignoring_heap_signal':normalized(rows)==normalized(ref),
                          'own_crashes':sum(r['status'].startswith('CRASH') for r in rows),'management_crashes':sum(r['status'].startswith('CRASH') for r in ref)}
    scanref=jsonl(S/'E3_piloto_orcamento_cegos/REPRO_scan_registered.jsonl')[-1]
    comparisons['registered_scan']={'own':scan['summary'],'management':scanref['summary'],'same':scan['summary']==scanref['summary']}
    sig=Counter(str(r['rc']) for r in scan['crashes'])
    thresholds=defaultdict(list)
    for r in fine:
        if r.get('dtau220',0)==0:thresholds[r['source']].append(r)
    boundary={k:{'last_finite':max((r['dtau440'] for r in v if not r['status'].startswith('CRASH')),default=None),
                 'first_crash':min((r['dtau440'] for r in v if r['status'].startswith('CRASH')),default=None)} for k,v in thresholds.items()}
    c04=load(S/'cetico_C04/RESULT_CETICO_C04.json')
    # Preserve the management evidence as DECLARADO, without copying its results into this run.
    from_manager={'source':str(S/'cetico_C04/RESULT_CETICO_C04.json'),'sha256':sha(S/'cetico_C04/RESULT_CETICO_C04.json'),
                  'statute':'DECLARADO_PELA_GERENCIA_NOT_REEXECUTED_HERE','claims':'400 draws:120 aborts,22 SIGSEGV and98 SIGABRT; original heap not identical to pilot'}
    completed=checkpoint['completed_wall_seconds']+sum(r['wall_seconds'] for r in remainder['records'])
    cpu=checkpoint['completed_cpu_seconds']+sum(r['cpu_seconds_including_children'] for r in remainder['records'])
    assert all(r['cpu_seconds_including_children']<900 for r in remainder['records'])
    old=B/'bis/e3_pilot_failure_diagnostic'
    predecessor=[{'path':str(old/n),'sha256':sha(old/n)} for n in ['DIAGNOSIS.json','DIAGNOSIS.md']]
    result={'at':now.isoformat(),'status':'T02_NATIVE_BEHAVIOR_REPRODUCED_SOURCE_MECHANISM_DERIVED','supersedes_scope':'native failure diagnosis only','predecessors':predecessor,
        'checkpoint':{'path':str(B/'bis/015/t02/checkpoint_dg14_dg02/RESULT.json'),'sha256':sha(B/'bis/015/t02/checkpoint_dg14_dg02/RESULT.json')},
        'crosscheck':cross,'exact_prior_replay':replay,'registered_scan_summary':scan['summary'],'native_signal_counts_scan':dict(sig),
        'fine_boundary':boundary,'comparisons':comparisons,'management_C04':from_manager,
        'rule':'On tested grid: (1+dtau440)>c*max(1,1+dtau220); c bracket depends on source and grid. Not the sign condition dtau220<0.',
        'source_slope':checkpoint['source_predicted_slope'],'measured_slope':checkpoint['measured_midpoint_slope'],'measured_slope_bracket':checkpoint['measured_slope_bracket'],
        'pooled_EDOM_fraction':checkpoint['pooled_fraction'],'pooled_binomial_SE':checkpoint['pooled_binomial_SE'],
        'per_seed_binomial_SE':checkpoint['per_seed_binomial_SE_at_pooled_fraction'],'candidate_metadata':checkpoint['blind_metadata_summary'],
        'unmeasured':['retLen','indAmax','Nrdwave','causal_identity_of_the_original_pilot_heap'],
        'sources':sources,'wall_seconds_subprocesses':completed,'cpu_seconds_subprocesses':cpu,'heavy_machine_hours':0,
        'pins_unchanged':True,'scientific_runtime_modified':False,'gate_changed':False,'new_PE':False,
        'opening015_sha256':sha(OUT/'ENTREGA_015_ABERTURA_operador.md'),'opening016_sha256':sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
    jp=old/'DIAGNOSIS_ADENDO_v2.json';mp=old/'DIAGNOSIS_ADENDO_v2.md';put(jp,result)
    report=f'''[REAL — comportamento nativo; DERIVED — mecanismo pela fonte C; nenhum novo teste físico]

Abertura015SHA256: {result['opening015_sha256']}
Abertura016SHA256: {result['opening016_sha256']}
Predecessores intactos: {json.dumps(predecessor,ensure_ascii=False)}

Replay exato: primeiros8sorteios coincidem;15concluem e o16aborta com rc{replay['returncode']} no mesmo processo. Em subprocessos separados abortam16/20/22/24(rc−6 nesta rodada);2/8 retornam domínio. O diagnóstico anterior de sorteio desconhecido fica corrigido nesse escopo. Identidade com o heap do piloto original continua DERIVED.

Grade fina:{boundary}. Na grade de122pontos das seis fontes(56+66), o critério não é o sinal de dtau220. A escala do limiar é max(1,1+dtau220); previsto pela fonte2·Imω440/Imω220={result['source_slope']:.8f}; medido2,0 com intervalo de grade{result['measured_slope_bracket']}. retLen/indAmax/Nrdwave não instrumentados, não medidos.

Scan registrado120:{scan['summary']}; sinais entre abortos:{dict(sig)}. Comparações com a gerência:{json.dumps(comparisons,ensure_ascii=False)}. C04(400sorteios,22SIGSEGV/98SIGABRT) permanece DECLARADO pela gerência, fonte hash{from_manager['sha256']}; não é contagem nova da bancada. A reprodução exata do sinal pode variar com o heap.

EDOM: previsão f550>1024 conferiu em150/150chamadas isoladas. Quatro sementes,8000sorteios:4,35%; SE binomial combinado0,228p.p., contra0,456p.p. por2000sorteios. O4:22/36excedem1024 no550,18/36excedem2048,4/36têm o220fora da banda1024. Os8semMf continuam sem diagnóstico. Nos cantos do posterior conhecido, o limite1024não demonstrou viés; não houve PE nova.

CPU medida={cpu:.3f}s; parede sequencial={completed:.3f}s; nenhum comando ultrapassou900sCPU. O tempo anunciado anteriormente de10–13min para DG02 foi substituído pela medição destes recibos. Runtime conferido antes:4621arquivos; nenhuma instalação ou modificação em/opt. Nenhum jobV1 relançado; nenhuma semente cega lida; nenhum gate alterado.

Próximo ramo obrigatório:T13(higiene), depoisT03(guarda/emenda).\n'''
    write(mp,report.encode());write(OUT/'ENTREGA_015_T02_diagnostico.md',report.encode())
    put(D/'RESULT.json',{'at':now.isoformat(),'status':result['status'],'diagnosis_json':str(jp),'diagnosis_sha256':sha(jp),'report_sha256':sha(mp),'cpu_seconds':cpu,'wall_seconds':completed,'heavy_machine_hours':0})
    p=OUT/'LEDGER_016.jsonl';write(p,p.read_bytes()+(json.dumps({'at':now.isoformat(),'event':'PARTB_T02_COMPLETED','receipt':str(D/'RESULT.json'),'external_calls':0})+'\n').encode(),True)
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — B/T02: PAGO como reprodução comportamental e diagnóstico DERIVED da fonte; CPU{cpu/3600:.6f}h; máquina leve{completed/3600:.6f}h, pesada0h. PróximoT13. Nenhum custo externo novo; soma parcial informada permanece no reciboT01.\n'.encode(),True)
    p=R/'A7/CONTINUIDADE.json';state=json.loads(p.read_bytes());state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_process=None,T02_final=str(D/'RESULT.json'),next='T13 hygiene exact paths and new integrity receipt, then T03. External dispatch awaiting specific approval; C6 stays closed.');put(p,state,True)
    print(json.dumps({'status':result['status'],'scan':scan['summary'],'signals':dict(sig),'comparisons':comparisons,'wall_seconds':completed,'cpu_seconds':cpu},ensure_ascii=False))
if __name__=='__main__':main()
