"""Summarize only completed, registered synthetic cells and actual machine cost."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,math
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import write,save,sha
def main():
    run=D/'nulls_campaign_001';r=json.loads((run/'RESULT.json').read_bytes())
    regpath=B/'RINGDOWN_5SIGMA_V1_1_2.json';reg=json.loads(regpath.read_bytes())
    assert sha(regpath)==r['registration_sha256'];cells=reg['nulls_v1_1']['cells']
    rows=[]
    for finished in r['finished']:
        if not finished['accepted']:continue
        name=finished['cell'];p=B/'bis'/('RESULT_E2_NULL_'+name+'.json')
        assert sha(p)==finished['receipt_sha256']
        data=json.loads(p.read_bytes());v=data['result']
        assert data['registration_sha256']==sha(regpath) and data['cell']==cells[name]
        assert v['draws']==cells[name]['draws'] and 0<=v['false_positives']<=v['draws']
        assert math.isclose(v['empirical_p'],v['false_positives']/v['draws'],rel_tol=1e-14,abs_tol=0)
        row=dict(cell=name,kind=cells[name]['kind'],draws=v['draws'],k=v['false_positives'],
            empirical_p=v['empirical_p'],UL95=v['one_sided_upper'],CI95=v['central_interval'],
            cpu_seconds=data['cpu_seconds'],wall_seconds=data['wall_seconds'],sha256=sha(p),
            physical_p=None,physical_sigma=None)
        if row['kind']=='route_IV':row['UL95_below_registered_p5']=v['one_sided_upper']<=2.87e-7
        else:row.update(covariance_variant=cells[name]['nuisance_covariance_variant'],
                        analytic_tail_control=v['analytic_tail_control'])
        rows.append(row)
    complete=(len(rows)==30 and r['fault'] is None and not r['not_started'])
    summary=dict(at=datetime.now(timezone.utc).isoformat(),status='T03_SYNTHETIC_TAILS_MEASURED' if complete else 'T03_MEDIDA_INCOMPLETE_WITH_COST',
        completed=len(rows),registered=len(cells),rows=rows,failed=[v for v in r['finished'] if not v['accepted']],
        not_started=r['not_started'],fault=r['fault'],machine_hours=r['machine_hours_union'],
        cpu_seconds=r['child_cpu_seconds'],campaign_sha256=sha(run/'RESULT.json'),
        registration_sha256=sha(regpath),physical_p=None,physical_sigma=None,gate_changed=False)
    save(run/'SUMMARY.json',summary)
    table='\n'.join(f"|{v['cell']}|{v['k']}|{v['empirical_p']:.8g}|{v['UL95']:.8g}|" for v in rows)
    note=f'''[REAL — calibração SINTÉTICA; não é detecção nem calibração física de sistemáticas]

# T03 — caudas e covariâncias registradas

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Abertura015SHA256: {sha(OUT/'ENTREGA_015_ABERTURA_operador.md')}
Registro SHA256: {sha(regpath)}

Estado: {summary['status']}; {len(rows)}/{len(cells)} células concluídas. Cada célula concluída consumiu exatamente10^8 draws e preserva a semente já registrada. Nenhuma repetição de célula V1 ou de tentativa incerta. As6células IV usam LRT>25; as24t5 usam matched_z>5 e as3covariâncias registradas. ICs por célula, sem correção de multiplicidade; não dão alegação global.

|Célula|k|p empírico|UL95 unilateral Clopper–Pearson|
|---|---:|---:|---:|
{table}

Somente nas células IV, a comparação UL95≤2,87e-7 avalia a suficiência SINTÉTICA do limiar25. Não determina p físico, sigma_sys ou sigma_jit,rec. t5 é escala comum com nuisance gaussiana; não reinterpretar como ruído independente nem converter estes controles em detecção.

Falha/limite: {json.dumps(r['fault'],ensure_ascii=False)}. Não iniciadas: {len(r['not_started'])}. Se parcial, os resultados concluídos permanecem e os demais não são inventados nem repetidos.

Custo: união de intervalos próprios={r['machine_hours_union']:.9f}h; CPU filhos={r['child_cpu_seconds']:.6f}s; parede supervisor={r['wall_seconds']:.6f}s. Alocação1h. Máximo6filhos; nenhuma PE concorrente. Chamadas remotas0; custos de coordenação desconhecidos permanecem desconhecidos.

Manifestos: RESULT.json sha256 {sha(run/'RESULT.json')}; SUMMARY.json sha256 {sha(run/'SUMMARY.json')}. Arquivos em ORDEM_013_RINGDOWN/bis/015/nulls_campaign_001 e recibos por célula em bis/. Tentativas e logs preservados.

→ CONTINUE: T04, qualificação400 e piloto só220. Nenhum gate ou original alterado; dados cegos não abertos.
'''
    write(OUT/'ENTREGA_015_T03_nulos_1e8.md',note.encode())
    if not complete:write(OUT/'ENTREGA_015_MEDIDA_T03_nulos_parciais.md',note.encode())
    p=OUT/'ENTREGA_016_PROGRESSO.md'
    write(p,p.read_bytes()+f"\n{summary['at']} | B/T03 nulos | {summary['status']}: {len(rows)}/30 | máquina{r['machine_hours_union']:.9f}h | próximo T04\n".encode(),True)
    cp=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(at=summary['at'],previous_goal_turn='PROGRESS',active_process=None,
        next_action='PART_B_T04_QUALIFICATION_400_THEN_PILOT',next='PART_B_T04_QUALIFICATION_400_THEN_PILOT',
        T03_nulls_delivery=str(run/'SUMMARY.json'),part_B_machine_hours=r['machine_hours_union'])
    save(cp,state,True)
    print(json.dumps({k:summary[k] for k in ('status','completed','machine_hours','cpu_seconds','fault')}))
if __name__=='__main__':main()
