"""Verify current custody and persist continuation without rewriting historical results."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import json
from deliver_nonminimal_wick_and_mimo_audit import H, OUT, sha, write, put, append

def main():
    now=datetime.now(timezone.utc);D=H/'balanced_and_ward_checkpoint';D.mkdir(exist_ok=False)
    names=['balanced_pair_normalization_v2','balanced_euler_tensor','balanced_pair_tensor',
        'balanced_current_source','balanced_subtotal_descent_audit','kimi_localized_consistency_audit',
        'temporal_ward_consistency_polarization']
    verified=[];rows=[]
    for name in names:
        manifest=H/name/'manifest.json';m=json.loads(manifest.read_bytes())
        for item in m['artifacts']:
            p=Path(item['path']);assert sha(p)==item['sha256'],p
            verified.append(dict(path=str(p),sha256=item['sha256']))
        result_path=H/name/('AUDIT.json' if name=='kimi_localized_consistency_audit' else 'results.json')
        r=json.loads(result_path.read_bytes())
        rows.append(dict(name=name,checks=r['checks'],cpu_seconds=r['cpu_seconds'],manifest_sha256=sha(manifest)))
    cost=Decimal(0);seen=set();entries=[]
    for line in (OUT/'LEDGER_016.jsonl').read_text('utf-8').splitlines():
        if not line.strip():continue
        item=json.loads(line);entries.append(item);value=item.get('cost_estimate_usd',item.get('cost_usd'))
        if value is None:continue
        key=item.get('execution_task_id') or item.get('job_id') or item.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(value))
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    snapshot=dict(at=now.isoformat(),batches=rows,checks=sum(r['checks'] for r in rows),
        cpu_seconds=sum(r['cpu_seconds'] for r in rows),manifest_entries_checked=len(verified),
        unique_artifacts_checked=len({v['path'] for v in verified}),partial_metered_cost_usd=str(cost),
        subscription_cost_unknown=True,opening_sha256=opening,own_processes=[],gate_changed=False,full_Q2=False)
    put(D/'results.json',snapshot)
    state_path=H/'CONTINUIDADE.json';state=json.loads(state_path.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration','own_processes']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_processes=[],
        completed_this_turn=['Balanced normalization transported to metric/ghost pairs, five currents and source with fixed weights',
            'Both pair and source finite-normalization changes have zero free-BV square; current changes explain the full defect change',
            'Two balanced Euler descendants do not span the converted subtotal defect: rank2->3, without fitting',
            'Kimi e710 received and independently audited; Jacobi accepted, order/sign/polarization corrections recorded',
            'Frob Theorem7 read at primary source; exact two-input one-loop consistency condition extracted'],
        next=['A7.b: assemble the SAME temporal family in s0a2+(Vx,a1Vy)+(Vy,a1Vx)=a1((Vx,Vy))+a2(s0Vx,Vy)+a2(s0Vy,Vx)',
            'Audit pending Kimi51c Euler graph and709 balanced-family results without duplicating calls',
            'Do not treat converted subtotal or restricted Euler span as whole A2; retain arity1/composite classical insertions and curved terms',
            'A7.b deadline2026-09-25T20:32:00Z; then A7.c4h, A7.d2h, A8; PartC only after A8; PartB/final remain'],
        pending_orchestration='Official coordinator delivery e710 complete/audited;51c running execution82c646b6-e910-4564-90e6-0c45fc865d91 worker44908.709,C2.1,C2.2,C2.3 admitted;C2.4/C2.5 staged;d3 afterwards. Coordinator owns all transitions; snapshot only.',
        partial_metered_cost_usd=str(cost))
    state['balanced_and_ward_update']=snapshot
    state['latest_verified_orchestration']['own_live_processes']=[]
    state['latest_verified_orchestration']['current_snapshot']=dict(at=now.isoformat(),
        source='Official coordinator message received current turn',
        e710_completed_job='d41046ee-a069-4545-a6ba-9c322662af46',
        next_job='039cab4b-a3a1-4cad-8d8c-349a55d705b3',next_execution='82c646b6-e910-4564-90e6-0c45fc865d91',
        next_worker=44908,C23_job='5cd7b089-26d0-415d-91d3-943bf00dead1',
        note='Older fields preserved as history, not current running-process claims')
    put(state_path,state,True)
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'results.json']],verified=verified))
    note=f'''[REAL — custódia e continuidade conferidas; DERIVED — cálculos indicados; Q2 OPEN]

Sete lotes: {snapshot['checks']} controles de álgebra, CPU somada
{snapshot['cpu_seconds']}s. A contagem reúne controles, não teoremas independentes.
{snapshot['manifest_entries_checked']} entradas de manifesto conferidas por SHA256,
{snapshot['unique_artifacts_checked']} artefatos distintos. Todos os processos
locais destes lotes terminaram rc0. A tentativa v1 de normalização que falhou
e a prévia longa recusada do adendo permanecem preservadas; os sucessores
estão explicitamente versionados e não são apresentados como primeiras tentativas.

O subtotal convertido permanece não nulo. A mudança do defeito foi localizada
nas cinco correntes; par e fonte isoladamente têm quadrado BV livre zero.
O teste de span dos dois Euler balanceados deu2→3. Isso não testa todos os
termos da identidade temporal, agora registrada com as duas inserções clássicas
e a correção de uma entrada do antibracket. Gate e originais intactos.

Kimi e710 entregue/auditado;51c em execução segundo a coordenação oficial,
709 preservado, cinco críticas C2 preparadas e admitidas por etapas. Nenhuma
chamada incerta repetida. Custo conhecido parcial somado por script USD{cost};
Kimi por assinatura sem custo unitário informado. Não é fatura total.

Continuidade em A7/CONTINUIDADE.json, backup imediato de bytes e troca atômica.
A7.b até20:32UTC; demais ramos continuam na ordem. PartC somente depois deA8.
AberturaSHA256={opening}.
'''
    write(OUT/'ENTREGA_016_MEDIDA_custodia_balanceada_e_Ward.md',note.encode())
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='BALANCED_WARD_CHECKPOINT',
        accounting='AGGREGATE_EXISTING_BATCHES_DO_NOT_ADD_CHECKS_OR_COSTS_AGAIN',snapshot=snapshot,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: custódia dos7lotes conferida, agregação{snapshot["checks"]}controles CPU{snapshot["cpu_seconds"]}s (não somar novamente). Custo parcialUSD{cost}. Próxima montagem usa condição temporal polarizada;Q2OPEN. AberturaSHA256={opening}.\n')
    print(json.dumps(snapshot),flush=True)

if __name__=='__main__':main()
