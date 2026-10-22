"""Deliver the matched ghost component and independently audited source operator."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid
H=Path(__file__).resolve().parent;C=H.parents[1];O=C/'TUNEL/DO_CHATGPT'
D=H/'finite_ghost_source_delivery';D.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat();stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data,existing=False):
    if isinstance(data,str):data=data.encode()
    if p.exists():
        assert existing,p
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+stamp)
        backup.write_bytes(old);assert backup.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    tmp.write_bytes(data);assert tmp.read_bytes()==data;tmp.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode(),existing)
g=json.loads((H/'finite_ghost_pair/results.json').read_bytes())
s=json.loads((H/'finite_source_covariant_operator_v3/results.json').read_bytes())
a=json.loads((H/'finite_source_covariant_operator_audit_v2/results.json').read_bytes())
assert all(not v['full_Q2'] for v in (g,s,a))
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
ghost=f'''[DERIVED — par ghost e combinação parcial; REAL — CAS; OPEN — Ward completo]
# A7.b — contato finito do par ghost na mesma referência
Abertura SHA256 `{opening}`. UTC {now}.

Aplicamos a mesma extensão R e os mesmos projetores harmônicos ao kernel
ghost DIRETO, com vértice não mínimo, dois bitensores e transposição do
segundo vértice na contração orientada. Não inferimos a amplitude de um
determinante mínimo ou do coeficiente de calor livre. Jatos e sinais de
integração por partes são os mesmos usados no par métrico.

PrimeiraK, base K[p²trAB,p²trA trB,pAp trB,pBp trA,pABp]:

    {g['first_K_coefficients']}

SegundaK, base K²[trAB,trA trB]:

    {g['second_K_coefficients']}

Com os pesos existentes (-1/2 para o par métrico cru, +1 para este par
ghost direto), a combinação de DIFERENÇAS LOCAIS, ainda dividida por C, é:

    K1: {g['common_raw_convention_combination_K1']}
    K2: {g['common_raw_convention_combination_K2']}

Os termos logarítmicos foram avaliados separadamente, não omitidos por
hipótese. Os coeficientes de troca das duas pernas são iguais nesta conta.
Para K1 foram escolhidos cinco pares por posto na ordem inversa à seleção
métrica; quatro pares NÃO utilizados no ajuste e um momento não axial
reproduziram os coeficientes. K2 usou dois pares e duas verificações novas.
São {g['checks']} verificações, rc0, CPU{g['cpu_seconds']}s.

A combinação é não nula. Não é Q2: faltam o contato da fonte com sua
Hessiana, o tadpole finito, W admissível e a contribuição Ward da própria
referência diferencial. Não foi escolhida uma subtração para cancelar o
resultado. Original um.py, kernel, gate e prescrição permanecem intactos.
'''
gf=O/'ENTREGA_016_A7b_contatos_finitos_ghost_e_combinacao_parcial.md';write(gf,ghost)
source=f'''[DERIVED — operador finito da fonte; REAL — duas rotas CAS; OPEN — soma causal]
# A7.b — fonte finita covariante, com ordem das derivadas preservada
Abertura SHA256 `{opening}`. UTC {now}.

Os contatos harmônicos dos kernels planos A(T,v;x) e B(T,Dv;x) foram
transportados para o ghost: A dá +D_(ijk)v; B dá +D_(ij)D_k v.
Esses sinais vêm da ação das derivadas do delta sobre T seguida do adjunto;
não são os sinais dos momentos logarítmicos de Taylor. As fases Fourier
foram verificadas explicitamente. À contribuição plana covariantizada
somou-se o contato K já medido com transporte da densidade externa.

Resultado, retirado C e os fatores globais já separados nas entregas:

    DeltaR/C = -7/48 G(Boxv)+13/96 Hess(divv)+g Box(divv)/32
             +K[65/288 G(v)-29/144 g divv]
             = G[-7/48 Boxv+13/192 grad(divv)+65K/288 v]
               +g[Box(divv)/32-29K divv/144].

G(v)=nabla v+(nabla v)^t. Não é só gauge: escrevendo
phi=Box(divv)/32-29K divv/144, a ação da Hessiana física E é

    E(DeltaR/C)=-2Hess(phi)+2g Box(phi)+6K g phi.

Foi usado E G=0 no MESMO fundo Einstein, e a identidade foi também
conferida diretamente com jatos polinomiais reais e a implementação de E,
sem substituir a Hessiana física pela gauge-fixada.

**Auditoria por outra rota:** os contatos planos foram reconstruídos por
momentos de S3, sem a inversão harmônica do primeiro cálculo:

    N_A=13/288 <A(n)(n.q)^3>-q²<A(n)(n.q)>/64,
    N_B=-5/48 <B(n)(n.q)^2>+5q²<B(n)>/192.

Para as dez fibras simétricas, p e v permaneceram simbólicos. Os coeficientes
planos e curvos coincidiram. A identidade dos jatos ordenados foi reutilizada
somente após conferir igualdade estrutural com o código antes auditado.
Outra verificação aplicou E em dois campos polinomiais, 16 componentes e
ordensK0,K1,K2. Há controles explicitamente não nulos.

Cálculos rc0: {s['checks']}+{a['checks']} verificações, CPU
{s['cpu_seconds']}+{a['cpu_seconds']}s. O termo K² dessa imagem é a ação
de E sobre o operador fonte obtido; não é uma nova amplitude fonte K²
calculada separadamente. Os jatos suaves W não foram declarados zero.
Nenhuma conclusão sobre a anomalia completa decorre só desta decomposição.

Tentativas preservadas: v1 falhou por parêntese excedente; v2 pela passagem
de polinômio zero a um jato de grau3; v3 corrige esse caso vazio, sem mudar
os coeficientes. Auditor v1 também tinha um parêntese excedente, corrigido
em v2. Logs e fontes de todas as tentativas foram mantidos no manifesto.
'''
sf=O/'ENTREGA_016_A7b_operador_covarante_da_fonte_finita.md';write(sf,source)
failed=['finite_source_covariant_operator_check.py','finite_source_covariant_operator_run.log',
 'finite_source_covariant_operator_check_v2.py','finite_source_covariant_operator_v2_run.log',
 'finite_source_covariant_operator_audit.py','finite_source_covariant_operator_audit_run.log']
measure=f'''[REAL — falhas técnicas registradas; DERIVED — resultados posteriores separados]
# A7.b — correções técnicas na fonte finita
Abertura SHA256 `{opening}`. UTC {now}.

Comando base: symbolic_runtime/Scripts/python.exe -X utf8 -B A7/<script>.
Os três ensaios abaixo terminaram rc1 antes de qualquer resultado científico:
v1/SyntaxError(parêntese), v2/TypeError(polynomial zero convertido em jato
com aridade insuficiente), auditorv1/SyntaxError(parêntese).
Fontes e logs preservados, hashes por script no manifesto. v3 e auditorv2
terminaram rc0. Custo externo desta correção: nenhuma nova chamada remota.
Próxima operação: inserir G(v) diretamente nos kernels do par métrico e ghost,
conferindo a fonte e os sinais na mesma referência. Q2 ainda não concluída.
'''
mf=O/'ENTREGA_016_MEDIDA_execucoes_fonte_finita.md';write(mf,measure)
files=[Path(__file__),gf,sf,mf,H/'finite_ghost_pair_engine.py',H/'finite_ghost_pair_check.py',H/'finite_ghost_pair_run.log',
 H/'finite_ghost_pair/manifest.json',H/'finite_ghost_pair/PRE_REGISTER.json',H/'finite_ghost_pair/results.json',
 H/'finite_source_covariant_operator_check_v3.py',H/'finite_source_covariant_operator_v3_run.log',
 H/'finite_source_covariant_operator_v3/manifest.json',H/'finite_source_covariant_operator_v3/PRE_REGISTER.json',
 H/'finite_source_covariant_operator_v3/results.json',H/'finite_source_covariant_operator_audit_v2.py',
 H/'finite_source_covariant_operator_audit_v2_run.log',H/'finite_source_covariant_operator_audit_v2/manifest.json',
 H/'finite_source_covariant_operator_audit_v2/PRE_REGISTER.json',H/'finite_source_covariant_operator_audit_v2/results.json']+[H/n for n in failed]
manifest=dict(at=now,opening_sha256=opening,artifacts=[dict(path=str(p),sha256=sha(p)) for p in files])
put(D/'delivery_manifest.json',manifest)
for row in manifest['artifacts']:assert sha(Path(row['path']))==row['sha256']
ledger=O/'LEDGER_016.jsonl';cpu=sum(r['cpu_seconds'] for r in (g,s,a))
event=dict(event='A7_FINITE_GHOST_AND_COVARIANT_SOURCE',at=now,target='A-7.b',
    manifest_sha256=sha(D/'delivery_manifest.json'),cpu_seconds=cpu,external_execution=False,
    completed_checks=g['checks']+s['checks']+a['checks'],failed_attempts=3,full_Q2=False)
write(ledger,ledger.read_bytes()+(json.dumps(event)+'\n').encode(),True)
progress=O/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\n- {now} A7.b PROGRESS: ghost finito e fonte covariante, {event["completed_checks"]} controles, CPU{cpu}s, rc0; três falhas técnicas preservadas. Soma Ward completa OPEN.\n'.encode(),True)
continuity=H/'CONTINUIDADE.json';v=json.loads(continuity.read_bytes())
v.update(at=now,previous_goal_turn='PROGRESS',finite_ghost_source_manifest=str(D/'delivery_manifest.json'))
v['completed_this_turn']=['Finite ghost pair K1/K2,7independent holdouts,rc0',
 'Actual finite source covariant operator fit12checks plus independent S3 and real Einstein audit116checks,rc0']
v['next']=['Monitor own finite_pair_ward_check session42551, do not duplicate; comparing exact gauge insertion with source image',
 'Keep differential reference, finite tadpole and smooth W explicit; partial difference not whole Q2',
 'A7.c after24h if unpaid; A7.d,A8,PartB,finalaudit still required']
put(continuity,v,True)
print(json.dumps(dict(verified=True,artifacts=len(files),checks=event['completed_checks'],cpu_seconds=cpu)))
