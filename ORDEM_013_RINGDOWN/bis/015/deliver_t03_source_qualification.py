"""Deliver R5 scope without claiming V1.1 activation or finishing T03."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
B=Path(__file__).resolve().parents[2];ROOT=B.parent;D=B/'bis/015/t03';OUT=ROOT/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
def write(p,raw,replace=False):
    if p.exists():
        assert replace;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
def main():
    a=load(D/'R5/generation_2048/RESULT.json');b=load(D/'R5/generation_4096/RESULT.json');c=load(D/'R5_SOURCE_CLOSING.json')
    tests=load(D/'source_tests_001/RESULT.json');native=load(D/'native_bin_control_001/RESULT.json');chain=load(D/'chain_tests_002/RESULT.json')
    assert a['status']=='R5_NOT_QUALIFIED' and b['status']=='R5_SOURCE_ONLY_QUALIFIED'
    assert b['returns']==1015 and not b['crashes'] and b['status_counts']=={'FINITE_WAVEFORM':1015}
    assert tests['source_sha256']==sha(B/'bis/e2_code_v1_1/pseob_source.py')
    assert tests['runner_sha256']==sha(B/'bis/e2_code_v1_1/pe_runner.py')
    assert chain['guard_sha256']==sha(B/'bis/e2_code_v1_1/registration_guard.py')
    ledger=[json.loads(x) for x in (OUT/'LEDGER_016.jsonl').read_text('utf-8-sig').splitlines() if x.strip()];costs={}
    for row in ledger:
        value=next((row[k] for k in ('cost_estimate_usd','cost_usd','custo_usd') if row.get(k) is not None),None)
        key=next((row[k] for k in ('execution_task_id','execution_id','request_id','job_id') if row.get(k)),None)
        if value is not None and key:costs[key]=Decimal(str(value))
    total=sum(costs.values(),Decimal(0));cpu=sum(r['cpu_seconds'] for r in [a,b,c,tests,native]);wall=sum(r['wall_seconds'] for r in [a,b,c,tests,native])
    evidence={str(p.relative_to(D)):sha(p) for p in [D/'R5/INPUT_MANIFEST.json',D/'R5/generation_2048/RESULT.json',D/'R5/generation_4096/RESULT.json',D/'R5_SOURCE_CLOSING.json',D/'source_tests_001/RESULT.json',D/'native_bin_control_001/RESULT.json',D/'chain_tests_002/RESULT.json']}
    elapsed=(now-datetime.fromisoformat(load(D/'COPY_RECEIPT.json')['at'])).total_seconds()/3600
    result=dict(at=now.isoformat(),status='T03_SOURCE_R5_PAID_GUARD_INTEGRATION_PENDING',source_generation_hz=4096,generation_sample_rate_hz=8192,analysis_band_hz=[20,1024],
      source_controls=len(tests['tests']),chain_controls=len(chain['tests']),native_comparison_calls=4,r5_cases_per_branch=1015,
      source_cpu_seconds_measured=cpu,source_wall_seconds_measured=wall,other_local_test_cpu_seconds=None,bench_elapsed_hours_since_copy=elapsed,
      heavy_machine_hours=0,new_external_calls=0,partial_metered_cost_usd=str(total),metered_execution_or_request_count=len(costs),evidence=evidence,
      source_runtime_scope=c['source_only_scope'],first_failed_generation=a['failures'],
      pending=['Wire V1.1 chain to checked_registration and new activation receipt','Allocation chain and R7 time_guard','Null runners use only new cells and forbid V1 ids','Reading-specific blinding and data-census promotions','Statistical extensions/registration design artifacts','Full mutation probes and immutable witness; no heavy job before machine-free receipt and R7'],
      opening015_sha256=sha(OUT/'ENTREGA_015_ABERTURA_operador.md'),opening016_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
    text=f'''[REAL — R5 da fonte qualificada; T03 ainda parcial; nenhum teste físico]

Abertura015SHA256: {result['opening015_sha256']}
Abertura016SHA256: {result['opening016_sha256']}

Na cópia irmã, pe_runner/pseob_source separam banda20–1024 da geração. O gerador usa fmax4096/fs8192 e devolve os bins exatos da grade de dados fs4096. A asserção de overflow precede o LAL. Retornos None/EDOM são escritos em EDOM_LOG.jsonl com massa/spin/hora, contados e cruzados com o hiper-retângulo posterior0,5%–99,5%; EDOM dentro dele impede aceitação. Quinze controles locais e quatro chamadas nativas de comparação passaram; erro máximo entre wrapper e referência na mesma grade =0. Não se comparou uma amostragem com outra como se fossem idênticas.

R5 executada source-only:1.000sorteios pelo build_priors emendado,3casos históricos(DRAW8,16,20) com440fixoRG e12cantos dentro da prior. A2048:1.013finitos+2EDOM,0aborto ⇒ NÃO QUALIFICADO. Ambos EDOM têm massas15/10 e spins0,99. f550RG nesse canto={c['minimum_mass_max_spin_corner']['f550_GR_hz']:.9f}Hz. A4096/8192 nos MESMOS1.015casos:1.015finitos,0EDOM,0aborto ⇒ R5 da fonte qualificada. Essa amostragem finita não prova ausência universal de erro no contínuo da prior.

Proveniência C04: quatro scripts e draws400 copiados com hashes, originais preservados. O supervisor conserva PRECALL/RETURN e recibos por filho; falha não vira rejeição física do prior. Os testes não leram strain, posterior cego ou semente real e não iniciaram PE. A V1 ainda retorna TimeoutError esperado após verificar seu contrato/runtime.

Guarda: funções de cadeia adicionadas ao módulo existente,18controles passaram, incluindo sub-objeto estatístico imutável, célula V1 reutilizada, pai errado, testemunha alterada, lacuna ordinal, job substituído e promoção antes da primeira testemunha. A primeira implementação presumiu lista para nulls.cells; a fonte é dicionário por ID, corrigido antes dos controles, tentativa preservada. Pins históricos vêm dos bytes. As funções AINDA NÃO estão ligadas a checked_registration: não há registro/testemunha V1.1 nem liberação de execução. A qualificação R5 cobre fonte/build_priors/validação/contrato temporal, não a ativação futura. Helpers de cadeia mudaram depois do import do filho; fonte e runner ficaram idênticos e os utilitários importados preservaram o AST, registrados no recibo de fechamento.

CPU medida dos recibos de fonte/controles={cpu:.3f}s; parede={wall:.3f}s; CPU de testes locais de cadeia não medida. Intervalo desde cópiaT03={elapsed:.4f}h. Máquina pesada0h. Chamadas externas novas0; soma parcial deduplicada do ledgerUS${total}, sem converter assinaturas/falhas de uso desconhecido em zero.

Próximo: ligar cadeia/ativação/alocações/relógioR7, novos nulos e descegamento por leitura, concluir desenho e probes, só então emitir testemunha. A geração4096 já está selecionada pela regraR4, sem mudar a prior. Ainda falta garantir relatório EDOM também em saída excepcional da PE e integrar geração explícita às injeções no ramo autorizado correspondente.
'''
    write(OUT/'ENTREGA_015_T03_R5_fonte.md',text.encode());write(D/'SOURCE_DELIVERY.json',(json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode())
    p=OUT/'LEDGER_016.jsonl';write(p,p.read_bytes()+(json.dumps(dict(at=now.isoformat(),event='PARTB_T03_SOURCE_R5_DELIVERED',receipt=str(D/'SOURCE_DELIVERY.json'),new_external_calls=0,partial_metered_cost_usd=str(total)))+'\n').encode(),True)
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — B/T03 PARCIAL: R5 a2048 recusada2EDOM; a4096=1015/1015finitos,0EDOM/aborto. Guarda18controles ainda sem ligação. Bancada{elapsed:.4f}h; CPU medida{cpu:.3f}s; pesada0h. Soma parcialUS${total}; custos desconhecidos preservados.\n'.encode(),True)
    p=ROOT/'ORDEM_016_QG/A7/CONTINUIDADE.json';state=load(p);state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_process=None,T03_source_delivery=str(D/'SOURCE_DELIVERY.json'),
      next='Continue T03: guard chain helpers tested18 but not wired. Implement activation receipt, allocation/R7, new null cells and reading-specific blinding; statistical design and full negative probes before witness. Source/runner R5 qualified4096/8192(1015/1015), source+runner hashes unchanged. EDOM failure-exit reporting remains. No R7/heavy job. External revised3payloads awaiting specific approval. C6 stays closed.')
    state['completed_this_turn']=['Generation/source/runner amendments in copy','15 focused source controls +4 native comparison calls','R5 2048 failed2EDOM then4096 qualified1015 finite','18 chain helper controls, original statistical subobject hash computed; not yet wired']
    write(p,(json.dumps(state,indent=2,ensure_ascii=False)+'\n').encode(),True)
    print(json.dumps({k:result[k] for k in ['status','source_cpu_seconds_measured','partial_metered_cost_usd','new_external_calls','heavy_machine_hours']}))
if __name__=='__main__':main()
