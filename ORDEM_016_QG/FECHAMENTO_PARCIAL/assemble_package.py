"""Consolidate measured receipts; sealing is a separate explicit command."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,re,sys
from audit_names import strip_comments,declarations
S=Path(__file__).resolve().parent
R=S.parent
ROOT=R.parent
OUT=ROOT/'TUNEL/DO_CHATGPT'
P=OUT/'FECHAMENTO_PARCIAL_016'
TRIO={'propext','Classical.choice','Quot.sound'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def write(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    raw=data.encode('utf-8') if isinstance(data,str) else data
    if p.exists():
        if p.read_bytes()==raw:return
        raise FileExistsError(p)
    t=p.with_name(p.name+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def copy(a,b):write(b,a.read_bytes())
def ident(name):return name.replace('D1′','D1prime').replace('D2′','D2prime').replace('D3′','D3prime')
def relative(p):return p.relative_to(P).as_posix()

def collect_unit(module,item,receipt,also=None):
    r=read(receipt);src=S/'lean'/(module+'.lean');log=receipt.with_suffix('.log')
    assert sha(src)==r['source_sha256'] and sha(log)==r['log_sha256']
    dest=P/'lean'/src.name
    copy(src,dest);copy(log,P/'logs'/log.name);copy(receipt,P/'logs'/receipt.name)
    own={};kind={}
    for line in log.read_text('utf-8',errors='strict').splitlines():
        if line.startswith('BENCH_DECL\t'):
            _,n,k,ax=line.split('\t');own[n]=list(filter(None,ax.split(',')));kind[n]=k
    assert all(set(v)<=TRIO for v in own.values())
    assert 'axiom' not in kind.values()
    assert not re.search(r'\b(sorry|admit|axiom)\b',strip_comments(src.read_text('utf-8')))
    return dict(module=module,item=item,also_items=also or [],rc=r['rc'],source=relative(dest),source_sha256=sha(dest),
        log='logs/'+log.name,log_sha256=sha(log),receipt='logs/'+receipt.name,receipt_sha256=sha(receipt),
        axioms=own,declaration_kinds=kind,new_declaration_count=len(own),
        wall_seconds=r['wall_seconds'],cpu_seconds=r['cpu_seconds'],peak_committed_bytes=r['peak_committed_bytes'])

def assemble():
    if (P/'PRONTO.json').exists():raise FileExistsError('Package sealed; do not overwrite it')
    joint=read(S/'JOINT_FINAL_RESULT.json');assert joint['result']['rc']==0,'Joint import failed: report MEDIDA before packaging'
    assert 'ContratoQG_v32_Proposta' in joint['modules'],'P3 compilation missing: do not announce a compiled proposal'
    plan=read(S/'SOURCE_PLAN.json');rows={x['module']:x for x in plan['sources']}
    batch=read(S/'BATCH_RESULT.json');states={x['module']:x for x in batch['states']}
    supp=read(S/'SUPPLEMENTAL_RESULTS.json');sr={x['module']:x for x in supp}
    superseded_attempts={x.get('supersedes_attempt') for x in supp if x['result'].get('rc')==0}
    assert all(x['expected_outcome_observed'] or x['module'] in superseded_attempts for x in supp),'Unexpected control result'
    P.mkdir(parents=True,exist_ok=True)
    units=[]
    for n in joint['modules']:
        row=rows.get(n,{});item=row.get('branch',sr.get(n,{}).get('item','P3'))
        receipt=Path(sr[n]['receipt']) if n in sr else Path(states[n]['receipt'])
        units.append(collect_unit(n,item,receipt,['A6'] if item=='C3' else []))
    units.append(collect_unit(joint['module'],'P2',Path(joint['receipt'])))
    assert all(x['rc']==0 for x in units)
    failure=[]
    for state in batch['states']:
        if state.get('rc')==0:continue
        n=state['module'];replacement=next((x['module'] for x in supp if x.get('supersedes')==n and x['result'].get('rc')==0),None)
        failure.append(dict(**state,replacement=replacement))
        copy(S/'lean'/(n+'.lean'),P/'recusas'/ (n+'.lean'))
        if state.get('receipt'):
            rp=Path(state['receipt']);copy(rp,P/'recusas'/rp.name);copy(rp.with_suffix('.log'),P/'recusas'/rp.with_suffix('.log').name)
        msg=f'# MEDIDA de integração: {n}\n\n[REAL] A compilação inicial teve status {state["status"]}.\n\nCorreção: {replacement or "não disponível; arquivo excluído dos imports ativos"}. O log integral permanece no pacote. Não há novo teorema nem mudança do gate.\n'
        write(P/'recusas'/('MEDIDA_'+n+'.md'),msg)
        write(OUT/('ENTREGA_016_MEDIDA_consolidacao_'+n+'.md'),msg)
    for x in supp:
        if x['expected_rc']==0 and x['result'].get('rc')!=0:
            rp=Path(x['receipt']);copy(Path(x['source']),P/'recusas'/(x['module']+'.lean'))
            copy(rp,P/'recusas'/rp.name);copy(rp.with_suffix('.log'),P/'recusas'/rp.with_suffix('.log').name)
        if x['expected_rc']!=1:continue
        rp=Path(x['receipt']);copy(Path(x['source']),P/'controles'/ (x['module']+'.lean'))
        copy(rp,P/'controles'/rp.name);copy(rp.with_suffix('.log'),P/'controles'/rp.with_suffix('.log').name)
    # Exact environment export versus original lexical names: no silent collision.
    census={}
    for line in (S/'logs/kernel_census_01.log').read_text('utf-8').splitlines():
        if line.startswith('KERNEL_DECL\t'):
            _,n,m,k=line.split('\t');census[n]=dict(module=m,kind=k)
    original_collisions=[]
    for row in plan['sources']:
        p=Path(row['original']);assert sha(p)==row['original_sha256']
        for n in declarations(p.read_text('utf-8-sig')):
            if n in census:original_collisions.append(dict(name=n,original=str(p),original_sha256=sha(p),canonical=census[n],adaptations=row['changes']+[dict(replacement=x['module'],reason=x['reason']) for x in supp if x.get('supersedes')==row['module']]))
    active_collisions=[];duplicates=[];seen={};reserved=[]
    for u in units:
        for n in u['axioms']:
            if n in census:active_collisions.append(dict(name=n,module=u['module'],canonical=census[n]))
            if n in seen:duplicates.append(dict(name=n,modules=[seen[n],u['module']]))
            seen[n]=u['module']
            if any(x.startswith(('qgPrice_','qgImport_')) for x in n.split('.')):reserved.append(n)
    def generated_import_equation(n):
        m=re.match(r'^(.*)\.eq_[0-9]+$',n)
        return bool(m and (m[1] in census or m[1] in seen))
    genuine_collisions=[x for x in active_collisions if not generated_import_equation(x['name'])]
    genuine_duplicates=[x for x in duplicates if not generated_import_equation(x['name'])]
    assert not genuine_collisions and not genuine_duplicates and not reserved
    for u in units:
        u['audited_declaration_count']=len(u['axioms'])
        u['introduced_declarations']=[n for n in u['axioms'] if n not in census and not generated_import_equation(n)]
        u['new_declaration_count']=len(u['introduced_declarations'])
    sources=read(S/'KERNEL_SNAPSHOT.json')['formal_sources']
    source_modules={x['path'][:-5].replace('/','.') for x in sources if x['path'].endswith('.lean') and x['path'].startswith(('TGL/','TGLExt/'))}
    seen_modules={v['module'] for v in census.values()}
    missing=sorted(source_modules-seen_modules)
    supplemental_lexical=[]
    for mod in missing:
        cp=S/'kernel_v371'/(mod.replace('.','/')+'.lean')
        for n in declarations(cp.read_text('utf-8-sig')):
            if n in seen:supplemental_lexical.append(dict(name=n,canonical_module=mod,bench_module=seen[n]))
    assert not supplemental_lexical
    audit=dict(census_declarations=len(census),census_modules=len(seen_modules),census_log_sha256=sha(S/'logs/kernel_census_01.log'),
        original_explicit_collisions=original_collisions,active_elaborated_collisions=active_collisions,active_duplicate_names=duplicates,
        genuine_unresolved_collisions=genuine_collisions,genuine_unresolved_duplicates=genuine_duplicates,
        generated_equation_reuse_note='Repeated .eq_N theorems belong to imported canonical or bench definitions present in the audited environment. Listed explicitly, excluded from new declaration counts; aggregate import checks coexistence.',
        reserved_names_created=reserved,unexpected_axioms=[],source_modules_without_exported_declarations=missing,
        supplementary_source_name_collisions=supplemental_lexical,
        limitation='Original/source fallback scan is lexical and excludes generated names; all active compiled own names exported exactly; joint import tests coexistence with TGL/TGLExt. Source-only unused modules are identified separately.')
    save(P/'P2_COLISOES.json',audit)
    imports=sorted({i for u in units for i in re.findall(r'^import (\S+)\s*$',(P/u['source']).read_text('utf-8'),re.M) if i.startswith(('TGL.','TGLExt.'))})
    save(P/'P2_COMPILACAO.json',dict(status='JOINT_IMPORT_COMPILED',base='v371',units=units,reproduction_order=joint['modules']+[joint['module']],
        failed_initial_attempts=failure,kernel_imports=imports,full_canonical_roots=['TGL','TGLExt'],
        per_process_limit_gib=12,legacy_limit_gib=8,canonical_rebuilt=False,gate_changed=False))
    write(P/'P2_COMPILACAO.md', '# P2 — consolidação Lean\n\n[REAL] '+str(len(units))+' unidades ativas com rc=0, incluindo o import conjunto. '+str(len(seen))+' nomes auditados na elaboração (inclui tipos, campos e auxiliares importados; não é contagem de teoremas novos).\n\nTodos os axiomas próprios são subconjunto do trio; nenhuma declaração axiomática nova. A lista por declaração está no JSON. A cópia de fontes v371 foi conferida pelo manifesto; os builds canônicos foram copiados, não recompilados nesta rodada. Compilador limitado a 12 GiB; isso não apaga recusas históricas sob 8 GiB.\n\n'+str(len(original_collisions))+' colisões explícitas nas fontes originais foram listadas, com as adaptações; zero colisões não resolvidas entre declarações próprias. Repetições dos auxiliares importados .eq_N estão listadas e excluídas da contagem de novidades. Módulos de fonte sem declarações no censo e a limitação lexical estão em P2_COLISOES.json.\n\nAs falhas iniciais e os controles negativos estão separados dos imports de produção. Não mover gate pela soma de rc.\n')
    support=read(S/'apoio_coordenacao/quadro_apoio.json');opens=read(S/'documents/P3_HIPOTESES_ABERTAS.json');items=[]
    for row in support['items']:
        item=ident(row['item']);us=[u for u in units if u['item']==item or item in u['also_items']]
        named=[h['name'] for h in opens if item in h['items'].split('/')]
        status=row['status'];notes=row['remaining_named']
        if item=='A2':status='MEDIDA';notes+='; A2.5c pago no escopo da transformada, não toda instanciação física.'
        if item=='A6':notes='A integração das 12 fontes foi paga em C3; a recusa antiga de empacotamento permanece histórica. Limite infinito forte continua aberto.'
        if item=='C3':named=[]
        if item=='D4':named=[]
        if item=='C1':notes+='; a presente integração usa 12 GiB, não satisfaz retroativamente o ensaio de 8 GiB.'
        if status=='MEDIDA':assert named,(item,'needs named missing lemma')
        items.append(dict(item=item,status=status,scope=notes,named_open_hypotheses=named,
            declarations=sorted({n for u in us for n in u['introduced_declarations']}),
            files=[dict(path=u['source'],sha256=u['source_sha256'],log=u['log'],log_sha256=u['log_sha256']) for u in us],
            prior_sources=row['sources'],prior_metrics=row['measured_metrics_from_evidence'],
            consolidation_cpu_hours=sum(u['cpu_seconds'] for u in us)/3600,consolidation_wall_hours=sum(u['wall_seconds'] for u in us)/3600,
            new_external_cost_usd=0,prior_item_total_cost_usd=None,unknown_cost_is_zero=False,
            identities_by_construction=['Reflexive transport or parameter matching by rfl is not an independent physical realization'] if item in ('A5','D6') else []))
    for item in ('D1','D2','D3'):items.append(dict(item=item,status='CANCELADO',scope='Substituído pelo ADENDO016-003-ter; conservar história, não implementar como alvo vigente',named_open_hypotheses=[],files=[],declarations=[],hours=None,cost_usd=None))
    save(P/'P1_QUADRO.json',dict(items=items,prior_costs=support['costs'],prior_hours=support['hours'],consolidation_start=read(S/'START.json'),gate_changed=False))
    md=['# P1 — quadro do fechamento parcial','', 'PAGO refere-se ao escopo indicado, não à confirmação física. MEDIDA preserva a parte compilada e nomeia o que falta. Custos desconhecidos não são zero; intervalos históricos não devem ser somados.','', '| Item | Estatuto | Escopo e pendências |','|---|---|---|']
    for x in items:md.append('| '+x['item']+' | '+x['status']+' | '+x['scope']+' '+', '.join(x['named_open_hypotheses'])+' |')
    md+=['','Nomes, hashes, recibos, horas por item e métricas anteriores: P1_QUADRO.json. A6/C3 compartilham evidência, não somar como duas provas.']
    write(P/'P1_QUADRO.md','\n'.join(md)+'\n')
    for doc in (S/'documents').iterdir():
        if doc.is_file() and '.bak_' not in doc.name:copy(doc,P/doc.name)
    for n in ['PROPOSTA_RUNTIME.py','reproduzir.py','run_lean.py','RUNTIME_CONTROLS.json','REPRODUCTION_CONTROLS.json','test_runtime_proposal.py'] :copy(S/n,P/n)
    # Primary prior reports are copied with their present hashes; dated index hashes are preserved too.
    evidence=[]
    candidates=read(S/'documents/P8_FONTES.json')+[x for row in support['items'] for x in row['sources']]
    for row in candidates:
        src=Path(row['path'])
        if any(x['source']==str(src) for x in evidence):continue
        assert src.is_relative_to(ROOT),'No cross-house source admitted'
        assert sha(src)==row['sha256'],('HISTORICAL_SOURCE_CHANGED',str(src),row['sha256'],sha(src))
        dest=P/'evidencias/historico'/src.relative_to(ROOT)
        copy(src,dest);evidence.append(dict(source=str(src),path=relative(dest),sha256=sha(dest),previously_indexed_sha256=row['sha256'],unchanged=sha(dest)==row['sha256']))
    save(P/'P8_COPIAS.json',evidence)
    for n in ['SOURCE_PLAN.json','SUPPLEMENTAL_PLAN.json','SUPPLEMENTAL_RESULTS.json','BATCH_RESULT.json','JOINT_RESULT.json','JOINT_FINAL_RESULT.json','KERNEL_SNAPSHOT.json','kernel_proof_manifest_origin.json','START.json','SUPPORT_PIN.json']:
        copy((S/'documents'/n) if n=='SUPPORT_PIN.json' else (S/n),P/'evidencias'/n)
    for n in ['REVISAO_EMPACOTAMENTO.json','REVISAO_EMPACOTAMENTO.md','REVISAO_DELTAS.json']:
        copy(S/'apoio_coordenacao'/n,P/'evidencias'/n)
    copy(S/'PACKAGING_ADJUDICATION.json',P/'evidencias/PACKAGING_ADJUDICATION.json')
    copy(S/'logs/kernel_census_01.log',P/'evidencias/kernel_census_01.log');copy(S/'logs/kernel_census_01.json',P/'evidencias/kernel_census_01.json')
    for n in ['joint_bundle_01.json','joint_bundle_01.log']:
        copy(S/'logs'/n,P/'evidencias/initial_aggregate'/n)
    for old in joint['excluded_superseded']:
        if states.get(old,{}).get('rc')==0:
            rp=Path(states[old]['receipt']);copy(rp,P/'evidencias/superseded'/rp.name)
            copy(rp.with_suffix('.log'),P/'evidencias/superseded'/rp.with_suffix('.log').name)
    shutil.copytree(S/'original_sources',P/'originais_bancada');shutil.copytree(S/'diffs',P/'diffs')
    shutil.copytree(S/'kernel_v371',P/'kernel_v371')
    cfg=read(S/'compile_config.json');save(P/'REPRODUCAO_CONFIG.json',dict(lake=cfg['lake'],external_imports=cfg['imports'][1:]))
    for n in ['lean-toolchain','lakefile.toml','lake-manifest.json']:copy(S/'compiler_env'/n,P/'reproduction_environment'/n)
    write(P/'P5_RUNTIME.md','# P5 — proposta de integração\n\nLeitores de custódia e compilação, com controles negativos. `all_verified` só tem esse escopo. A gerência fixa EXPECTED_MANAGEMENT_PACKAGE_SHA256 externamente após conferir PRONTO; sem esse pin, a proposta recusa. O recibo e as linhas BENCH_DECL são cruzados com o índice. Nenhum retorno fornece um habitante físico H2/H3. C6, sem unidade Lean compilada, recusa por falta de evidência, preservando a MEDIDA. Os '+str(len(read(S/'RUNTIME_CONTROLS.json')['cases']))+' casos de RUNTIME_CONTROLS são ensaios sintéticos de engenharia, não provas físicas.\n')
    write(P/'P7_REPRODUCAO.md','# P7 — reprodução\n\nExecutar `python -X utf8 -B reproduzir.py --work <nova_pasta> --expected-ready-sha256 <hash_recebido_da_gerencia>` em Windows com a mesma toolchain e dependências Mathlib registradas. O script confere o pin externo e os hashes, copia a base v371 e recompila só os módulos ativos e o import conjunto. Não executa um.py nem lake build. Os logs desta entrega são da rodada de consolidação; o script de reprodução integral ainda não foi executado de ponta a ponta. Falta de toolchain/dependência é erro visível.\n')
    index='# ENTREGA016 — FECHAMENTO PARCIAL\n\n[REAL] Pacote em FECHAMENTO_PARCIAL_016. A entrega só se efetiva com PRONTO.json escrito por último.\n\n'+ '\n'.join('- '+n for n in ['P1_QUADRO.md / .json','P2_COMPILACAO.md / .json e P2_COLISOES.json','P3_CONTRATO.md, P3_CLAUSULAS.json, P3_HIPOTESES_ABERTAS.md e lean/ContratoQG_v32_Proposta.lean','P4_LEITOR_A8.md e controles/','P5_RUNTIME.md / PROPOSTA_RUNTIME.py','P6_ARTIGO_PT_EN.md','P7_REPRODUCAO.md / reproduzir.py','P8_ERRATAS.md / P8_COPIAS.json','P9_PAUSA_RINGDOWN.md / P9_PARTE_B.json'])+'\n\nCompilação conjunta: rc=0. Escopo condicionado item a item; a proposta v3.2 não é um habitante físico. O gate não mudou. A gerência incorpora e realiza seu rito; nenhuma fonte canônica foi editada.\n\nParte B preservada até T06, sem hora pesada. Próximo passo T11 após o selo; correção recebida da gerência tem prioridade. Relatório final016 continua devido depois da Parte B e citará o hash de PRONTO.\n'
    write(OUT/'ENTREGA_016_FECHAMENTO_PARCIAL.md',index)
    save(S/'ASSEMBLY_RESULT.json',dict(package=str(P),active_units=len(units),own_declarations=len(seen),original_collisions=len(original_collisions),stage='ASSEMBLED_NOT_SEALED',gate_changed=False))
    print('ASSEMBLED_NOT_SEALED',len(units),len(seen))

def seal():
    assert P.is_dir() and not (P/'PRONTO.json').exists()
    audit=read(P/'P2_COLISOES.json');assert not audit['genuine_unresolved_collisions'] and not audit['genuine_unresolved_duplicates']
    assert all(x['unchanged'] and sha(P/x['path'])==x['sha256']==x['previously_indexed_sha256'] for x in read(P/'P8_COPIAS.json'))
    assert read(P/'P2_COMPILACAO.json')['status']=='JOINT_IMPORT_COMPILED'
    for u in read(P/'P2_COMPILACAO.json')['units']:
        for kind in ['source','log','receipt']:assert sha(P/u[kind])==u[kind+'_sha256']
    snapshot=read(P/'evidencias/KERNEL_SNAPSHOT.json')
    for row in snapshot['formal_sources']+snapshot['copied_build']:assert sha(P/'kernel_v371'/row['path'])==row['sha256']
    files={p.relative_to(P).as_posix():sha(p) for p in sorted(P.rglob('*')) if p.is_file()}
    assert not any(n.endswith('.tmp') for n in files)
    index=OUT/'ENTREGA_016_FECHAMENTO_PARCIAL.md'
    save(P/'PRONTO.json',dict(at=datetime.now(timezone.utc).isoformat(),status='PARTIAL_THEORETICAL_PACKAGE_DELIVERED',files=files,
        index=dict(path=str(index),sha256=sha(index)),gate_changed=False,canonical_written=False,part_B_resume='T11'))
    print('SEALED',len(files),sha(P/'PRONTO.json'))
if __name__=='__main__':
    if sys.argv[1:] == ['--seal']:seal()
    else:assemble()
