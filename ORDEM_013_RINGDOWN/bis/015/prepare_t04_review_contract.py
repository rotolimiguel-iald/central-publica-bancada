"""Extract current acceptance references; no execution or change of a criterion."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,ast
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;B=D.parents[1];ROOT=B.parent;OUT=ROOT/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(ROOT/'ORDEM_016_QG'))
from prepare_part_d import save,write,sha

def main():
    code=B/'bis/e2_code_v1_1_2';source=code/'pe_runner.py'
    functions={n.name:dict(first_line=n.lineno,last_line=n.end_lineno) for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef)}
    regp=B/'RINGDOWN_5SIGMA_V1_1_2.json';reg=json.loads(regp.read_bytes());cfg=reg['pe_jobs']['GW250114_PILOT_V2_S220']
    checks=[
      dict(id='identity',evidence=['t04/pilot/RESULT.json','CONTROLLER.json','LAUNCH_CONTEXT.json'],
        criterion='Same registration/job and clean owned process group before any next job'),
      dict(id='terminal',evidence=['PRIVATE_CONVERGENCE.json'],function='terminal_state',
        criterion='Finite terminal quantities, non-plateau, strict ncall<maxcall and delta_logz<dlogz; captured before adding live points',
        limitation='Raw live_logl not included by this terminal_state receipt; do not claim independent recomputation of unpersisted live arrays'),
      dict(id='weights_and_samples',evidence=['PRIVATE_CONVERGENCE.json','raw result hdf5'],function='convergence',
        criterion='Finite nonnegative weights,positive sum; ESS=(sumw)^2/sum(w^2)>=registered minimum;posterior count>=registered minimum;ncall_reported==ncall'),
      dict(id='edom',evidence=['EDOM_LOG.jsonl','EDOM_SUMMARY.json','PRIVATE_CONVERGENCE.json'],function='edom_posterior_status',
        criterion='EDOM log count agrees with sourcecounter;0inside declared marginal99%mass/spin box',
        limitation='The mass/spin box is the registered diagnostic; not a theorem excluding all numerical bias'),
      dict(id='paired_columns',evidence=['ANALYST_OUTPUT.json','PRIVATE_REMNANT_CONVERSION.json'],function='posterior_columns',
        criterion='All physical/deformation and derived columns finite,paired; fixed440columns exactly0;derived remnant and external cosmology scope retained'),
      dict(id='cost',evidence=['CONTROLLER.json','PRIVATE_CONVERGENCE.json','t04/pilot/RESULT.json'],
        criterion='Actual wall,CPU and process observations;sourcecalls and sampler_ncall distinct;sum per-sourcewall is not jobwall or exactCPU'),
      dict(id='reported_quantity',evidence=['ANALYST_OUTPUT.json'],
        criterion='Own nonblind dtau220 interval versus published comparison; alignedv4HM versus precessingv5PHM family caveat;no discovery sigma from pilot'),
      dict(id='branch_after_terminal',evidence=['CONTROLLER.json','PRIVATE_CONVERGENCE.json','ANALYST_STATUS.json','FAILURE.json'],
        criterion='T04C/D/H/E/F per measured status; cleanup first; newID/seed/allocation before any authorized new run;never repeat existing job')]
    at=datetime.now(timezone.utc).isoformat()
    result=dict(at=at,status='READ_ONLY_REVIEW_MAP_NOT_CONVERGENCE_RESULT',
        registration_sha256=sha(regp),job='GW250114_PILOT_V2_S220',settings=cfg['sampler'],
        source_sha256=sha(source),function_locations={k:functions[k] for k in ('terminal_state','convergence','posterior_columns','edom_posterior_status','likelihood_snapshot')},
        checks=checks,branch_C_rate='r=sampler_ncall/cost.wall_seconds from completed measured receipt,not sum of per-sourcewall',
        branch_C_formula='min(floor(0.9*28800*r),9000000);if<=3000000 goD;budget must be registered beforejob',
        source_not_changed=True,science_not_reexecuted=True,gate_changed=False)
    target=D/'t04/REVIEW_CONTRACT.json';save(target,result)
    note=f'''[REAL — leitura de código registrado; INPUT — critérios já escritos na ordem]

Abertura016SHA256: {sha(OUT/'ENTREGA_016_ABERTURA_operador.md')}
Data: {at}

Mapa de leitura do resultadoT04: bis/015/t04/REVIEW_CONTRACT.json SHA256 {sha(target)}. Fonte pe_runner.py SHA256 {sha(source)}; registroSHA256 {sha(regp)}. Nenhum critério modificado, nenhum resultado de convergência anunciado.

Aceitação exige status terminal, dlogz<{cfg['sampler']['dlogz']}, ncall<{cfg['sampler']['maxcall']}, ESS≥{cfg['sampler']['minimum_effective_samples']}, posterior≥{cfg['sampler']['minimum_posterior_samples']}, contadores coerentes, controleEDOM e colunas físicas pareadas. O vetor live_logl bruto não é persistido pelo recibo terminal: a revisão não alegará recomputação independente desse vetor a partir de campos que não existem.

Custo: sampler_ncall, source_calls e likelihood_calls são contagens distintas. Soma de tempos das fontes também não é parede do job nem CPU exata. Se houver ramoC, r vem de ncall/parede medida no recibo; nova alocação/ID/semente precedem qualquer novojob. A comparação com o posterior publicado conserva a diferença de família alignedv4HM versus precessingv5PHM.

Piloto78755 continua sendo a única rodada desta etapa. Nenhuma nova chamada remota ou ciência nesta preparação. O relatório continua dependente dos recibos terminais.
'''
    write(OUT/'ENTREGA_015_T04_mapa_da_revisao.md',note.encode())
    cp=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=json.loads(cp.read_bytes())
    state.update(at=at,previous_goal_turn='PROGRESS_AND_VERIFIED_WAIT',T04_review_contract=str(target))
    save(cp,state,True)
    progress=OUT/'ENTREGA_016_PROGRESSO.md'
    write(progress,progress.read_bytes()+f'\n{at} | B/T04 leitura preparada | critérios do código vigente mapeados, limite de evidência declarado | ciênciaadicional0h; piloto78755ativo\n'.encode(),True)
    print(json.dumps(dict(status=result['status'],checks=len(checks),sha256=sha(target))))
if __name__=='__main__':main()
