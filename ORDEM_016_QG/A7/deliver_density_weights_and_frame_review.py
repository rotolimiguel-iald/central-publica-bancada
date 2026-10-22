"""Publish the density conversion correction and a pre-registered assembly diagnostic."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal
import json,hashlib,uuid
H=Path(__file__).resolve().parent;OUT=H.parents[1]/'TUNEL/DO_CHATGPT'
D=H/'density_weights_frame_delivery';D.mkdir(exist_ok=False)
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S_%f')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,raw,existing=False):
    if p.exists():
        assert existing
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+stamp);assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex);t.write_bytes(raw);assert t.read_bytes()==raw and raw;t.replace(p)
def put(p,v,existing=False):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'),existing)
def txt(p,t):write(p,t.encode('utf-8'))
folders=['real_density_fourier_vertex','mixed_b_h_current_v3','wick_current_weights','kimi_normal_frame_contact_review/local_audit_v2','ward_current_assembly_diagnostic']
results={f:json.loads((H/f/'results.json').read_bytes()) for f in folders}
checks=sum(v.get('checks',0) for v in results.values());cpu=sum(v['cpu_seconds'] for v in results.values())
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
ledger=OUT/'LEDGER_016.jsonl';seen=set();cost=Decimal(0)
for line in ledger.read_text('utf-8').splitlines():
    r=json.loads(line);val=r.get('cost_estimate_usd')
    if val is None:val=r.get('cost_usd')
    if val is None:continue
    key=r.get('execution_task_id') or r.get('job_id') or r.get('request_id')
    if key and key in seen:continue
    if key:seen.add(key)
    cost+=Decimal(str(val))
txt(D/'DERIVACAO.md',f'''[DERIVED — conversão e combinatória verificadas; montagem completa/Q2 OPEN]

## Correção de sinal ao lado da entrega anterior

A inversa bosônica anterior permanece:GD=-4kappa S GQ e Ghb=G GQ.
O passo incorreto era tomar V3stored/(16kappa) como vértice em derivadas REAIS.
O arquivo metric_principal_vertices.py armazena o polinômio FOURIER.
Na ação S=-integral chi sqrt(g)R/(2kappa), cada monômio localizado tem DUAS
derivadas, inclusive a fronteira dchi.B. Substituir partial por ip dá i²=-1.
Logo V3real=-V3stored/(16kappa), V2real=-V2stored/(8kappa).

Uma expansão independente de g^-1,sqrt(g),Gamma por coeficientes nilpotentes
reconstruiu C_GammaGamma com Gamma REAL e a corrente B. Em5 configurações,
V3stored=-16 V3real(kappa=1), incluindo dchi não nulo;16 verificações.
Exemplo: densidade cúbica real=-1; vértice armazenado=16.
Portanto o diagrama com UM EH e Jb direto recebe+1/4, não-1/4.
Dois vértices EH-derivados têm os dois sinais e preservam o produto.
mixed_b_h_current_engine_v3.py corrige somente esse fator;575checks novamente.
O controle Y passa a128/16807 e contato-259/192; XY a-1222/16807 e-35/32.
A entrega anterior e v2 ficam preservadas com errata explícita, não apagadas.

## Pesos de Wick derivados sem olhar o resíduo

Na expansão euclidiana formal exp(-V/hbar), o coeficiente cruzado conectado
da ação efetiva é-<VX VY>. Para VX=x.A.x/2 e VY=y.B.y/2, Gamma_G²/2 dá
<VX VY>=tr(A G B G^T)/2. O par métrico tem peso-1/2.
Para barX cX barY cY, a contração cruzada é negativa; o par ghost tem+1.
Para a média da corrente, a primeira ordem é-<C V>:
* corrente simétrica C=J_AB h_A h_B c/2: peso-1/2 na contração matricial;
* corrente b h c: peso-1 em UM emparelhamento ordenado (os dois cancelam1/2);
* corrente ghost: peso-1 no resultado que JÁ inclui os dois emparelhamentos.
O cálculo por derivadas bosônicas simbólicas e álgebra exterior conferiu11
identidades. Não são fatores ajustados para cancelar um número da bancada.
É necessário ainda ligar todos os representantes de densidade à MESMA Ward.

## Controle da montagem parcial e termo que falta

Antes da execução foi registrada a soma candidata
pair+source+current_metric/2+current_bh+current_ghost,
com corrente situada emY, h externo emX e c externo emY.
Com h11,c0,x=(1,2,-1,1) e jatos EXPONENCIAIS completos:
* lambda=eta=0:resíduo0;
* lambda=0,eta=e0:resíduo0;
* lambda=e0-e1,eta=e0:resíduo-14928/117649.
No segundo caso,pair=3281/117649,source=-796/117649,metric=-12104/117649,
bh=128/16807,ghost=2671/117649. A soma com os pesos pré-fixados é0.
O valor antigo3960/117649 tinha apenas gradienteY, demais jatos nulos;
não é o mesmo teste que chiY com jatos exponenciais de todas as ordens.

O teste NÃO cobre todos os tensores/pontos/estados e não prova Q2=0.
Ainda faltam correntes situadas emX com h externo e ghost interno, contra
o vértice ghost emY, além dos setores já abertos. Essas inserções podem
contribuir quando dchiX!=0; a identificação não prova que absorvam todo o
resíduo. Um resíduo fora da diagonal diagnostica montagem incompleta ou
incompatível, não uma anomalia LOCAL da extensão. Nenhum peso foi reajustado.

## Parecer Kimi normal-frame

Recebido e lido inteiro, consumo registrado uma vez:378738tokens totais;
assinatura sem custo monetário alocado. Detector não axial conferido:
estruturas(14,-14,2) e(0,-7,-2); contatos/C_E=113/8 e83/288; ordem5=14.
A diferença de esquemas(-35/144,-1/12,7/72) foi conferida.
Correção: diferença não nula NÃO prova não naturalidade de um esquema.
Dois operadores naturais podem diferir por contratermo natural local não zero,
como K g_ab box(div c). A naturalidade da prescrição coordenada continua
OPEN até conferir sua transformação; não foi refutada por aquela diferença.
Taylor radial para testes suaves vale como identidade de jatos finitos com
resto, não série necessariamente convergente. Convenção de fase já tinha
ponte medida; falta de contexto do parecer não reabre esse item.
29 controles na auditoria v2;v1 preservada por testar apenas soma das entradas
da matriz de rotação, substituída por conferência componente a componente.

Total{checks} verificações (inclui575 repetidas pela mudança de sinal) +3
diagnósticos da soma;CPU{cpu}s. Primeiro comando da densidade usou Python
semSymPy e falhou antes do cálculo; log preservado, runtimeA4 concluiu rc0.
Custo externo conhecido parcial recontado:US${cost}, estimativa/não fatura.
Nada alterado emum.py,kernel,gate ou fontes canônicas. A7b segue até20:32UTC.
Abertura sha256:{opening}.
''')
txt(OUT/'ENTREGA_016_A7b_conversao_densidade_e_pesos.md',f'''[DERIVED — avanço parcial da montagem; Q2 OPEN]

Correção explícita: EH armazenado é polinômio Fourier; V3real=-Vstored/(16kappa).
Logo a corrente mista recebe+1/4. Densidade reconstruída diretamente conferiu
a conversão; v3 passa575checks. V2 e entrega anterior permanecem com errata.
Pesos de Wick foram derivados por variáveis simbólicas/álgebra exterior, sem
ajuste aos resultados. Com corrente emY, o controle lambda0/etae0 cancela
exatamente. Com variação também emX resta-14928/117649; faltam inserções
da corrente emX e a montagem restante. Não é anomalia local calculada.

Revisão Kimi: números do detector conferidos; recusada a inferência de que
diferença de esquemas por si prove não naturalidade. Memória de fase preservada.
Prova, escopo, custos e hashes:{D/'DERIVACAO.md'} e manifest.json.
{checks} verificações+3diagnósticos,CPU{cpu}s;parcial conhecidoUS${cost}.
Nenhum gate movido. Próximo: corrente no extremo oposto, sem mudar pesos.
Abertura sha256:{opening}.
''')
txt(OUT/'ENTREGA_016_MEDIDA_corrente_mista_conversao_real.md',f'''[DERIVED — errata medida ao lado; preservados os artefatos anteriores]

Falha: a entrega correntes_mista_e_ghost usou-1/4 na inserção mista,
identificando o vértice Fourier com a densidade real sem o fator i².
Correção demonstrada: V3real=-V3stored/(16kappa); prefator+1/4.
Comando:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/real_density_fourier_vertex_check.py.
rc0,16checks;log{H/'real_density_fourier_vertex_runtime_v2.log'},sha256{sha(H/'real_density_fourier_vertex_runtime_v2.log')}.
Reexecução mixed_b_h_current_check_v3.py:rc0,575checks;logsha256{sha(H/'mixed_b_h_current_run_v3.log')}.
Prévia usando Python314 falhou por ausência deSymPy, antes do cálculo;
log{H/'real_density_fourier_vertex_run.log'},sha256{sha(H/'real_density_fourier_vertex_run.log')}.
Próximo: completar posiçãoX da corrente. Nenhum ajuste por cancelamento.
Custo conhecido parcialUS${cost};abertura sha256{opening}.
''')
txt(OUT/'ENTREGA_016_MEDIDA_montagem_corrente_extremo_oposto.md',f'''[REAL — montagem parcial não é a Ward completa]

Comando:A4/symbolic_runtime/Scripts/python.exe -X utf8 -B A7/ward_current_assembly_diagnostic.py.
rc0;CPU{results['ward_current_assembly_diagnostic']['cpu_seconds']}s.
Pesos pré-registrados, não ajustados. Controle dchi apenasY com jatos exponenciais:
resíduo0. Incluindo jatosX:resíduo-14928/117649 no ponto declarado.
Log:{H/'ward_current_assembly_diagnostic_run.log'};sha256{sha(H/'ward_current_assembly_diagnostic_run.log')}.
Faltam correntes emX com ghost interno. Prosseguir com esses termos e conferir
o resíduo. Não promovê-lo a Q2 ou retirar a contribuição por conveniência.
Custo conhecido parcialUS${cost};abertura sha256{opening}.
''')
files=[Path(__file__),D/'DERIVACAO.md',OUT/'ENTREGA_016_A7b_conversao_densidade_e_pesos.md',
    OUT/'ENTREGA_016_MEDIDA_corrente_mista_conversao_real.md',OUT/'ENTREGA_016_MEDIDA_montagem_corrente_extremo_oposto.md',
    H/'mixed_b_h_current_engine_v3.py',H/'mixed_b_h_current_check_v3.py',H/'mixed_b_h_current_v3_conversion.json',
    H/'real_density_fourier_vertex_run.log',H/'real_density_fourier_vertex_runtime_v2.log',
    H/'wick_current_weights_run.log',H/'ward_current_assembly_diagnostic_run.log',H/'kimi_normal_frame_contact_audit_run_v2.log']
for folder in folders:files.extend([H/folder/'manifest.json',H/folder/'results.json'])
put(D/'manifest.json',dict(at=now.isoformat(),opening_sha256=opening,checks=checks,cpu_seconds=cpu,
    Q2=False,gate_changed=False,known_partial_usd=str(cost),artifacts=[dict(path=str(p),sha256=sha(p)) for p in files]))
ev=dict(at=now.isoformat(),event='DENSITY_CONVERSION_WICK_WEIGHTS_AND_FRAME_AUDIT',target='A7.b',
    checks=checks,diagnostic_cases=3,cpu_seconds=cpu,manifest_sha256=sha(D/'manifest.json'),remote_call=False)
write(ledger,ledger.read_bytes()+(json.dumps(ev)+'\n').encode(),True)
cont=H/'CONTINUIDADE.json';v=json.loads(cont.read_bytes());elapsed=(now-datetime.fromisoformat(v['at'])).total_seconds()/3600
progress=OUT/'ENTREGA_016_PROGRESSO.md'
write(progress,progress.read_bytes()+f'\r\n- {now.isoformat()} A7.b PROGRESS/MEDIDA:density/Wick/frame{checks}checks+3diagnósticos;CPU{cpu}s;bancada{elapsed:.6f}h;corrente b-h v3 sinal+1/4;Ycancela,Xresta-14928/117649;parcialUS${cost};Q2 OPEN.\r\n'.encode(),True)
v.update(at=now.isoformat(),previous_goal_turn='PROGRESS',completed_this_turn=['Direct density conversion fixes mixed-current sign +1/4 in v3','Wick coefficients derived symbolically','Y-only exponential-jet assembly control zero; XY residual -14928/117649','Kimi normal-frame response read and audited; nonnaturality inference rejected'],
    density_weights_frame_manifest=str(D/'manifest.json'),mixed_current_active_engine=str(H/'mixed_b_h_current_engine_v3.py'),
    kimi_normal_frame_contact_review=str(H/'kimi_normal_frame_contact_review/local_audit_v2/manifest.json'),
    next=['Contract metric and b currents located inX with externalhX and internalghost against ghost vertexY; preserve all external jets',
          'Verify off-diagonal full assembly without fitting weights; include other placements if required',
          'Audit new Kimi/MiMo results independently; source934328 and Kimi218 running per coordinator',
          'A7b deadline20:32UTC; curvature,smooth,tadpoles,higher arities remain',
          'A7c/d,A8,ORDEM015PartB and final full audit remain'])
put(cont,v,True)
for artifact in json.loads((D/'manifest.json').read_bytes())['artifacts']:assert sha(Path(artifact['path']))==artifact['sha256']
print(json.dumps(dict(checks=checks,cpu_seconds=cpu,known_partial_usd=str(cost),verified_artifacts=len(files),manifest=str(D/'manifest.json'))))
