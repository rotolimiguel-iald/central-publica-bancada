from pathlib import Path
from datetime import datetime
import json, os
BASE=Path(__file__).resolve().parent
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def save(relative, text):
    path=BASE/relative; original=path.read_bytes() if path.exists() else None
    data=text.encode('utf-8')
    if original==data:return
    if original is not None:
        backup=path.with_name(path.name+'.bak_'+STAMP);backup.write_bytes(original)
        assert backup.read_bytes()==original
    temp=path.with_name(path.name+'.tmp_'+STAMP);temp.write_bytes(data)
    assert temp.stat().st_size==len(data)>0
    if original is not None:assert path.read_bytes()==original
    os.replace(temp,path);assert path.read_bytes()==data

p=BASE/'iald_orchestrator/panel.html'
s=p.read_text(encoding='utf-8')
s=s.replace('<button id="run" class="primary">','<button id="coordinate" class="primary">Preparar pedido com Física</button><button id="run">')
s=s.replace('Execução direta dos conectores: ainda não passa pelo projeto Física. Nesta entrega: respostas e artefatos textuais.', 'Com Física: salve o pedido, abra o Codex pelo link e envie a mensagem preparada. A coordenação segue até a síntese no projeto. Sem verificações periódicas. Execução direta pula essa preparação. Nesta entrega: respostas e artefatos textuais.')
s=s.replace('<div id="error"', '<div id="dispatch" class="notice" hidden><a id="dispatch-link">Abrir Codex e enviar pedido</a><p class="muted">O botão abre uma mensagem preenchida. Clique em Enviar no Codex para iniciar.</p><button id="copy-dispatch">Copiar instrução</button></div>\n<div id="error"')
s=s.replace('<h2>Trabalho registrado</h2>','<h2>Coordenações com Física</h2><div id="coordinations"></div><h2 class="spaced">Execuções registradas</h2>')
save('iald_orchestrator/panel.html',s)

p=BASE/'iald_orchestrator/panel.js';s=p.read_text(encoding='utf-8')
s=s.replace("let active = null,", "const stages={awaiting_dispatch:'Pronto para enviar no Codex',draft_dispatching:'Abrindo tarefa no projeto',draft_waiting:'Física prepara o prompt',prompt_ready:'Prompt preparado',execution_dispatching:'Encaminhando execução',execution_waiting:'Executor em andamento',synthesis_ready:'Resultado pronto para síntese',synthesis_dispatching:'Encaminhando síntese',synthesis_waiting:'Física compõe a resposta',completed:'Concluída',failed:'Falha visível',cancelled:'Cancelada'};\nlet activeCoordination=null, coordinationRequestId=null, coordinationPrompt=null, dispatchPrompt='';\nlet active = null,")
s=s.replace("renderQuotaActions(s);", "renderQuotaActions(s);renderCoordinations(s);",1)
s=s.replace("$('run').disabled=!s.sources.ok;", "$('run').disabled=!s.sources.ok;$('coordinate').disabled=!s.sources.ok;")
s=s.replace("async function loadJob(id){try{", "async function loadJob(id){try{activeCoordination=null;$('dispatch').hidden=true;")
start=s.index('async function showCoordinator()')
end=s.index("$('preview').onclick",start)
s=s[:start]+'''async function showCoordinator(){try{const s=await api('/status');$('coordinator-link').href=s.coordinator.project_url;$('coordinator-status').textContent='Física prepara o prompt e recebe o resultado para compor a resposta final. Cada novo pedido usa sua própria tarefa no projeto. Acionamento pelo botão, com envio no Codex; nenhuma verificação periódica.';}catch(e){failure(e);}}
function renderCoordinations(s){$('coordinations').replaceChildren();for(const job of s.coordination_jobs||[]){const b=text('button',stages[job.stage]||job.stage,'job');b.append(text('small',new Date(job.created_at).toLocaleString('pt-BR')));b.onclick=()=>loadCoordination(job.id);$('coordinations').append(b);}if(!s.coordination_jobs?.length)$('coordinations').append(text('p','Nenhum pedido com Física ainda.'));}
async function loadCoordination(id){try{clearTimeout(timer);const job=await api('/coordination/'+id);activeCoordination=id;active=null;dispatchPrompt=job.dispatch_prompt;$('dispatch-link').href=job.codex_url;$('dispatch').hidden=['completed','failed','cancelled'].includes(job.stage);$('job-status').textContent=stages[job.stage]||job.stage;$('answer').textContent=job.final_text||job.error||job.execution?.result?.text||'';$('usage').textContent=job.execution?.result?'Consumo do executor: '+JSON.stringify(job.execution.result.usage||'indisponível')+' · chamadas ao ChatGPT Work/Codex coordenador têm consumo separado.':'';$('selection').replaceChildren();$('matrix').textContent='';showDecision(job.execution?.decision);$('cancel').hidden=['completed','failed','cancelled'].includes(job.stage);await refresh();}catch(e){failure(e);}}
$('coordinate').onclick=async()=>{try{$('error').textContent='';$('coordinate').disabled=true;const prompt=$('prompt').value;if(prompt!==coordinationPrompt){coordinationRequestId=crypto.randomUUID();coordinationPrompt=prompt;}const job=await api('/coordination',{prompt,request_id:coordinationRequestId});await loadCoordination(job.id);}catch(e){failure(e);}finally{$('coordinate').disabled=false;}};
$('copy-dispatch').onclick=async()=>{try{await navigator.clipboard.writeText(dispatchPrompt);$('error').textContent='Instrução copiada. Cole e envie no Codex.';}catch(e){failure(e);}};
'''+s[end:]
s=s.replace("if(active){await api('/tasks/'", "if(activeCoordination){await api('/coordination/'+activeCoordination+'/cancel',{});await loadCoordination(activeCoordination);}else if(active){await api('/tasks/'")
s=s.replace("$('refresh').onclick=refresh;", "$('refresh').onclick=()=>activeCoordination?loadCoordination(activeCoordination):active?loadJob(active):refresh();")
save('iald_orchestrator/panel.js',s)

p=BASE/'iald_orchestrator/runtime.py';s=p.read_text(encoding='utf-8')
s=s.replace('*, routing_prompt=None):','*, routing_prompt=None, start_worker=True):')
s=s.replace('        threading.Thread(target=self._drain, daemon=True, name="iald-orchestrator").start()\n        return self.task(task_id)', '        if start_worker:self.start_worker()\n        return self.task(task_id)\n\n    def start_worker(self):\n        threading.Thread(target=self._drain, daemon=True, name="iald-orchestrator").start()')
save('iald_orchestrator/runtime.py',s)
p=BASE/'iald_orchestrator/coordination.py';s=p.read_text(encoding='utf-8')
start=s.index("        if action=='execute':");end=s.index("        if action=='sync_execution':",start)
s=s[:start]+'''        if action=='execute':
            self._change(job_id,{'prompt_ready'},'execution_dispatching',action)
            task=None
            try:
                task=self.runtime.submit(job['prepared_prompt'],str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+job_id)),routing_prompt=job['prompt'],start_worker=False)
                value=self._change(job_id,{'execution_dispatching'},'execution_waiting','execution_bound',execution_task_id=task['id'])
            except Exception:
                if task:self.runtime.cancel(task['id'])
                current=self.get(job_id)
                if current['stage']=='execution_dispatching':
                    self._change(job_id,{'execution_dispatching'},'failed','execution_failed',error='Não foi possível registrar a execução; nenhuma nova chamada foi iniciada.')
                raise
            self.runtime.start_worker()
            return value
'''+s[end:]
save('iald_orchestrator/coordination.py',s)
p=BASE/'coordinator.json';data=json.loads(p.read_text(encoding='utf-8'))
data.update(transport_status='CODEX_APP_ON_DEMAND',automatic_polling=False,trigger='ADMIN_BUTTON_THEN_CODEX_SEND',transport_scope='Botão registra pedido e abre rascunho no Codex; após Enviar, ferramentas do app coordenam prompt, executor e síntese. Sem API privada ou agendamento.',workflow_guide='COORDINATOR.md')
save('coordinator.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('Button UI and durable transitions updated with byte backups.')
