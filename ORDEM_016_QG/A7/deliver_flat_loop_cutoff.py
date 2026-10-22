"""Publish exact localized flat loop extraction without promoting its scope."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib,json,uuid

H=Path(__file__).resolve().parent;D=H/'flat_loop_cutoff';O=H.parents[1]/'TUNEL/DO_CHATGPT'
now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
    if p.exists():
        old=p.read_bytes();backup=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex)
        backup.write_bytes(old);assert backup.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2).encode()
def append(p,text):write(p,p.read_bytes()+text.encode())
for row in json.loads((D/'manifest.json').read_bytes())['artifacts']:
    assert sha(Path(row['path']))==row['sha256'],row['path']
r=json.loads((D/'results.json').read_bytes());opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
proof=r'''[DERIVED — localização plana de bolhas; completar vértices EH e extensão]

## Dados não reduzidos e localização

Para cada jato externo mu (0 para h, i para partial_Xi h), sejam F0^mu_ab
e F1^mu,j_ab as contrações com o vértice Y sem e com derivada externa.
Os fatores dos motores são conservados: métrica /16; ghost com transposta
do vértice Y; multiplicidade m_ab=1 diagonal e2 fora da diagonal.

W^mu(chiY)=sum_a 2/m_ab [-chiY partial_Ya F0^mu_ab
 -(partial_Ya chiY)F0^mu_ab
 +sum_j {chiY partial_Ya partial_Yj F1^mu,j_ab
 +(partial_Ya chiY)partial_Yj F1^mu,j_ab
 +(partial_Yj chiY)partial_Ya F1^mu,j_ab
 +(partial_Ya partial_Yj chiY)F1^mu,j_ab}].

O coeficiente final de h após adjunção X é
L=chiX W^0 - sum_i partial_Xi(chiX W^i).
No plano, os kernels não reduzidos dependem de X-Y:
partial_Xi F=-partial_Yi F. Isso vale para F, NÃO autoriza derivar
chiY em X. No motor extra_word aplica-se apenas ao kernel.
Daí L=chiX W^0 - (dchiX)_i W^i +chiX W^i[partial_Yi F].
A fórmula resulta da regra do produto e adjunção em testes compactos.
São necessários F0,F1 e seus jatos: os W^mu com chiY=1 não os determinam.

## Comparação com os dados já existentes

Novo motor calcula os propagadores planos e suas derivadas diretamente:
G_ghost=delta/z e G_metric=(delta_ac delta_bd+delta_ad delta_bc
-delta_ab delta_cd)/(2z). Mantém os vértices existentes.
Em X-Y=(1,2,-1,1), os80 valores para h11,h01, cinco jatos X,
quatro componentes de c e dois tipos de laço coincidem EXATAMENTE com
as bases C0/C1 da extração bilocal anterior. O ponto não é axial.
64 valores de localização têm aritmética racional exata;8 cancelamentos
no cutoff constante e2 controles de não cancelamento completam154.

Para h11,c0, a combinação ghost-metric/2 é:
chiX=chiY=1, gradientes nulos: 0;
dchiY=(1,0,0,0): 2344/117649;
dchiY=(1,0,0,0),dchiX=(1,-1,0,0): 9112/117649;
dchiY=0 e HessY=[[1,2,0,0],[2,-1,0,0],[0,0,0,0],[0,0,0,0]]:
360/16807. Em todos os casos os valores chiX=chiY=1 são locais;
esses jatos admitem realizações por funções suaves compactas.

Não se usa o cancelamento com cutoff constante como prova para cutoff
variável. Os termos adicionais são resultados, não erro numérico.

## Identidade de comparação da extensão (derivação, ainda sem soma numérica)

Defina C_D(f)=R(Df)-D R(f), R comutando com multiplicação suave.
Se W_R^mu usa os F estendidos antes das derivadas e W^mu é a expressão
fora da diagonal, então Delta^mu=W_R^mu-R(W^mu) é
sum_a 2/m_ab [chiY C_partialYa(F0^mu_ab)
 -sum_j {chiY C_partialYa partialYj(F1^mu,j_ab)
 +(partial_Ya chiY)C_partialYj(F1^mu,j_ab)
 +(partial_Yj chiY)C_partialYa(F1^mu,j_ab)}].
O termo HessY multiplica R(F1), portanto não cria um comutador adicional.
Para P=chiX W_R^0-partial_Xi(chiX W_R^i), e
Q=R[chiX W^0-partial_Xi(chiX W^i)], segue exatamente
P-Q=chiX Delta^0-partial_Xi(chiX Delta^i)
     +sum_i C_partialXi(chiX W^i).
Prova: substituir W_R=R(W)+Delta; a comutação de R com multiplicação
elimina os termos sem derivada, e os demais são a definição de C_partial.
Não se acrescenta contato à adjunção de distribuições já estendidas.
Multiplicar uma derivada de delta por chiX exige seus jatos completos.

## Limites e próximo passo

O vértice métrico usado aqui é GammaGamma. A corrente de divergência
EH foi derivada separadamente e NÃO foi somada a estas bolhas.
Também faltam os contatos da extensão das expressões localizadas,
curvatura, aridades superiores e a identificação causal. Não é Q2 completo
nem demonstração de cancelamento da anomalia. O próximo cálculo é
incorporar a corrente EH ao vértice localizado, conservando estes dados
não reduzidos, e só então montar a comparação de extensão acima.
Nenhum original, kernel ou gate foi alterado.
'''
p=D/'DERIVACAO.md';assert not p.exists();write(p,proof.encode())
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=r['checks'],cpu_seconds=r['cpu_seconds'],
    artifacts=[dict(path=str(p),sha256=sha(p)) for p in [D/'manifest.json',D/'DERIVACAO.md',H/'flat_loop_cutoff_run.log',Path(__file__)]],full_Q2=False)
p=D/'delivery_manifest.json';assert not p.exists();write(p,dump(manifest))
ledger=O/'LEDGER_016.jsonl'
append(ledger,json.dumps(dict(at=now.isoformat(),event='FLAT_LOOP_TWO_CUTOFF_UNREDUCED_EXTRACTION',target='A7.b',
    checks=r['checks'],cpu_seconds=r['cpu_seconds'],rc=0,manifest_sha256=sha(p),remote_call=False))+'\n')
total=Decimal(0);seen=set()
for line in ledger.read_text('utf-8-sig').splitlines():
    if not line.strip():continue
    e=json.loads(line);key=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
    if v is not None and (key is None or key not in seen):
        total+=Decimal(str(v))
        if key:seen.add(key)
started=datetime.fromisoformat(json.loads((D/'PRE_REGISTER.json').read_bytes())['at'])
wall=(now-started).total_seconds()/3600
note=f'''[DERIVED — bolhas planas com dois cutoffs; Q2 completo OPEN]

{now.isoformat()}. Abertura SHA256 {opening}.

Extração não reduzida dos laços ghost e métrico GammaGamma, com h e Dh
externos. Reconstrução independente dos80 coeficientes prévios em ponto
não axial;154 verificações totais, CPU{r['cpu_seconds']}s, rc0.
Com cutoffs constantes ghost-métrica/2=0. Para h11,c0, dchiY=e0:
2344/117649; incluindo dchiX=e0-e1:9112/117649. A fronteira é necessária.
A corrente EH completa permanece separada; não se atribui esse resíduo
ao conjunto final. Derivada também a identidade abstrata P-Q dos contatos
dos laços, com sinais explícitos e sem inventar contatos na adjunção.

Comando: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/flat_loop_cutoff_check.py.
Log {H/'flat_loop_cutoff_run.log'}; SHA256 {sha(H/'flat_loop_cutoff_run.log')}.
Manifesto {p}; SHA256 {sha(p)}. Derivação: {D/'DERIVACAO.md'}.
Intervalo registrado de bancada{wall:.6f}h; CPU não confundida com parede.
Parcial conhecido de provedores US${total}; pendentes/desconhecidos não são zero.
Próximo: vértice EH localizado completo e contatos dos kernels não reduzidos.
Nenhum original, kernel ou gate alterado.
'''
out=O/'ENTREGA_016_A7b_lacos_planos_dois_cutoffs.md';assert not out.exists();write(out,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: laços planos h/Dh dois cutoffs,154checks,CPU{r["cpu_seconds"]}s,bancada{wall:.6f}h; parcialUS${total}; corrente EH/contatos completos OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
    completed_this_turn=['Unreduced flat metric/ghost loop kernel jets localized at both endpoints','154 exact checks including80 nonaxial comparisons with old coefficients','General contact comparison identity derived without assuming extension commutes with derivatives'],
    flat_loop_cutoff_manifest=str(D/'delivery_manifest.json'),own_live_processes=[],
    next=['Add full EH boundary current to localized cubic vertex; retain flat_loop_cutoff raw kernel data',
          'Assemble extension contacts for localized loops; then curvature/higherarity within A7b timebox',
          'Audit new Kimi/MiMo replies through coordinator; DeepSeek70e9 remains blocked',
          'A7b deadline20:32Z; A7c/d,A8,PartB and full audit remain'])
write(p,dump(c));print(json.dumps(dict(delivery=str(out),checks=r['checks'],partial_cost=str(total))))
