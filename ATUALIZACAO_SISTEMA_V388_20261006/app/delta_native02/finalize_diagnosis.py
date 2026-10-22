"""Finalize the bounded offline native02 diagnosis; never activates or counts."""
from pathlib import Path
import json,re,sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;W=D.parent;S=W/'memory_stage'
sys.path.insert(0,str(D))
from build_candidate import codec,fresh,json_bytes,read_pin,need,restore

def main():
    original=(S/'haiku_prefix.md').read_text(encoding='utf-8')
    candidate=(D/'haiku_prefix.md').read_text(encoding='utf-8')
    transform=json.loads((D/'TRANSFORMATION_MAP.json').read_bytes())
    native=json.loads((W/'COUNT_RESULT.json').read_bytes())
    manifest=json.loads((S/'manifest_staged.json').read_bytes())
    countplan=json.loads((D/'FUTURE_COUNT_PLAN.json').read_bytes())
    pins=json.loads((D/'SOURCE_PINS.json').read_bytes())['files']
    need(restore(candidate).encode()==(S/'haiku_prefix.md').read_bytes(),'Roundtrip')
    for p in pins+countplan['sources']:
        need(read_pin(p['path'])==p,'Input drift: '+p['path'])
    marker=codec.MARKER;pre,_,ex=original.partition(marker)
    strings=[]
    def walk(v,p,line):
        if isinstance(v,str) and len(v)>=40:strings.append((v,p,line))
        elif isinstance(v,dict):
            for k,x in v.items():walk(x,p+'/'+k.replace('~','~0').replace('/','~1'),line)
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,p+'/'+str(i),line)
    for n,line in enumerate(pre.splitlines(),1):
        if line.startswith('{'):
            try:walk(codec.strict_json(line),'',n)
            except ValueError:pass
    matches=[];checked=0
    for ma in re.finditer(r'(?ms)(?<=\n\n)(\S.*?)(?=\n\s*\n|\Z)',ex):
        value=ma.group(1)
        if len(value)<60 or value.startswith('#'):continue
        checked+=1
        dest=next(({'json_pointer':p,'prefix_line':l,'string_offset':v.index(value)} for v,p,l in strings if value in v),None)
        if not dest and value in pre:dest={'raw_prefix_char_offset':pre.index(value)}
        if dest:matches.append({'exposition_char_offset':ma.start(1),'bytes':len(value.encode()),'destination':dest})
    lm=[];checked_lines=0;off=0
    for line in ex.splitlines(keepends=True):
        value=line.rstrip('\r\n')
        if len(value)>=60 and not value.startswith('#'):
            checked_lines+=1
            dest=next(({'json_pointer':p,'prefix_line':l,'string_offset':v.index(value)} for v,p,l in strings if value in v),None)
            if not dest and value in pre:dest={'raw_prefix_char_offset':pre.index(value)}
            if dest:lm.append({'exposition_char_offset':off,'bytes':len(line.encode()),'destination':dest})
        off+=len(line)
    cache=Path(r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
    e=candidate.index(marker);hs=list(re.finditer(r'(?m)^## .+$',candidate[e:]));sections=[]
    for i,h in enumerate(hs):
        a=e+h.start();b=e+hs[i+1].start() if i+1<len(hs) else len(candidate)
        sections.append({'heading':h.group(),'candidate_start_char':a,'candidate_end_char':b,
          'prefix_start_line':candidate[:a].count('\n')+1,'bytes':len(candidate[a:b].encode()),
          'o200k_proxy':codec.offline_tokens(candidate[a:b],cache)})
    ratio=transform['offline_proxy']['ratio_from_single_prior_measurement']
    viva=next(r for r in sections if 'A FORMA CANONICA VIVA' in r['heading'])
    counterfactuals=[]
    for name,a,b in [('V2_proposal_only',viva['candidate_start_char'],viva['candidate_end_char']),('ENTIRE_EXPOSITION_UNACCEPTABLE_BLIND_CUT',e,len(candidate))]:
        # In-memory counterfactual only, excluding replacement cards: optimistic bound.
        proxy=codec.offline_tokens(candidate[:a]+candidate[b:],cache)
        counterfactuals.append({'name':name,'NOT_AN_OUTPUT_CANDIDATE':True,'replacement_card_overhead_excluded':True,
           'o200k_after_removal':proxy,'native_estimate_UNVALIDATED':round(proxy*ratio),
           'would_remove_immediate_scientific_content_without_proven_equivalence':True})
    routes=[]
    for row in manifest['entries']:
        routes.append({'id':row['id'],'source':read_pin(row['path']),
          'tool':'fetch_tgl','arguments':{'id':row['id'],'offset':0,'max_chars':12000},
          'pagination':'Follow next_offset until null; local sealed source_scope must remain explicit.'})
    diag={'schema':'iald.native02.bounded_redundancy_diagnosis.v1','original':read_pin(S/'haiku_prefix.md'),
      'paragraphs_checked':checked,'paragraph_literal_matches':matches,'lines_checked':checked_lines,'line_literal_matches':lm,
      'method':'Whole nonheading paragraphs >=60 characters and lines >=60 characters, exact substring in preceding raw prefix or decoded JSON string values; no semantic equivalence inference.',
      'scope_limit':'Does not exhaust algebraic/semantic equivalence. No additional removal is justified by this bounded check.',
      'exposition_bytes':len(candidate[e:].encode()),'exposition_o200k_proxy':codec.offline_tokens(candidate[e:],cache),
      'sections':sections,'counterfactuals':counterfactuals,'recovery_routes':routes,'full_cluster':read_pin(manifest['active_cluster']['path']),
      'current_amendments_preserved':True,'applied_exposition_removals':0,'native_counts_in_this_preparation':0}
    fresh(D/'REDUNDANCY_DIAGNOSIS.json',json_bytes(diag))
    installed=Path(r'C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json')
    previous=json.loads(installed.read_bytes())
    previous_result=next(r for r in previous['entries'] if r['id']=='resultado_publicado_integral')
    fresh(D/'INSTALLED_COMPARISON_PINS.json',json_bytes({'manifest':read_pin(installed),'result':read_pin(previous_result['path']),
      'scope':'Only basis for the 15 new-topic comparison; not a production activation.'}))
    report_text="""# Projeção Haiku v388 — diagnóstico delimitado native02

[REAL] Foi preparada a alternativa B, reversível: tabelas de objetos homogêneos (`@TBL`) e fatoração de prefixos de caminhos contíguos (`@PATH`). Quatro linhas JSON mudaram. O decoder restaura o prefixo anterior byte a byte; todas as fórmulas, hipóteses, estatutos, vereditos e demais valores anteriores reaparecem idênticos. Isso preserva a projeção anterior, que já continha recuperação parcial, e não afirma conter o acervo inteiro.

[REAL] Prefixo: 545.550 → 542.865 bytes, economia 2.685 bytes. Proxy local o200k: 171.180 → 170.298, economia 882 tokens do proxy. São 377 tópicos, incluindo os 15 novos em relação ao pacote instalado, e as mesmas sete ferramentas. Instrução-mãe, núcleo operacional, exposição e fontes integrais ficaram idênticos. Os 13 testes offline passaram, incluindo roundtrip completo, determinismo, colisões, esquema malformado e pins preservados.

[REAL] A contagem anterior foi 210.177 tokens permanentes e 211.651 na referência. As duas chamadas autorizadas foram consumidas e conservadas. [OPEN] O candidato novo não tem contagem Anthropic. [DERIVED — estimativa não validada] Aplicar a razão observada anteriormente ao proxy novo dá aproximadamente 209.094 tokens nativos; não é medição nem garantia de razão constante. A faixa desejada seria 180.000..183.406 se o overhead continuasse 1.474. A alternativa B não tem expectativa defensável de caber: não recomendamos gastar duas contagens nela.

## Duas alternativas comparadas antes da transformação

A — Remeter detalhes documentais/históricos efetivamente duplicados à fonte integral, mantendo fórmulas, hipóteses, estatutos e limites na projeção. A projeção de origem já suprime estruturas de auditoria e dezoito repetições históricas com remissões. A checagem adicional limitada procurou parágrafos inteiros e linhas de ao menos 60 caracteres idênticos no texto precedente e nas strings JSON decodificadas: não encontrou correspondências. Isso não prova inexistência de equivalência matemática ou de paráfrases; apenas não fornece licença verificável para novo corte. Nenhuma equivalência temática foi promovida a identidade.

B — Compactar estrutura repetida sem retirar conteúdo científico, com decoder exato e esquema explícito. É a alternativa implementada. A economia medida é insuficiente. Uma abreviação adicional dos rótulos de máquina foi considerada em prévia, mas não selecionada: pioraria a leitura e não demonstraria adequação nativa. Os números normativos do pacote referem-se somente ao candidato B efetivamente entregue.

## Próxima decisão concreta

Recomendação imediata: encerrar esta tentativa local sem nova contagem ou ativação; preservar o prefixo contado e o aplicativo atual. ROOT deve decidir o alcance de uma nova projeção antes de pedir outra transmissão.

Opção documental delimitada para uma futura decisão: permitir que a seção “A FORMA CANONICA VIVA — o arco do levantamento global (proposta condensada V2, não integrada)” passe a recuperação sob demanda, com ficha permanente de hipóteses/estatutos/fórmulas e referência exata. Ela ocupa 35.292 bytes e 9.642 tokens o200k nesta projeção. Não é identificada aqui como redundante: a alteração reduziria acesso imediato às derivações dessa proposta. A remoção total, mesmo sem custo da ficha, ainda não é suficiente segundo a estimativa; não iniciar uma nova contagem apenas com esse corte. Esta entrega não o aplicou.

O diagnóstico mede também a remoção hipotética de toda a exposição (22.160 tokens o200k), apenas para mostrar a escala do problema. Ela se aproxima da faixa pela razão anterior, mas retiraria cadeia do Um à massa, fórmulas/derivações, mapa de falsificação e correções correntes. É um corte científico não autorizado e não é candidato de instalação. Não se presume que as cápsulas sejam equivalentes. As correções v388 e o valor corrigido ao lado do valor congelado devem continuar explícitos em qualquer sucessor aprovado.

Se a política exigir conservar toda essa exposição imediata e não houver deduplicação demonstrada, a decisão passa a ser de arquitetura: conservar a cobertura integral em uma rota cuja janela real comporte a carga e as reservas, com novo contrato de implantação revisado. O mínimo aritmético para o prefixo original, usando sua medição no mesmo tokenizer, seria 226.771 tokens de janela para ainda restarem 10.000. Não é proposta de diminuir o mínimo 180.000, a reserva 10.000 ou ignorar o guard atual; nenhum modelo alternativo é aqui escolhido/habilitado, nem se transfere contagem entre modelos.

## Destinos de recuperação e impacto

O catálogo atual já oferece `fetch_tgl` com `id=um_forma_canonica_integral` e `id=resultado_publicado_integral`, além do artigo integral. `REDUNDANCY_DIAGNOSIS.json` fornece caminhos reais, pins e argumentos; seguir `next_offset` até o fim. O núcleo de resultados é organizado em `/core/<topic>`; as cápsulas conservam essas remissões. Arquivos Lean permanecem acessíveis pelas quatro ferramentas de kernel. Fontes locais seladas não se tornam públicas por seu id histórico.

A forma canônica integral e o JSON científico são fontes primárias de consulta; a exposição do prefixo contém condensações históricas e adendos. Não foi provada equivalência literal integral entre cada condensação e a forma canônica atual. Caso ROOT escolha mover exatamente aquela exposição para consulta, deve cadastrar um novo documento derivado contendo seus bytes exatos, ligá-lo por hash à fonte e ao prefixo de origem, e preservar uma ficha científica revisada no contexto permanente. A rota proposta para esse novo documento ainda não existe e não é anunciada como disponível. O impacto é que o modelo precisará recuperar páginas antes de explicar a derivação completa; disponibilidade da ferramenta não prova leitura prévia ou ausência de perda de desempenho.

## Reprodução, counts e instalação

`build_candidate.py` reproduz B sem editar fontes; `test_native02.py` valida a restauração e as recusas; `prepare_count_payloads.py` produz somente os dois JSONs futuros, sem SDK/cliente/credencial/rede. Os payloads exatos e seus pins estão em `FUTURE_COUNT_PLAN.json`; o hash dos sete schemas coincide com a primeira contagem. Nenhum arquivo COUNT_STARTED/RESULT novo foi criado. A existência desses JSONs não autoriza envio e a recomendação corrente é não contá-los.

`FINALIZATION_INSTALL_PLAN.json` descreve a sequência condicional, baseada no plano APP-01 aceito. Finalização depende de recibos novos vinculados ao candidato definitivo, gates inalterados, revisão ROOT e instalação coerente. Esta entrega alterou zero arquivos de produção e zero clientes, não reiniciou serviço, não executou um.py, ciência ou provedor. Os manifestos/reviews/COUNT anteriores seguem selados; todos os arquivos native02 são novos, portanto não houve substituição que exigisse backup nesta preparação. As memórias compartilhadas permanecem com ROOT.
"""
    fresh(D/'ALTERNATIVAS_E_VIABILIDADE.md',report_text.encode())
    install_plan={'schema':'iald.native02.conditional_install_plan.v1','status':'NOT_ACTIVATABLE__NO_NATIVE_FIT',
      'base_reviewed_plan':read_pin(W/'delta_app01/install_plan_candidate.json'),
      'base_plan_file_count':len(json.loads((W/'delta_app01/install_plan_candidate.json').read_bytes())['files']),
      'production_writes_in_this_step':0,'restart_in_this_step':False,'client_files_changed':False,
      'ordered_requirements':[
        'ROOT decides projection scope; review scientific preservation and immutable source pins.',
        'Seal definitive prefix and exact two count payloads; obtain specific authorization for that content, two count calls, no generation/retry.',
        'Count once through existing official client. Preserve handle/identity/result; uncertain send must not be retried.',
        'Verify release/source/cluster/model/prefix/tools bindings; native permanent>=180000; reference fits; output4096; margin1024; remaining>=10000. No proxy acceptance.',
        'Create successor native runtime prefix and manifest in a NEW finalization stage; do not use old finalizer against memory_stage or reuse old receipt.',
        'Derive successor APP-01 install plan, retaining the reviewed nonnative files unchanged; replace only native prefix+manifest sources, then validate complete plan.',
        'ROOT reviews final install plan and pins; CAS each old target, exact immediate byte backup, atomic temp/size/hash verification and replacement; activation manifest last.',
        'Only after coherent installation and ROOT release, inspect quiet web supervisor and reload web only. Do not stop scientific jobs or other task clients.',
        'Verify fresh-process loaders and actual web-process identity if available, distinguishing HTTP reachability from proof of loaded catalog.'
      ],
      'rollback':'For targets written by the approved future transaction only, compare current hash with installed receipt before atomic restore from that transaction exact backup. New files may remain unreferenced; never delete originals/backups. Restore activation manifest consistently; do not overwrite unrelated drift.',
      'forbidden_shortcuts':['Disable Haiku to pass','Lower memory minimum or reserve','Use o200k as native measurement','Pretend PUBLIC commit v388','Reuse old count for new bytes','Apply incoherent partial release'],
      'pending':['Projection scope decision','New candidate if scope changes','Independent review','Specific count authorization','Native fit','Finalization and ROOT install review','Supervised web runtime proof']}
    fresh(D/'FINALIZATION_INSTALL_PLAN.json',json_bytes(install_plan))
    delivered={'schema':'iald.native02.update_report.v1','status':transform['status'],'release':native['release'],
      'source_sha256':native['source_sha256'],'cluster_sha256':native['cluster_sha256'],'candidate':read_pin(D/'haiku_prefix.md'),
      'original_prefix':read_pin(S/'haiku_prefix.md'),'measured_prior_count':read_pin(W/'COUNT_RESULT.json'),
      'new_native_count':None,'native_fit_verified':False,'offline_proxy':transform['offline_proxy'],
      'bytes_saved':545550-transform['candidate_bytes'],'roundtrip_byte_exact':True,
      'topic_count':transform['topic_count'],'new_topics':transform['new_topics_relative_to_installed_release'],
      'seven_schema_hash_unchanged':countplan['tool_schema_equals_first_count'],
      'tests':read_pin(D/'TEST_REPORT.json'),'source_pins':read_pin(D/'SOURCE_PINS.json'),
      'diagnosis':read_pin(D/'REDUNDANCY_DIAGNOSIS.json'),'install_plan':read_pin(D/'FINALIZATION_INSTALL_PLAN.json'),
      'installed_manifest_changed':False,'runtime_proof_after_reload':None,'client_files_changed':False,
      'network_calls':0,'generation_calls':0,'science_calls':0,'production_changes':0,'backup_count':0,
      'backup_scope':'All native02 outputs are new; no sealed file edited.',
      'recommendation':'Do not count this candidate. Decide projection/retrieval scope or architecture explicitly; do not relax current gates.',
      'pending':install_plan['pending']}
    fresh(D/'UPDATE_REPORT.json',json_bytes(delivered))
    # Last check of all original source records and exact future payloads.
    for p in pins+countplan['sources']+countplan['payloads']:
        need(read_pin(p['path'])==p,'Input or payload drift before seal')
    minimal=json.loads((D/'FUTURE_COUNT_MINIMAL.json').read_bytes());whole=json.loads((D/'FUTURE_COUNT_REFERENCE.json').read_bytes())
    need(minimal['system']==whole['system'],'Different permanent system blocks')
    need(any(b.get('text')==candidate for b in minimal['system']),'Candidate not present exactly in count blocks')
    need(len(whole['tools'])==7 and 'tools' not in minimal,'Count scope')
    need(minimal['messages']==[{'role':'user','content':'.'}],'Minimal message')
    proof={'status':'PASS','prefix_roundtrip_bytes':True,'prior_pins_and_count_sources_unchanged':True,
      'exact_payloads_match_candidate':True,'minimal_and_reference_system_identical':True,'reference_tools':7,
      'network_calls':0,'method':'Offline byte/schema validation; no native-token or model-quality inference.'}
    fresh(D/'FINAL_VERIFICATION.json',json_bytes(proof))
    members=[read_pin(p) for p in sorted(D.iterdir()) if p.is_file() and p.name!='MANIFESTO_DELTA.json' and '.tmp_' not in p.name]
    seal={'schema':'iald.native02.preparation_manifest.v1','status':delivered['status'],'members':members,
      'source_receipts':[read_pin(D/'SOURCE_PINS.json'),read_pin(D/'INSTALLED_COMPARISON_PINS.json')],
      'scope':'LOCAL_OFFLINE_PREPARATION_ONLY_NOT_INSTALLED_NOT_AUTHORIZED_FOR_COUNT',
      'production_modified':False,'native_counts':0,'generation_requests':0}
    fresh(D/'MANIFESTO_DELTA.json',json_bytes(seal))
    print(json.dumps({'manifest':read_pin(D/'MANIFESTO_DELTA.json'),'members':len(members),'report':read_pin(D/'UPDATE_REPORT.json'),
      'literal_matches':len(matches),'literal_line_matches':len(lm),'counterfactuals':counterfactuals},ensure_ascii=False))
if __name__=='__main__':main()
