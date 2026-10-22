"""Deliver the flat reference conversion without replacing previous artifacts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;O=H.parents[1]/'TUNEL/DO_CHATGPT';D=H/'flat_reference_ward'
now=datetime.now(timezone.utc).isoformat();stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data,existing=False):
    if isinstance(data,str):data=data.encode()
    if p.exists():
        assert existing,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(data)
    assert t.read_bytes()==data;t.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,indent=2,ensure_ascii=False),existing)
r=json.loads((D/'results.json').read_bytes());opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
report=f'''[DERIVED — referência plana convertida; REAL — CAS; OPEN — continuação curva e Q2]
# A7.b — parcela Ward da referência harmônica plana
Abertura SHA256 `{opening}`. UTC {now}.

**O avanço:** a referência harmônica não podia ser declarada Ward-neutra.
Agora sua contribuição plana foi calculada nos mesmos pares métrico,
ghost e fonte, mantendo R=FP[(1-a)mu^(2a)z^a .]. A recorrência aceita
na revisão Kimi permite escrever cada R(U_b), b>=2, como derivadas de
R(U2) mais um contato local explícito. Não escolhemos uma nova extensão.

Na base [p⁴Tpv, p²pTp pv, p⁴trT pv], sempre contato/C:

| parcela | coeficientes |
|---|---|
| diferença local antes medida | {r['contact_coefficients']} |
| referência escalar agora medida | {r['reference_coefficients']} |
| soma finita plana neste cálculo | {r['total_flat_finite_coefficients']} |

A fonte contribui por E DeltaR, com E física, não a gauge-fixada. Aplicamos
E ao tensor teste e verificamos o contato dessa fonte contra os três casos
da conta anterior. Nos pares mantivemos o peso métrico -1/2 e ghost +1.

**Verificação por outra expressão escalar:** para um harmônico H_l e
homogeneidade -m-4, k=(m-l)/2 e N=(m+l+4)/2, l<=m, a constante finita
de Fourier, convertida de volta ao símbolo diferencial e dividida por C, é

    (-1)^(l+1) [H_k+H_(N-1)-1] / [2^(m+2) k! (N-1)!].

Ela resulta de expandir (1-a) Gamma(-k+a)/Gamma(N-a), depois de retirar
o fator logarítmico comum log(4mu²/p²)-2EulerGamma. A soma dos contatos
harmônicos anteriores com a nova parcela reproduziu os nove casos m<=4.
Não usamos essa fórmula como transformada Lorentziana completa no espaço-forma.

Foram {r['checks']} controles: nove expressões escalares, três comparações
da fonte e uma previsão não axial não usada no ajuste. Nesta última, a
parcela da referência é -2597/108. CPU{r['cpu_seconds']}s, rc0.

**Correção ao lado:** a conta antiga que usava uma referência P4 global
produziu {r['prior_global_P4_reference_coefficients']} na mesma ordem da
base. A diferença medida entre os dois cálculos é
{r['difference_from_prior_global_P4']}. Não são coeficientes intercambiáveis.
R não comuta com a extração de derivadas; a igualdade dos kernels fora
da diagonal não identifica automaticamente suas normalizações locais.
Preservamos ambos os resultados, sem atribuir ao antigo a normalização
dos pares crus calculada agora. Sua primitiva anterior cobre seu próprio
contato, não esta nova lista por simples troca de rótulo.

**Ainda separado:** a parcela logarítmica comum, os harmônicos altos na
curvatura, o tadpole finito, W admissível, cutoff e a hierarquia causal.
Os cálculos logarítmicos anteriores têm suas próprias evidências; este
teste não os reexecutou nem demonstra a STI completa. Em particular,
harmônicos l>m podem não ter diferença local, mas têm referência não local:
nunca apagá-los numa extensão desta conta ao fundo curvo. Q2 segue OPEN.
Nenhum contratermo, original, kernel ou gate foi alterado.
'''
rf=O/'ENTREGA_016_A7b_referencia_harmonica_plana_Ward.md';write(rf,report)
files=[Path(__file__),rf,H/'flat_reference_weight_engine.py',H/'prepare_flat_reference_inputs.py',
 H/'flat_reference_metric_engine.py',H/'flat_reference_ghost_engine.py',H/'flat_reference_inputs_manifest.json',
 H/'flat_reference_ward_check.py',H/'flat_reference_ward_run.log',D/'PRE_REGISTER.json',D/'results.json',D/'manifest.json']
manifest=dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files])
put(D/'delivery_manifest.json',manifest)
for item in manifest['artifacts']:assert sha(Path(item['path']))==item['sha256']
event=dict(at=now,event='A7_FLAT_HARMONIC_REFERENCE_WARD_MEASURED',target='A7.b',
 manifest_sha256=sha(D/'delivery_manifest.json'),checks=r['checks'],cpu_seconds=r['cpu_seconds'],
 remote_execution=False,full_Q2=False,prior_reference_difference=r['difference_from_prior_global_P4'])
ledger=O/'LEDGER_016.jsonl';write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {now} A7.b PROGRESS: referência harmônica plana calculada,13controles,CPU{r["cpu_seconds"]}s,rc0; diferença para a normalização global anterior registrada, sem sobrescrita. Q2 OPEN.\n'.encode(),True)
cont=H/'CONTINUIDADE.json';v=json.loads(cont.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',flat_reference_ward_manifest=str(D/'delivery_manifest.json'))
v['completed_this_turn'].append('Flat scalar reference Ward contribution and difference from prior global reference,13checks,rc0')
v['next']=['Curved harmonic reference: preserve l>m nonlocal sectors; do not extrapolate flat conversion',
 'Keep finite tadpole, admissible W, cutoff and higher T-product arities explicit',
 'Await independent Kimi/MiMo/DeepSeek responses through existing coordinator',
 'A7.b timebox until approximately2026-09-25T20:32Z; then A7.c if unpaid,A7.d,A8,PartB,finalaudit']
v['own_live_processes']=[]
put(cont,v,True)
print(json.dumps(dict(delivered=True,artifacts=len(files),checks=r['checks'],cpu_seconds=r['cpu_seconds'])))
