"""Record revised Part D and prepare distinct, bounded scientific requests."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid,sys
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'ORDEM_016_QG';D=R/'D6';O=D/'orchestration';IN=ROOT/'TUNEL/PARA_CHATGPT';OUT=ROOT/'TUNEL/DO_CHATGPT'
CAN=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw,replace=False):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        assert replace;old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f'))
        with bak.open('xb') as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;tmp.replace(p)
def save(p,x,replace=False):write(p,(json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode(),replace)
def excerpt(p,first=1,last=None):
    lines=p.read_text('utf-8-sig').splitlines();last=len(lines) if last is None else last
    meta=dict(path=str(p),sha256=sha(p),first_line=first,last_line=last)
    text='SOURCE '+json.dumps(meta,ensure_ascii=False)+'\n'+'\n'.join(f'{i+1}: {s}' for i,s in enumerate(lines) if first<=i+1<=last)
    return meta,text
def main():
    O.mkdir(parents=True,exist_ok=False)
    a=IN/'ADENDO_016_003_decisoes_do_operador_e_parte_D.md';b=IN/'ADENDO_016_003b_suspensao_D1_D3.md';c=IN/'ADENDO_016_003c_o_campo_e_a_luz_D1_D3_revistos.md'
    pins={str(p):sha(p) for p in [a,b,c,CAN/'TheGravitonIsTheConjugatedPhase.lean',CAN/'TheLightInterface.lean',CAN/'ContratoQG_v31.lean']}
    expected={a:'076940a20f26cf94',b:'b2294b54d2a37abc',CAN/'TheGravitonIsTheConjugatedPhase.lean':'6f5f04ab96dd16f8',CAN/'TheLightInterface.lean':'6d1e1567a4cc5b05',CAN/'ContratoQG_v31.lean':'2f2c6561a5a5d832'}
    assert all(pins[str(p)].startswith(h) for p,h in expected.items())
    _,cs=excerpt(c)
    common='ORDEM_016, Parte D revista pelo ADENDO003c, solicitada diretamente pelo operador em 26/09. Texto científico autorizado da missão; não ler arquivos externos. Responder em português. Você entrega texto para revisão: não executou Lean, não move gate nem confirma física. Uma pergunta delimitada; apontar hipóteses faltantes sem chamar rfl de reconhecimento físico. Memória comum do transporte é referência; o adendo atual prevalece quanto ao escopo. Não iniciar os D1/D2/D3 antigos cancelados.\n'
    tasks=[
      ('mimo','draft','recognition_content_tomita_strategy',
       'Qual é a menor construção Lean não circular de ReconhecimentoPeloConteudo, a partir de U unitário, UΩ=Ω\' e U M U*=M\', que demonstra transporte do grafo fechado de Tomita e identifica J e Delta por unicidade, reaproveitando os lemas fornecidos? Entregue mapa de dependências, assinatura e rascunho Lean; se unicidade polar/cálculo funcional não estiver disponível, nomeie exatamente o lema faltante, nunca ponha a conclusão entre as premissas. Distinga transporte definido por conjugação de reconhecimento de operadores previamente construídos. O controle U=1 vai em identities_by_construction. Não invente nomes de lemas da biblioteca.',
       [(c,1,None),(CAN/'ProfileTomitaTransport.lean',19,155),(CAN/'ProfileModularTransport.lean',19,73)]),
      ('deepseek','draft','recognition_content_negative_control',
       'Qual controle finito exato distingue transporte genuíno do par (M,Ω) de normalizar só M no D6? Construa em M2(C) sobre Hilbert-Schmidt um U não trivial que normalize a representação esquerda mas, sem transportar corretamente o vetor de referência fiel, não entrelace os dados modulares. Forneça matrizes, S,J,Delta, um vetor testemunha e fórmulas auditáveis em Python; explique por que UΩ≠Ω isoladamente NÃO implica falha se Ω\'=UΩ. Inclua o controle positivo com Ω\'=UΩ e separe a afirmação existencial (pode falhar sem a hipótese) de uma falsa universal. Nenhuma alegação de execução ou de validade geral na rede.',
       [(c,1,None),(a,9,21)]),
      ('gemini','draft','part_d_revision_documentary_audit',
       'Quais são exatamente as tarefas vigentes após os três adendos? Faça tabela curta com cancelado/substituto, ordem D6→D1prime→D2prime→D3prime→D4→D5→B, teto, controle e estatuto. Compare fontes e identifique enunciados que não podem ser promovidos a prova (incluindo escape Weinberg-Witten condicional). Só auditoria documental de baixa complexidade; não desenvolva física nova nem execute código.',
       [(a,1,64),(b,1,None),(c,1,None)])]
    catalog=[]
    for provider,role,lemma,question,sources in tasks:
        refs=[];pieces=[]
        for p,f,l in sources:
            meta,s=excerpt(p,f,l);refs.append(meta);pieces.append(s)
        prompt=common+'\nPERGUNTA ÚNICA: '+question+'\n\n'+'\n\n'.join(pieces)
        assert len(prompt)<=20000,(provider,len(prompt))
        req=str(uuid.uuid4());constraint=dict(mission_id='ORDEM_016',branch_id='D6' if provider!='gemini' else 'D.escopo',lemma_id=lemma,role=role,required_provider=provider,max_calls=1)
        if provider=='mimo':constraint.update(max_cost_usd=None,max_output_tokens=131072)
        if provider=='deepseek':constraint.update(max_cost_usd=None,max_output_tokens=393216)
        payload=O/(provider+'_submit.json');save(payload,dict(operation='submit',request_id=req,prompt=prompt,execution_constraints=constraint))
        catalog.append(dict(provider=provider,request_id=req,branch=constraint['branch_id'],payload=str(payload),payload_sha256=sha(payload),prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),chars=len(prompt),sources=refs,status='PREPARED_NOT_SUBMITTED'))
    save(O/'prepared_units.json',catalog)
    receipt=dict(at=now.isoformat(),status='PART_D_REVISED_READ_AND_PREPARED',sources=pins,um_py_pin_status='UNVERIFIED_ACCESS_DENIED_WINDOWS',
        cancelled=['D1 old spin2 network','D2 old product network','D3 old spin2 obstruction'],order=['D6','D1prime','D2prime','D3prime','D4','D5','B'],
        D6_timebox_hours=10,part_D_timebox_hours=60,origin_thread_id='01a070fc-9484-7e13-a654-c6b5f61093a4',
        inputs_ontology='Photon network h=+/-1; graviton conjugate form, not asserted propagating spin2 particle',
        D6_reuse=['ProfileTomitaTransport.lean','ProfileModularTransport.lean','UnitaryPartialTransport.lean'],
        ringdown_preserved=dict(candidate=str(ROOT/'ORDEM_013_RINGDOWN/bis/015/t03/CANDIDATE_V1_1_002.json'),controls_current_guard=41,candidate_controls=34,registered=False,clock_started=False),
        catalog_sha256=sha(O/'prepared_units.json'),new_external_calls=0,kimi_next='Independent critique after MiMo draft/local check; never retry C2.2',opening_sha256=sha(OUT/'ENTREGA_016_ABERTURA_operador.md'))
    save(D/'REVISION_RECEIPT.json',receipt)
    text=f'''[REAL — leitura e preparação; INPUT/ONTO — escolhas do operador]

Abertura016SHA256: {receipt['opening_sha256']}

ADENDO003c lido integralmente, sha256 {sha(c)}. D1..D3 antigos cancelados, sem trabalho novo neles. Ordem vigente: D6, D1′, D2′, D3′, D4, D5; depois B. Teto D6 10h; ParteD 60h. A rede selecionada é a do fóton; identificação do gráviton como forma conjugada conserva INPUT/ONTO. Provas cobrem somente seus enunciados algébricos e hipóteses. Nenhum gate alterado.

Pins dos adendos003/003b e três fontes Lean citadas conferem. Leitura de um.py foi recusada pelo Windows; seu pin v371 não foi conferido, nem inferido de memória. Isso não impede a consulta das fontes Lean, registradas individualmente.

Reaproveitamento localizado: ProfileTomitaTransport já transporta o grafo fechado entre perfis; ProfileModularTransport define e verifica dados transportados. O alvo D6 exige reconhecer dados previamente dados pelo conteúdo, distinguindo isso de defini-los por conjugação.

Preparadas três unidades distintas: MiMo rascunho D6; DeepSeek controle negativo finito; Antigravity auditoria documental dos adendos. Kimi reservado para crítica independente da construção resultante. Catalogo D6/orchestration/prepared_units.json. PREPARADO não significa enviado ou concluído; recibos posteriores determinarão execução.

Ringdown preservado: candidato002, 41 controles integrados e 34 do candidato passaram; sem registro V1.1, relógio R7 ou trabalho pesado. Continuação da ParteB agora aguarda ParteD, conforme novo adendo. C6 permanece encerrado pelo timebox; C2.2 falho não repetido. Novas chamadas externas nesta preparação:0.
'''
    write(OUT/'ENTREGA_016_D_ABERTURA_adendo003c.md',text.encode())
    p=R/'A7/CONTINUIDADE.json';s=json.loads(p.read_bytes());s.update(at=now.isoformat(),previous_goal_turn='PROGRESS',own_live_process=None,own_live_processes=[],part_D=receipt,next='Execute D6 first; dispatch three distinct prepared D6/documentary units through existing coordinator after previews. Reserve Kimi independent critique. B candidate002 controls passed, no publication/clock; return B only after D6,D1prime,D2prime,D3prime,D4,D5. Preserve all earlier failures and permission decisions.');save(p,s,True)
    p=OUT/'ENTREGA_016_PROGRESSO.md';write(p,p.read_bytes()+f'\n{now.isoformat()} — ParteD003c incorporada: D6 prioritário; antigosD1-D3 cancelados; B preservada sem relógio. Guard41/candidato34 passaram. Três unidades preparadas, nenhum envio ainda. AberturaSHA256 {receipt["opening_sha256"]}.\n'.encode(),True)
    p=OUT/'LEDGER_016.jsonl';write(p,p.read_bytes()+(json.dumps(dict(at=now.isoformat(),event='PART_D_003C_PREPARED',catalog=str(O/'prepared_units.json'),new_external_calls=0))+'\n').encode(),True)
    print(json.dumps(dict(status=receipt['status'],units=[{k:x[k] for k in ['provider','request_id','chars','payload_sha256']} for x in catalog]),ensure_ascii=False))
if __name__=='__main__':main()
