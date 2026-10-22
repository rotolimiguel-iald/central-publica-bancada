"""Audit successful proof artifacts, adjudicate criticism and preserve continuation."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import sys,re,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'D6';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha
def main():
    now=datetime.now(timezone.utc);opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
    batches=[('RecognitionGraph_v2.lean','graph_02',7),('RecognitionSquare.lean','square_01',3),('RecognitionModular_v2.lean','modular_02',7),('RecognitionReadout.lean','readout_01',3),('RecognitionInverse_v2.lean','inverse_02',2),('ContentContractProposal.lean','contract_01',2)]
    artifacts=[];names=[]
    for fn,label,count in batches:
        s=D/fn;rp=D/(label+'.json');lp=D/(label+'.log');r=json.loads(rp.read_bytes())
        assert r['rc']==0 and r['source_sha256']==sha(s) and r['log_sha256']==sha(lp)
        assert not r['newer_kernel_files'] and not r['scan_errors']
        assert not re.search(r'\b(sorry|axiom)\b',s.read_text('utf-8'))
        ax=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",lp.read_text('utf-8-sig'))
        assert len(ax)==count
        assert all(set(a.strip() for a in v.split(','))<={'propext','Classical.choice','Quot.sound'} for _,v in ax)
        names.extend(n for n,_ in ax)
        artifacts.append(dict(source=str(s),source_sha256=sha(s),receipt_sha256=sha(rp),log_sha256=sha(lp),declarations=dict(ax),wall_seconds=r['wall_seconds'],cpu_seconds=r['cpu_user_seconds']+r['cpu_kernel_seconds']))
    assert len(names)==len(set(names))==24
    controls=[json.loads((D/f'FINITE_CONTROL_{i:03}.json').read_bytes()) for i in (1,2)]
    assert all(t['passed'] for c in controls for t in c['tests'])
    kp=D/'orchestration/kimi_graph_critic_delivery.json';k=json.loads(kp.read_bytes());answer=k['job']['execution']['result']['text']
    assert hashlib.sha256(answer.encode()).hexdigest()==k['response_sha256']
    write(D/'KIMI_GRAPH_CRITIC.txt',answer.encode())
    lid='f12e7df1-c4cb-4966-933a-41a4cecc32b4';p=OUT/'LEDGER_016.jsonl';raw=p.read_bytes()
    ledger=[json.loads(line) for line in raw.decode('utf-8-sig').splitlines() if line.strip()]
    if not any(e.get('execution_id')==lid or e.get('execution_task_id')==lid for e in ledger):
        entry=dict(at=now.isoformat(),provider='kimi',branch='D6',role='skeptic',request_id=k['job']['request_id'],job_id=k['job']['id'],execution_id=lid,status='completed',usage=k['usage'],cost_usd=None,cost_status=k['cost_status'],response_sha256=k['response_sha256'],receipt_sha256=sha(kp),scientific_status='DECLARADO_CRITIQUE_OF_GRAPH_ONLY_NOT_NEW_MODULAR_FILES')
        write(p,raw+(json.dumps(entry,ensure_ascii=False)+'\n').encode(),True);ledger.append(entry)
    costs={}
    for e in ledger:
        key=next((e[q] for q in ['execution_task_id','execution_id','request_id','job_id'] if e.get(q)),None)
        cost=next((e[q] for q in ['cost_estimate_usd','cost_usd','custo_usd'] if e.get(q) is not None),None)
        if key and cost is not None:costs[key]=Decimal(str(cost))
    partial=sum(costs.values(),Decimal(0))
    failed=[json.loads((D/f'{l}.json').read_bytes()) for l in ['graph_01','modular_01','inverse_01']]
    cpu=sum(a['cpu_seconds'] for a in artifacts)+sum(r['cpu_user_seconds']+r['cpu_kernel_seconds'] for r in failed)
    wall=sum(a['wall_seconds'] for a in artifacts)+sum(r['wall_seconds'] for r in failed)
    result=dict(at=now.isoformat(),status='D6_CONDITIONAL_RECOGNITION_CHAIN_KERNEL_CHECKED_PHYSICAL_INSTANCE_OPEN',opening_sha256=opening,artifacts=artifacts,
      declarations=24,finite_checks=sum(len(c['tests']) for c in controls),finite_control_sha256=[sha(D/f'FINITE_CONTROL_{i:03}.json') for i in (1,2)],
      failed_cycles_preserved=['graph_01','modular_01','inverse_01'],compile_cpu_seconds_including_failures=cpu,compile_wall_seconds_including_failures=wall,
      same_hilbert_analytic_bridge=True,cross_hilbert_graph_bridge=True,
      conditional_obligation='PairTomitaAnalyticRealizationMeasured for each independently specified physical pair/flow/J',
      remaining=['Instantiate the named analytic realizations on the selected photon net, not by defining the target as a conjugate copy.','Connect the proposed clause to the physical contract after these witnesses; no physical ContratoH2 inhabitant supplied.','New modular/readout files were compiled, not externally reviewed by the Kimi graph-only critique.'],
      kimi_receipt_sha256=sha(kp),kimi_response_sha256=k['response_sha256'],kimi_usage=k['usage'],kimi_cost=None,
      partial_metered_cost_usd=str(partial),unknown_costs_not_zero=True,gate_changed=False,canonical_files_written=False,ringdown_started=False)
    save(D/'MODULAR_BRIDGE_DELIVERY.json',result)
    adjudication='''[DERIVED — revisão local do parecer; REAL apenas nos recibos de execução citados]

Parecer Kimi recebido como crítica, não como prova. Ele examinou RecognitionGraph_v2 e o primeiro controle; não examinou as fontes modulares produzidas posteriormente.

ACEITO: acrescentar inversa do reconhecimento e igualdade dos domínios; explicitar realização analítica de cada par; testar U diferente de sua inversa, fluxo imaginário e referência não separante. Implementado em RecognitionInverse_v2 (rc0/trio), RecognitionModular_v2/RecognitionReadout e FINITE_CONTROL_002 (13 checks adicionais).

CORRIGIDO: target_graph não pode ser eliminado para T previamente fornecido e arbitrário. A fonte permite CONSTRUIR um transportado; isso não identifica automaticamente um T independente. Manter realizações separadas não é circularidade: nenhuma contém comparação por U.

CORRIGIDO: a existência de um grafo fechado não exige, por si, vetor cíclico e separante. Contraexemplo: omega=0, em H não nulo, produz o grafo {(0,0)}, realizado pelo operador de domínio {0}; não é cíclico nem separante. As hipóteses padrão são suficientes para a teoria modular, não equivalentes ao campo source_graph isolado.

CORRIGIDO: rotação 3-4-5 tem denominador5, portanto não é diádica. O segundo controle usa V=[[0,1],[i,0]], com V diferente de V*, entradas gaussianas diádicas. Exp/log do fluxo usa tolerância explícita, não é rotulado aritmética exata.

REFINADO: positividade verificada somente em elementos de uma base não basta em geral. O segundo controle também verifica que a matriz COMPLETA dos meios-operadores nessa base é diagonal com entradas reais estritamente positivas. As fórmulas candidatas de J2 são verificadas pela regra de Tomita obtida diretamente do novo par e pela fatoração; a igualdade de transporte isolada não é vendida como descoberta.

REUTILIZAÇÃO: os lemas gerais de raiz e potências imaginárias já estão em V350PositiveRootIntertwining e V351ResolventImaginaryIntertwining. A alegação genérica de infraestrutura ausente não vale para esta rota limitada pelo resolvente. A nova ligação compilou sem um segundo cálculo funcional. Restam testemunhas analíticas da rede escolhida, como documentado no predicado nomeado.
'''
    write(D/'KIMI_ADJUDICACAO.md',(adjudication+'\nAbertura SHA256: '+opening+'\nParecer SHA256: '+k['response_sha256']+'\n').encode())
    note=f'''[REAL — cadeia condicional compilada na bancada; OPEN — instanciação física]

Abertura016 SHA256: {opening}

O adendo003c rege a missão: rede do fóton h=±1, gráviton como forma conjugada [INPUT/ONTO], D6 primeiro; os antigos D1/D2/D3 cancelados. Nenhuma leitura ontológica virou premissa matemática oculta.

D6 agora encadeia reconhecimento do par → grafo fechado de Tomita → grafo de S* S → resolvente → raiz positiva/fator polar → potências imaginárias → fluxos fornecidos independentemente. A cadeia reutiliza V350PositiveRootIntertwining e V351ResolventImaginaryIntertwining. A cláusula final é same_horizon_by_content_from_realizations, em ContentContractProposal.lean. Dá U J U*=Jprime e U flow(t) U*=flowprime(t), para pares representados no mesmo Hilbert. O transporte de grafos admite Hilberts distintos. Não confundir esse recorte com uma construção de qualquer rede.

24 declarações auditadas no trio, zero sorry/axioma novo nas fontes bem-sucedidas. Ciclos: grafo2, quadrado1, modular2, leitura1, inversa2, contrato1; tentativas falhas preservadas. CPU de compilação total {cpu:.6f}s; parede somada {wall:.6f}s, incluindo falhas. Dois controles finitos: 18+13 verificações; defeitos antigos2/9; novo controle de fluxo rejeita referência errada com defeito quadrado {controls[1]['wrong_reference_flow_defect_squared']:.16g}. Erro máximo positivo {controls[1]['max_flow_error']}, tolerância {controls[1]['flow_tolerance']}; isso não transforma teste finito em prova de rede.

O que falta fica nomeado: PairTomitaAnalyticRealizationMeasured para cada par físico. Exige realizar o grafo/resolvente/fator polar de cada lado e caracterizar seu próprio fluxo numa imagem densa. Nenhum campo pede entrelaçamento por U. A cláusula apenas consome essas testemunhas; ainda não foi exibido um habitante físico de ContratoH2 nem aplicada a proposta ao contrato canônico. A identificação por U=1 permanece separada.

Kimi concluiu a crítica do grafo, request {k['job']['request_id']}, job {k['job']['id']}; {k['usage']['prompt_tokens']} tokens entrada, {k['usage']['completion_tokens']} saída. Parecer adjudicado em D6/KIMI_ADJUDICACAO.md: aceitas inversa/domínios/controles; corrigidas eliminação indevida da realização alvo, necessidade indevida de ciclicidade para qualquer grafo e exemplo racional chamado diádico. Parecer não revisou os arquivos modulares novos. Custo da assinatura desconhecido, não zero; parcial metrado da missão US${partial}.

MiMo/DeepSeek/Gemini: três novos payloads preparados, ainda NÃO enviados porque a revisão automática exige autorização específica de egress; pergunta ao operador pendente. As três falhas anteriores seguem terminais, sem retry. Nenhum gate, original científico ou memória canônica alterado. Ringdown permanece não registrado e sem início de relógio.

Manifesto: D6/MODULAR_BRIDGE_DELIVERY.json SHA256 {sha(D/'MODULAR_BRIDGE_DELIVERY.json')}, com caminhos, hashes e recibos de cada fonte/log. Próximo: instanciar ou medir precisamente a ligação ao par físico, usando o predicado já nomeado; prosseguir D1′→D2′→D3′→D4→D5→B conforme a árvore. Não construir um segundo cálculo funcional.
'''
    write(OUT/'ENTREGA_016_D6_ligacao_modular_condicional.md',note.encode())
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — D6 ligação condicional24declarações no trio, controles18+13; Kimi concluído/adjudicado. Instanciação física nomeada OPEN. CPUcompilação{cpu:.6f}s/parede{wall:.6f}s incluindo falhas; parcialUS${partial}, Kimi assinatura desconhecida. Três payloads adicionais aguardam consentimento específico exigido por auto-review. Gate intacto.\n'.encode(),True)
    p=R/'A7/CONTINUIDADE.json';st=json.loads(p.read_bytes());st.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_process=None,own_live_processes=[],D6_modular_delivery=str(D/'MODULAR_BRIDGE_DELIVERY.json'),D6_kimi_review=str(D/'KIMI_ADJUDICACAO.md'),next='D6 now has24 compiled declarations/trio; graph+square+resolvent+J+imaginary powers+independent readout+domain inverse+proposed clause. Conditional obligation PairTomitaAnalyticRealizationMeasured remains for each selected physical pair; source graph not enough to identify arbitrary target. Kimi graph critique completed/adjudicated, 318015in/38197out, unknowncost; ledger recorded. 31 finite checks in2fixtures. No live compiler. New MiMo/DeepSeek/Gemini payloads in connections_catalog still NOT SUBMITTED after auto-review rejection; async specific-egress approval pending. Do not bypass/retry. Follow D6 then D1prime...B; B remains unregistered.');save(p,st,True)
    print(json.dumps(dict(status=result['status'],declarations=24,finite_checks=31,compile_cpu_seconds=cpu,partial_metered_cost_usd=str(partial))))
if __name__=='__main__':main()
