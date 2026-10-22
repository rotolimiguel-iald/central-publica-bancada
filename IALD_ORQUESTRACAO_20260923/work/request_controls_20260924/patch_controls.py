from pathlib import Path
from iald_orchestrator.safe_files import replace_bytes
BASE=Path(__file__).resolve().parent
def edit(name,replacements):
 p=BASE/name;raw=p.read_bytes();nl='\r\n' if b'\r\n' in raw else '\n';text=raw.decode().replace('\r\n','\n')
 for old,new in replacements:
  assert text.count(old)==1,(name,old[:120]);text=text.replace(old,new)
 replace_bytes(p,text.replace('\n',nl).encode())

edit('iald_orchestrator/canonical_memory.py',[
 ('def prepare(prompt, directory=MEMORY):','def prepare(prompt, directory=MEMORY, *, allowed_sources=None):'),
 ('    header = CORE +', '''    if allowed_sources is not None:
        names={d['name'] for d in manifest['documents']}
        if not set(allowed_sources) <= names:
            raise ValueError('Fonte autorizada não está no índice científico; não ampliar a lista.')
        manifest=dict(manifest,documents=[d for d in manifest['documents'] if d['name'] in allowed_sources])
    header = CORE +'''),
 ("    for row in rows:\n        if row['rowid']", "    for row in rows:\n        if row['document'] not in hashes:\n            continue\n        if row['rowid']")])

edit('iald_orchestrator/runtime.py',[
 ('from . import VERSION, providers, jev, canonical_memory','from . import VERSION, providers, jev, canonical_memory, request_controls as controls'),
 ('            if recover:', '''            if 'execution_constraints' not in {r[1] for r in db.execute('PRAGMA table_info(tasks)')}:
                db.execute('ALTER TABLE tasks ADD COLUMN execution_constraints TEXT')
            controls.init(db)
            if recover:'''),
 ('    def preview(self, prompt):','    def preview(self, prompt, execution_constraints=None):'),
 ('        packet = canonical_memory.prepare(prompt)\n        classification = classify(prompt)', '''        c=controls.normalize(execution_constraints)
        packet = canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None)
        controls.enforce_packet(packet,c,providers.SYSTEM)
        quote=controls.quote(c)
        with self.db() as db: controls.check(db,c,quote)
        classification = classify(prompt)'''),
 ('\n        decision = route(prompt, self.connections(), self.counts(), classification=classification)',
  '\n        decision = route(prompt, controls.restrict(self.connections(),c), self.counts(), classification=classification)'),
 ('        decision["jev"] = {"status": "not_called_in_preview"}',
  '        decision["execution_constraints"] = c\n        decision["cost_reservation"] = quote\n        decision["jev"] = {"status": "not_called_in_preview"}'),
 ('def submit(self, prompt, request_id, *, routing_prompt=None, start_worker=True):','def submit(self, prompt, request_id, *, routing_prompt=None, start_worker=True, execution_constraints=None):'),
 ('        prompt = validate_prompt(prompt)\n        routing_prompt', '        prompt = validate_prompt(prompt)\n        constraints=controls.normalize(execution_constraints)\n        constraints_json=controls.encode(constraints)\n        routing_prompt'),
 ('        stamp, task_id = now(), str(uuid.uuid4())', '''        retired=BASE/'state/session_requests'/f'{request_id}.json'
        if retired.is_file() and json.loads(retired.read_bytes()).get('status')=='superseded_before_submission':
            raise ValueError('Pedido retirado antes da submissão; execução proibida.')
        if constraints:
            preview=self.preview(prompt,constraints)
            if not preview['selected']:
                raise ValueError('Executor obrigatório indisponível ou inelegível; sem substituição.')
        stamp, task_id = now(), str(uuid.uuid4())'''),
 ('SELECT id,prompt,routing_prompt FROM tasks WHERE request_id=?','SELECT id,prompt,routing_prompt,execution_constraints FROM tasks WHERE request_id=?'),
 ('if existing["prompt"] != prompt or (existing["routing_prompt"] or existing["prompt"]) != routing_prompt:',
  'if existing["prompt"] != prompt or (existing["routing_prompt"] or existing["prompt"]) != routing_prompt or (existing["execution_constraints"] or "null") != constraints_json:'),
 ('INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,routing_prompt) VALUES(?,?,?,?,?,\'queued\',?)',
  'INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,routing_prompt,execution_constraints) VALUES(?,?,?,?,?,\'queued\',?,?)'),
 ('(task_id, request_id, prompt, stamp, stamp, routing_prompt))','(task_id, request_id, prompt, stamp, stamp, routing_prompt, constraints_json))'),
 ('for key in ("decision", "result"):\n            result[key]', 'for key in ("decision", "result", "execution_constraints"):\n            result[key]'),
 ('            classification, jev_status = jev.classify_with_jev(routing_prompt or prompt)\n            packet = canonical_memory.prepare(prompt)', '''            c=controls.normalize(self.task(task_id)['execution_constraints'])
            if c:
                classification,jev_status=classify(routing_prompt or prompt),{'status':'not_called_for_controlled_request'}
            else:
                classification, jev_status = jev.classify_with_jev(routing_prompt or prompt)
            packet = canonical_memory.prepare(prompt,allowed_sources=c.get('allowed_sources') if c else None)
            controls.enforce_packet(packet,c,providers.SYSTEM)
            quote=controls.quote(c)'''),
 ('            decision = route(prompt, self.connections(), self.counts(), classification=classification)',
  '            decision = route(prompt, controls.restrict(self.connections(),c), self.counts(), classification=classification)'),
 ('            decision["canonical_memory"] = packet["receipt"]',
  '            decision["execution_constraints"]=c\n            decision["cost_reservation"]=quote\n            decision["canonical_memory"] = packet["receipt"]'),
 ('                cursor = db.execute("INSERT INTO attempts',
  '                db.execute("BEGIN IMMEDIATE")\n                controls.reserve(db,task_id,c,quote,now())\n                cursor = db.execute("INSERT INTO attempts'),
 ('cancel=cancel, memory_packet=packet,','cancel=cancel, memory_packet=packet, execution_constraints=c,'),
 ('            with self.db() as db:\n                db.execute("UPDATE attempts SET finished_at=?,status=\'returned\',usage=? WHERE id=?",',
  '            with self.db() as db:\n                controls.settle(db,task_id,c,result)\n                db.execute("UPDATE attempts SET finished_at=?,status=\'returned\',usage=? WHERE id=?",')])

edit('iald_orchestrator/providers.py',[
 ('process_callback=None, memory_packet=None):','process_callback=None, memory_packet=None, execution_constraints=None):'),
 ('    prompt = validate_prompt(packet[\'prompt\'])', '''    from . import request_controls as controls
    constraints=controls.normalize(execution_constraints)
    if constraints and name != constraints['required_provider']:
        raise ValueError('Executor diverge da restrição; chamada bloqueada.')
    controls.enforce_packet(packet,constraints,SYSTEM)
    if constraints: controls.quote(constraints)
    prompt = validate_prompt(packet['prompt'])'''),
 ('result = mimo.execute(SYSTEM + "\\n\\nTAREFA:\\n" + prompt, cancel=cancel)',
  'result = mimo.execute(SYSTEM + "\\n\\nTAREFA:\\n" + prompt, cancel=cancel, max_output=constraints["max_output_tokens"] if constraints else mimo.MAX_OUTPUT)')])

edit('iald_orchestrator/coordination.py',[
 ('from .policy import validate_prompt, FORBIDDEN','from .policy import validate_prompt, FORBIDDEN\nfrom . import request_controls as controls'),
 ('    def create(self,prompt,request_id):', '''            if 'execution_constraints' not in {r[1] for r in db.execute('PRAGMA table_info(coordination_jobs)')}:
                db.execute('ALTER TABLE coordination_jobs ADD COLUMN execution_constraints TEXT')

    def create(self,prompt,request_id,execution_constraints=None):'''),
 ('        prompt=validate_prompt(prompt)', '        prompt=validate_prompt(prompt)\n        c=controls.normalize(execution_constraints); serialized=controls.encode(c)'),
 ("        with self.runtime.db() as db:\n            db.execute('BEGIN IMMEDIATE')\n            existing=", '''        if c:
            preview=self.runtime.preview(prompt,c)
            if not preview['selected']: raise ValueError('Executor obrigatório inelegível; nenhum Work criado.')
        retired=BASE/'state/session_requests'/f'{request_id}.json'
        if retired.is_file() and json.loads(retired.read_bytes()).get('status')=='superseded_before_submission':
            raise ValueError('Pedido retirado; não submeter.')
        with self.runtime.db() as db:
            db.execute('BEGIN IMMEDIATE')
            existing='''),
 ('SELECT id,prompt FROM coordination_jobs WHERE request_id=?','SELECT id,prompt,execution_constraints FROM coordination_jobs WHERE request_id=?'),
 ("if existing['prompt']!=prompt:", "if existing['prompt']!=prompt or (existing['execution_constraints'] or 'null')!=serialized:"),
 ('INSERT INTO coordination_jobs(id,request_id,prompt,created_at,updated_at,stage) VALUES(?,?,?,?,?,?)',
  'INSERT INTO coordination_jobs(id,request_id,prompt,created_at,updated_at,stage,execution_constraints) VALUES(?,?,?,?,?,?,?)'),
 ("(job_id,request_id,prompt,stamp,stamp,'awaiting_dispatch'))", "(job_id,request_id,prompt,stamp,stamp,'awaiting_dispatch',serialized))"),
 ('        value=dict(row)', "        value=dict(row)\n        value['execution_constraints']=json.loads(value['execution_constraints']) if value['execution_constraints'] else None"),
 ("            value['canonical_memory'] = prepare(value['prompt'])", "            c=value['execution_constraints']\n            value['canonical_memory'] = prepare(value['prompt'],allowed_sources=c.get('allowed_sources') if c else None)\n            from .providers import SYSTEM\n            controls.enforce_packet(value['canonical_memory'],c,SYSTEM)"),
 ("            row=db.execute('SELECT stage FROM coordination_jobs WHERE id=?'", "            row=db.execute('SELECT stage,execution_constraints FROM coordination_jobs WHERE id=?'"),
 ("            previous=row['stage'];fields.update", "            if action in ('begin_draft','begin_synthesis'):\n                controls.check_work(db,json.loads(row['execution_constraints']) if row['execution_constraints'] else None)\n            previous=row['stage'];fields.update"),
 ("        if action=='begin_draft':\n            return", "        if action=='begin_draft':\n            if job['execution_constraints'] and not self.runtime.preview(job['prompt'],job['execution_constraints'])['selected']:\n                raise ValueError('Executor obrigatório inelegível; Work não enviado.')\n            return"),
 ("routing_prompt=job['prompt'],start_worker=False)", "routing_prompt=job['prompt'],start_worker=False,execution_constraints=job['execution_constraints'])")])

edit('iald_orchestrator/transport.py',[
 ('    def submit(self, prompt, request_id):','    def submit(self, prompt, request_id, execution_constraints=None):'),
 ('return self.coordination.create(prompt, request_id)','return self.coordination.create(prompt, request_id, execution_constraints)')])
edit('transport_cli.py',[
 ("result = transport.submit(request['prompt'], request['request_id'])", "result = transport.submit(request['prompt'], request['request_id'], request.get('execution_constraints'))"),
 ("    elif operation == 'receipt':", '''    elif operation == 'preview_execution':
        result = transport.coordination.runtime.preview(request['prompt'],request.get('execution_constraints'))
    elif operation == 'submit_execution':
        runtime=transport.coordination.runtime
        task=runtime.submit(request['prompt'],request['request_id'],execution_constraints=request.get('execution_constraints'),start_worker=False)
        runtime._drain()  # Keep the official adapter alive until its bounded call ends.
        result=runtime.task(task['id'])
    elif operation == 'receipt':''')])
edit('mcp_server.py',[
 ('def iald_selection_preview(task: str) -> dict:', 'def iald_selection_preview(task: str, execution_constraints: dict | None = None) -> dict:'),
 ('return runtime.preview(task)','return runtime.preview(task, execution_constraints)'),
 ('def iald_coordination_submit(prompt: str, request_id: str) -> dict:', 'def iald_coordination_submit(prompt: str, request_id: str, execution_constraints: dict | None = None) -> dict:'),
 ('return Transport(coordination).submit(prompt, request_id)','return Transport(coordination).submit(prompt, request_id, execution_constraints)')])
edit('iald_orchestrator/web.py',[
 ('runtime.preview(body.get("prompt"))','runtime.preview(body.get("prompt"),body.get("execution_constraints"))'),
 ('runtime.submit(body.get("prompt"), body.get("request_id", ""))','runtime.submit(body.get("prompt"), body.get("request_id", ""),execution_constraints=body.get("execution_constraints"))'),
 ("coordination.create(body.get('prompt'),body.get('request_id',''))", "coordination.create(body.get('prompt'),body.get('request_id',''),body.get('execution_constraints'))")])
