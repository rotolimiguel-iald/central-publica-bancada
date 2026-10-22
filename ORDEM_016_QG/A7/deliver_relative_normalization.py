"""Connect measured signs without repeating the loop computation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
HERE=Path(__file__).resolve().parent;OUT=HERE.parents[1]/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,b):
    if isinstance(b,str):b=b.encode()
    if p.exists():
        old=p.read_bytes()
        if old==b:return
        bk=p.with_name(p.name+'.bak_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
        bk.write_bytes(old);assert bk.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
now=datetime.now(timezone.utc).isoformat();opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
folder=HERE/'finite_relative_normalization_v2';r=json.loads((folder/'results.json').read_bytes())
report=f'''[DERIVED — ligação de sinais existentes; REAL — composição CAS; OPEN — continuação causal curva]
# A7.b — normalização relativa formal já disponível na bancada
Abertura SHA256 `{opening}`. UTC {now}.

O sinal não precisava de nova bolha: marked_vertex_independent já verificou
mixed_bubble_Wick_sign e effective_bubble_after_Q_inverse_minus. Seu script
foi re-hasheado contra o recibo antes do reaproveitamento; não foi reexecutado.
Na ordenação da fonte T U h eta e do vértice bareta V h c, externalizar T,c
e contrair os ghosts dá +1. A expansão conectada de Gamma=-hbar log Z dá
o sinal negativo; o inverso Q^-1 tem outro sinal negativo. Com G_H=4kappa S/p²
e fonte iU, o fator da correção h* c é portanto

    (-hbar) (4kappa) (-1) i = +4 i kappa hbar.

A Hessiana física é E/(4kappa), e a transformação de gauge em Fourier é
iK. Logo, na convenção formal/euclidiana já adotada,

    Gamma1_hh (iK) + (E/4kappa) Gamma1_h*c
       = i hbar A0 [P4 K + E R0] no setor logarítmico,

e o lambda relativo deixado simbólico na entrega finita vale **1**.
Isso usa a Hessiana física; a gauge-fixada não pode substituí-la.

A mudança entre símbolos de momento e derivadas também não introduz
um sinal relativo entre graus3 e4: (-i)^n i^n=1. Para o contato euclidiano,
C_E/(16pi^4)=-2A0. A quebra finita principal bruta é assim

    -2 i hbar A0 W_1(T,v),
    W_1=(187/1920) q4 Tq·v +(73/960) q4 trT(q·v)
                         -(33/160) q²(qTq)(q·v).

Não é nula. A subtração dos dois contatos já medidos a remove; o
completamento com chi arbitrário está em ENTREGA_016_A7b_contatos_cutoff_finito.md.
O fator relativo foi **composto**, não escolhido para cancelar o resultado.

Cinco verificações algébricas novas, CPU {r['cpu_seconds']}s; zero novo laço,
zero chamada remota, zero alteração em originais ou gate. Isto resolve a
normalização relativa na convenção formal da conta. Não registra como feita
a continuação de toda amplitude temporal Lorentziana no espaço-forma nem a
coincidência com a hierarquia causal completa: essas continuam distintas.

Reprodução: symbolic_runtime/Scripts/python.exe -X utf8 -B
A7/finite_relative_normalization_v2.py, em destino novo. Manifesto ao lado.
'''
rp=folder/'LIGACAO_DOS_SINAIS.md';save(rp,report)
save(OUT/'ENTREGA_016_A7b_normalizacao_relativa_finita.md',report)
save(OUT/'ENTREGA_016_MEDIDA_parser_lambda.md',f'''[REAL — falha local de parser preservada; nenhuma falha física inferida]
Abertura SHA256 `{opening}`. UTC {now}.
finite_relative_normalization.py falhou ao ler a expressão já calculada
"lambda/32 + 43/960": lambda é palavra reservada no parser Python/Sympy.
O log preservado tem SHA256 `{sha(HERE/'finite_relative_normalization_run.log')}`.
A chamada de shell terminava com Get-Content e retornou0; o código de saída
do subprocesso falho não foi guardado separadamente. A falha é visível pelo
traceback; não é registrada como sucesso nem como chamada remota.
v2 apenas remapeia o nome textual para um Symbol antes do parse, preservando
coeficientes e equações. Finalizou os cinco checks e escreveu results.json.
Script v1 SHA256 `{sha(HERE/'finite_relative_normalization.py')}`;
v2 SHA256 `{sha(HERE/'finite_relative_normalization_v2.py')}`.
Próximo ramo: fases causais/curvatura e inserções multilocais da prescrição.
''')
files=[rp,folder/'PRE_REGISTER.json',folder/'results.json',HERE/'finite_relative_normalization_v2.py',
    HERE/'finite_relative_normalization_v2_run.log',HERE/'finite_relative_normalization.py',
    HERE/'finite_relative_normalization_run.log',HERE/'marked_vertex_independent/results.json',
    HERE/'marked_vertex_independent_check.py',HERE/'antifield_vertex/PRE_REGISTER.json',
    HERE/'metric_bubble_v2/results.json',HERE/'finite_antifield_contact_v3/results.json']
save(folder/'manifest.json',json.dumps(dict(at=now,opening_sha256=opening,
    artifacts=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in files]),ensure_ascii=False,indent=2))
ledger=OUT/'LEDGER_016.jsonl';event='A7_RELATIVE_EUCLIDEAN_CONTACT_NORMALIZATION'
if event.encode() not in ledger.read_bytes():
    e=dict(event=event,at=now,provider='local',target='A-7.b',cpu_seconds=r['cpu_seconds'],
        checks=5,new_loop_integrals=0,report_sha256=sha(rp),full_Q2=False)
    save(ledger,ledger.read_bytes()+(json.dumps(e,ensure_ascii=False)+'\n').encode())
cont=HERE/'CONTINUIDADE.json';d=json.loads(cont.read_bytes())
d['at']=now;d['completed_this_turn'].append('Existing Wick sign connected to source inverses:formal Euclidean relative lambda=1; no new loop')
d['relative_normalization_manifest']=str(folder/'manifest.json')
d['latest_orchestration']=dict(at=now,source='Official coordinator message',
    nonterminal_registered={'kimi':3,'mimo':2,'total':5},staging={'kimi':4,'mimo':3,'total':7},
    currently_executing='Kimi tensor_contact_skeptic',
    execution_job='9eefec6b-74ed-41c0-a50f-d5098179eba0',
    failed_mimo_job='f423503e-8c02-467a-b8cc-c3db91323a82',
    new_mimo_job='cc22fd63-7326-4a83-b770-57822c8f874d')
d['pending_orchestration']='5 registered,7 staging; Kimi tensor_contact_skeptic running; MiMo filtration terminal failed'
d['next']=['Continue A7.b: curved finite terms and actual causal insertion hierarchy, including cutoff matching',
    'Read independent Kimi/MiMo reviews as completed without repeating failed units',
    'A7.c only if24h timebox expires; A7.d,A8,Part B and final full requirement audit remain']
save(cont,json.dumps(d,ensure_ascii=False,indent=2))
progress=OUT/'ENTREGA_016_PROGRESSO.md'
save(progress,progress.read_bytes()+f'\n- {now} — A7.b PROGRESSO: reaproveitado sinal Wick medido,lambda formal/euclidiano=1;5checks,CPU{r["cpu_seconds"]}s,sem novo laço. Parserlambda falho preservado. Fila5+staging7,Kimiativo,MiMofiltraçãofalhou. Abertura{opening}.\n'.encode())
print(json.dumps(dict(report=str(rp),status='ACTIVE_PROGRESS',artifacts=len(files)),ensure_ascii=False))
