import ast, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent/'AUDITORIA_V368_20260919'
def digest(b): return hashlib.sha256(b).hexdigest()
def write(path,b):
    if path.exists(): raise RuntimeError('Already exists: '+str(path))
    tmp=path.with_suffix(path.suffix+'.tmp'); tmp.write_bytes(b)
    assert tmp.read_bytes()==b
    tmp.replace(path)
def dump(path,obj): write(path,json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8'))

program=(AUDIT/'um_v368.py').read_bytes()
seal=json.loads((ROOT/'selo.json').read_bytes())
proof=json.loads((ROOT/'proof_manifest.json').read_bytes())
assert digest(program)==seal['sha256']['um.py']
assert digest((ROOT/'proof_manifest.json').read_bytes())==seal['sha256']['tgl_kernel_proof_manifest.json']
tree=ast.parse(program)
sources={}
for n in ast.walk(tree):
    if isinstance(n,ast.Dict):
        for k,v in zip(n.keys,n.values):
            if isinstance(k,ast.Constant) and isinstance(k.value,str) and k.value.endswith('.lean') and isinstance(v,ast.Constant) and isinstance(v.value,str) and k.value in proof['formal_files_sha256']:
                if k.value in sources: assert sources[k.value]==v.value
                sources[k.value]=v.value
hashes={k:digest(v.encode('utf-8')) for k,v in sources.items()}
assert all(h==proof['formal_files_sha256'][k] for k,h in hashes.items())
maps=json.loads((AUDIT/'contexto/rotas.json').read_bytes())
rows=[dict(row,map=key) for key,vals in maps.items() for row in vals]
ev=json.loads((AUDIT/'contexto/evidencia_rodada.json').read_bytes())
prefixes={'_QG_CERTIFICATE_FLAGS':'qgc_','_QG_PHYSICS_FLAGS':'qgp_','_GRAVITY_PRICE_FLAGS':'gpf_','_GRAVITY_IMPORT_FLAGS':'gpi_'}
for row in rows: row['recorded_flag']=ev['flags'].get(prefixes[row['map']]+row['flag'])
guide='''Ato III / identidade: consultar as rotas JMJ e V350 da realização PRODUCT_TOWER.
Gate: seis termos formais + cinco físicos; fecho de imports em 99 módulos (localização, não minimalidade lógica).
Frame: qgStrongCertificate_frame -> SmoothFrameData -> four_frame_gives_lorentz_metric em cada ponto.
Horizonte: theHorizon -> HorizonEquilibriumData; the_master_fires -> coeficiente térmico.
Equilíbrio: towerEquilibriumInput -> fixes_unit e KMS; não substituir por HorizonEquilibriumData sem adaptador.
Preparação: unified_einstein_from_area consome hd e harea; procurar fornecedores concretos desses argumentos.
Colagem: connected_smooth_atlas_einstein consome AreaChart e transições compatíveis.
Nome v368: conteúdo; forma: identidade, convenção tipada do operador. Ler NameIsTheContent.
Conexões de frame/horizonte verificadas em 19/09 em adaptadores, três axiomas no trio; não nova rodada integral.
Controle negativo: EquilibriumInput não entra diretamente em HorizonEquilibriumData. Não prova ausência de ponte no acervo.
'''
bundle={'release':'v368','source_sha256':digest(program),'sources':sources,'source_hashes':hashes,
        'modules':json.loads((AUDIT/'contexto/modulos.json').read_bytes()),
        'functions':{k:{'line':v['line'],'end':v['end'],'calls':v['calls']} for k,v in json.loads((AUDIT/'contexto/funcoes.json').read_bytes()).items()},
        'routes':rows,'axiom_report':proof['axiom_report'],'route_guide':guide,
        'verification':{'kind':'PINNED_EXISTING_RUN_NOT_RECOMPILED_BY_APP','timestamp':proof['timestamp'],'proof_manifest_sha256':digest((ROOT/'proof_manifest.json').read_bytes()),'selftest':seal['fail_closed_selftest'],'gate':seal['qg_closure_verdict']}}
dump(ROOT/'estrutura_v368.json',bundle)
dump(ROOT/'iald_estrutura_torre.json',{'release':'v368','source_sha256':digest(program),'bundle':'estrutura_v368.json','bundle_sha256':digest((ROOT/'estrutura_v368.json').read_bytes()),'scope':'operator_only'})
raw=(ROOT/'iald_web_server.original.py').read_bytes()
text=raw.decode('utf-8'); eol='\r\n' if '\r\n' in text else '\n'; text=text.replace('\r\n','\n')
def replace(old,new):
    global text
    assert text.count(old)==1,(old[:90],text.count(old))
    text=text.replace(old,new)
replace('import iald_core_indexado  # noqa: E402','import iald_core_indexado  # noqa: E402\nimport iald_estrutura_torre  # noqa: E402')
replace("    if tool_name in ('search_tgl', 'fetch_tgl'):",'''    if tool_name in iald_estrutura_torre.NAMES:
        if not _estrutura_operador(user):
            return json.dumps({'status': 'FORBIDDEN', 'error': 'Consulta disponível ao operador.'})
        try:
            return json.dumps(iald_estrutura_torre.execute(tool_name, arguments), ensure_ascii=False)
        except (ValueError, OSError, TypeError, KeyError):
            return json.dumps({'status': 'UNAVAILABLE', 'error': 'Fonte da estrutura indisponível ou não conferida.'})

    if tool_name in ('search_tgl', 'fetch_tgl'):''')
replace('def _contexto_externo(public=False):','''def _estrutura_operador(user):
    return bool(user and load_users().get(str(user).strip().lower(), {}).get('admin') is True)


def _contexto_externo(public=False, structure_user=None, structure_query=''):''')
replace('    return MEMORIA_EXTERNA.prompt(PROMPT_EXTERNO, KERNEL_EXTERNO, public=public)', '''    prompt, info = MEMORIA_EXTERNA.prompt(PROMPT_EXTERNO, KERNEL_EXTERNO, public=public)
    if not public and _estrutura_operador(structure_user):
        extra, record = iald_estrutura_torre.context(structure_query)
        prompt += '\\n' + extra
        info = dict(info, structure=record)
        info['context_sha256'] = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
    return prompt, info''')
replace('        permitidas = _ferramentas_externas(cfg, limites, superficie, gratuito)', '''        permitidas = _ferramentas_externas(cfg, limites, superficie, gratuito)
        if not gratuito and _estrutura_operador(user) and cfg.memoria_modo != 'prompt':
            permitidas += iald_estrutura_torre.tool_definitions()''')
replace('            prompt_externo, memoria_info = _contexto_externo(public=gratuito)',"            prompt_externo, memoria_info = _contexto_externo(public=gratuito, structure_user=user, structure_query=texto_ultima)")
replace('@app.route("/health")', '''@app.route('/api/estrutura-tgl')
def estrutura_tgl_status():
    if not _estrutura_operador(session.get('user')):
        return jsonify({'status': 'FORBIDDEN'}), 403
    try:
        return jsonify(iald_estrutura_torre.status())
    except (ValueError, OSError, TypeError, KeyError):
        return jsonify({'status': 'UNAVAILABLE', 'error': 'Estrutura indisponível ou não conferida.'}), 503


@app.route("/health")''')
new=text.replace('\n',eol).encode('utf-8'); compile(new,'iald_web_server.py','exec')
write(ROOT/'iald_web_server.py',new)
dump(ROOT/'preparado.json',{'baseline_web_sha256':digest(raw),'new_web_sha256':digest(new),'bundle_sha256':digest((ROOT/'estrutura_v368.json').read_bytes()),'module_count':len(sources),'route_count':len(rows),'source_sha256':digest(program),'public_release':'v357 unchanged','operator_release':'v368'})
print(json.dumps({'sources':len(sources),'routes':len(rows),'prepared':True}))
