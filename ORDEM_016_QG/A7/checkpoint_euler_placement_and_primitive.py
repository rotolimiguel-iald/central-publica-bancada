"""Persist the concrete Euler/arity-one advances and their restricted proof scopes."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);D=H/'euler_placement_and_primitive_checkpoint';D.mkdir(exist_ok=False)
    batches=[('quartic_antibracket_arity_one','quartic_antibracket_arity_one_check.py'),
        ('balanced_cubic_euler_contact','balanced_cubic_euler_contact_check.py'),
        ('balanced_euler_metric_vertex','balanced_euler_metric_vertex_check.py'),
        ('balanced_euler_higher_jet_audit','balanced_euler_higher_jet_audit.py'),
        ('kimi_euler_census_audit','kimi_euler_census_audit.py'),
        ('euler_subtotal_placement_audit','euler_subtotal_placement_audit.py'),
        ('balanced_euler_constant_cutoff','balanced_euler_constant_cutoff_check.py'),
        ('balanced_flat_primitive','balanced_flat_primitive_check.py')]
    rows=[];verified=[]
    for name,script in batches:
        manifest=H/name/'manifest.json';m=json.loads(manifest.read_bytes())
        for entry in m['artifacts']:
            p=Path(entry['path']);assert sha(p)==entry['sha256'],p;verified.append(entry)
        result=H/name/('AUDIT.json' if name=='kimi_euler_census_audit' else 'results.json')
        r=json.loads(result.read_bytes())
        rows.append(dict(name=name,script=str(H/script),script_sha256=sha(H/script),checks=r['checks'],
            cpu_seconds=r['cpu_seconds'],manifest_sha256=sha(manifest),structured_run_log=str(result),
            structured_run_log_sha256=sha(result),observed_exit_code=0,
            receipt_scope='Return code observed in tool response; results file is structured run evidence, not reconstructed terminal stdout'))
    entries=[json.loads(v) for v in (OUT/'LEDGER_016.jsonl').read_text('utf-8').splitlines() if v.strip()]
    cost=Decimal(0);seen=set()
    for e in entries:
        value=e.get('cost_estimate_usd',e.get('cost_usd'))
        if value is None:continue
        key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(value))
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    snapshot=dict(at=now.isoformat(),batches=rows,checks=sum(v['checks'] for v in rows),
        cpu_seconds=sum(v['cpu_seconds'] for v in rows),verified_manifest_entries=len(verified),
        unique_verified_artifacts=len({v['path'] for v in verified}),partial_metered_cost_usd=str(cost),
        subscription_unit_cost_unknown=True,own_processes=[],opening_sha256=opening,full_Q2=False,gate_changed=False)
    put(D/'results.json',snapshot)
    note=f'''[DERIVED — ligações Euler/Ward e primitiva delimitada; REAL — custódia]

Resultados reunidos nesta rodada:
1. a1((Vchi,Veta)) é divergência no inventário heat/Wick de espaço-forma
   constante: sua integral compacta zera, mas a densidade não é zero.
2. Três grafos Euler cúbicos foram calculados, incluindo o canal Qbarc
   omitido pelo parecer Kimi. A auditoria independente preserva o original
   e corrige o censo, os sinais e a eliminação prematura de b.
3. Depois de traduzir A(q)delta para h A(D+lambda+eta)c, a MÉDIA SIMÉTRICA
   dos três grafos reproduz exatamente o subtotal R_bal já existente,
   em todas40 componentes para os jatos de cutoff testados. Não se devem
   somar as duas representações. Separadamente, cada ordenação difere.
4. Com jatos de cutoff zero, o representante principal plano permanece
   não nulo em40componentes, é q0-fechado e tem primitiva local quadrática
   explícita, com duas direções homogêneas mantidas simbólicas.

Escopo da classe zero: esse representante livre, plano, quadrático, de
acoplamento constante. Não foi demonstrada classe zero de toda Q2 curva,
nem admissibilidade de uma família causal/real completa, nem um estado
interagente no horizonte físico. No caso localizado, a consistência é
inhomogênea e inclui a2(q0Vchi,Veta)+a2(q0Veta,Vchi).

Oito lotes, {snapshot['checks']} controles agregados, CPU
{snapshot['cpu_seconds']}s. Controles de aritmética e identidades são
discriminados nas entregas; a soma não é quantidade de teoremas.
{snapshot['verified_manifest_entries']} entradas / {snapshot['unique_verified_artifacts']}
artefatos distintos conferidos por SHA256. Processos locais encerrados rc0.
Comandos e logs estruturados constam em results.json; nenhum stdout foi
reconstituído como se fosse captura original.

Custo externo conhecido parcial USD{cost}, sem nova chamada remota desta
bancada; Kimi51c registrado uma vez com tokens e custo unitário desconhecido.
709 segue sob acompanhamento da coordenação oficial, sem chamada duplicada.
A7.b continua até seu teto20:32UTC; ramos restantes conservam a ordem.
Nenhum original/kernel/gate alterado. AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_custodia_Euler_e_primitiva.md',note.encode())
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'results.json',D/'DERIVACAO.md']],verified=verified))
    state_path=H/'CONTINUIDADE.json';state=json.loads(state_path.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration','own_processes']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_processes=[],
        completed_this_turn=[
            'a1 of mixed antibracket computed: compact integral zero as an explicit divergence under the stated spaceform inventory',
            'Three actual cubic Euler contacts and order5 pair jets computed without changing the prescribed normalization',
            'Kimi51c received/audited: omitted double ghost contractions and incorrect cutoff identity corrected',
            'In the tested cutoff jets, symmetric Euler sum equals converted subtotal in all40 components; do not add them twice',
            'Constant-cutoff flat representative is nonzero but free-BRST closed and explicitly exact; two homogeneous primitive parameters remain unchosen'],
        next=[
            'Receive and audit Kimi709 balanced-family result; no duplicate scientific request',
            'Complete the known arity1 terms of the temporal polarized consistency equation, distinguishing density and integrated identities',
            'Remaining full A2 requires curved/scalar terms and actual a2(q0V,V) in one family; neither the flat primitive nor the two-cutoff sample discharges that scope',
            'A7.b deadline2026-09-25T20:32:00Z; then A7.c4h,A7.d2h,A8,PartC afterA8,PartB/final'],
        pending_orchestration='Official snapshot:51c job039cab4b complete/audited.709 job8639533b execution814fd0d0 worker66365 was running; coordinator asked for fresh status. C2.4 job7f044602 admitted; C2.5 and d3 staged. No local provider worker.',
        partial_metered_cost_usd=str(cost))
    state['euler_placement_and_primitive_update']=snapshot
    state['latest_verified_orchestration']['own_live_processes']=[]
    state['latest_verified_orchestration']['current_snapshot']=dict(at=now.isoformat(),
        source='Official coordinator messages; latest status refresh requested, not presumed',
        completed_job='039cab4b-a3a1-4cad-8d8c-349a55d705b3',
        running_last_seen_job='8639533b-6775-4a5c-8d7f-988659d58c2d',
        running_last_seen_execution='814fd0d0-65cc-4dcd-97d5-f52e16b1b798',coordinator_worker=66365,
        C24_job='7f044602-7a5c-4c9a-8f59-7930175e4e93',older_fields_are_history=True)
    put(state_path,state,True)
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='EULER_PLACEMENT_PRIMITIVE_CHECKPOINT',
        accounting='AGGREGATE_EXISTING_BATCHES_DO_NOT_COUNT_AGAIN',snapshot=snapshot,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: ligação Euler=subtotal simétrico no teste, primitiva plana explícita;8lotes/{snapshot["checks"]}controles CPU{snapshot["cpu_seconds"]}s, agregação não somar de novo. Custo conhecido parcialUSD{cost}. Continuidade atualizada;Q2curvaOPEN. AberturaSHA256={opening}.\n')
    print(json.dumps({k:v for k,v in snapshot.items() if k!='batches'}),flush=True)

if __name__=='__main__':main()
