from pathlib import Path
import datetime,hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[1]
out=root.parent/'TUNEL/DO_CHATGPT'
stamp=datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,b):
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.rename(p)
def replace_with_backup(p,b):
    old=p.read_bytes()
    create(p.with_name(p.name+'.bak_'+stamp.strftime('%Y%m%d_%H%M%S_%f')),old)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    t.replace(p)
def append(p,b):replace_with_backup(p,p.read_bytes()+b)
folder=root/'A1/probes'
src=folder/'ProbeNoncommutingInternal_v4.lean'
log=folder/'noncommuting_internal_04.log'
rec=folder/'noncommuting_internal_04.json'
d=json.loads(rec.read_text())
assert d['rc']==0 and not d['newer_kernel_files'] and not d['scan_errors']
assert sha(src)==d['source_sha256'] and sha(log)==d['log_sha256']
a=subprocess.run([sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),str(src),str(log)],capture_output=True)
assert a.returncode==0,a.stdout+a.stderr
create(folder/'noncommuting_internal_axioms.json',a.stdout)
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
v2=folder/'ProbeNoncommutingInternal_v2.lean'
v3=folder/'ProbeNoncommutingInternal_v3.lean'
same=sha(v2)==sha(v3)
report=f'''[REAL] A-1.b1 — controle não comutante e rejeição por fidelidade.

Abertura SHA256: {opening}

[DERIVED — Lean isolado] V=C³, Ω=e0; U(a)=diag(1,exp(i*a0),1); D(t) fixa e0 e gira o plano (e1,e2). Foram provadas continuidade, leis de grupo, unitariedade matricial e preservação de Ω. Para a=(π,0,0,0), t=π/2 e ψ=e1, D(t)U(a)ψ≠U(a)D(t)ψ. Assim o controle está fora da hipótese de commuting_translations_excluded.

Mas U(0,1,0,0)=I. O teorema contract_rejects_this_translation_action recebe o ContratoH2 REAL e uma leitura injetiva entrelaçando suas translações com o controle; deriva contradição precisamente de translations_faithful. Não usa a parede de comutação. Não se construiu W, rede ou realização modular a partir das matrizes, nem se identificou D com um fluxo modular verdadeiro. Esta é uma rejeição condicional por campo, não um arquivo negativo rc 1 de preenchimento do registro.

Quatro compilações; rc final 0; 16 declarações auditadas no trio, sem sorry/axioma novo. As falhas iniciais eram de redução de notação e conjugação dos coeficientes reais. ERRO OPERACIONAL preservado: v3 ficou byte-idêntica a v2 ({same}), pois a substituição não encontrou o texto; sua repetição não foi avanço matemático. Após diagnosticar isso, v4 aplica a mudança com assert e fecha. Não excedeu seis ciclos.

Fonte {src} SHA256 {sha(src)}
Log {log} SHA256 {sha(log)}
Recibo/comando {rec} SHA256 {sha(rec)}
Auditoria {folder/'noncommuting_internal_axioms.json'} SHA256 {sha(folder/'noncommuting_internal_axioms.json')}
Passe final: {d['wall_seconds']}s parede; {d['cpu_user_seconds']+d['cpu_kernel_seconds']}s CPU; pico committed {d['peak_process_committed_bytes']} bytes; zero alteração canônica detectada. Não move gate. Próximo A-2.1.
'''
create(out/'ENTREGA_016_A1b1_controle_nao_comutante.md',report.encode())

receipts=[]
for p in (root/'A1').rglob('*.json'):
    try:x=json.loads(p.read_text(encoding='utf-8'))
    except (ValueError,UnicodeError):continue
    if not isinstance(x,dict) or not {'command','wall_seconds','cpu_user_seconds','cpu_kernel_seconds','rc','source_sha256'}<=x.keys():continue
    receipts.append({'file':str(p),'sha256':sha(p),'rc':x['rc'],'utc':x['utc'],
      'wall_seconds':x['wall_seconds'],'cpu_seconds':x['cpu_user_seconds']+x['cpu_kernel_seconds']})
wall=sum(x['wall_seconds'] for x in receipts)
cpu=sum(x['cpu_seconds'] for x in receipts)
start=min(datetime.datetime.fromisoformat(x['utc']) for x in receipts)
bench=(stamp-start).total_seconds()/3600
ledger=[json.loads(l) for l in (out/'LEDGER_016.jsonl').read_text().splitlines() if l]
cost=sum(float(x.get('custo_usd') or 0) for x in ledger)
tokens=sum(sum(int(x.get(k) or 0) for k in ['tokens_in','tokens_cache','tokens_out']) for x in ledger)
summary={'utc':stamp.isoformat(),'opening_sha256':opening,'all_compile_receipts':receipts,
 'wall_hours_summed':wall/3600,'cpu_hours_summed':cpu/3600,'observed_bench_elapsed_hours':bench,
 'external_cost_usd':cost,'executor_tokens':tokens,'A1a':'MEDIDA: original reproduction resource failure',
 'A1b':'five controls compiled in the precise conditional scopes of individual reports',
 'A1c':'typed expectation-valued tensor refinement; operator locality remains OPEN',
 'gate_moved':False,'next':'A-2.1'}
create(root/'A1/A1_delivery_manifest.json',json.dumps(summary,ensure_ascii=False,indent=2).encode())
reports=['MEDIDA_A1a_memoria','A1b1_controle_nao_comutante','MEDIDA_A1b2_tensor_forjado',
 'A1b3_consumidor_energia_positiva','A1b4_controle_nao_KMS','A1b5_campos_com_mordida','A1c_extensao_tensor']
links='\n'.join(f'- ENTREGA_016_{s}.md SHA256 {sha(out/("ENTREGA_016_"+s+".md"))}' for s in reports)
final=f'''[REAL] A-1 — contrato auditado com resultados e limitações medidos.

Abertura SHA256: {opening}

| Ramo | Resultado verificado |
|---|---|
| a | MEDIDA/NÃO PAGO na reprodução integral: duas falhas de memória em 8 GiB; corpo do tipo v3.1 preservado em variante de imports e trechos literais selecionados recompilados. Não se afirma reproduzir seis negativos originais. |
| b1 | Controle contínuo unitário não comutante construído; comparação com H2 rejeitada por fidelidade. Nenhuma rede física fabricada. |
| b2 | Transformação condicional H3→H3 com tensor não simétrico preserva a leitura nula e resposta. Não prova não-localidade de operadores. |
| b3 | Consumidor analítico de PositiveEnergy exclui modo unitário de frequência negativa. |
| b4 | KMSAt rejeita fluxo identidade quando as duas expectativas de borda não coincidem. |
| b5 | Remover suavidade/normalização admite controles explícitos; hipótese T(0)=theta(0)=0 dita para o segundo. |
| c | Proposta StressTensorDataLocal: simetria, conservação por testes integráveis e covariância por boost; herda janelas/controles H3 e rejeita b2. Localidade de operadores OPEN. |

Os resultados condicionais não habitam o H2/H3 físico. Não movem a fronteira ou gate. Auditor externo de outro provedor ainda NÃO executado: a seleção por provedor/teto está indisponível, com manutenção na tarefa responsável. Não tratar auditoria mecânica como parecer externo. MiMo rascunho A1b1 dispensado antes de qualquer submit para evitar trabalho redundante; nenhuma chamada externa na missão até aqui.

Recursos de todas as {len(receipts)} compilações registradas em A1, incluindo falhas: {wall/3600:.9f}h parede somada e {cpu/3600:.9f}h CPU. Intervalo de bancada observado desde o primeiro recibo: {bench:.6f}h (inclui esperas, não medição de raciocínio ativo). B pesada: 0h. Ledger por script: US${cost}, tokens executores {tokens}; uso coordenador não medido pelo ledger.

{links}

Manifesto A1/A1_delivery_manifest.json SHA256 {sha(root/'A1/A1_delivery_manifest.json')}.
Próximo: A-2.1, quatro pontes de boost. A-1 permanece entregue COM MEDIDAS, sem apagar os itens não pagos.
'''
create(out/'ENTREGA_016_A1_contrato.md',final.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{stamp.isoformat()} | A-1 | entregue COM MEDIDAS; b1 finalizado, a reprodução integral e crítica externa não pagas | bancada observada {bench:.6f}h; Lean total {wall/3600:.9f}h parede, {cpu/3600:.9f}h CPU; ledger US${cost}, tokens {tokens}; B pesada 0h | A-2.1 próximo.\n'.encode())

# Prepared only, never submitted: retain UUID/prompt and mark obsolete before use.
for p in [root/'A0/delegation_a1b1.json',root.parent/'IALD_ORQUESTRACAO_20260923/state/session_requests/3529180f-e29d-4c42-94ef-f0fbba21771b.json']:
    x=json.loads(p.read_text(encoding='utf-8'))
    assert x['job_id'] is None and x['status']=='prepared_not_submitted'
    x['status']='superseded_before_submission'
    x['superseded_at']=stamp.isoformat()
    x['reason']='Local finite control completed; do not spend a draft call on completed work. Independent review remains pending.'
    replace_with_backup(p,json.dumps(x,ensure_ascii=False,indent=2).encode())
print(json.dumps({'b1_audit':json.loads(a.stdout)[0]['auditoria'],'compilations':len(receipts),'A1_report':str(out/'ENTREGA_016_A1_contrato.md'),'sha256':sha(out/'ENTREGA_016_A1_contrato.md'),'next':'A-2.1'}))
