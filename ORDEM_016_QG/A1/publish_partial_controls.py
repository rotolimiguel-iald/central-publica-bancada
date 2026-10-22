"""Publish audited partial A-1 results; keep the unexecuted branches explicit."""
from pathlib import Path
import hashlib
import json
import datetime
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
out=root.parent/'TUNEL/DO_CHATGPT'
folder=root/'A1/probes'
stamp=datetime.datetime.now(datetime.timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def create(p,raw):
    assert not p.exists(),p
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and raw
    tmp.rename(p)
def append(p,raw):
    before=p.read_bytes()
    backup=p.with_name(p.name+'.bak_'+stamp.strftime('%Y%m%d_%H%M%S_%f'))
    create(backup,before)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(before+raw)
    assert tmp.read_bytes()==before+raw
    tmp.replace(p)
    assert p.read_bytes().startswith(before) and backup.read_bytes()==before

cases=[('b2_control','ProbeForgedStress_v2.lean','forged_stress_02'),
       ('b2_contract','ProbeForgedStressContract.lean','forged_contract_01'),
       ('analytic','AnalyticBoundaryControl_v2.lean','analytic_boundary_02'),
       ('b3','ProbePositiveEnergy_v2.lean','positive_energy_02'),
       ('b4','ProbeNonKMS_v3.lean','non_kms_02')]
audit_args=[]
entries=[]
for branch,name,label in cases:
    source=folder/name
    log=folder/(label+'.log')
    receipt=folder/(label+'.json')
    data=json.loads(receipt.read_text())
    assert data['rc']==0 and not data['newer_kernel_files'] and not data['scan_errors']
    assert sha(source)==data['source_sha256'] and sha(log)==data['log_sha256']
    audit_args.extend([str(source),str(log)])
    entries.append({'branch':branch,'source':str(source),'source_sha256':sha(source),
                    'log':str(log),'log_sha256':sha(log),'receipt':str(receipt),
                    'receipt_sha256':sha(receipt),'wall_seconds':data['wall_seconds'],
                    'cpu_seconds':data['cpu_user_seconds']+data['cpu_kernel_seconds']})
proc=subprocess.run([sys.executable,'-X','utf8','-B',str(root/'A0/auditar_axiomas.py'),*audit_args],capture_output=True)
assert proc.returncode==0,proc.stdout+proc.stderr
create(root/'A1/partial_controls_axioms.json',proc.stdout)
opening=sha(out/'ENTREGA_016_ABERTURA_operador.md')
manifest={'utc':stamp.isoformat(),'opening_sha256':opening,'entries':entries,
          'audit_sha256':sha(root/'A1/partial_controls_axioms.json'),
          'scope':'CONDITIONAL_THEOREMS_IN_ISOLATED_WORKSPACE; no physical inhabitant constructed',
          'remaining_A1':['b1 noncommuting toy','b5 smooth_on/admissible_unit','c local extension',
                           'exact A1.a reproduction remains unpaid after memory failures']}
create(root/'A1/partial_controls_manifest.json',(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
def attachments(branches):
    rows=[]
    for e in entries:
        if e['branch'] in branches:
            rows += [f"- Fonte: {e['source']} — SHA256 {e['source_sha256']}",
                     f"- Log: {e['log']} — SHA256 {e['log_sha256']}",
                     f"- Recibo/comando: {e['receipt']} — SHA256 {e['receipt_sha256']}"]
    return '\n'.join(rows)
def report(slug,title,body,branches):
    selected=[e for e in entries if e['branch'] in branches]
    wall=sum(e['wall_seconds'] for e in selected)
    cpu=sum(e['cpu_seconds'] for e in selected)
    text=f'''[REAL] {title}

Abertura SHA256: {opening}

{body}

Reprodução: executar o vetor de argumentos integral nos recibos, com o runner isolado A0/compile_isolated_v2.py e LEAN_PATH incluindo A1/minimal_imports. Cada resultado listado teve rc 0, #print axioms no trio permitido, sem sorry, sem axiom novo e zero arquivo canônico posterior ao marcador. Auditoria: A1/partial_controls_axioms.json, SHA256 {manifest['audit_sha256']}.

Recursos dos passes citados: {wall:.6f} s parede, {cpu:.6f} s CPU; máquina pesada B: 0 h. São tempos dos passes, não total das tentativas. Falhas anteriores preservadas nos recibos *_01. Coordenação remota: nenhuma chamada; preview local selecionou rota proibida.

{attachments(branches)}

Move / não move: NÃO MOVE H2, H3, import-H3 nem gate. Provas condicionais isoladas, ainda não incorporadas ao kernel; nenhum par físico ou índice do operador foi escolhido.
'''
    create(out/('ENTREGA_016_'+slug+'.md'),text.encode())
report('MEDIDA_A1b2_tensor_forjado','A-1.b2 — transformação condicional de um H3 em outro H3 com fonte não simétrica.',
'''[DERIVED — termo Lean compilado] Tome n=(1,1,0,0), A23=1, A32=-1, demais componentes zero, f(ψ,x)=T_nn(ψ,x). Então T̃=T+fA e F̃(S)=F(sym S). A função transportH3 recebe C:ContratoH3 W R N T e a hipótese explícita de T simétrico. Produz ContratoH3 W R N T̃, preservando o H2, G, estados admissíveis, carga modular, resposta geométrica e equação local Raychaudhuri–Einstein. A não trivialidade de C implica um estado admissível/ponto com f≠0; ali T̃ não é simétrico.

Isto é mais específico que dizer que «o tipo não menciona simetria»: a transformação habita exatamente as definições da v3.1 e não lê uma hipótese de que T̃ seja um tensor físico. A preparação minimal_imports preservou byte a byte todo o corpo original; alterou somente os imports. A reprodução byte a byte original A-1.a continua NÃO PAGA.

[OPEN] A existência do H3 inicial e de uma fonte simétrica compatível não foi construída. O resultado é uma transformação condicional, não prova de não-vacuidade do contrato. A violação demonstrada é SIMETRIA; não se infere não-localidade de operadores a partir de uma matriz de expectativas. A-1.c deve rejeitar este ataque pela simetria e declarar separadamente o que ainda não tipa sobre localidade.''',{'b2_control','b2_contract'})
report('A1b3_consumidor_energia_positiva','A-1.b3 — consumidor analítico genuíno de PositiveEnergy.',
'''[DERIVED — termo Lean compilado] Para a∈forwardCone e ‖ψ‖=1, a existência do modo U(ta)ψ=exp(−it)ψ contradiz PositiveEnergy W. O consumidor positive_energy_excludes_negative_unit_mode aplica o campo do contrato, não uma nova premissa de espectro positivo.

Prova: o teorema de três linhas da Mathlib dá unicidade da extensão limitada a cada faixa a partir da borda real. Uma extensão com borda exp(−it) coincide no semiplano superior com exp(−iz), cujo módulo cresce como exp(Im z); isso contradiz o limite uniforme exigido por PositiveEnergy.

O modo negativo, a direção no cone e a normalização são hipóteses EXPLÍCITAS do consumidor. Não foi alegada nesta rodada a construção desse autovetor na torre da gerência. O ramo paga um consumidor, alternativa admitida na ordem; não uma refutação incondicional de um brinquedo ainda não instanciado.''',{'analytic','b3'})
report('A1b4_controle_nao_KMS','A-1.b4 — fluxo identidade rejeitado por KMS em estado não tracial.',
'''[DERIVED — termo Lean compilado] identity_flow_not_kms usa o predicado KMSAt real da v3.1. Para A,B na álgebra da cunha, se ⟨A*Ω,BΩ⟩≠⟨B*Ω,AΩ⟩, o fluxo α(t)=id não satisfaz KMSAt W α 1.

A extensão KMS teria valor constante na borda inferior. Três linhas força constância no interior; continuidade passa ao fecho e à borda superior, impondo a igualdade dos dois valores, contrária à hipótese. O campo kms é portanto consumido analiticamente, separado dos outros campos que também poderiam excluir um fluxo trivial.

[OPEN] A,B com essa desigualdade são dados explícitos do controle; nenhum W físico novo foi construído. O resultado compilou com rc 0 como teorema de rejeição, não como um arquivo negativo rc 1. O sítio matemático da incompatibilidade é precisamente KMSAt.''',{'analytic','b4'})
ledger=[json.loads(l) for l in (out/'LEDGER_016.jsonl').read_text().splitlines() if l]
cost=sum(float(e.get('custo_usd') or 0) for e in ledger)
tokens=sum(sum(int(e.get(k) or 0) for k in ['tokens_in','tokens_cache','tokens_out']) for e in ledger)
append(out/'ENTREGA_016_PROGRESSO.md',f'\n{stamp.isoformat()} | A-1.b2/b3/b4 | resultados condicionais compilados e auditados; A-1.b1/b5/c pendentes | passes {sum(e["wall_seconds"] for e in entries)/3600:.9f} h parede; {sum(e["cpu_seconds"] for e in entries)/3600:.9f} h CPU (suporte compartilhado contado uma vez); B pesada 0 h. Ledger: US$ {cost}; tokens {tokens}.\n'.encode())
print(json.dumps({'reports':3,'audited_declarations':sum(e['n_declaracoes_auditadas'] for e in json.loads(proc.stdout)),
                  'manifest_sha256':sha(root/'A1/partial_controls_manifest.json'),'remaining':manifest['remaining_A1']}))
