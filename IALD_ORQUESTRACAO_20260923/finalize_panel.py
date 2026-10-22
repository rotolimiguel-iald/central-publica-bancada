"""Atomic UI refinement: show quota recheck after a new refusal, not just at startup."""
from datetime import datetime
import os
from pathlib import Path
import re

base=Path(__file__).resolve().parent/'iald_orchestrator'
for name in ('panel.js','panel.html'):
    path=base/name;old=path.read_bytes();text=old.decode('utf-8')
    if name=='panel.html':
        text=text.replace('<th>Tentativas hoje</th>','<th>Tentativas neste painel · dia UTC</th>')
        text=text.replace('<tbody id="accounts"></tbody></table></details>','<tbody id="accounts"></tbody></table><div id="quota-actions" class="actions spaced"></div></details>')
        assert 'id="quota-actions"' in text
    else:
        text=text.replace("const s=await api('/status');$('providers').replaceChildren();", "const s=await api('/status');renderQuotaActions(s);$('providers').replaceChildren();")
        replacement="""function renderQuotaActions(s){$('quota-actions').replaceChildren();for(const p of s.providers.filter(p=>p.status==='provider_limit_reported')){const b=text('button','Já conferi a cota de '+p.label+'; permitir próxima tentativa');b.onclick=async()=>{try{await api('/connections/'+p.id+'/allow-retry',{});await refresh();}catch(e){failure(e);}};$('quota-actions').append(b);}}
async function showCoordinator(){try{const s=await api('/status');$('coordinator-link').href=s.coordinator.project_url;$('coordinator-status').textContent='Memória padrão verificada em '+s.coordinator.memory_observation_date+'. '+(s.coordinator.transport_status==='APP_MEDIATED_SOURCE_AND_PROMPT_TEST_PASSED'?'Consulta às fontes, preparação de prompt e síntese final validadas pelo ChatGPT Work. A conexão automática deste painel com o projeto ainda está pendente.':'Conexão com o projeto em preparação.');}catch(e){failure(e);}}"""
        text,count=re.subn(r'async function showCoordinator\(\).*?(?=\r?\n)',lambda m:replacement,text,count=1)
        assert count==1 and 'renderQuotaActions(s);' in text
    new=text.encode('utf-8')
    assert new!=old and len(new)>len(old)
    backup=path.with_name(path.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.write_bytes(old);assert backup.read_bytes()==old
    temp=path.with_name(path.name+'.tmp');temp.write_bytes(new)
    assert temp.read_bytes()==new and path.read_bytes()==old
    os.replace(temp,path);assert path.read_bytes()==new
    print(f'{name}: {len(old)} -> {len(new)} bytes')
