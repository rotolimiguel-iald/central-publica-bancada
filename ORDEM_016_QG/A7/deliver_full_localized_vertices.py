"""Publish metric and ghost boundary completion with explicit density choices."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid

H=Path(__file__).resolve().parent;D=H/'full_localized_vertices_delivery';D.mkdir(exist_ok=False)
O=H.parents[1]/'TUNEL/DO_CHATGPT';now=datetime.now(timezone.utc)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,b):
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+now.strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex);bk.write_bytes(old);assert bk.read_bytes()==old
 t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(b);assert b and t.read_bytes()==b;t.replace(p)
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2).encode()
def append(p,s):write(p,p.read_bytes()+s.encode())
names=['localized_eh_cubic','full_eh_localized_loop','localized_ghost_boundary'];results=[];artifacts=[]
for name in names:
 m=H/name/'manifest.json'
 for item in json.loads(m.read_bytes())['artifacts']:assert sha(Path(item['path']))==item['sha256'],item['path']
 results.append(json.loads((H/name/'results.json').read_bytes()));artifacts.extend([m,H/(name+'_run.log')])
checks=sum(r['checks'] for r in results);cpu=sum(r['cpu_seconds'] for r in results)
opening=sha(O/'ENTREGA_016_ABERTURA_operador.md')
proof=r'''[DERIVED — vértices localizados planos e laços fora da diagonal; Q2 OPEN]

## Corrente métrica e sinal

Mantida a ação S_EH=-1/(2kappa) integral chi sqrt(g)R e a identidade
sqrt(g)R=C_GammaGamma+div B, com a corrente previamente construída
B^mu=sqrt(g)(g^ab Gamma^mu_ab-g^mu,a Gamma^b_ab).
A contribuição da corrente na ação localizada é
+1/(2kappa) integral (partial_mu chi)B^mu.

b3 é a polarização cúbica dessa corrente, com o fator Fourier i removido.
Os vértices matriciais existentes armazenam o polinômio Fourier V3raw=16k V3.
Na mesma convenção, o novo vértice é
W_local=chi W_GammaGamma-8 (partial_mu chi)b3^mu.
Para momento total Q das três pernas e momento ell=-Q do cutoff:
-8 ell.b3=+8Q.b3=eh_boundary_vertex_raw. Isso confere o sinal relativo,
não se identifica uma derivada física real com ip sem a convenção dita.

Realização: os jatos internos são (B,partial_0 B,...,partial_3 B).
Se a derivada de b3 atua numa perna interna, preenche blocos 10/01 de W0.
Se atua em h externo, preenche o bloco00 de Wi. Não se acrescenta uma
perna: é a corrente do mesmo vértice. A avaliação matricial reproduz o
vértice completo para40 configurações, incluindo troca das pernas internas.
A identidade de Ward cúbica independente, com Q diferente de0, confere:
V3raw(Gc,U,V)+2 V2raw(L_c U,V)+2 V2raw(U,L_c V)
=2(Q.c)V2raw(U,V). Aqui V2 e V3 são as densidades EH completas.
São166 verificações; trocar o sinal ou omitir a corrente altera controles.

## Localização nas duas extremidades

O novo motor conserva separadamente cinco variantes de cada vértice:
chi vezes o vértice bulk e quatro partial_l chi vezes a corrente.
A adjunção atua também nesses coeficientes. Por isso a integração em X
pede HessX chi, e a integração em Y pode pedir thirdY chi. Descartar os
jatos de ordem superior porque o vértice original só tinha h/Dh é incorreto.
Para os dois tensores externos11 e01, no ponto(1,2,-1,1),97 verificações
conferem a recuperação do caso constante e dos dados GammaGamma anteriores.
Os termos métricos completos e os intermediários estão ambos preservados.

## Ghost: conservar a integração por partes, com sua fronteira

O vértice dirigido existente representa -(partial_mu barc_nu)Z^mu,nu,
com Z a variação de calibre linear em h. A densidade não integrada
barc_nu partial_mu Z^mu,nu, localizada ANTES da integração, obedece
integral chi barc div Z=-integral(chi dbarc+dchi barc)Z.
Portanto a correção é -(dchi)barc Z. Ela é construída substituindo, em
cada coluna derivada de barc do vértice existente, d_mu barc por
(partial_mu chi)barc; a normalização e a orientação dirigida são preservadas.

A comparação de20 configurações com a fórmula explícita de Z confere
o vértice original e o corrigido, sem usar o motor de corrente métrica.
Todos20 controles mudam se a fronteira ghost for omitida. A soma dos laços
usa transposição no segundo vértice ghost e /16 no par métrico, como antes.
São91 verificações nesta etapa. Não é uma escolha implícita de nova
prescrição: as duas densidades, equivalentes a cutoff constante, e a
diferença dchi que as relaciona ficam EXPLÍCITAS. O representante usado
na prescrição causal final terá de conservar essa mesma relação.

## Resultado que distingue bulk, fluxo e anomalia

Para h11,c0, X-Y=(1,2,-1,1), chiX=chiY=1 no ponto:
* Todos os demais jatos nulos: ghost_full-metric_full/2=0.
* dchiY=e0:3960/117649.
* dchiY=e0 e dchiX=e0-e1:57856/117649.
* Somente partial_Y0 partial_Y0 partial_Y1 chiY=1:-12/2401.

O último exemplo mostra concretamente a dependência do terceiro jato.
Os valores intermediários sem fronteira ghost continuam nos arquivos;
não são a soma completa calculada nesta entrega.

Não se exige que o fluxo de uma interação localizada por cutoff variável
se anule. Não chamar esse valor fora da diagonal de anomalia quântica.
A fonte localizada, a variação BRST dos termos de cutoff, as contribuições
de contato da extensão, curvatura e aridades superiores ainda precisam
ser montadas na mesma prescrição. Não foi calculado Q2 completo.
Nenhum original, kernel, definição de horizonte ou gate foi alterado.
'''
write(D/'DERIVACAO.md',proof.encode());artifacts.extend([D/'DERIVACAO.md',Path(__file__)])
manifest=dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,full_Q2=False,
 artifacts=[dict(path=str(p),sha256=sha(p)) for p in artifacts]);write(D/'manifest.json',dump(manifest))
ledger=O/'LEDGER_016.jsonl';append(ledger,json.dumps(dict(at=now.isoformat(),event='FULL_EH_AND_GHOST_LOCALIZED_VERTICES',target='A7.b',checks=checks,cpu_seconds=cpu,rc=0,manifest_sha256=sha(D/'manifest.json'),remote_call=False))+'\n')
total=Decimal(0);seen=set()
for line in ledger.read_text('utf-8-sig').splitlines():
 if not line.strip():continue
 e=json.loads(line);k=e.get('execution_task_id') or e.get('job_id') or e.get('request_id');v=e.get('cost_estimate_usd',e.get('cost_usd'))
 if v is not None and (k is None or k not in seen):
  total+=Decimal(str(v))
  if k:seen.add(k)
start=datetime.fromisoformat(json.loads((H/'localized_eh_cubic/PRE_REGISTER.json').read_bytes())['at']);wall=(now-start).total_seconds()/3600
note=f'''[DERIVED — corrente EH e fronteira ghost incorporadas aos laços planos]

{now.isoformat()}. Abertura SHA256 {opening}.

O vértice matricial localizado reproduz o EH completo:
W_local=chi W_GammaGamma-8 dchi.b3, na normalização16kappa.
Identidade de Ward cúbica conferida com momento total não nulo.
Incorporada também a fronteira ghost da identidade
integral chi barc divZ=-integral(chi dbarc+dchi barc)Z.
As densidades e suas diferenças regionais estão explícitas; não se muda
a prescrição causal silenciosamente.

{checks} verificações exatas (166+97+91), CPU{cpu}s, três execuções rc0.
Com cutoff constante a soma ghost-métrica/2 continua0; com jatos variáveis
o fluxo de fronteira permanece, incluindo terceiro jato Y (-12/2401 num
controle). Esse fluxo fora da diagonal não é a anomalia quântica.
Próximo: variação BRST do cutoff e extensão dos kernels completos, junto
da fonte já derivada. Curvatura/aridades e Q2 completo seguem OPEN.

Manifesto {D/'manifest.json'}; SHA256 {sha(D/'manifest.json')}.
Comandos: A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/[localized_eh_cubic_check.py,full_eh_localized_loop_check.py,localized_ghost_boundary_check.py], separadamente.
Logs e hashes no manifesto. Intervalo de bancada registrado{wall:.6f}h.
Parcial de provedores US${total}, custos pendentes não contados como zero.
Nenhum original, kernel ou gate alterado.
'''
out=O/'ENTREGA_016_A7b_vertices_localizados_EH_ghost.md';assert not out.exists();write(out,note.encode())
append(O/'ENTREGA_016_PROGRESSO.md',f'\n- {now.isoformat()} A7.b PROGRESS: EH e ghost localizados,354checks,CPU{cpu}s,bancada{wall:.6f}h; parcialUS${total}; fluxo fora da diagonal medido,Q2 OPEN.\n')
p=H/'CONTINUIDADE.json';c=json.loads(p.read_bytes());c.update(at=now.isoformat(),previous_goal_turn='PROGRESS',
 completed_this_turn=['Full cubic EH localized matrix vertex normalized and Ward checked','Metric bubble includes boundary at both endpoints','Ghost pre-IBP boundary restored, combined loops expose third cutoff jet'],
 full_localized_vertices_manifest=str(D/'manifest.json'),own_live_processes=[],
 next=['Compute BRST cutoff flux for full localized representatives; distinguish from quantum contact anomaly',
       'Extend unreduced full metric/ghost kernels with both cutoffs and combine source; curvature and arities remain',
       'Audit pending Kimi/MiMo via coordinator; keep DeepSeek70e9 blocked',
       'A7b deadline20:32Z; A7c/d,A8,PartB and final audit remain'])
write(p,dump(c));print(json.dumps(dict(delivery=str(out),checks=checks,cpu_seconds=cpu,partial_cost=str(total))))
