"""Pin completed T02 evidence while the remaining native checks are live."""
from pathlib import Path
from datetime import datetime,timezone
from collections import defaultdict
import json,hashlib,math,uuid
B=Path(__file__).resolve().parents[2];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT';R=ROOT/'ORDEM_016_QG'
D=B/'bis/015/t02/checkpoint_dg14_dg02';S=ROOT/'TUNEL/PARA_CHATGPT/ORDEM_015_INSUMOS/reproducoes_da_gerencia'
now=datetime.now(timezone.utc);sources={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):sources[str(p)]=sha(p);return json.loads(p.read_bytes())
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
def main():
    D.mkdir(exist_ok=False)
    dg14=B/'refeito/015/dg14/out'
    replay=load(dg14/'replay24.json');draws=load(dg14/'draws24_1024.json');grid=load(dg14/'grid_draw16_fmax1024.json');line=load(dg14/'line_draw16_fmax1024.json')
    management=load(S/'dg14/DG14_MEDICAO.json')
    crash=[r['tag'] for r in draws if r['rc']!=0]
    assert crash==management['crash_draws_fmax1024']
    assert len(grid)==management['grid_points'] and sum(r['rc']!=0 for r in grid)==management['grid_crashes']
    assert len(line)==management['line_points']
    by=defaultdict(list)
    for r in line:by[r['dtau220']].append(r)
    thresholds=[]
    for a,rows in sorted(by.items()):
        fails=[r['dtau440'] for r in rows if r['rc']!=0];ok=[r['dtau440'] for r in rows if r['rc']==0]
        thresholds.append({'dtau220':a,'last_finite':max(ok) if ok else None,'first_crash':min(fails) if fails else None})
    lp=B/'bis/015/t02/dg14_runs/line.stdout';sources[str(lp)]=sha(lp)
    qnm=json.loads(next(l[4:] for l in lp.read_text().splitlines() if l.startswith('QNM ')))
    predicted=2*qnm['44']['im']/qnm['22']['im']
    # Difference of adjacent threshold midpoints for positive d220, grid step .25.
    intervals={r['dtau220']:(r['last_finite'],r['first_crash']) for r in thresholds}
    lo0,hi0=intervals[0.0];lo1,hi1=intervals[.5];lo2,hi2=intervals[1.0]
    slope=(.5*(lo2+hi2)-.5*(lo0+hi0))/1.0
    interval_slope=(lo2-hi0,hi2-lo0)
    values=[];seeds=[]
    ref=load(S/'DG02/dg02_result.json')
    for seed in [20260923,132203,7,99]:
        key=f'seed_{seed}';row=load(B/f'bis/015/t02/dg02_runs/{key}.json')[key]
        assert row==ref[key],seed
        values.append(row['frac_f550_gt_1024']);seeds.append({'seed':seed,**row})
    mean=sum(values)/4;N=sum(r['N'] for r in seeds)
    summary=load(B/'bis/015/t02/remainder_runs/metadata.json')['blind_summary'];assert summary==ref['blind_summary']
    cpaths=[B/'bis/e3_pilot_failure_diagnostic/sources/LALSimIMRSpinAlignedEOB.c',B/'bis/e3_pilot_failure_diagnostic/sources/LALSimIMREOBHybridRingdown.c']
    for p in cpaths:sources[str(p)]=sha(p)
    receipts=[load(B/'bis/015/t02/dg14_runs/RESULT.json'),load(B/'bis/015/t02/dg02_runs/RESULT.json')]
    result={'at':now.isoformat(),'status':'T02_PARTIAL_CHECKPOINT_REMAINDER_LIVE','native_crash_draws':crash,
      'returncodes':[r['rc'] for r in draws if r['rc']!=0],'thresholds':thresholds,'source_predicted_slope':predicted,
      'measured_midpoint_slope':slope,'measured_slope_bracket':interval_slope,'QNM':qnm,
      'seeds':seeds,'pooled_fraction':mean,'pooled_binomial_SE':math.sqrt(mean*(1-mean)/N),
      'per_seed_binomial_SE_at_pooled_fraction':math.sqrt(mean*(1-mean)/2000),
      'blind_metadata_summary':summary,'retLen_indAmax_Nrdwave':'NOT_INSTRUMENTED_NOT_MEASURED',
      'original_SIGSEGV_cause':'DERIVED_same_sequence_not_identical_heap','sources':sources,
      'completed_wall_seconds':sum(r['wall_seconds'] for x in receipts for r in x['records']),
      'completed_cpu_seconds':sum(r.get('cpu_seconds',r.get('cpu_seconds_including_children')) for x in receipts for r in x['records']),
      'remaining_process_session':53314,'gate_changed':False,'heavy_machine_hours':0}
    put(D/'RESULT.json',result)
    text=f'''[REAL / DERIVED — T02 parcial; diagnóstico de software, não significância física]

Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}

DG14: replay24, grade56 e linha65 concluídos. Abortam exatamente16/20/22/24(rc−6 nesta rodada); EDOM nos2/8. Contagens coincidem com os JSON da gerência. O16 como causa do SIGSEGV original permanece DERIVED, pois o heap original não foi reproduzido. A nova execução não inventa medição de retLen/indAmax/Nrdwave.

Declive: {predicted:.9f} previsto pela razão de frequências de amortecimento na fonte C; {slope:.3f} entre pontos médios dos limiares, intervalo da grade{interval_slope}. O fator cresce com max(1,1+dtau220); não é mera condição dtau220<0.

DG02:8000sorteios, quatro sementes preservadas. Fração f550>1024={100*mean:.3f}%; SE binomial agregado={100*result['pooled_binomial_SE']:.3f}p.p.; SE por semente no mesmo p={100*result['per_seed_binomial_SE_at_pooled_fraction']:.3f}p.p. O arredondamento histórico4,4±0,5% corresponde à escala por2000sorteios, não à incerteza combinada de8000. Nenhum viés do posterior é inferido deste contador de prior.

Metadados: {summary}. Mesmas contagens22/36,18/36,4/36 da gerência, sem abrir strain ou posterior cego.

Restam crosscheck150formas e frenteD; sessão53314 confirmada em execução. Próximo: concluir T02, entregar DIAGNOSIS_ADENDO_v2 e passar a T13. Resultados completos, fontes e custos: {D/'RESULT.json'}.
'''
    write(OUT/'ENTREGA_015_T02_parcial_DG14_DG02.md',text.encode())
    p=OUT/'LEDGER_016.jsonl';entry={'at':now.isoformat(),'event':'PARTB_T02_PARTIAL_NATIVE_REPRODUCTION','receipt':str(D/'RESULT.json'),'external_calls':0}
    write(p,p.read_bytes()+(json.dumps(entry)+'\n').encode(),True)
    p=R/'A7/CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',T02_partial=str(D/'RESULT.json'),
       own_live_process={'session_id':53314,'scope':'T02 DG02 crosscheck and frontD; sequential, poll only','confirmed_live_by_write_stdin':True},
       next='Poll53314, complete T02 comparison/DIAGNOSIS_ADENDO_v2, then T13. Revised external dispatch awaits explicit approval. No C6 restart.')
    put(p,state,True)
    print(json.dumps({k:result[k] for k in ['status','native_crash_draws','source_predicted_slope','measured_midpoint_slope','pooled_fraction','completed_wall_seconds','completed_cpu_seconds','remaining_process_session']}))
if __name__=='__main__':main()
