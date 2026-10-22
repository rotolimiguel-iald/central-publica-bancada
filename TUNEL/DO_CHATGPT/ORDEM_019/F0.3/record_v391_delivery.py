"""Record the verified cutover and the unresolved legacy client reload."""
from pathlib import Path
import json,subprocess,sys
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923');W=Path(__file__).resolve().parent
sys.dont_write_bytecode=True;sys.path.insert(0,str(B))
from iald_orchestrator.safe_files import save_json,replace_bytes,utc_now
from iald_orchestrator.program_controls import require_claim,record_route
from iald_orchestrator import canonical_memory as cm
require_claim('F0.3','codex-coordenadora')
assert not (W/'MEMORY_DELIVERY.json').exists(), 'Recover completed stages; never duplicate memory appends'
p=json.loads((W/'PREPARATION_V391.json').read_bytes())
fresh=json.loads((W/'FRESH_PROCESS_VERIFICATION.json').read_bytes())
mcp=json.loads((W/'MCP_FRESH_PROCESS.json').read_bytes())
assert fresh['status']==mcp['status']=='PASS'
assert cm.status()['generation']==p['generation']
legacy=json.loads((W/'MCP_LEGACY_OBSERVATION.json').read_bytes())
seal=next(x for x in p['sources'] if Path(x['path']).name=='um_absoluto_selo.json')
program=next(x for x in p['sources'] if Path(x['path']).name=='um.py')
note=f"""
## 07/10/2026 — F0.3: memória comum v391 ativa, recarga MCP legada ainda aberta

[REAL operacional] Por aviso expresso de selagem da gerência c1, a geração {p['generation']} (epoch {p['epoch']}) foi construída dos 13 originais admitidos, fixada em cópias imutáveis e ativada com backup atômico. {p['chunks']} trechos; hashes, SQLite, todos os trechos/linhas e recuperação em três modos conferidos em processo novo. Selo v391 {seal['sha256']}, programa {program['sha256']}, lidos do disco. MCP novo também confere. O leitor atual resolve ACTIVE por consulta; v389 permanece por versão.

[REAL documental / INPUT do operador] O contexto indexa estatuto_da_prova_v391: PROVADA = validade/fecho lógico; CONFIRMADA = creditação; kernel, ritos e GPU com os estatutos da fonte; GPU COMPUTED; NOT_FALSIFIED nunca é confirmação; gate preservado. Não houve novo rito/compilação nem reclassificação de resultado empírico nesta atualização.

[REAL operacional] Jev: referência atual JEV_CONTEXT_REFERENCE_V391.json aponta a nova geração verificada localmente; sondas/calibração remotas históricas permanecem v368/v389. Zero novas chamadas. F9.9.A01 não respondida; sombra desligada.

[OPEN operacional] O MCP legado conectado retornou geração {legacy['canonical_memory']['generation']} sem ACTIVE_POINTER_PER_REQUEST. Reinício pelo cliente pendente; teste de servidor novo não prova recarga dos antigos. Até confirmar, usar CLI absoluto em processo novo; não alterar restrições memory_generation para forçar execução. F0.3 permanece EM_CURSO e não recebe declaração integral de ENTREGUE.
Evidência: {W/'RESULTADO.json'}; relato {W/'ENTREGA_MEMORIA_V391.md'}. Nenhum original científico, kernel, gate, configuração de permissão ou cliente público/mobile modificado.
"""
md="# F0.3 — memória v391 ativada; recarga dos clientes antigos pendente\n"+note+"""
Reaproveitamento: Nós vivo consultado antes de produzir; builder e verificador existentes; mecanismo ACTIVE da F9.2 e pacote do Nós vivo da F9.9. Todas as linhas e trechos do índice foram comparados às cópias exatas. Uma instância do leitor atual importada antes da troca reconheceu a geração nova sem reiniciar.

Ação concreta restante: no Codex, Configurações → Servidores MCP → iald-orchestrator → Restart; reconectar o mesmo MCP nas sessões Claude Code antigas. Depois consultar iald_orchestration_status e exigir a geração desta entrega com resolution=ACTIVE_POINTER_PER_REQUEST. Não há ferramenta de reinício desses clientes nesta sessão. A documentação oficial descreve Restart: https://learn.chatgpt.com/docs/extend/mcp?surface=cli . Não se infere que reiniciar um cliente recarrega os demais.

Não foram mortos processos ou injetado código em sessões. A verificação da entrada MCP nova teve apenas chamada de status e encerrou o servidor de teste. A referência do Jev certifica fontes locais, não nova inferência remota sobre v391.

Correção do teste preservada: a primeira comparação de trechos usou read_text e normalizou CRLF; corrigida para decodificar bytes. As fontes e o retrato não mudaram.
"""
replace_bytes(W/'ENTREGA_MEMORIA_V391.md',md.encode())
summary={'unit':'F0.3','status':'V391_ACTIVE_VERIFIED_LEGACY_CLIENT_RELOAD_PENDING','at':utc_now(),
 'release':'v391','generation':p['generation'],'epoch':p['epoch'],'documents':p['documents'],'chunks':p['chunks'],
 'seal':seal,'program':program,'fresh_process_verification':str(W/'FRESH_PROCESS_VERIFICATION.json'),
 'mcp_fresh_process':str(W/'MCP_FRESH_PROCESS.json'),'activation_receipt':str(W/'ACTIVATION_RECEIPT.json'),
 'jev_current_reference':str(W/'JEV_CONTEXT_REFERENCE_V391.json'),'legacy_observation':legacy,
 'completed':['immutable_versioned_generation','all_source_and_index_hashes','all_chunks_and_line_ranges','fresh_process_read',
 'fresh_process_mcp','modern_resident_pointer_refresh','jev_context_reference_step_6','old_v389_preserved'],
 'remaining':['Legacy Codex/Claude MCP clients need client-managed restart and generation confirmation'],
 'provider_calls':0,'science_execution':False,'originals_modified':False,'gate_modified':False,'shadow_enabled':False,
 'board_status':'EM_CURSO','not_delivered_reason':'ORDEM 019 also requires legacy MCP processes reloaded or reading current generation by version.'}
save_json(W/'RESULTADO.json',summary)
previous=json.loads((W.parent/'F9.9/MEMORY_DELIVERY.json').read_bytes());records=[]
for item in previous['surfaces']:
 path=Path(item['path']);old=path.read_bytes()
 content=(f"\n- F0.3 v391 ativa; MCP legado pendente — ver MEMORY_2.md e {W/'RESULTADO.json'}.\n" if path.name=='MEMORY.md' else note).encode()
 new=old+content
 if path.name=='MEMORY.md':assert len(new)<=24576,'Keep index under 24 KiB'
 replace_bytes(path,new);assert path.read_bytes().startswith(old)
 records.append({'path':str(path),'before_sha256':cm.digest(old),'sha256':cm.digest(new),'bytes':len(new),'append_only':True})
save_json(W/'MEMORY_DELIVERY.json',{'at':utc_now(),'surfaces':records,'backup':'immediate byte copies; atomic replace; old prefix preserved'})
route={'tipo':'ROTA','rota_id':'iald.ordem019.f0_3.memoria_v391','dominio':'IALD_OPERACIONAL','titulo':'F0.3 — memória v391 por versão, Jev atualizado, recarga MCP legada pendente',
 'status':'EXAMINADA','estatuto':'REAL','olhou_dados':False,'pergunta':'A memória comum e a referência do Jev leem o selo v391 sem perder a proveniência anterior?',
 'metodo':'13 cópias de bytes; builder existente; todos os trechos/linhas e hashes; novo processo CLI e MCP; troca atômica de ACTIVE.',
 'resultado':f"Geração {p['generation']}; {p['chunks']} trechos; leitura nova aprovada; instância MCP legada ainda antiga.",
 'veredito':summary['status'],'defeito':'Recarga das instâncias MCP legadas não comprovada.',
 'nao_refazer':'Não reconstruir geração validada, nem repetir sondas remotas F9.9. Reutilizar recibos.',
 'proximo_passo':'Reiniciar clientes MCP legados pelo ciclo de vida oficial e confirmar geração; então F0.3 ENTREGUE.',
 'artefatos':[str(W/'RESULTADO.json'),str(W/'FRESH_PROCESS_VERIFICATION.json'),str(W/'MCP_FRESH_PROCESS.json')],
 'onde':str(B),'nota':'Registro local; nenhuma chamada de provedor, nenhuma alteração de gate.'}
save_json(W/'ROTA.json',route)
res=record_route(W/'ROTA.json',unit='F0.3',member='codex-coordenadora')
replace_bytes(W/'MAPA_RECIBO.json',res.encode())
event=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','anotar','--quem','codex-coordenadora','--tipo','memoria_v391_verificada_recarga_mcp_pendente','--unidade','F0.3','--dados',json.dumps(summary,ensure_ascii=False)],capture_output=True,encoding='utf-8',check=True)
replace_bytes(W/'QUADRO_EVENTO.json',event.stdout.encode())
evidence=[]
for x in sorted(W.iterdir()):
 if x.is_file() and '.bak_' not in x.name and '.tmp_' not in x.name and x.name!='MANIFESTO_EVIDENCIAS.json':
  raw=x.read_bytes();evidence.append({'path':str(x),'bytes':len(raw),'sha256':cm.digest(raw)})
save_json(W/'MANIFESTO_EVIDENCIAS.json',{'at':utc_now(),'unit':'F0.3','status':summary['status'],'files':evidence,'provider_calls':0})
print(json.dumps({'status':summary['status'],'generation':p['generation'],'memory_surfaces':len(records),'evidence_files':len(evidence),'board_event':event.stdout.strip(),'map_receipt':res.strip()},ensure_ascii=False))

