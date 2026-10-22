"""Bounded static selective A inventory; no candidate, count or activation."""
from pathlib import Path
import json,re,sys,ast
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;W=D.parent;S=W/'memory_stage';B=W/'delta_native02'
sys.path.insert(0,str(B))
from build_candidate import codec,read_pin,need,fresh,json_bytes,dump,sha

def main():
    tree=read_pin(D/'ARVORE_ALTERNATIVAS.json')
    seal=json.loads((B/'MANIFESTO_DELTA.json').read_bytes())
    for row in seal['members']:need(read_pin(row['path'])==row,'Sealed B changed')
    sources=[S/'haiku_prefix.md',S/'haiku_provenance.json',S/'manifest_staged.json',W/'COUNT_RESULT.json',B/'MANIFESTO_DELTA.json',B/'REDUNDANCY_DIAGNOSIS.json']
    before=[read_pin(p) for p in sources]
    text=(S/'haiku_prefix.md').read_text(encoding='utf-8')
    manifest=json.loads((S/'manifest_staged.json').read_bytes())
    provenance=json.loads((S/'haiku_provenance.json').read_bytes())
    native=json.loads((W/'COUNT_RESULT.json').read_bytes())
    data_path=Path(next(x['path'] for x in manifest['entries'] if x['id']=='resultado_publicado_integral'))
    data_raw=data_path.read_bytes();data=json.loads(data_raw)
    new=set(json.loads((B/'TRANSFORMATION_MAP.json').read_bytes())['new_topics_relative_to_installed_release'])
    rows=[];topic=None;lists=0;refs=0
    for n,line in enumerate(text.splitlines(),1):
        if line.startswith('### '):topic=line[4:] if line[4:] in data['core'] else None
        if line.startswith('{') and topic:
            try:v=codec.strict_json(line)
            except ValueError:continue
            if 'checks' not in v:continue
            checks=v['checks'];source=data['core'][topic]
            need('checks' in source,'Source pointer missing')
            if isinstance(checks,list):need(checks==source['checks'],'Literal checks differ');lists+=1
            else:refs+=1
            rows.append({'topic':topic,'new_topic':topic in new,'prefix_line':n,'json_pointer':'/core/'+topic+'/checks',
              'source_file':str(data_path),'source_file_sha256':sha(data_raw),'source_value_sha256':sha(dump(source['checks']).encode()),
              'source_value_items':len(source['checks']),'projected_value_bytes':len(dump(checks).encode()),
              'projection_kind':'LITERAL_LIST' if isinstance(checks,list) else 'ALREADY_PARTIAL_REFERENCE',
              'coverage':'Original projection may already omit detail; references do not prove scientific verification.',
              'fetch_tool':'fetch_tgl','fetch_id':'resultado_publicado_integral'})
    formal=[]
    for row in provenance['formal_declaration_excerpts']:
        path=S/'kernel'/row['source_path'];raw=path.read_bytes()
        need(len(raw)==row['source_bytes'] and sha(raw)==row['source_sha256'],'Formal source pin')
        ls=raw.decode('utf-8-sig').splitlines();decl=[]
        for item in row['declarations']:
            i=item['line']-1
            need(0<=i<len(ls) and item['name'] in ls[i],'Formal declaration line')
            decl.append({'name':item['name'],'kind':item['kind'],'line':item['line'],'source_line':ls[i]})
        formal.append({'source':read_pin(path),'catalog_path':row['source_path'],'excerpt_bytes':row['excerpt_bytes'],
          'proof_bodies_loaded':row['proof_bodies_loaded'],'declarations':decl,'tool':'iald_kernel_read',
          'arguments':{'path':row['source_path'],'start_line':1,'max_lines':160},'selected_for_removal':False,
          'reason':'Essential declaration heads, ambient variables, structures and hypotheses for H1/H2/H3; not a second collection of loaded proofs.'})
    pattern=r'<ENUNCIADOS_LEAN_DAS_HIPOTESES>.*?</ENUNCIADOS_LEAN_DAS_HIPOTESES>\s*'
    blocks=re.findall(pattern,text,flags=re.S);need(len(blocks)==5,'Five formal blocks')
    cut=re.sub(pattern,'',text,flags=re.S);output=[];removed=0
    for line in cut.splitlines(keepends=True):
        if line.startswith('{'):
            try:v=codec.strict_json(line)
            except ValueError:v=None
            if isinstance(v,dict) and 'checks' in v:
                del v['checks'];line=dump(v)+'\n';removed+=1
        output.append(line)
    cache=Path(r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
    base_proxy=codec.offline_tokens(text,cache);cut_proxy=codec.offline_tokens(''.join(output),cache)
    ratio=native['budget']['permanent_tokens']/base_proxy;estimate=round(cut_proxy*ratio)
    need(removed==len(rows)==215 and lists==9 and refs==206,'Inventory accounting')
    need(estimate>183406,'Unexpected feasibility requires review')
    selected=next(r for r in rows if r['topic']=='partial_closure_016_v372')
    plan={'schema':'iald.selective03.bounded_analysis.v1','status':'INFEASIBLE_WITHIN_AUTHORIZED_DOCUMENTARY_SCOPE__NO_NEW_CANDIDATE',
      'alternatives_before_analysis':tree,'prefix_source':read_pin(S/'haiku_prefix.md'),'scientific_json':read_pin(data_path),
      'checks_inventory':rows,'checks_count':len(rows),'checks_value_bytes':sum(r['projected_value_bytes'] for r in rows),
      'checks_literal_lists':lists,'checks_already_partial_references':refs,'formal_inventory':formal,
      'formal_excerpt_bytes_total':sum(r['excerpt_bytes'] for r in formal),'formal_block_count':len(blocks),
      'all_formal_proof_bodies_already_on_demand':all(r['proof_bodies_loaded'] is False for r in formal),
      'A1_example_exact_source':selected,
      'A1_example_impact':'Two package-integrity labels could be fetched while retaining their declared outcome/count. Small saving does not qualify whole projection; not applied.',
      'A2_removal_rejected':'Essential formal heads carry immediate hypotheses/formulas. Proof bodies already on demand.',
      'A3_prior_literal_audit':read_pin(B/'REDUNDANCY_DIAGNOSIS.json'),
      'optimistic_bound':{'not_a_candidate':True,'NOT_SAVED_AS_PREFIX':True,'formal_blocks_removed':5,'all_checks_fields_removed':removed,
        'includes_protected_new_science_and_formulas':True,'reference_card_overhead':0,'baseline_o200k':base_proxy,
        'hypothetical_o200k':cut_proxy,'native_tokens':None,'native_estimate_UNVALIDATED':estimate,
        'excess_over_183406_estimate_UNVALIDATED':estimate-183406,
        'scope':'Only inventoried groups; no global impossibility proof. Native/proxy ratio and1474 overhead not guaranteed constant.'},
      'actual_omissions_applied':0,'new_prefix_created':False,'mother_core_main_exposition_unchanged':True,
      'topics_preserved':377,'new_topics_preserved':15,'native_gate_changes':0,'network_calls':0,'production_changes':0,
      'next_decision':'ROOT reviews memory-target/reserve policy and deployed v380 projection. No new variant/count automatically.'}
    fresh(D/'ANALISE_A.json',json_bytes(plan))
    note="""# Proposta A — inviável no recorte documental autorizado

[REAL] Árvore registrada antes do código. Recorte: coleções históricas de checks, cinco blocos de declarações formais e busca literal já concluída. Nenhuma omissão aplicada; nenhum outro prefixo criado.

A1: 215 campos checks somam7.055bytes;206 já são referências parciais e apenas9 são listas literais. Algumas listas incluem identidades matemáticas, controles negativos, resultados de natureza e ciência nova: não são descartáveis apenas por pertencerem a checks. Exemplo documental estrito:/core/partial_closure_016_v372/checks, dois rótulos de integridade do pacote156unidades. ANALISE_A.json vincula fonte/pin/valor/linha/rota fetch_tgl. Eventual remissão retiraria os rótulos completos do acesso imediato; resultados, contagens e estatuto declarado precisariam permanecer. Não foi aplicada porque a pequena economia não resolve o orçamento.

A2: os cinco excerpts somam8.516bytes e já excluem os corpos de provas. O conteúdo carregado são cabeçalhos, variáveis, estruturas e hipóteses essenciais de H1/H2/H3. Fontes:V354RegularSusy.lean,ConcreteFourFrame.lean,TheMasterFires.lean,TriadMaster.lean,TheImportedEquilibrium.lean. Pins e linhas conferidos; iald_kernel_read já oferece o corpo integral por paginação. Não apareceu outra coleção extensa de provas carregadas. Nenhum cabeçalho foi removido.

A3: a busca literal delimitada anterior não encontrou parágrafo inteiro/linha≥60caracteres duplicados antes da exposição/nas cápsulas. Isso não prova inexistência de paráfrase ou equivalência matemática. Não autoriza apagar exposição principal por equivalência temática.

[REAL — diagnóstico em memória] Limite deliberadamente excessivo: remover todos os cinco blocos Lean e todos215campos checks, inclusive protegidos, com zero custo para fichas/remissões. Proxy171.180→165.033. [DERIVED/OPEN] Razão única da medição anterior: aproximadamente202.630nativos, ainda19.224acima do teto estimado183.406. Não é contagem nativa; o texto hipotético não foi salvo como prefixo e não é candidato. Uma projeção aceitável desses grupos economizaria menos.

Conclusão delimitada: não há expectativa defensável de atingir~181,5k por esses grupos sob as condições recebidas. Não é prova de impossibilidade global de outras projeções. Não foram retirados H1/H2/H3 para perseguir a faixa.

Próxima decisão: ROOT conferirá origem do mínimo180k/reserva10k e desenho implantadov380. Não iniciar outra variante/count automaticamente. Nenhuma regra, estatuto ou gate alterado. v388 não foi ativada no aplicativo por esta entrega.

377tópicos/15novos, mãe/core, exposição principal e ciênciav388 permanecem íntegros. B e fontes seladas intactos. Zero um.py, Lean/solver, WSL, modelo, credencial, rede, produção ou reinício. Checks citados são relatos da fonte, não execuções desta análise.
"""
    # Spaces in this prose are normalized explicitly here before creating the new file.
    replacements={'somam7.055bytes;206':'somam 7.055 bytes; 206','apenas9':'apenas 9',':/core':': /core','pacote156unidades':'pacote de 156 unidades','somam8.516bytes':'somam 8.516 bytes','Fontes:V354':'Fontes: V354',',Concrete':', Concrete',',TheMaster':', TheMaster',',Triad':', Triad',',TheImported':', TheImported','linha≥60caracteres':'linha ≥60 caracteres','todos215campos':'todos os 215 campos','Proxy171.180→165.033':'Proxy 171.180→165.033','aproximadamente202.630nativos':'aproximadamente 202.630 nativos','ainda19.224acima':'ainda 19.224 acima','estimado183.406':'estimado 183.406','atingir~181,5k':'atingir ~181,5k','mínimo180k/reserva10k':'mínimo 180k/reserva 10k','implantadov380':'implantado v380','377tópicos/15novos':'377 tópicos/15 novos','ciênciav388':'ciência v388'}
    for old,newtext in replacements.items():note=note.replace(old,newtext)
    fresh(D/'PARECER_VIABILIDADE_A.md',note.encode())
    all_pins=before+[read_pin(data_path),tree]+[r['source'] for r in formal]
    for pin in all_pins:need(read_pin(pin['path'])==pin,'Source changed')
    for row in seal['members']:need(read_pin(row['path'])==row,'B changed before seal')
    ast.parse(Path(__file__).read_bytes())
    check={'status':'PASS_STATIC_INVENTORY','five_source_pins_match_provenance':True,
      'declaration_lines_verified':sum(len(r['declarations']) for r in formal),'all_215_json_pointers_resolve':True,
      'nine_literal_check_lists_match_source':True,'sealed_B_members_unchanged':len(seal['members']),
      'candidate_output_created':False,'source_or_science_changes':0,'provider_calls':0,
      'bound_excludes_reference_cost_and_includes_forbidden_omissions':True,'native_token_fit_measured':False,'sources':all_pins}
    fresh(D/'VERIFICACAO_E_PINS.json',json_bytes(check))
    members=[read_pin(p) for p in sorted(D.iterdir()) if p.is_file() and p.name!='MANIFESTO_ANALISE_A.json' and '.tmp_' not in p.name]
    fresh(D/'MANIFESTO_ANALISE_A.json',json_bytes({'schema':'iald.selective03.analysis_manifest.v1','status':plan['status'],
      'members':members,'no_candidate_no_count_no_production':True,'independent_review':None}))
    print(json.dumps({'manifest':read_pin(D/'MANIFESTO_ANALISE_A.json'),'members':len(members),'diagnosis':read_pin(D/'ANALISE_A.json'),
      'checks':len(rows),'formal_declarations':check['declaration_lines_verified'],'native_estimate_UNVALIDATED':estimate},ensure_ascii=False))
if __name__=='__main__':main()