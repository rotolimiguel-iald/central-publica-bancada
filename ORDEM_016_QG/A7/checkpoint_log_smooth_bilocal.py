"""Checkpoint: preserve normalization corrections, final scalar contact, and C2 custody."""
from datetime import datetime,timezone
from pathlib import Path
import json
from deliver_nonminimal_wick_and_mimo_audit import H,OUT,BASE,sha,write,put,append

def main():
    now=datetime.now(timezone.utc);D=H/'log_smooth_bilocal_checkpoint';D.mkdir(exist_ok=False)
    runs=[('balanced_log_pair_v3','balanced_log_pair_run_v3.log',True),
        ('balanced_log_pair_v4','balanced_log_pair_run_v4.log',False),
        ('smooth_line_compatibility_v2','smooth_line_compatibility_run_v2.log',False),
        ('bilocal_scalar_euler_zerojet','bilocal_scalar_euler_zerojet_run.log',False)]
    manifests=[];batches=[];verified=[]
    for name,log,superseded in runs:
        folder=H/name;mp=folder/'manifest.json';manifests.append(mp)
        m=json.loads(mp.read_bytes());r=json.loads((folder/'results.json').read_bytes())
        for item in m['artifacts']:
            p=Path(item['path']);assert sha(p)==item['sha256'];verified.append(item)
        batches.append(dict(name=name,checks=r['checks'],cpu_seconds=r['cpu_seconds'],superseded=superseded,
            superseded_reason='Wrong sign of z multiplication in geometric term' if superseded else None,
            manifest_sha256=sha(mp),results_sha256=sha(folder/'results.json'),
            log=str(H/log),log_sha256=sha(H/log),observed_rc=0))
    cm=H.parent/'ADENDO_002_CRITICAS/C21_AUDIT/manifest.json';manifests.append(cm)
    for item in json.loads(cm.read_bytes())['artifacts']:
        assert sha(Path(item['path']))==item['sha256'];verified.append(item)
    failures=[]
    for script,log,reason in [
        ('balanced_log_pair_check.py','balanced_log_pair_run.log','Genuine smooth-line incompatibility: Euler(f,1)=3/4 not1'),
        ('balanced_log_pair_check_v2.py','balanced_log_pair_run_v2.log','Verifier used expand where rational cancellation required'),
        ('smooth_line_compatibility_check.py','smooth_line_compatibility_run.log','Wrong sign in density expectation; exposed the same z sign in geometric v3 term')]:
        failures.append(dict(script=str(H/script),script_sha256=sha(H/script),log=str(H/log),log_sha256=sha(H/log),
            observed_rc=1,reason=reason,cpu_seconds=None))
    # A failed external unit is terminal. Read only its explicitly handed-off receipt.
    fs=BASE/'state/handoffs/1ceac5cf-2093-4076-adea-1e335d25afb3_delivery.json'
    fd=BASE/'state/handoffs/kimi_C22_failure_diagnostic.json'
    job=json.loads(fs.read_bytes())['job'];ex=job['execution'];diag=json.loads(fd.read_bytes())
    assert ex['status']=='failed' and ex['result'] is None
    assert diag['terminal_event']['error']['name']=='APITimeoutError'
    failure=dict(at=now.isoformat(),event='C22_EXTERNAL_CRITIQUE_TIMEOUT_TERMINAL',target='ADENDO002.C2.2',
        provider='kimi',request_id=job['request_id'],job_id=job['id'],execution_task_id=ex['id'],
        status='failed',result=None,usage=None,cost_estimate_usd=None,unknown_not_zero=True,
        receipt_sha256=sha(fs),diagnostic_sha256=sha(fd),retry=False,
        next='C2.3 distinct unit explicitly authorized, coordinator owns worker19647')
    put(D/'C22_FAILURE.json',failure)
    ledger=OUT/'LEDGER_016.jsonl';rows=[json.loads(t) for t in ledger.read_text('utf-8').splitlines() if t.strip()]
    assert not any(t.get('event')==failure['event'] and t.get('execution_task_id')==ex['id'] for t in rows)
    c21=json.loads((cm.parent/'AUDIT.json').read_bytes())
    opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    result=dict(at=now.isoformat(),batches=batches,failed_attempts=failures,
        final_checks=sum(b['checks'] for b in batches if not b['superseded']),
        successful_run_cpu_including_superseded_seconds=sum(b['cpu_seconds'] for b in batches)+c21['cpu_seconds'],
        failed_attempt_cpu_unknown_not_zero=True,verified_manifest_entries=len(verified),
        unique_verified_artifacts=len({v['path'] for v in verified}),C21_manifest=str(cm),C22=failure,
        partial_metered_cost_usd='2.6912534940',subscription_and_failed_call_cost_unknown=True,
        final_scalar_curvature='CE*K/4 in densitized Euler two-endpoint zerojet; massless equal scalar profiles',
        smooth_compatibility='Constant line repaired canonically; full causal family not established',
        deadline_utc='2026-09-25T20:32:00Z',own_processes=[],full_Q2=False,gate_changed=False,
        opening_sha256=opening)
    put(D/'results.json',result)
    note=f'''[DERIVED+CAS — parcela escalar curva verificada; crítica externa confrontada]

R_bal ingênuo em f/log/1 falhou para a linha suave: Euler(f,1)=3/4,
Euler(1,f)=-1/4. O produto suave impõe1 e0. Esta subfamília foi corrigida;
os grafos planos f/f e sua montagem de Ward não foram alterados.

Correção ao lado: o sinal do termo z nas distribuições estava errado na
tabela v3. Duas multiplicações x produzem sinal positivo. A v4 e o teste
independente de dualidade corrigem o contato geométrico a+3/8 e a conversão
de densidade a-3/8. Os valores anteriores1/16,1/8,1/2 NÃO são os resultados
finais válidos. As tentativas e seus hashes foram preservados.

Cálculo bilocal: diferenciar antes de fixar y=0 e incluir sqrt(g) dá
CE*K/4 nas DUAS pontas para o escalar sem massa; omitir densidade deixa
diferença3/8. Escopo: jato escalar sem derivadas adicionais, O(K), prescrição
parcial euclidiana auxiliar. Não é Q2 inteira nem classe não nula demonstrada.

C2.1 Kimi confrontada: várias ligações cobradas já constam das fontes
completas (b2,b3,b5).23recibos e7paresfonte/logconferidos sem recompilar.
C2.2 terminou em timeout e permanece falha sem resposta; não foi repetida.
C2.3 é unidade distinta, autorizada e em execução pela coordenação.

{result['final_checks']}controles nos lotes finais (controles, não teoremas);
CPU{result['successful_run_cpu_including_superseded_seconds']}s inclui repetição
bem-sucedida superada e auditoriaC2.1. CPUtentativasfalhas desconhecida.
Gasto medido parcial US$2.6912534940; assinaturas/timeout não informados.
A7.b ainda ativo até20:32UTC; depois A7.c,d,A8,ParteC,ParteB e relatório.
AberturaSHA256={opening}. Originais/kernel/gate intactos.
'''
    write(D/'ENTREGA.md',note.encode());write(OUT/'ENTREGA_016_MEDIDA_custodia_curvatura_escalar.md',note.encode())
    refs=manifests+[D/'results.json',D/'C22_FAILURE.json',D/'ENTREGA.md',Path(__file__),fs,fd,
        H/'audit_c21_full_sources_run.log']+[H/log for _,log,_ in runs]
    put(D/'manifest.json',dict(artifacts=[dict(path=str(p),sha256=sha(p)) for p in refs],full_Q2=False))
    state=H/'CONTINUIDADE.json';j=json.loads(state.read_bytes())
    j.update(at=now.isoformat(),status='ACTIVE',previous_goal_turn='PROGRESS',own_processes=[],
        completed_this_turn=['General log/f/one profile table and genuine smooth-line defect',
            'Canonical smooth product subfamily and distribution duality caught/corrected geometric-density sign',
            'First-curvature scalar Euler contact equal at two endpoints after density',
            'C2.1 complete-source audit removes redundant proposed repairs; C2.2 terminal timeout recorded'],
        next=['A7.b only until2026-09-25T20:32:00Z; remaining vector/tensor curved vertices and globally admissible temporal family not inferred from scalar zerojet',
            'Do not reuse v3 geometric sign; v4 and smooth_v2 supersede it; final scalar densitized coefficient CE*K/4',
            'At timebox A7.c name missing Q2/contact family; do not assert nonzero cohomology class without full consistency',
            'Then A7.d typed UV, A8 proposal, ADENDO002PartC, ORDEM015PartB and final full audit'],
        pending_orchestration='C2.1 audited/accounted once. C2.2 terminal timeout execution0a16f9f1-0f94-4da9-8bdf-a7bded7ee8eb, no retry. C2.3 running job5cd7b089-26d0-415d-91d3-943bf00dead1 executionbd2072d7-7e6a-488b-bc3a-0ecd714632e7 worker19647 COORDINATOROWNED. C2.4/C2.5 FIFO; d3 staged only before20:32.',
        log_smooth_bilocal_update=dict(manifest=str(D/'manifest.json'),results=result))
    put(state,j,True)
    # One append per file in this process: include both new records in one write.
    event=dict(at=now.isoformat(),event='LOG_SMOOTH_BILOCAL_CUSTODY',target='A7.b',remote_call=False,
        manifest_sha256=sha(D/'manifest.json'),aggregate_not_additional_cpu=True)
    append(ledger,json.dumps(failure)+'\n'+json.dumps(event)+'\n')
    append(OUT/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} A7.b PROGRESS: contatoescalarbilocalK/4, linhasuavecompatível, errodesinalcorrigido;{result["final_checks"]}controlesfinais, Q2OPEN. C2.1confrontada,C2.2timeoutsemretry,C2.3distintarunning. AberturaSHA256={opening}.\n')
    print(json.dumps(dict(checks=result['final_checks'],cpu=result['successful_run_cpu_including_superseded_seconds'],verified=len(verified),manifest=str(D/'manifest.json'))))

if __name__=='__main__':main()
