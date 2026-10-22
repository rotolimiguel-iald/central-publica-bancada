"""Button-driven, durable ChatGPT project workflow. No timer or private ChatGPT API."""
from __future__ import annotations
import json
from pathlib import Path
import uuid
from urllib.parse import urlencode
from .runtime import BASE, Runtime, now
from .policy import validate_prompt, FORBIDDEN
from . import request_controls as controls

PROJECT='g-p-6804cf9af0cc81918b3bd8915b7579c3'
TERMINAL={'completed','failed','cancelled'}

class Coordination:
    def __init__(self,runtime=None):
        self.runtime=runtime or Runtime(recover=False)
        with self.runtime.db() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS coordination_jobs (
                id TEXT PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, prompt TEXT NOT NULL,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL, stage TEXT NOT NULL,
                thread_id TEXT, prepared_prompt TEXT, execution_task_id TEXT, final_text TEXT,
                error TEXT, version INTEGER NOT NULL DEFAULT 0)''')
            db.execute('''CREATE TABLE IF NOT EXISTS coordination_events (
                id INTEGER PRIMARY KEY, job_id TEXT NOT NULL, at TEXT NOT NULL,
                action TEXT NOT NULL, from_stage TEXT NOT NULL, to_stage TEXT NOT NULL)''')

            if 'execution_constraints' not in {r[1] for r in db.execute('PRAGMA table_info(coordination_jobs)')}:
                db.execute('ALTER TABLE coordination_jobs ADD COLUMN execution_constraints TEXT')

    def create(self,prompt,request_id,execution_constraints=None):
        prompt=validate_prompt(prompt)
        c=controls.normalize(execution_constraints); serialized=controls.encode(c)
        if not isinstance(request_id,str):raise ValueError('Identificador inválido.')
        uuid.UUID(request_id)
        if not self.runtime.source_status()['ok']:raise ValueError('Fontes não conferem.')
        with self.runtime.db() as db:
            existing=db.execute('SELECT id,prompt,execution_constraints FROM coordination_jobs WHERE request_id=?',(request_id,)).fetchone()
        if existing:
            if existing['prompt'] != prompt or (existing['execution_constraints'] or 'null') != serialized:
                raise ValueError('Identificador já usado com outro pedido/restrições.')
            return self.get(existing['id'])
        if c:
            preview=self.runtime.preview(prompt,c)
            if not preview['selected']: raise ValueError('Executor obrigatório inelegível; nenhum Work criado.')
        retired=BASE/'state/session_requests'/f'{request_id}.json'
        if retired.is_file() and json.loads(retired.read_bytes()).get('status')=='superseded_before_submission':
            raise ValueError('Pedido retirado; não submeter.')
        with self.runtime.db() as db:
            db.execute('BEGIN IMMEDIATE')
            existing=db.execute('SELECT id,prompt,execution_constraints FROM coordination_jobs WHERE request_id=?',(request_id,)).fetchone()
            if existing:
                if existing['prompt']!=prompt or (existing['execution_constraints'] or 'null')!=serialized:raise ValueError('Identificador já usado por outro pedido.')
                job_id=existing['id']
            else:
                pending=db.execute("SELECT count(*) FROM coordination_jobs WHERE stage NOT IN ('completed','failed','cancelled')").fetchone()[0]
                if pending>=5:raise ValueError('Há cinco coordenações pendentes. Conclua ou cancele uma.')
                job_id=str(uuid.uuid4());stamp=now()
                db.execute('INSERT INTO coordination_jobs(id,request_id,prompt,created_at,updated_at,stage,execution_constraints) VALUES(?,?,?,?,?,?,?)',
                    (job_id,request_id,prompt,stamp,stamp,'awaiting_dispatch',serialized))
        return self.get(job_id)

    def get(self,job_id):
        uuid.UUID(job_id)
        with self.runtime.db() as db:
            row=db.execute('SELECT * FROM coordination_jobs WHERE id=?',(job_id,)).fetchone()
        if row is None:raise ValueError('Coordenação não encontrada.')
        value=dict(row)
        value['execution_constraints']=json.loads(value['execution_constraints']) if value['execution_constraints'] else None
        from .transport import configuration
        config=configuration()
        enabled=bool(config.get('enabled'))
        value.update(project_id=PROJECT,automatic_polling=enabled,
                     transport='CODEX_APP_HEARTBEAT' if enabled else 'CODEX_APP_ON_DEMAND')
        # Only the non-secret job identifier enters the external-app URL.
        prompt=(f'Processe a coordenação IALD {job_id}. Leia {BASE / "COORDINATOR.md"} e siga o fluxo '
            'até a resposta final. Autorizo criar uma nova tarefa no ChatGPT Work do projeto Física para '
            'este pedido; se já houver tarefa vinculada, continue nela. Use o transporte configurado; não crie automações duplicadas.')
        value['codex_url']='codex://new?'+urlencode({'path':str(BASE),'prompt':prompt})
        value['dispatch_prompt']=prompt
        if value['stage'] not in TERMINAL:
            from .canonical_memory import prepare
            c=value['execution_constraints']
            value['canonical_memory'] = prepare(value['prompt'],allowed_sources=c.get('allowed_sources') if c else None)
            from .providers import SYSTEM
            controls.enforce_packet(value['canonical_memory'],c,SYSTEM)
        if value['execution_task_id']:
            value['execution']=self.runtime.task(value['execution_task_id'])
        return value

    def listing(self):
        with self.runtime.db() as db:
            return [dict(row) for row in db.execute('SELECT id,stage,created_at,updated_at,error FROM coordination_jobs ORDER BY created_at DESC LIMIT 30')]

    def _change(self,job_id,expected,new_stage,action,**fields):
        if not set(fields)<={'thread_id','prepared_prompt','execution_task_id','final_text','error'}:
            raise ValueError('Campos de transição inválidos.')
        with self.runtime.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT stage,execution_constraints FROM coordination_jobs WHERE id=?',(job_id,)).fetchone()
            if row is None or row['stage'] not in expected:
                raise ValueError('Etapa incompatível ou já realizada; leia o estado antes de agir.')
            if action in ('begin_draft','begin_synthesis'):
                controls.check_work(db,json.loads(row['execution_constraints']) if row['execution_constraints'] else None)
            previous=row['stage'];fields.update(stage=new_stage,updated_at=now())
            db.execute('UPDATE coordination_jobs SET '+','.join(k+'=?' for k in fields)+',version=version+1 WHERE id=?',(*fields.values(),job_id))
            db.execute('INSERT INTO coordination_events(job_id,at,action,from_stage,to_stage) VALUES(?,?,?,?,?)',(job_id,now(),action,previous,new_stage))
        return self.get(job_id)

    def act(self,job_id,action,payload=None):
        payload={} if payload is None else payload
        if not isinstance(payload,dict):raise ValueError('Dados devem ser um objeto.')
        job=self.get(job_id)
        if action=='begin_draft':
            if job['execution_constraints'] and not self.runtime.preview(job['prompt'],job['execution_constraints'])['selected']:
                raise ValueError('Executor obrigatório inelegível; Work não enviado.')
            return self._change(job_id,{'awaiting_dispatch'},'draft_dispatching',action)
        if action=='bind_thread':
            thread_id=payload.get('thread_id','')
            if not isinstance(thread_id,str):raise ValueError('Identificador de tarefa inválido.')
            uuid.UUID(thread_id)
            if payload.get('project_id')!=PROJECT:raise ValueError('Projeto incorreto.')
            return self._change(job_id,{'draft_dispatching'},'draft_waiting',action,thread_id=thread_id)
        if action=='accept_prompt':
            prepared=validate_prompt(payload.get('prompt'))
            # Preserve the actual user request even if a coordinator draft drops it.
            combined='PEDIDO DO OPERADOR:\n'+job['prompt']+'\n\nCONTEXTO E PROMPT PREPARADOS NO PROJETO FÍSICA:\n'+prepared
            validate_prompt(combined)
            return self._change(job_id,{'draft_waiting'},'prompt_ready',action,prepared_prompt=combined)
        if action=='execute':
            self._change(job_id,{'prompt_ready'},'execution_dispatching',action)
            task=None
            try:
                task=self.runtime.submit(job['prepared_prompt'],str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+job_id)),routing_prompt=job['prompt'],start_worker=False,execution_constraints=job['execution_constraints'])
                value=self._change(job_id,{'execution_dispatching'},'execution_waiting','execution_bound',execution_task_id=task['id'])
            except Exception:
                if task:self.runtime.cancel(task['id'])
                current=self.get(job_id)
                if current['stage']=='execution_dispatching':
                    self._change(job_id,{'execution_dispatching'},'failed','execution_failed',error='Não foi possível registrar a execução; nenhuma nova chamada foi iniciada.')
                raise
            self.runtime.start_worker()
            return value
        if action=='sync_execution':
            if job['stage']!='execution_waiting':return job
            task=job['execution']
            if task['status']=='result_ready':
                return self._change(job_id,{'execution_waiting'},'synthesis_ready',action)
            if task['status'] in ('failed','cancelled','interrupted'):
                return self._change(job_id,{'execution_waiting'},'failed',action,error=task['error'] or task['status'])
            return job
        if action=='begin_synthesis':
            return self._change(job_id,{'synthesis_ready'},'synthesis_dispatching',action)
        if action=='synthesis_sent':
            return self._change(job_id,{'synthesis_dispatching'},'synthesis_waiting',action)
        if action=='complete':
            answer=payload.get('text')
            if not isinstance(answer,str) or not answer.strip() or len(answer)>120000 or FORBIDDEN.search(answer):
                raise ValueError('Síntese inválida, excessiva ou com referência confidencial.')
            return self._change(job_id,{'synthesis_waiting'},'completed',action,final_text=answer.strip())
        if action=='fail':
            error=payload.get('error','Falha não especificada.')
            if not isinstance(error,str) or len(error)>600 or FORBIDDEN.search(error):raise ValueError('Diagnóstico inválido.')
            if job['stage'] in TERMINAL:return job
            return self._change(job_id,{job['stage']},'failed',action,error=error)
        if action=='cancel':
            if job['stage'] in TERMINAL:return job
            if job['execution_task_id']:self.runtime.cancel(job['execution_task_id'])
            return self._change(job_id,{job['stage']},'cancelled',action,error='Cancelada. Uma chamada já enviada pode terminar no provedor.')
        raise ValueError('Ação desconhecida.')
