from pathlib import Path
import datetime, hashlib, json, subprocess, sys

root=Path(__file__).resolve().parents[1]
out=root.parent/'TUNEL/DO_CHATGPT'
folder=root/'A1/probes'
stamp=datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,b):
    assert not p.exists(),p
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b
    tmp.rename(p)
def append(p,b):
    before=p.read_bytes()
    backup=p.with_name(p.name+'.bak_'+stamp.strftime('%Y%m%d_%H%M%S_%f'))
    create(backup,before)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(before+b)
    assert tmp.read_bytes()==before+b
    tmp.replace(p)

source=folder/'ProbeFieldMutations_v2.lean'
log=folder/'field_mutations_02.log'
receipt=folder/'field_mutations_02.json'
d=json.loads(receipt.read_text())
assert d['rc']==0 and not d['newer_kernel_files'] and not d['scan_errors']
assert sha(source)==d['source_sha256'] and sha(log)==d['log_sha256']
a=subprocess.run([sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),str(source),str(log)],capture_output=True)
assert a.returncode==0,a.stdout+a.stderr
create(folder/'field_mutations_axioms.json',a.stdout)
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
text=f'''[REAL] A-1.b5 — os campos smooth_on e admissible_unit excluem controles explícitos.

Abertura SHA256: {opening}

[DERIVED — Lean isolado] roughFrame preserva arrasto por boosts, determinante não nulo na cunha e coluna fiducial modular, mas seu coeficiente E22=1+|x2| não é diferenciável em x2=0. replaceFrame transforma qualquer H2 em um registro idêntico salvo smooth_on:True, usando esse quadro. Portanto, retirar smooth_on não é mera convenção. Não se afirma ter construído o H2 inicial.

[DERIVED — condicional] admitZero transforma H3 em H3WithoutUnit, substituindo admissible por insert 0 admissible. Exige explicitamente T(0,x)=0 e theta(0,x)=0, além do H3 inicial; não são extraídas gratuitamente do tipo. Todos os demais campos são preservados, inclusive não trivialidade, carga modular e Raychaudhuri. admitZero_not_unit prova que a normalização falha no novo conjunto. Logo admissible_unit tem efeito demonstrado nessa classe.

Não houve edição do contrato da gerência. Os dois registros de mutação foram extraídos de sua fonte e alteram somente o campo-alvo para True. Fonte inicial e falha permanecem. Segunda compilação rc=0; nove declarações auditadas, somente propext/Classical.choice/Quot.sound; sem sorry ou axioma novo. Avisos de tática redundante não alteram o resultado.

Fonte: {source}, SHA256 {sha(source)}
Log: {log}, SHA256 {sha(log)}
Recibo com comando completo: {receipt}, SHA256 {sha(receipt)}
Auditoria: {folder/'field_mutations_axioms.json'}, SHA256 {sha(folder/'field_mutations_axioms.json')}

Passe: {d['wall_seconds']:.6f} s parede; {d['cpu_user_seconds']+d['cpu_kernel_seconds']:.6f} s CPU; pico committed {d['peak_process_committed_bytes']} bytes. Zero arquivos canônicos posteriores ao marcador. Falha anterior preservada em field_mutations_01. B pesada: 0 h. Não move o gate nem constrói o par físico. Próximo: controle não comutante A-1.b1 e extensão A-1.c.
'''
create(out/'ENTREGA_016_A1b5_campos_com_mordida.md',text.encode())
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{stamp.isoformat()} | A-1.b5 | PAGO no escopo condicional: 9 declarações auditadas; smooth_on/admissible_unit têm efeito | passe {d["wall_seconds"]/3600:.9f} h parede; {(d["cpu_user_seconds"]+d["cpu_kernel_seconds"])/3600:.9f} h CPU; B pesada 0h; nenhuma chamada remota nova. A-1.b1/c pendentes.\n'.encode())

orchestration=f'''[REAL] Orquestração — correção ao lado após autorização de 24/09/2026.

Abertura SHA256: {opening}

[INPUT] O operador autorizou Kimi, MiMo, Claude e Gemini/Antigravity para distribuição das tarefas desta missão. Isso supera o veto anterior a Claude/Antigravity, sem remover tetos de custo, chamada ou escopo.

[REAL] O seletor não possui campo executável por pedido para impor provedor/teto; isso foi confirmado pela tarefa coordenadora 01a0ce2b-8c2f-71b0-a9a8-91b17715a569. Unidade A-1.b1 preparada para MiMo sob request_id 3529180f-e29d-4c42-94ef-f0fbba21771b, ainda SEM submit/job_id. Uma chamada, teto US$0,50. Pedi ajuste mínimo por pedido à tarefa responsável, com testes sem provedores e preservação das políticas globais. Não criei worker/heartbeat/fila novos.

MiMo: rascunho A-1.b1. Kimi: crítica posterior após resultado/falha medida. Claude: auditoria de encadeamento quando necessária. Gemini: controle alternativo se disponível. Papéis são estratégia inicial, não ranking de qualidade medido. A sessão de origem constrói e compila.

O status em novo processo ainda deu Gemini unavailable/ModuleNotFoundError; diagnóstico enviado à coordenadora. Registro: A0/orchestration_fresh_process_v2.json SHA256 {sha(root/'A0/orchestration_fresh_process_v2.json')}. Não chamei provedor remoto. Preview selecionou Claude e não executou. Retomada deve preservar UUID/prompt e conferir capacidade real antes de submeter.
'''
create(out/'ENTREGA_016_MEDIDA_orquestracao_distribuicao_20260924.md',orchestration.encode())
print(json.dumps({'audit':json.loads(a.stdout),'report_sha256':sha(out/'ENTREGA_016_A1b5_campos_com_mordida.md')}))
