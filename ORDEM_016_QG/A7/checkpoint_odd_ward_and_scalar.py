"""Custody checkpoint; retain the complete mission after these restricted advances."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);D=H/'odd_ward_and_scalar_checkpoint';D.mkdir(exist_ok=False)
    cases=[('classical_insertion_euler_v2','results.json','classical_insertion_euler_run_v2.log'),
        ('odd_insertion_ward_sign_audit','results.json','odd_insertion_ward_sign_audit_run.log'),
        ('kimi_composite_normalization_audit','AUDIT.json','kimi_composite_normalization_audit_run.log'),
        ('balanced_scalar_euler_v2','results.json','balanced_scalar_euler_run_v2.log'),
        ('principal_sector_assembly','results.json','principal_sector_assembly_run.log')]
    rows=[];verified=[]
    for name,result,log in cases:
        p=H/name/'manifest.json';m=json.loads(p.read_bytes())
        for item in m['artifacts']:
            assert sha(Path(item['path']))==item['sha256'],item['path'];verified.append(item)
        r=json.loads((H/name/result).read_bytes())
        rows.append(dict(name=name,checks=r['checks'],cpu_seconds=r['cpu_seconds'],manifest_sha256=sha(p),
            result_sha256=sha(H/name/result),log=str(H/log),log_sha256=sha(H/log),observed_rc=0))
    entries=[json.loads(line) for line in (OUT/'LEDGER_016.jsonl').read_text('utf8').splitlines() if line.strip()]
    cost=Decimal(0);seen=set()
    for e in entries:
        val=e.get('cost_estimate_usd',e.get('cost_usd'))
        if val is None:continue
        key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id')
        if key and key in seen:continue
        if key:seen.add(key)
        cost+=Decimal(str(val))
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    result=dict(at=now.isoformat(),batches=rows,checks=sum(r['checks'] for r in rows),
        cpu_seconds=sum(r['cpu_seconds'] for r in rows),verified_manifest_entries=len(verified),
        unique_verified_artifacts=len({e['path'] for e in verified}),partial_metered_cost_usd=str(cost),
        failed_attempts=[dict(script='classical_insertion_euler_check.py',rc=1,reason='handwritten Wick sign expectation reversed; engine unchanged',cpu_seconds=None),
            dict(script='balanced_scalar_euler_check.py',rc=1,reason='extra q2 in candidate Hessian cc term; v2 corrected derivative degree',cpu_seconds=None)],
        failed_attempt_cpu_unknown_not_zero=True,own_processes=[],full_Q2=False,gate_changed=False,
        accounting='Aggregate successful batches only; do not add their CPU/checks a second time',opening_sha256=opening)
    put(D/'results.json',result)
    note=f'''[DERIVED+CAS — consistência principal Einstein-sigma; REAL — custódia]

1. Calculados os três canais clássicos adicionais a2(qV,V): métrico,
   misto e ghost. O controle original retornou um sinal global oposto.
2. A eq155 de Fröb exige o sinal da inserção ímpar. A tradução foi
   verificada numa álgebra de Grassmann independente e na corrente
   clássica. Corrigido apenas o leitor: residual0/16, grafos preservados.
3. Calculados os três modos escalares tangentes. Corrente conferida
   para funções suaves arbitrárias. Sua contribuição não foi descartada
   pelo fato de sigma de fundo ser constante.
4. Soma métrico+ghost+escalares: residual localizado0/16 nos cutoffs
   calculados, e primitiva local explícita no setor plano constante.
   Coeficientes por colocação A=-629/6144,B=-151/6144,C=167/1536.
5. Kimi709 recebido, auditado e contabilizado uma vez. A família split
   proposta é distinta da R_bal; seus contatos parciais foram conferidos,
   mas os valores do Rliteral e a unicidade alegados foram corrigidos.

Não se promove este resultado à Q2 curva completa. Faltam reunir os
contatos K/K² na mesma normalização e conferir as outras aridades,
causalidade/realidade no domínio lorentziano. Primitivas condicionais
antigas não são medidas desses coeficientes. Gate e originais intactos.

Cinco lotes: {result['checks']}controles, CPU{result['cpu_seconds']}s,
{result['verified_manifest_entries']}entradas/{result['unique_verified_artifacts']}arquivos
distintos conferidos por SHA256. Dois defeitos de implementação registrados
e preservados; seus tempos CPU não medidos não entram como zero.
Recibos contêm logs reais e rc observado, sem stdout reconstruído.
Custo externo conhecido parcial USD{cost}; Kimi assinatura sem custo
unitário informado. Nenhum processo local permanece em execução.

A7.b conserva teto20:32UTC. Depois A7.c, A7.d, A8, ParteC doADENDO002,
ParteB/ORDEM015 e relatório final. C2.1 em execução sob coordenação;
C2.2..5 admitidos; não duplicar. Nenhuma conclusão da missão antecipada.
AberturaSHA256={opening}.
'''
    write(D/'DERIVACAO.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_custodia_Ward_escalar.md',note.encode())
    logs=[H/row['log'] if not Path(row['log']).is_absolute() else Path(row['log']) for row in rows]
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in [Path(__file__),D/'results.json',D/'DERIVACAO.md']+logs],verified=verified))
    p=H/'CONTINUIDADE.json';state=json.loads(p.read_bytes())
    state.setdefault('head_history',[]).append({k:state.get(k) for k in ['at','previous_goal_turn','completed_this_turn','next','pending_orchestration','own_processes']})
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_processes=[],
        completed_this_turn=[
            'Three actual classical-insertion Euler channels calculated; sign mismatch diagnosed rather than fitted',
            'Frob odd distinguished-insertion convention checked independently; principal localized metric/ghost consistency0/16',
            'Three scalar fluctuation modes included; arbitrary-field scalar current derived and flat primitive verified',
            'Combined principal Einstein-sigma coefficients measured; localized consistency0/16 in tested jets',
            'Kimi709 response audited1001controls; split residues accepted, literal-R contacts/uniqueness corrected'],
        next=[
            'A7.b remaining until2026-09-25T20:32:00Z: actual curved K/K2 contacts in the same R_bal; old conditional curved primitive is not that calculation',
            'Parity convention also applies to curvature-dependent a1 odd inputs; do not combine old arity1 expressions without this translation',
            'Avoid redoing flat principal calculations: scalar+metric+ghost representative, primitive and sampled inhomogeneous consistency are already measured',
            'At deadline record remaining precise scope in A7.c; then A7.dUV,A8,PartC afterA8,PartB/final per complete objective'],
        pending_orchestration='Official message: Kimi709 complete/audited, ledger once. C2.1 job3bafcf09-fb40-4080-9b4d-6237cc26fd6a executiona5b31f2f-f7a1-4734-95a9-d65ae2c0299c worker72209 coordinator-owned; C2.2..5 admitted. C2.5 job7bcb6868-f9ce-456c-b42e-f8d5dd6041c3. d3 staged subject20:32deadline. Do not poll coordinator workers via stdin.',
        partial_metered_cost_usd=str(cost))
    state['odd_ward_and_scalar_update']=result
    state['latest_verified_orchestration']['own_live_processes']=[]
    state['latest_verified_orchestration']['current_snapshot']=dict(at=now.isoformat(),source='Official coordinator message; no independent worker polling',
        completed_job='8639533b-6775-4a5c-8d7f-988659d58c2d',completed_audited=True,
        running_last_seen_job='3bafcf09-fb40-4080-9b4d-6237cc26fd6a',running_last_seen_execution='a5b31f2f-f7a1-4734-95a9-d65ae2c0299c',coordinator_worker=72209,
        C25_job='7bcb6868-f9ce-456c-b42e-f8d5dd6041c3',older_fields_are_history=True)
    put(p,state,True)
    append(OUT/'LEDGER_016.jsonl',json.dumps(dict(at=now.isoformat(),event='ODD_WARD_SCALAR_CHECKPOINT',
        accounting='AGGREGATE_EXISTING_BATCHES_DO_NOT_COUNT_AGAIN',snapshot=result,manifest_sha256=sha(D/'manifest.json')))+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: paridade corrigida da fonte;3escalares adicionados;consistência conjunta0/16 e primitiva plana.5lotes/{result["checks"]}controles CPU{result["cpu_seconds"]}s (não duplicar);custo conhecidoUSD{cost}. Q2curvaOPEN.Continuidade/custódia atualizadas.AberturaSHA256={opening}.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='batches'}),flush=True)

if __name__=='__main__':main()
