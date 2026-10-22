"""Custody for the compiled square bridge and three distinct connection tasks."""
from pathlib import Path
import sys,json,re,uuid,hashlib
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];D=R/'D6';O=D/'orchestration'
OUT=R.parent/'TUNEL/DO_CHATGPT';CAN=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
sys.path.insert(0,str(R))
from prepare_part_d import save,write,sha,excerpt

def main():
    now=datetime.now(timezone.utc).isoformat()
    src=D/'RecognitionSquare.lean';log=D/'square_01.log';rec=D/'square_01.json'
    r=json.loads(rec.read_bytes());assert r['rc']==0 and not r['newer_kernel_files'] and not r['scan_errors']
    assert sha(src)==r['source_sha256'] and sha(log)==r['log_sha256']
    axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log.read_text('utf-8-sig'))
    assert len(axioms)==3 and all(set(x.strip() for x in a.split(',')) <= {'propext','Classical.choice','Quot.sound'} for _,a in axioms)
    assert not re.search(r'\b(sorry|axiom)\b',src.read_text('utf-8'))
    delivery=dict(at=now,status='COMPILED_CONDITIONAL_GRAPH_SQUARE_AND_RESOLVENT',source_sha256=sha(src),log_sha256=sha(log),receipt_sha256=sha(rec),axioms=dict(axioms),cycles=1,opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'),scope='Graph covariance and recognition of independently supplied resolvents by graph equations. Density, positivity and spectral hypotheses remain explicit; not yet full D6.',gate_changed=False)
    save(D/'SQUARE_DELIVERY.json',delivery)
    common=('ORDEM016 D6, unidade NOVA sobre o grafo e resolvente agora compilados. Não repetir os pedidos anteriores falhos. Fontes científicas autorizadas pelo operador, somente texto para a bancada; nenhuma execução/prova alegada pelo modelo. Uma pergunta, Lean compilado somente pela bancada. Não criar nova teoria nem modificar o cânone. Objetivo: reutilizar lemas existentes, não rederivar. D6 tem prioridade.\n')
    tasks=[
      ('mimo','draft','polar_recognition_from_compiled_resolvent',
       'Qual é a menor ligação Lean do resolvente identificado em RecognitionSquare à igualdade U J U*=Jprime para fatores polares fornecidos independentemente, reaproveitando positive_sqrt_intertwines? Trabalhe primeiro com dois pares no MESMO H e U unitário não trivial, identifique rigorosamente qualquer restrição. Proponha representação limitada C=sqrt(R*(1-R)), S R=J C e densidade de ran(C), com prova de identificação de J por continuidade. Entregue assinatura/rascunho e enumere obrigações analíticas de cada lado; não assuma J-intertwining, não defina Jprime por conjugação, nem invente API. Não refaça o grafo já compilado.',
       [(src,1,None),(CAN/'V350PositiveRootIntertwining.lean',1,None),(CAN/'V350ScalarTomitaPolarFactor.lean',1,None),(CAN/'V351ResolventImaginaryPowers.lean',13,36)]),
      ('deepseek','draft','imaginary_recognition_reuse_v351',
       'Como ligar unitary_recognizes_square_resolvent diretamente ao teorema existente resolventImaginaryPower_intertwines para obter U Delta^{it} U*=Deltaprime^{it} de pares independentes no mesmo H, sem uma hipótese que já seja a conclusão? Forneça rascunho Lean com orientação correta das multiplicações, pacote mínimo positivo/contração/injetividade de R e 1-R e cláusula de identificação das potências modulares previamente dadas. Aponte explicitamente quais hipóteses de realização ainda precisam ser instanciadas da construção Tomita. A API existente basta; não construir outro cálculo funcional. Distinguir fórmula do resolvente de afirmação geral sobre qualquer rede.',
       [(src,1,None),(CAN/'V351ResolventImaginaryIntertwining.lean',1,None),(CAN/'V351ResolventImaginaryPowers.lean',1,59)]),
      ('gemini','draft','d6_compiled_declaration_inventory',
       'Faça apenas um inventário documental dos dez nomes presentes nos dois logs de compilação, associando-os aos enunciados nas duas fontes: nome, premissas explícitas, conclusão literal e o que NÃO conclui sobre J/Delta. Conte os nomes em cada log, liste conjunto de axiomas e sinalize advertências sem confundi-las com falhas. Não audite matemática profunda, não trate log como execução própria e não escreva código. Entregue tabela curta utilizável no relatório D6. Esta unidade é distinta da auditoria anterior dos adendos, que falhou antes do envio.',
       [(D/'RecognitionGraph_v2.lean',1,None),(src,1,None),(D/'graph_02.log',1,None),(log,1,None)])]
    catalog=[]
    for provider,role,lemma,question,sources in tasks:
        refs=[];parts=[]
        for p,f,l in sources:
            meta,part=excerpt(p,f,l);refs.append(meta);parts.append(part)
        prompt=common+'PERGUNTA ÚNICA: '+question+'\n\n'+'\n\n'.join(parts)
        assert len(prompt)<=20000,(provider,len(prompt))
        rid=str(uuid.uuid4());payload=O/(lemma+'_submit.json')
        constraints=dict(mission_id='ORDEM_016',branch_id='D6',lemma_id=lemma,role=role,required_provider=provider,max_calls=1)
        if provider=='mimo':constraints.update(max_output_tokens=131072,max_cost_usd=None)
        if provider=='deepseek':constraints.update(max_output_tokens=393216,max_cost_usd=None)
        save(payload,dict(operation='submit',request_id=rid,prompt=prompt,execution_constraints=constraints))
        catalog.append(dict(provider=provider,request_id=rid,payload=str(payload),payload_sha256=sha(payload),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),chars=len(prompt),sources=refs,status='PREPARED_NOT_SUBMITTED'))
    save(O/'connections_catalog.json',catalog)
    note=f'''[REAL — compilação isolada; DERIVED sob hipóteses explícitas]

Abertura016 SHA256: {delivery['opening_sha256']}

D6: RecognitionSquare.lean compilou rc0, três declarações no trio, sem sorry nem axioma novo, ciclo1. A aplicação do transporte de grafos ao pareamento adjunto identifica o grafo do quadrado antilinear; as equações de realização do resolvente identificam resolventes fornecidos independentemente. Não se pressupõe a equação de entrelaçamento. A definição para relações arbitrárias não prova densidade nem autoadjunção.

Fonte SHA256: {sha(src)}; log SHA256: {sha(log)}; recibo SHA256: {sha(rec)}. CPU: {r['cpu_user_seconds']+r['cpu_kernel_seconds']} s; parede: {r['wall_seconds']} s. Aviso apenas de variáveis CompleteSpace não usadas no primeiro lema. Nenhum arquivo novo no kernel monitorado.

Reutilização localizada: V350PositiveRootIntertwining.positive_sqrt_intertwines e V351ResolventImaginaryIntertwining.resolventImaginaryPower_intertwines já fornecem as etapas espectrais no mesmo Hilbert. Próximo: conectar as realizações analíticas e fatores polares, sem uma segunda implementação do cálculo funcional. D6 completo ainda OPEN. Unidades MiMo/DeepSeek/Gemini preparadas para ligação polar, potências imaginárias e inventário documental. Crítica Kimi anterior em coordenação, sem resultado recebido. Nenhum gate ou relógio de ringdown mudou.
'''
    write(OUT/'ENTREGA_016_D6_quadrado_e_resolvente.md',note.encode())
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now} — D6 PARCIAL: mais3declarações no trio(rc0,ciclo1), grafo quadrado e resolvente. CPU9,625s. Cálculo funcional existente localizado; ligação modular ainda OPEN. Três unidades distintas preparadas, sem custo remoto novo medido.\n'.encode(),True)
    p=R/'A7/CONTINUIDADE.json';st=json.loads(p.read_bytes());st.update(at=now,own_live_process=None,own_live_processes=[],D6_square_delivery=str(D/'SQUARE_DELIVERY.json'),D6_connections_catalog=str(O/'connections_catalog.json'),next='D6: connect existing V350PositiveRootIntertwining and V351ResolventImaginaryIntertwining to compiled graph/resolvent. Three new connection payloads PREPARED, ask existing coordinator to preview normal-user token and dispatch once; Kimi critique previously requested. Ringdown stays unregistered.');save(p,st,True)
    print(json.dumps([dict(provider=x['provider'],request_id=x['request_id'],chars=x['chars']) for x in catalog]))
if __name__=='__main__':main()
