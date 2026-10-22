from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,sys
root=Path(__file__).resolve().parents[1]
out=root.parent/'TUNEL/DO_CHATGPT'
folder=root/'A2'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,data):
 assert not p.exists(),p
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(data)
 assert t.read_bytes()==data
 t.rename(p)
def append(p,data):
 old=p.read_bytes()
 new(p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_%f')),old)
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(old+data)
 assert t.read_bytes()==old+data
 t.replace(p)

r=json.loads((folder/'delegation_a23_core.json').read_bytes())
assert r['job_id']
audit=subprocess.run([sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),
 str(folder/'LightRayContourTransport_v2.lean'),str(folder/'contour_transport_02.log')],capture_output=True)
assert audit.returncode==0,audit.stdout+audit.stderr
new(folder/'contour_transport_axioms.json',audit.stdout)
receipt=json.loads((folder/'contour_transport_02.json').read_bytes())
assert receipt['rc']==0 and receipt['source_sha256']==sha(folder/'LightRayContourTransport_v2.lean')
assert receipt['log_sha256']==sha(folder/'contour_transport_02.log')
assert not receipt['newer_kernel_files'] and not receipt['scan_errors']
entry={'ts':now.isoformat(),'alvo':'A-2','ramo':'A-2.3.a','provedor':'mimo',
 'modelo_informado':'mimo-v2.6-pro','request_id':r['request_id'],'job_id':r['job_id'],
 'tokens_in':0,'tokens_cache':0,'tokens_out':0,'custo_usd':0,
 'question_sha256':r['prompt_sha256'],'answer_sha256':None,'turnos_fisica_coordenacao':0,
 'desfecho':'registered_awaiting_dispatch_not_executed',
 'reason':'Official submit only; required_provider=mimo, maximum capacity; model usage pending worker. Kimi review not yet submitted.'}
ledger=out/'LEDGER_016.jsonl'
rows=[json.loads(l) for l in ledger.read_text().splitlines() if l]
assert not any(x.get('job_id')==r['job_id'] for x in rows)
append(ledger,(json.dumps(entry,ensure_ascii=False)+'\n').encode())
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
preview=json.loads((folder/'a23_mimo_preview.json').read_bytes())
mem=preview['canonical_memory']
report=f'''[REAL] Orquestração da A-2.3.a registrada e checkpoint analítico.

Abertura SHA256: {opening}

Unidade: {r['request_id']}
Job: {r['job_id']}
Estado verificado no recibo de submissão: {r['status']}. Não significa execução concluída.
Executor obrigatório: MiMo (mimo-v2.6-pro); uma unidade idempotente, sem fallback; max_completion_tokens=131072, sem teto financeiro local, por ordem posterior do operador. A prévia selecionou MiMo. Fluxo oficial Física → MiMo → Física; worker existente notificado, sem segunda fila ou transições concorrentes.

Memória: generation={mem['generation']}, {mem['context_bytes']} bytes de contexto, modo={mem.get('memory_mode')}; {mem['coverage']}, {mem['freshness']}. Não é o corpus integral nem atualidade dos originais indisponíveis nesta consulta. Submissão SHA256 {sha(folder/'a23_mimo_submit_response.json')}. A fonte do pedido e as linhas estão no recibo; confidenciais não integram a unidade.

Distribuição: MiMo desenvolve densidade e extensão ao fecho da meia-inclusão. Kimi K3 max fará a crítica em unidade posterior, após resultado e respeitando o limite Work ainda vigente. Claude/Antigravity estão disponíveis para unidades adicionais justificadas; não chamados como cópias redundantes. Esta distribuição é decisão operacional, não benchmark de superioridade. A validação Kimi da sessão mantenedora foi chamada pública curta; não confundir com revisão matemática desta missão.

Avanço local adicional: LightRayContourTransport_v2 compila com rc0, 2 teoremas no trio. rectangle_identity é Cauchy no retângulo; horizontal_integral_eq_of_vertical_limit deriva a igualdade das integrais horizontais a partir de holomorfia, integrabilidade dos bordos e LIMITES VERTICAIS explicitamente assumidos. Esses limites não foram escondidos nem provados por este arquivo. Juntam-se aos 15 ingredientes do checkpoint anterior. Densidade e isotonia do K inteiro continuam OPEN; o ramo permanece ativo.

Fonte: {folder/'LightRayContourTransport_v2.lean'} — {sha(folder/'LightRayContourTransport_v2.lean')}
Log: {folder/'contour_transport_02.log'} — {sha(folder/'contour_transport_02.log')}
Recibo: {folder/'contour_transport_02.json'} — {sha(folder/'contour_transport_02.json')}
Auditoria: {folder/'contour_transport_axioms.json'} — {sha(folder/'contour_transport_axioms.json')}

Ledger registra submissão com zero tokens/custo de executor até esse ato; consumo futuro será registrado quando o worker realmente executar. O custo de coordenação não foi medido nesse total. Não move gate. Não muda os originais nem as memórias canônicas da missão.
'''
p=out/'ENTREGA_016_MEDIDA_orquestracao_A2_3a_registrada.md'
new(p,report.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{now.isoformat()} | A-2.3.a | MiMo registrado, job {r["job_id"]}; execução pendente no worker único. Mais 2 teoremas condicionais Cauchy compilados; densidade/isotonia OPEN. Ledger registra submissão, não chamada executada; B pesada 0h.\n'.encode())
print(json.dumps({'report':str(p),'sha256':sha(p),'job_id':r['job_id']}))
