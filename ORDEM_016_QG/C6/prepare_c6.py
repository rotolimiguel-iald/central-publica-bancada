"""Start the bounded Part-C Q2 continuation and prepare two distinct textual checks."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,sys,uuid,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'C6';H=ROOT/'A7';Q=D/'orchestration';Q.mkdir(exist_ok=False)
sys.path.insert(0,str(H))
from deliver_nonminimal_wick_and_mimo_audit import OUT,BASE,sha,put,append
now=datetime.now(timezone.utc)
put(D/'START.json',dict(at=now.isoformat(),deadline_utc=(now+timedelta(hours=8)).isoformat(),ceiling_hours=8,
    authority='ADENDO016002 PartC.C6; A7b remains closed',
    prescription='Continue the explicitly partial balanced f/f and f/log pair extension with the audited smooth-line completion; no mixing with Rraw',
    local_target='Densitized rank-two metric-pair Euler contact O(K), both endpoints, before vertex contractions',
    pending_dictionary='d3 original staged text may discuss Rraw; its answer must be reconciled, not used to replace the present pair prescription',
    scope='4D Euclidean auxiliary spaceform, sigma constant; not physical horizon, not Lorentzian causal completion',
    reuse=[str(H/'bilocal_first_curvature_engine.py'),str(H/'bilocal_covariant_jet_engine.py'),str(H/'bilocal_scalar_euler_zerojet.py')],
    no_new_physical_choice=True,opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')))
base='''ORDEM016 ParteC.C6, continuação limitada deQ2 após encerramentoA7b. Memória científica comum obrigatória, texto somente, sem execução alegada, sem originais/gate. Uma pergunta por unidade. Não completar automaticamente Q2 nem escolher partição. Use o auxiliar euclidiano4D espaço-forma, K constante, y mantido até finalizar derivadas; assinatura física não inferida. H0 e H1 são os já custodiados abaixo; não ajustar coeficientes. R_bal e sua correção de compatibilidade com linha suave são a prescrição parcial corrente; não misturar com Rraw nem presumir família causal completa.\n'''
units=[('mimo','rank_two_euler_parametrix_operator','draft',
'''Derive/verifique explicitamente o operador de Euler densitizado que atua na PRIMEIRA linha métrica H_ab,cd(x,y) de bilocal_first_curvature_engine.metric, a ordemK em ambas pontas. Candidato: sqrt(g)[roughBox h_ab -2K h_ab+2K g_ab tr(h)], com duas conexões covariantes em cada ponta. Ele satisfaz o parametrix fora da diagonal com a S1 e o log publicados? Mostre os termos de conexão, curvatura escalar e potencial, a ordem correta de derivar/ancorar e um controle não diagonal que possa rejeitar um sinal errado. Não inventar ghostWick/vértice novo; não calcular loopcompleto. Se candidato divergir, dê resíduo e origem, sem alterar a fonte para zerá-lo. Esta é uma NOVA unidadeC6após falha terminalMiMo46ftransversecocycle; não é retry dela.\n''',
[(H/'bilocal_first_curvature_engine.py',None),(H/'bilocal_covariant_jet_engine.py',None),(H/'bilocal_vector_euler_zerojet.py',(1,78))]),
('deepseek','rank_two_pair_zerojet_invariant_check','skeptic',
'''Qual é o contato local densitizado CE*K*delta ao aplicar o operador de Euler na primeira linha de um PAR de propagadores métricos H_ab,cd H_ef,gh, sem derivadas externas adicionais, usando EXATAMENTE o algoritmo pair_delta abaixo? Dê fórmula tensorial/invariantes ou redução exata verificável; se não alcançar, indique a etapa que impede. Operador candidato sqrt(g)(roughBox-2K Id+2K g tr), covariante em todos índices, com seus termos de conexão. Já foram medidos escalar CE*K/4 e vetor7CE*K delta_abdelta_cd/16 nessa prescrição; não são entradas para ajustar o tensor. Precisa comparar as duas pontas incluindo densidade e log e manter a ação apenas sobre a primeira linha. Não afirmar que zerojet é loopQ2, nem substituir cálculo por argumento de ausência de anomalia4D. O cálculo local será independente da sua resposta.\n''',
[(H/'bilocal_first_curvature_engine.py',None),(H/'bilocal_scalar_euler_zerojet.py',(1,62)),(H/'balanced_log_pair_engine.py',None),(H/'smooth_line_compatibility_check_v2.py',(1,95))])]
rows=[]
for provider,lemma,role,question,srcs in units:
    prompt=base+question;refs=[]
    for p,span in srcs:
        lines=p.read_text('utf-8-sig').splitlines();lo,hi=span if span else (1,len(lines));part=lines[lo-1:hi]
        ref=dict(path=str(p),sha256=sha(p),first_line=lo,last_line=lo+len(part)-1);refs.append(ref)
        prompt+='\nSOURCE '+json.dumps(ref,ensure_ascii=False)+'\n'+'\n'.join(f'{lo+i}: {line}' for i,line in enumerate(part))+'\n'
    assert len(prompt)<=20000,(provider,len(prompt))
    rid=str(uuid.uuid4());ec=dict(mission_id='ORDEM_016',branch_id='C6',lemma_id=lemma,role=role,required_provider=provider,max_calls=1,max_cost_usd=None,max_output_tokens=131072 if provider=='mimo' else 393216)
    payload=Q/(provider+'_submit.json');put(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=ec))
    put(Q/(rid+'_origin.json'),dict(at=now.isoformat(),thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',house='Central de Patentes',request_id=rid,payload=str(payload),payload_sha256=sha(payload),sources=refs,status='PREPARED_NOT_SUBMITTED'))
    a=subprocess.run([sys.executable,'-X','utf8','-B',str(BASE/'transport_cli.py')],input=json.dumps(dict(operation='preview_execution',prompt=prompt,execution_constraints=ec)),text=True,encoding='utf-8',capture_output=True,cwd=BASE)
    preview=json.loads(a.stdout);put(Q/(provider+'_preview.json'),dict(returncode=a.returncode,response=preview));assert a.returncode==0 and preview.get('selected')==provider
    rows.append(dict(provider=provider,request_id=rid,payload=str(payload),payload_sha256=sha(payload),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),sources=refs,preview=str(Q/(provider+'_preview.json')),prompt_chars=len(prompt),status='PREPARED_NOT_SUBMITTED'))
put(Q/'prepared_units.json',rows)
append(OUT/'LEDGER_016.jsonl',''.join(json.dumps(dict(at=now.isoformat(),event='C6_UNITS_PREPARED',remote_call=False,**row),ensure_ascii=False)+'\n' for row in rows))
print(json.dumps([dict(provider=x['provider'],request_id=x['request_id'],prompt_chars=x['prompt_chars']) for x in rows]))
