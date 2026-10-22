"""Report integrated code and the draft, keeping final activation explicitly unpaid."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json
from deliver_t03_source_qualification import sha,write,load
B=Path(__file__).resolve().parents[2];ROOT=B.parent;D=B/'bis/015/t03';OUT=ROOT/'TUNEL/DO_CHATGPT'
def main():
    now=datetime.now(timezone.utc)
    names=['guard_integration_tests_001/RESULT.json','guard_integration_tests_002/RESULT.json',
        'reading_failure_tests_001/RESULT.json','reading_failure_tests_002/RESULT.json',
        'null_covariance_tests_001/RESULT.json','statistics_001/RESULT.json']
    rows=[load(D/n) for n in names];cpu=sum(r['cpu_seconds'] for r in rows);wall=sum(r['wall_seconds'] for r in rows)
    candidate=D/'CANDIDATE_V1_1_001.json';draft=load(candidate);meta=load(D/'CANDIDATE_001_RECEIPT.json')
    assert sha(candidate)==meta['sha256']
    actual={p.relative_to(B/'bis/e2_code_v1_1').as_posix():sha(p) for p in (B/'bis/e2_code_v1_1').rglob('*.py')}
    assert actual==draft['own_code_tree_sha256']
    assert len(rows[1]['tests'])==34 and len(rows[3]['tests'])==44 and len(rows[4]['rows'])==24
    assert not (B/'RINGDOWN_5SIGMA_V1_1.json').exists() and not (B/'bis/PART_015_BUDGET_START.json').exists()
    costs={}
    for text in (OUT/'LEDGER_016.jsonl').read_text('utf-8-sig').splitlines():
        if not text.strip():continue
        r=json.loads(text);v=next((r[k] for k in ('cost_estimate_usd','cost_usd','custo_usd') if r.get(k) is not None),None)
        key=next((r[k] for k in ('execution_task_id','execution_id','request_id','job_id') if r.get(k)),None)
        if key and v is not None:costs[key]=Decimal(str(v))
    total=sum(costs.values(),Decimal(0));elapsed=(now-datetime.fromisoformat(load(D/'COPY_RECEIPT.json')['at'])).total_seconds()/3600
    opening015=sha(OUT/'ENTREGA_015_ABERTURA_operador.md');opening016=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    result=dict(status='T03_INTEGRATED_CODE_AND_DRAFT_NOT_REGISTERED',at=now.isoformat(),
        candidate_sha256=sha(candidate),evidence={n:sha(D/n) for n in names},
        latest_guard_controls=34,latest_reading_failure_controls=44,covariance_variants_compared=24,
        published_samples_measured=rows[5]['total_published_samples'],event_bootstrap_unit=31,bootstrap_draws=2000,
        measured_CPU_seconds_this_turn=cpu,measured_wall_seconds_this_turn=wall,other_local_CPU_unmeasured=True,
        bench_interval_since_copy_hours=elapsed,heavy_machine_hours=0,new_external_calls=0,partial_metered_cost_usd=str(total),
        opening015_sha256=opening015,opening016_sha256=opening016,
        metadata_count_correction=meta['metadata_count_correction'],code_tree_sha256=actual,
        next=['Before sealing bind R5 qualified source configuration to every registered/allocated job box (guard currently binds source/functions/results, not every job prior)',
              'Final candidate-level negative probes, source-scope and current-tree coverage; no witness until these pass',
              'Publish initial V1.1 and witness/activation receipt only, still no real clock/heavy job',
              'Then T05/T06/T11/T12 in order; versioned activation receipt handling for later subamendments needs explicit preservation of old cited receipt'])
    text=f'''[REAL — ligação e controles locais; rascunho V1.1, ainda não registrado]

Abertura015SHA256: {opening015}
Abertura016SHA256: {opening016}

checked_registration da cópia agora usa a cadeia V1.1 e a ativação própria. A ativação verifica recibo, testemunha, probes, resultado R5, entradas e escopo das funções qualificadas. Eventos cegos exigem também o recibo de auditoria da gerência. A cadeia de alocações verifica cada elo, seu pai, cronologia, testemunha, pino do config, licenças e preservação dos jobs anteriores; uma emenda nova não invalida automaticamente a alocação de um ancestral. Trinta e quatro controles integrados passaram em fixture, incluindo runtime real pinado e relógio sintético; nenhum recibo da gerência real foi criado.

blinding passa a autorizar por leitura e alvo, com recibo da mesma leitura/registro/dataset e sistemáticas verdes. A seleção retorna apenas colunas rotuladas pela leitura; não abre a semente nem libera posterior bruto compartilhado. Quarenta e quatro controles passaram, incluindo R-LIN abaixo/acima do alvo exato {rows[3]['target_R_LIN_exact']}, leituras sem alvo, ausência de identidade e exceções da PE. A saída excepcional ordinária registra contagem/fração/hash do EDOM sem fingir posterior disponível; uma inconsistência contador/log é falha explícita. Um sinal nativo fatal não executa esse handler Python: não se afirmou cobertura dele.

As 24 variantes V=0/KDE0,7/WLS reproduziram as projeções e caudas analíticas do DG11 arquivado. Nenhum sorteio dessas campanhas foi executado. Curtose medida em 608.681 amostras dos 33 produtos públicos; resíduos entre eventos medidos por leitura/população. Bootstrap de 2.000 reamostragens sobre os 31 EVENTOS, com WLS das médias posteriores, registrado como diagnóstico — não é bootstrap do ajuste KDE nem calibração de sigma_sys. Escala t5 comum continua INPUT, não conclusão da curtose.

Rascunho {candidate.name}: piloto novo só-220, geração4096/fs8192, banda20–1024, 30 células novas com IDs/sementes sem reutilização, extensões estatísticas fora do sub-objeto congelado, alvos por leitura, caudas homoscedásticas exatas e estrato O4b. O sub-objeto da V1 ficou idêntico. Nenhuma testemunha, ativação ou relógio real foi publicado.

Correção de contagem: a fonte contém 30 eventos sem censo e 8 sem elegibilidade; os 8 já estão dentro dos 30. Há 30 eventos distintos, não 38. O rascunho conserva as duas pendências por evento e não inventa oito candidatas adicionais; nenhuma promoção.

Antes de selar, falta ligar a qualificação R5 à caixa de cada job no leitor: o código já verifica a fonte e suas funções, mas não compara ainda toda prior de job com a configuração qualificada. O rascunho foi construído da configuração qualificada; a recusa a uma caixa alterada precisa ser explícita no leitor e na bateria final. Também será necessário conservar recibos de ativação anteriores quando vierem sub-emendas, sem sobrescrever artefato citado. São pendências operacionais localizadas, não novo teorema ou avanço do gate.

CPU medida neste turno {cpu:.3f}s, parede medida {wall:.3f}s; outras ações locais sem CPU medida. Intervalo desde cópia T03 {elapsed:.4f}h; pesada0h. Chamadas externas novas0; soma parcial deduplicada US${total}, sem atribuir zero a custos desconhecidos. Três payloads externos revisados permanecem sem envio, na pendência específica já comunicada.

Recibo: bis/015/t03/INTEGRATION_CANDIDATE_DELIVERY.json. RascunhoSHA256: {sha(candidate)}.
'''
    write(D/'INTEGRATION_CANDIDATE_DELIVERY.json',(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode())
    write(OUT/'ENTREGA_015_T03_integracao_e_rascunho.md',text.encode('utf-8'))
    p=OUT/'LEDGER_016.jsonl';write(p,p.read_bytes()+(json.dumps(dict(at=now.isoformat(),event='PARTB_T03_INTEGRATION_DRAFT',receipt=str(D/'INTEGRATION_CANDIDATE_DELIVERY.json'),new_external_calls=0,partial_metered_cost_usd=str(total)))+'\n').encode(),True)
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — B/T03 PARCIAL: entrada V1.1/alocações integradas34controles; leitura/falhas44; covariância24; curtose608681amostras e bootstrap31eventos. Rascunho pronto, sem registro; falta vínculo caixa↔R5/probes finais. Bancada desde cópia{elapsed:.4f}h; CPU medida{cpu:.3f}s; pesada0h; parcialUS${total}.\n'.encode(),True)
    p=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=load(p)
    state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_process=None,own_live_processes=[],
        T03_integration_candidate_delivery=str(D/'INTEGRATION_CANDIDATE_DELIVERY.json'),
        completed_this_turn=['checked_registration chain/activation and allocations wired;34 integrated controls',
            'Reading-specific release and EDOM exception audit;44 controls','24 covariance variants matched DG11',
            '608681 public samples kurtosis,31-event WLS bootstrap2000','V1.1 draft assembled;30 distinct metadata events vs38 overlapping mentions'],
        next='Finish T03: candidate D/t03/CANDIDATE_V1_1_001.json exists, draft only. Before witness add R5 qualified-config↔job box binding in guard (currently result/source/functions bound, priors not); update tests using real qualified cfg instead of job stubs. Final complete candidate mutation controls/current-tree pins then V1.1 witness/activation. Current guard34 tests and reading44 passed; null covariance changed after guard test002 but24 direct comparisons passed. Preserve earlier attempts. Later subamendment fixed activation receipt path conflicts with immutable prior cited receipt: resolve versioned preservation explicitly. Then T05 etc. No real clock/heavy job. C6 closed; external3payloads still awaiting specific approval.')
    write(p,(json.dumps(state,indent=2,ensure_ascii=False)+'\n').encode(),True)
    print(json.dumps({k:result[k] for k in ('status','latest_guard_controls','latest_reading_failure_controls','covariance_variants_compared','measured_CPU_seconds_this_turn','heavy_machine_hours')}))
if __name__=='__main__':main()
