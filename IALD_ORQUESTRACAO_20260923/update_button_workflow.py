"""Atomic attachment of the project workflow to existing local surfaces."""
from pathlib import Path
from datetime import datetime
import os

base=Path(__file__).resolve().parent

def change(relative,transform):
    path=base/relative;old=path.read_bytes();text=old.decode('utf-8')
    new=transform(text).encode('utf-8')
    assert new!=old, f'Nenhuma mudança em {relative}'
    backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(old);assert backup.read_bytes()==old
    temp=path.with_name(path.name+'.button.tmp');temp.write_bytes(new)
    assert temp.read_bytes()==new and len(new)>0 and path.read_bytes()==old
    os.replace(temp,path);assert path.read_bytes()==new
    print(relative)

def runtime(text):
    text=text.replace('from .policy import route, validate_prompt','from .policy import route, validate_prompt, classify\nfrom .process_lock import process_lock')
    text=text.replace('            if recover:\n', "            if 'routing_prompt' not in {r[1] for r in db.execute('PRAGMA table_info(tasks)')}:\n                db.execute('ALTER TABLE tasks ADD COLUMN routing_prompt TEXT')\n            if recover:\n")
    old='''                db.execute("UPDATE tasks SET status='interrupted', error='Servidor reiniciado; revise antes de reenviar.', updated_at=? WHERE status IN ('running','queued')", (now(),))'''
    text=text.replace(old,'''                with process_lock(self.db_path, blocking=False) as idle:
                    if idle:
                        db.execute("UPDATE tasks SET status='interrupted', error='Servidor reiniciado; revise antes de reenviar.', updated_at=? WHERE status IN ('running','queued')", (now(),))''')
    text=text.replace('def submit(self, prompt, request_id):','def submit(self, prompt, request_id, *, routing_prompt=None):')
    text=text.replace('        prompt = validate_prompt(prompt)\n','        prompt = validate_prompt(prompt)\n        routing_prompt = validate_prompt(routing_prompt) if routing_prompt is not None else prompt\n',1)
    text=text.replace('SELECT id,prompt FROM tasks WHERE request_id=?','SELECT id,prompt,routing_prompt FROM tasks WHERE request_id=?')
    text=text.replace('if existing["prompt"] != prompt:', 'if existing["prompt"] != prompt or (existing["routing_prompt"] or existing["prompt"]) != routing_prompt:')
    text=text.replace("INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status) VALUES(?,?,?,?,?,'queued')", "INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,routing_prompt) VALUES(?,?,?,?,?,'queued',?)")
    text=text.replace('(task_id, request_id, prompt, stamp, stamp))','(task_id, request_id, prompt, stamp, stamp, routing_prompt))')
    text=text.replace('with self.worker_lock:', 'with self.worker_lock, process_lock(self.db_path):')
    text=text.replace('SELECT id,prompt FROM tasks WHERE status=', 'SELECT id,prompt,routing_prompt FROM tasks WHERE status=')
    text=text.replace('self._perform(row["id"], row["prompt"])','self._perform(row["id"], row["prompt"], row["routing_prompt"] or row["prompt"])')
    text=text.replace('def _perform(self, task_id, prompt):','def _perform(self, task_id, prompt, routing_prompt=None):')
    text=text.replace('classification, jev_status = jev.classify_with_jev(prompt)','classification, jev_status = jev.classify_with_jev(routing_prompt or prompt)\n            classification["estimated_input_tokens"] = classify(prompt)["estimated_input_tokens"]')
    compile(text,'runtime.py','exec');return text

def web(text):
    text=text.replace('from .runtime import Runtime','from .runtime import Runtime\nfrom .coordination import Coordination')
    text=text.replace('    runtime = Runtime()','    runtime = Runtime()\n    coordination = Coordination(runtime)')
    text=text.replace('return jsonify(runtime.status())','return jsonify({**runtime.status(), "coordination_jobs": coordination.listing()})')
    extra='''    @bp.post(root + "/coordination")
    def create_coordination():
        body = request.get_json()
        return jsonify(coordination.create(body.get("prompt"), body.get("request_id", ""))), 201

    @bp.get(root + "/coordination/<job_id>")
    def get_coordination(job_id):
        return jsonify(coordination.get(job_id))

    @bp.post(root + "/coordination/<job_id>/cancel")
    def cancel_coordination(job_id):
        return jsonify(coordination.act(job_id, "cancel"))

'''
    text=text.replace('    app.register_blueprint(bp)',extra+'    app.register_blueprint(bp)')
    compile(text,'web.py','exec');return text

def mcp(text):
    text=text.replace('from iald_orchestrator.runtime import Runtime','from iald_orchestrator.runtime import Runtime\nfrom iald_orchestrator.coordination import Coordination')
    text=text.replace('runtime = Runtime(recover=False)','runtime = Runtime(recover=False)\ncoordination = Coordination(runtime)')
    extra='''@server.tool()
def iald_coordination_get(job_id: str) -> dict:
    """Lê um pedido criado pelo botão da IALD; não cria tarefa nem chama modelo."""
    return coordination.get(job_id)


@server.tool()
def iald_coordination_action(job_id: str, action: str, payload: dict | None = None) -> dict:
    """Avança somente o pedido autorizado do painel. execute pode consumir a conexão selecionada.

    Ações: begin_draft, bind_thread, accept_prompt, execute, sync_execution,
    begin_synthesis, synthesis_sent, complete, fail, cancel. Leia COORDINATOR.md.
    Não cria novas tarefas ChatGPT; essa etapa usa as ferramentas oficiais do aplicativo.
    """
    return coordination.act(job_id, action, payload)


'''
    text=text.replace('if __name__ == "__main__":',extra+'if __name__ == "__main__":')
    compile(text,'mcp_server.py','exec');return text

change('iald_orchestrator/runtime.py',runtime)
change('iald_orchestrator/web.py',web)
change('mcp_server.py',mcp)
change('iald_orchestrator/coordination.py',lambda t:t.replace("self.runtime.submit(job['prepared_prompt'],str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+job_id)))","self.runtime.submit(job['prepared_prompt'],str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+job_id)),routing_prompt=job['prompt'])"))
change('bridge.py',lambda t:t.replace('import sys','import sys\nimport time').replace("    print(json.dumps(result,ensure_ascii=False))", "    if operation=='act' and request.get('action')=='execute':\n        while coordinator.runtime.worker_lock.locked() or coordinator.get(request['job_id'])['execution']['status'] in ('queued','running'):\n            time.sleep(.2)\n        result=coordinator.act(request['job_id'],'sync_execution')\n    print(json.dumps(result,ensure_ascii=False))"))
change('test_orchestrator.py',lambda t:t.replace('INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?)','INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,decision,result,error) VALUES(?,?,?,?,?,?,?,?,?)'))
