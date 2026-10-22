"""Record this local increment; do not activate registration or start heavy work."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json
from deliver_t03_source_qualification import sha,write,load

B=Path(__file__).resolve().parents[2];ROOT=B.parent;D=B/'bis/015/t03';OUT=ROOT/'TUNEL/DO_CHATGPT'

def main():
    now=datetime.now(timezone.utc);proof=D/'clock_nulls_tests_001/RESULT.json';r=load(proof)
    assert r['status']=='R7_AND_NULL_ENTRY_CONTROLS_PASSED_NOT_REGISTERED'
    assert all(sha(B/'bis/e2_code_v1_1'/name)==pin for name,pin in r['files_sha256'].items())
    assert not (B/'bis/PART_015_BUDGET_START.json').exists()
    costs={}
    for line in (OUT/'LEDGER_016.jsonl').read_text('utf-8-sig').splitlines():
        if not line.strip():continue
        row=json.loads(line)
        amount=next((row[k] for k in ('cost_estimate_usd','cost_usd','custo_usd') if row.get(k) is not None),None)
        key=next((row[k] for k in ('execution_task_id','execution_id','request_id','job_id') if row.get(k)),None)
        if amount is not None and key:costs[key]=Decimal(str(amount))
    total=sum(costs.values(),Decimal(0))
    elapsed=(now-datetime.fromisoformat(load(D/'COPY_RECEIPT.json')['at'])).total_seconds()/3600
    opening015=sha(OUT/'ENTREGA_015_ABERTURA_operador.md');opening016=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    result=dict(at=now.isoformat(),status='T03_CLOCK_NULLS_CONTROLS_PAID_ACTIVATION_PENDING',
        evidence_sha256=sha(proof),patch_sha256=sha(D/'CLOCK_NULLS_PATCH_001.json'),
        tests=len(r['tests']),cpu_seconds=r['cpu_seconds'],wall_seconds=r['wall_seconds'],
        bench_elapsed_hours_since_copy=elapsed,heavy_machine_hours=0,new_external_calls=0,
        partial_metered_cost_usd=str(total),cost_scope='Metered receipts only; unknown costs remain unknown',
        opening015_sha256=opening015,opening016_sha256=opening016,
        pending=['checked_registration latest-chain/activation integration','Allocation chain',
                 'Reading-specific blinding','New statistical design/covariance variants',
                 'EDOM reporting on exceptional exit','Full end-to-end mutation controls and registration witness'])
    text=f'''[REAL — controles locais; T03 parcial, registro ainda não ativado]

Abertura015SHA256: {opening015}
Abertura016SHA256: {opening016}

O time_guard da cópia irmã agora lê a regra R7 e exige relógio, testemunha, recibo de máquina livre e origem do orçamento conferidos. Valida os 168h de calendário, o saldo com todos os dígitos, a cronologia e eventual redução expressa registrada na abertura. Uma sub-emenda posterior não reinicia o relógio. Ausência/alteração de recibos e arquivo, orçamento arredondado/aumentado, início precoce ou futuro, prazo errado, testemunha ambígua e prazo vencido são recusados.

null_runner e null_campaign consultam exclusivamente nulls_v1_1.cells; IDs da V1 são recusados antes de simulação/subprocesso. O recibo de campanha usa nome V1.1 com hash do registro, preservando o antigo. Isso ainda não implementa as novas variantes de covariância nem executa suas simulações.

{len(r['tests'])} controles passaram em fixture isolada, incluindo chamadas reais dos pontos de entrada dos nulos com autorização simulada. CPU {r['cpu_seconds']:.6f}s; parede {r['wall_seconds']:.6f}s. Nenhuma semente real, strain ou posterior cego foi lido. O relógio real não existe; pesada 0h. As três árvores antigas de código conferiram contra os pinos do registro V1.

A entrada checked_registration ainda precisa ser ligada à cadeia e à ativação V1.1; portanto estes controles não são ativação nem liberação científica. Alocações, descegamento por leitura, desenho estatístico e bateria completa continuam pendentes. A qualificação R5 anterior permanece restrita à fonte/runner.

Antigravity: tarefa documental T01 já preparada sob request_id preservado338e46bc-512c-499c-9a41-db9f5e8e8dbf, não submetida. A revisão automática anterior recusou o envio dos três payloads revisados, exigindo consentimento específico para memória/trechos científicos. Confirmação pendente; zero chamadas externas novas. Soma parcial deduplicada do ledger US${total}; custos desconhecidos não viraram zero.

Evidência: bis/015/t03/clock_nulls_tests_001/RESULT.json, SHA256 {sha(proof)}.
Desde a criação da cópia T03: {elapsed:.4f}h de intervalo de bancada; não é medição de máquina pesada.
'''
    write(OUT/'ENTREGA_015_T03_relogio_nulos_controles.md',text.encode('utf-8'))
    write(D/'CLOCK_NULLS_DELIVERY.json',(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
    p=OUT/'LEDGER_016.jsonl'
    write(p,p.read_bytes()+(json.dumps(dict(at=now.isoformat(),event='PARTB_T03_CLOCK_NULLS_CONTROLS',receipt=str(D/'CLOCK_NULLS_DELIVERY.json'),new_external_calls=0,partial_metered_cost_usd=str(total)))+'\n').encode(),True)
    p=OUT/'ENTREGA_016_PROGRESSO.md'
    write(p,p.read_bytes()+f'\n{now.isoformat()} — B/T03 PARCIAL: R7 e entradas nulas31controles em fixture, originais preservados; ativação/cadeia principal ainda pendentes. Bancada desde cópia{elapsed:.4f}h; CPU{r["cpu_seconds"]:.6f}s; pesada0h. Soma parcialUS${total}; 0chamadas externas novas.\n'.encode(),True)
    p=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=load(p)
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_process=None,own_live_processes=[],
        T03_clock_nulls_delivery=str(D/'CLOCK_NULLS_DELIVERY.json'),
        completed_this_turn=['R7 time_guard implemented in sibling copy; real clock absent',
                            'Null entry points reject V1 IDs and preserve old campaign receipt',
                            '31 local fixture controls passed; original code trees checked'],
        next='Continue T03: checked_registration STILL reads old V1/check_activation; wire to latest V1.1 chain and new activation with probes/R5 receipts. R7 time_guard and new null cell selection now implemented and fixture-tested31; no real clock. Implement allocation chain, reading-specific blinding, covariance variants/statistical design, exceptional-exit EDOM receipt, end-to-end probes then witness. External 3 revised payloads awaiting specific approval; do not resubmit. C6 closed.')
    write(p,(json.dumps(state,indent=2,ensure_ascii=False)+'\n').encode(),True)
    print(json.dumps({k:result[k] for k in ('status','tests','cpu_seconds','new_external_calls','partial_metered_cost_usd')}))

if __name__=='__main__':main()
