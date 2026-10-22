"""Record the exact graph result and prepare independent criticism of its scope."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,re,sys,uuid,hashlib
R=Path(__file__).resolve().parents[1];D=R/'D6';OUT=R.parent/'TUNEL/DO_CHATGPT'
sys.path.insert(0,str(R))
from prepare_part_d import write,save,sha,excerpt
def main():
    now=datetime.now(timezone.utc);s=D/'RecognitionGraph_v2.lean';log=D/'graph_02.log';receipt=json.loads((D/'graph_02.json').read_bytes())
    text=log.read_text('utf-8-sig');axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)
    assert receipt['rc']==0 and len(axioms)==7 and not receipt['newer_kernel_files'] and not receipt['scan_errors']
    assert all(set(x.strip() for x in names.split(','))<={'propext','Classical.choice','Quot.sound'} for _,names in axioms)
    assert not re.search(r'\b(sorry|axiom)\b',s.read_text('utf-8'))
    control=json.loads((D/'FINITE_CONTROL_001.json').read_bytes());assert len(control['tests'])==18 and all(x['passed'] for x in control['tests'])
    costs={}
    for line in (OUT/'LEDGER_016.jsonl').read_text('utf-8-sig').splitlines():
        if not line.strip():continue
        x=json.loads(line);v=next((x[k] for k in ['cost_estimate_usd','cost_usd','custo_usd'] if x.get(k) is not None),None)
        key=next((x[k] for k in ['execution_task_id','execution_id','request_id','job_id'] if x.get(k)),None)
        if key and v is not None:costs[key]=Decimal(str(v))
    result=dict(at=now.isoformat(),status='D6_GRAPH_KERNEL_CHECKED_MODULAR_IDENTIFICATION_STILL_OPEN',
        opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),source_sha256=sha(s),log_sha256=sha(log),receipt_sha256=sha(D/'graph_02.json'),
        axioms={name:[x.strip() for x in names.split(',')] for name,names in axioms},cycles=2,
        graph_statement='(U x U) closure GraphTomita(M,Omega) = closure GraphTomita(N,Omega_prime)',
        hypotheses=['U unitary','U Omega = Omega_prime','A in M iff U A U* in N'],
        closed_operator_extra_hypotheses=['independently given source and target operators realize their closed Tomita graphs'],
        unpaid=['identify independently supplied modular J through polar uniqueness','identify independently supplied Delta^{it} including domains/functional calculus','same_horizon_by_content into a copied contract','independent critique'],
        finite_control=dict(receipt_sha256=sha(D/'FINITE_CONTROL_001.json'),tests=18,J_defect_squared=control['wrong_reference_J_defect_squared'],Delta_defect_squared=control['wrong_reference_Delta_defect_squared'],scope=control['scope']),
        partial_metered_cost_usd=str(sum(costs.values(),Decimal(0))),transport_failures_unknown_cost=True,gate_changed=False)
    save(D/'GRAPH_DELIVERY.json',result)
    ad=R.parent/'TUNEL/PARA_CHATGPT/ADENDO_016_003c_o_campo_e_a_luz_D1_D3_revistos.md'
    references=[];parts=[]
    for p in [s,D/'recognition_control.py',ad]:
        meta,part=excerpt(p);references.append(meta);parts.append(part)
    question=('Crítica independente D6: qual é o alcance exato da construção abaixo e a menor lacuna formal a fechar para obter U J U*=Jprime e U Delta^{it} U*=Deltaprime^{it} de dados previamente dados? '+
      'Sete declarações do grafo compilaram rc0, axiomas no trio; isso não afirma as conclusões modulares. O controle finito teve18checks, defeitosJ²=2/Delta²=9 quando se mantém a referência errada. '+
      'Ataque dependências escondidas, tautologia, domínios e suficiência do controle; proponha uma rota curta para unicidade polar/cálculo funcional sem pôr a conclusão entre premissas. '+
      'Não redija teoria nova, não escolha partição, não prometa compilar. D6 vem primeiro; identificação da luz/gráviton é INPUT/ONTO. Um único parecer com diagnóstico preciso e lemas necessários. '+
      'Falhas MiMo/DeepSeek anteriores foram locais DPAPI antesHTTP, não quota. Esta crítica de fontes já produzidas é unidade nova, não repetição de C2.2 ou dos pedidos falhos.\n\n')
    prompt=question+'\n\n'.join(parts);assert len(prompt)<=20000,len(prompt)
    rid=str(uuid.uuid4());payload=D/'orchestration/kimi_graph_critic_submit.json'
    save(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=dict(mission_id='ORDEM_016',branch_id='D6',lemma_id='recognition_graph_independent_scope_critic',role='skeptic',required_provider='kimi',max_calls=1)))
    catalog=[dict(provider='kimi',request_id=rid,payload=str(payload),payload_sha256=sha(payload),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),chars=len(prompt),sources=references,status='PREPARED_NOT_SUBMITTED')]
    save(D/'orchestration/kimi_graph_critic_catalog.json',catalog)
    note=f'''[REAL — grafo compilado na bancada; OPEN — identificação modular geral]

Abertura016SHA256: {result['opening_sha256']}

D6: ReconhecimentoPeloConteudo tem U unitário, UΩ=Ω′ e transporte da subálgebra. Não contém equação modular entre suas premissas. recognition_tomita_graph prova transporte do grafo; recognition_closed_tomita_graph passa ao fecho por homeomorfismo; recognition_identifies_closed_operator identifica operadores previamente dados quando seus grafos são os fechos correspondentes. U=1 está separado em identityByConstruction.

Compilação isolada2 rc0, sete declarações auditadas no trio; zero sorry; nenhum arquivo novo no kernel. Primeira tentativa rc1 (reescrita dependente) preservada; corrigida ao lado em RecognitionGraph_v2.lean. FonteSHA256 {sha(s)}; logSHA256 {sha(log)}; reciboSHA256 {sha(D/'graph_02.json')}.

Controle finito M2 sobre Hilbert–Schmidt: U é multiplicação à esquerda pela matriz de troca. Preserva a álgebra esquerda, mas não Ω=diag(2,1)/sqrt5. Manter a referência antiga produz defeito de norma quadrada2 em J e9 em Delta no vetor e12. Com Ω′=UΩ, os18controles finitos passam, incluindo transporte de S/J/Delta. UΩ≠Ω sozinho NÃO implica falha quando o alvo é Ω′. É controle computacional finito, não teorema da rede.

Ainda OPEN: da igualdade dos grafos à identificação de J e Delta^it previamente fornecidos, via unicidade polar e cálculo funcional, e consumo na cópia do contrato. Não se vende definição por conjugação como esse resultado. Crítica Kimi preparada, sem resultado ainda; as três tentativas anteriores terminaram em falhas locais de transporte, sem uso/custo medidos. ParcialUS${result['partial_metered_cost_usd']}; custos desconhecidos não são zero. Nenhum gate mudou. Próximo: crítica/ligação modular D6, antes de D1′.
'''
    write(OUT/'ENTREGA_016_D6_grafo_e_controle.md',note.encode())
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — D6 PARCIAL: grafo/fecho/operador7declarações no trio(rc0,ciclo2), controlefinito18. J/Delta^it gerais OPEN. CríticaKimi preparada. ParcialUS${result["partial_metered_cost_usd"]}; nenhum gate/relógio.\n'.encode(),True)
    p=R/'A7/CONTINUIDADE.json';state=json.loads(p.read_bytes());state.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_process=None,own_live_processes=[],D6_graph_delivery=str(D/'GRAPH_DELIVERY.json'),next='D6 graph7declrc0/trio and finite18controls. Need general modular J/Delta identification via uniqueness, not definition by conjugation. Kimi independent critic catalog prepared; send through existing coordinator with correct Windows identity preview. MiMo/DeepSeek terminal DPAPI, Gemini init inventory mismatch no prompt sent. No retries. Full D6 10h from11:42Z, then D1prime,D2prime,D3prime,D4,D5,B. Ringdowndraft002 preserved unregistered.');save(p,state,True)
    print(json.dumps(dict(status=result['status'],axioms=len(axioms),kimi_request_id=rid,prompt_chars=len(prompt),partial_metered_cost_usd=result['partial_metered_cost_usd'])))
if __name__=='__main__':main()
