"""Append the verified cross-session capability to affected operational memories."""
from pathlib import Path
import hashlib
import json
from iald_orchestrator.safe_files import replace_bytes, save_json, utc_now

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
MARKER = 'IALD_GLOBAL_SKILL_DISCOVERY_VERIFIED_20260924'

def main():
    validation = json.loads((BASE/'validation/global_skill_validation.json').read_bytes())
    assert len(validation['fresh_app_server_discovery'])==2
    assert all(s['scope']=='user' and s['enabled'] for s in validation['fresh_app_server_discovery'])
    assert validation['models_called']==0 and validation['new_tasks_created']==0
    receipt = json.loads((BASE/'state/transport_last_check.json').read_bytes())
    historical = json.loads((BASE/'validation/unattended_delivery.json').read_bytes())
    assert receipt['checked_at'] > historical['at']
    note = r'''

## 24/09/2026 — Orquestração global entre sessões do Codex

<!-- IALD_GLOBAL_SKILL_DISCOVERY_VERIFIED_20260924 -->

[INPUT] O operador determinou que a orquestração esteja disponível em qualquer sessão local do Codex, sem depender desta conversa de instalação.

[REAL] Instalada a habilidade de usuário `C:\Users\rotol\.agents\skills\iald-orquestrar\SKILL.md`, com descoberta implícita e chamada explícita `$iald-orquestrar`; instrução correspondente acrescentada ao AGENTS global, preservando integralmente seus bytes anteriores. Mantidos servidor MCP global, fila, adaptadores e heartbeat existentes. O guia TRANSPORTE_DESASSISTIDO.md passou a documentar clientes de outras sessões, recibos com request_id/job_id e um único worker para as transições. Não há novo agendamento nem envio automático de respostas a todas as sessões de origem; o resultado é consultável na fila e na tarefa Work vinculada.

[REAL — medição] Processo novo do app-server Codex descobriu a habilidade em scope=user, enabled=true, tanto na pasta de orquestração quanto em diretório temporário externo. Processo MCP novo enumerou as nove ferramentas; consulta CLI à fila e prévia do seletor funcionaram fora de BASE. Validador de skill passou. Nenhuma tarefa/modelo foi criado/chamado nessa validação. Evidência: Chatgpt/IALD_ORQUESTRACAO_20260923/validation/global_skill_validation.json. O AGENTS atualizado também foi reinjetado nesta sessão pelo aplicativo.

[REAL — correção temporal ao lado] O registro de instalação dizia que o primeiro disparo do agendador ainda não havia sido observado. Depois da instalação, esta tarefa recebeu heartbeats sucessivos e consultas vazias foram registradas em state/transport_last_check.json. O recibo observado nesta entrega está anexado ao relatório global; isto comprova consulta agendada, não uma nova execução fim a fim. O relatório histórico da instalação é preservado.

[OPEN — escopo] A capacidade depende deste host/contas; não concede acesso automático a uma sessão em nuvem. Jev/Antigravity, limites de contexto, integração de e-mails/agenda e avaliação de qualidade conservam suas pendências anteriores. Não houve mudança no kernel, um.py, gate ou acervos jurídicos. Web/iOS interno/iOS externo/Android: nenhum código de cliente ou binário afetado por esta instalação de habilidade local. Todas as memórias alteradas têm backup imediato de bytes.
'''
    claude = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
    targets = [ROOT/'memory'/n for n in ('TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md')]
    targets += [claude/n for n in ('central-de-patentes-estado.md','MEMORY_2.md','atlas-lar-miguel.md')]
    targets += [Path(r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md'), Path(r'C:\LAR_MIGUEL\ATLAS.md'), BASE/'README.md']
    entries = [(p,note) for p in targets]
    entries.append((claude/'MEMORY.md', '\n\n<!-- '+MARKER+' -->\n- [Orquestração global 24/09](MEMORY_2.md): habilidade iald-orquestrar instalada em .agents/skills, descoberta por processo Codex novo em duas pastas. Mesma fila/heartbeat, sem duplicação; recibos de origem e fallback CLI.\n'))
    records=[]
    for path,text in entries:
        old=path.read_bytes()
        backup=None
        if MARKER.encode() not in old:
            prior=set(path.parent.glob(path.name+'.bak_*'))
            newline='\r\n' if b'\r\n' in old else '\n'
            replace_bytes(path, old+text.replace('\n',newline).encode('utf-8'))
            new_backups=set(path.parent.glob(path.name+'.bak_*'))-prior
            assert len(new_backups)==1
            backup=new_backups.pop()
            assert backup.read_bytes()==old
        data=path.read_bytes()
        assert data.startswith(old) and MARKER.encode() in data
        records.append({'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),
                        'backup':str(backup) if backup else None})
    config=json.loads((BASE/'coordinator.json').read_bytes())
    config.update(scheduler_trigger_observed=True, scheduler_observation_receipt=receipt,
                  global_skill='iald-orquestrar', global_skill_validation='validation/global_skill_validation.json')
    save_json(BASE/'coordinator.json',config)
    save_json(BASE/'validation/global_skill_delivery.json',{
        'at':utc_now(), 'validation_record':'validation/global_skill_validation.json',
        'scheduler_observation_receipt':receipt, 'surfaces':records,
        'global_instructions':str(Path(r'C:\Users\rotol\.codex\AGENTS.md'))})
    print(json.dumps({'memory_surfaces_verified':len(records), 'skill_discovered_in_fresh_process':True,
                     'new_automations':0},ensure_ascii=False))

if __name__=='__main__':
    main()
