"""Apply the operator's later instruction: MiMo has no local spending/call ceiling."""
from pathlib import Path
from iald_orchestrator.safe_files import replace_bytes
BASE=Path(__file__).resolve().parent
def edit(name,pairs):
 p=BASE/name;s=p.read_text(encoding='utf-8')
 for old,new in pairs:
  assert s.count(old)==1,(name,old[:100]);s=s.replace(old,new)
 replace_bytes(p,s.encode())

edit('iald_orchestrator/request_controls.py',[
 ("'max_calls','max_projection_chars'}", "'max_calls'}"),
 ("    if type(c['max_projection_chars']) is not int or not 1000 <= c['max_projection_chars'] <= 20000:",
  "    if 'max_projection_chars' not in c: c['max_projection_chars']=None if c['required_provider']=='mimo' else 20000\n    if c['max_projection_chars'] is not None and (type(c['max_projection_chars']) is not int or not 1000 <= c['max_projection_chars'] <= 20000):"),
 ("        cost = c.get('max_cost_usd')\n        if not isinstance(cost,str) or not re.fullmatch(r'0\\.[0-9]{1,8}',cost) or not Decimal('0') < Decimal(cost) <= Decimal('0.50'):\n            raise ValueError('MiMo exige teto por chamada positivo e não superior a US$0,50.')\n        c['max_cost_usd'] = str(Decimal(cost).normalize())\n        if type(c.get('max_output_tokens')) is not int or not 1 <= c['max_output_tokens'] <= 4096:\n            raise ValueError('MiMo exige limite de saída entre 1 e 4096 tokens.')",
  "        if c.get('max_cost_usd') is not None:\n            raise ValueError('Ordem posterior do operador: MiMo sem teto financeiro local; remover o teto antigo.')\n        c['max_cost_usd']=None\n        c.setdefault('max_output_tokens',131072)\n        if type(c['max_output_tokens']) is not int or not 1 <= c['max_output_tokens'] <= 131072:\n            raise ValueError('Saída MiMo deve respeitar o limite técnico 1..131072.')"),
 ("    p=pricing()\n    upper=", "    return {'reserved_usd':'0','scope':'EXECUTOR_ONLY','billing':'PAID_NO_LOCAL_FINANCIAL_CAP','max_output_tokens':c['max_output_tokens'],'operator_override':'MIMO_MAXIMUM_20260924'}\n    p=pricing()\n    upper="),
 ("    if len(system+'\\n\\nTAREFA:\\n'+packet['prompt']) > c['max_projection_chars']:",
  "    if c['max_projection_chars'] is not None and len(system+'\\n\\nTAREFA:\\n'+packet['prompt']) > c['max_projection_chars']:"),
 ("    rows=list(db.execute('SELECT * FROM request_budget_ledger WHERE mission=?',(c['mission_id'],)))",
  "    if c['required_provider']=='mimo':\n        return  # Explicit later operator instruction: no artificial MiMo quotas.\n    rows=list(db.execute('SELECT * FROM request_budget_ledger WHERE mission=?',(c['mission_id'],)))"),
 ("    upper=Decimal(q['reserved_usd'])\n    if sum((Decimal(r['accounted_usd']) for r in branch),Decimal(0))+upper>Decimal('0.50'):\n        raise ValueError('Reserva ultrapassa US$0,50 no ramo.')\n    if sum((Decimal(r['accounted_usd']) for r in rows),Decimal(0))+upper>Decimal('10'):\n        raise ValueError('Reserva ultrapassa US$10 na missão.')\n", ""),
 ("q['reserved_usd'],q['reserved_usd'],'RESERVED_OR_UNCERTAIN'))",
  "q['reserved_usd'],q['reserved_usd'],'UNMETERED_OR_UNCERTAIN' if c['required_provider']=='mimo' else 'RESERVED_OR_UNCERTAIN'))")])

# Remove unreachable financial-enforcement proposal; pricing remains documentary only.
p=BASE/'iald_orchestrator/request_controls.py';s=p.read_text(encoding='utf-8');a=s.index('    p=pricing()\n',s.index('def quote'));b=s.index('\ndef enforce_packet',a);replace_bytes(p,(s[:a]+s[b:]).encode())

edit('iald_orchestrator/mimo.py',[
 ('MAX_OUTPUT = 4096','CONTEXT_WINDOW = 1048576\nMAX_OUTPUT = 131072\nMAX_INPUT_BYTES = CONTEXT_WINDOW - MAX_OUTPUT - 4096\nMAX_RESPONSE_BYTES = 32_000_000'),
 ("len(prompt.encode('utf-8')) > 40000", "len(prompt.encode('utf-8')) > MAX_INPUT_BYTES"),
 ('timeout=180','timeout=7200'),
 ('response.read(2_000_001)','response.read(MAX_RESPONSE_BYTES + 1)'),
 ('len(body) > 2_000_000','len(body) > MAX_RESPONSE_BYTES'),
 ("    return 'installed_pending_auth_validation'\n\n\nclass NoRedirect", '''    # A reviewed configuration migration may preserve the prior authentication
    # evidence without misrepresenting it as a new paid connection test.
    migration = BASE/'validation/mimo_maximum_migration.json'
    if RECEIPT.is_file() and migration.is_file():
        old=json.loads(RECEIPT.read_bytes()); proof=json.loads(migration.read_bytes())
        current=signature(); previous=old.get('signature',{})
        if (old.get('status')=='ready' and proof.get('validation_type')=='OFFLINE_CAPABILITY_UPDATE_PRIOR_AUTH'
            and proof.get('previous_adapter_sha256')==previous.get('adapter_sha256')
            and proof.get('current_adapter_sha256')==current['adapter_sha256']
            and {k:v for k,v in previous.items() if k!='adapter_sha256'}=={k:v for k,v in current.items() if k!='adapter_sha256'}):
            return 'ready'
    return 'installed_pending_auth_validation'


class NoRedirect''')])

edit('iald_orchestrator/canonical_memory.py',[
 ('*, allowed_sources=None):','*, allowed_sources=None, mode="standard"):'),
 ('    # Keep a fixed ceiling for memory; the policy accounts for the final packet.',
  "    if mode not in ('standard','maximum'): raise ValueError('Modo de memória desconhecido.')\n    maximum=mode=='maximum'\n    # Maximum mode packs against a conservative UTF-8 byte bound; not an exact tokenizer."),
 ('    allowance = min(15000, 36000 - len(prompt.encode()) - len(header.encode()))',
  "    allowance = (1048576-131072-8192 if maximum else 36000) - len(prompt.encode()) - len(header.encode())\n    if not maximum: allowance=min(15000,allowance)"),
 ("        if query:\n            rows += list(db.execute('SELECT rowid,* FROM passages WHERE passages MATCH ? ORDER BY bm25(passages) LIMIT 30', (query,)))", '''        if maximum:
            rows=[]
            priority=['um_absoluto_forma_canonica.md','A_PROVA_DA_QG_TGL_arvore.md',
                'ERRATA_20260919_sinal_do_acoplamento_nao_minimo.md','A Ponte Einstein Cartan Miguel.tex',
                'paper_PT.tex','DESENHO_DO_FECHAMENTO_QG.md','um_absoluto_selo.json']
            for name in priority:
                rows += list(db.execute('SELECT rowid,* FROM passages WHERE document=? ORDER BY rowid',(name,)))
        if query:
            rows += list(db.execute('SELECT rowid,* FROM passages WHERE passages MATCH ? ORDER BY bm25(passages) LIMIT ?', (query,1000 if maximum else 30)))'''),
 ("counts.get(row['document'], 0) >= 3", "(not maximum and counts.get(row['document'], 0) >= 3)"),
 ('    validate_prompt(body)', "    if maximum:\n        if FORBIDDEN.search(body): raise ValueError('Referência confidencial no contexto.')\n    else:\n        validate_prompt(body)"),
 ("'blocked_passages': blocked, 'weights_modified': False", "'blocked_passages': blocked, 'weights_modified': False, 'memory_mode':mode, 'packing':'CONSERVATIVE_UTF8_BYTES' if maximum else 'BOUNDED_RETRIEVAL'")])

edit('iald_orchestrator/providers.py',[
 ('row.update(status=mimo.connection_status(), daily_run_limit=None,','row.update(status=mimo.connection_status(), daily_run_limit=None, context_budget=mimo.CONTEXT_WINDOW,'),
 ("packet = memory_packet if memory_packet is not None else canonical_memory.prepare(prompt)", "packet = memory_packet if memory_packet is not None else canonical_memory.prepare(prompt,mode='maximum' if name=='mimo' else 'standard')"),
 ("    prompt = validate_prompt(packet['prompt'])\n    if len((SYSTEM + prompt).encode()) > 39000:",
  "    prompt = packet['prompt'] if name=='mimo' else validate_prompt(packet['prompt'])\n    if name!='mimo' and len((SYSTEM + prompt).encode()) > 39000:"),
 ('result = mimo.execute(SYSTEM + "\\n\\nTAREFA:\\n" + prompt, cancel=cancel, max_output=',
  'result = mimo.execute(SYSTEM.replace("Limite a resposta a cerca de 1500 palavras.", "Desenvolva a resposta e a matemática na extensão necessária à tarefa e às evidências.") + "\\n\\nTAREFA:\\n" + prompt, cancel=cancel, max_output='),
 ('if len(result["text"]) > 120000:', 'if len(result["text"]) > (32_000_000 if name=="mimo" else 120000):')])

edit('iald_orchestrator/runtime.py',[
 ("        packet = canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None)",
  "        packet = canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None,mode='maximum' if c and c['required_provider']=='mimo' else 'standard')"),
 ("            packet = canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None)",
  "            packet = canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None,mode='maximum' if c and c['required_provider']=='mimo' else 'standard')"),
 ('        decision["execution_constraints"] = c', '''        if decision['selected']=='mimo' and packet['receipt']['memory_mode']!='maximum':
            packet=canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None,mode='maximum')
            controls.enforce_packet(packet,c,providers.SYSTEM)
            decision['canonical_memory']=packet['receipt']
            decision['task']['estimated_input_tokens']=classify(providers.SYSTEM+packet['prompt'])['estimated_input_tokens']
        decision["execution_constraints"] = c'''),
 ('            decision["execution_constraints"]=c', '''            if decision['selected']=='mimo' and packet['receipt']['memory_mode']!='maximum':
                packet=canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None,mode='maximum')
                controls.enforce_packet(packet,c,providers.SYSTEM)
                decision['task']['estimated_input_tokens']=classify(providers.SYSTEM+packet['prompt'])['estimated_input_tokens']
            decision["execution_constraints"]=c''')])
