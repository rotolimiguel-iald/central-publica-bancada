"""Documentary closures with byte receipts; no target strain is read."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
B=Path(__file__).resolve().parents[1];D=B.parent/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=B/'bis/M3_M5_DELIVERY_MANIFEST.json'
if '--verify' in sys.argv:
    rows=json.loads(manifest.read_bytes())['files']
    for p,s in rows.items():
        if sha(Path(p))!=s:raise ValueError('Changed artifact '+p)
    print('PASS',len(rows));raise SystemExit
def new(p,s):
    if p.exists():raise FileExistsError(p)
    raw=s.encode();t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(raw)
    if t.read_bytes()!=raw:raise ValueError('Write mismatch')
    t.replace(p)
files={};opening=D/'ENTREGA_013BIS_ABERTURA_operador.md';now=datetime.now(timezone.utc).isoformat()
def links(names):
    lines=['| Artefato | SHA256 lido |','|---|---|']
    for name in names:
        p=B/name;files[str(p)]=sha(p);lines.append(f'| [{name}](<{p.as_posix()}>) | `{sha(p)}` |')
    return '\n'.join(lines)
common=f'''

Data UTC: {now}. Abertura do operador SHA256 `{sha(opening)}`. Ordem 013BIS e protocolo do túnel. Axiomas: **N/A — sem Lean**. Teoremas novos: **0**; esta entrega gera Markdown/JSON e não declara fonte Lean. Nenhum canônico, memória ou gate foi alterado.

Verificação de custódia nesta máquina:
```powershell
& C:\\Python314\\python.exe -B "{Path(__file__)}" --verify
```
Os medidores/revisores listados devem ser reproduzidos em cópia isolada, pois recusam sobrescrita. Hashes certificam identidade de bytes, não a interpretação física. Critérios NÃO PAGOS continuam explícitos; a entrega não os promove por nome de marco.
'''
new(B/'C3_ADENDO_HZ_013BIS.md',f'''[DERIVED condicional — precisão editorial ao lado; nenhuma cosmologia selecionada]

Em C3_ADENDO_RMOD_RPROP_013BIS.md, a expressão “cosmologia indicada no módulo” significa H(z) fornecido pelo chamador, a declarar em cada cálculo. O módulo não escolhe H0 ou parâmetros cosmológicos. Retirar tau_star da integral exige constância ao longo de todo o percurso no relógio local adotado, não só constância na fonte. Gamma=pi*beta*nu²/kappa refere-se à coerência adjacente do oscilador e ao duplo comutador adicionalmente postulado; a construção de domínios de operadores e de um estado físico regional completo permanece OPEN.

Original SHA256 `{sha(B/'C3_ADENDO_RMOD_RPROP_013BIS.md')}`; parecer independente `{sha(B/'bis/C3_PHYSICAL_WALLS_REVIEW.md')}`. Data {now}. Abertura `{sha(opening)}`. Nenhuma conta numérica ou fonte anterior foi alterada.
''')
m3='''[REAL documental / DERIVED condicional — M3; OPEN nas pontes físicas de realização, R-MOD e R-PROP]

# ENTREGA 013 M3 — template, C2 e paredes R-MOD/R-PROP

| Critério | Disposição e prova |
|---|---|
| C3.2: fase, início, polarizações e consumidores | PAGO no recorte implementado: template com fase relativa a t_start, zero antes do início, plus/cross explícitos e consumo Bilby testado. NÃO PAGO plugin de likelihood pyRing; wrapper PyCBC exige TimeSeries/epoch fornecidos. C3_README e JSONs abaixo ancoram as convenções. |
| C2: oráculo de realização nomeada | PAGO como 22.000 ajustes condicionais, 1.000 por célula; ruído recolorido de biblioteca finita, agrupamento dito. NÃO PAGO desenrolamento físico universal ou calibração populacional da Parte B. |
| R-MOD 1: estado e região | PAGO como parede: BW não implica Kerr global; rotas corrotante restrita, superradiante e Unruh perdem hipóteses distintas. NÃO PAGO construção do estado físico e integrais Kay–Wald/Sewell inacessíveis. |
| R-MOD 2: segundos e taxa | PAGO na álgebra: ds/dt=kappa/(2pi) e gerador quadrático POSTULADO dão Gamma=pi*beta*nu²/kappa na coerência adjacente. NÃO PAGO derivar esse gerador de salto raiz ou identificar K unilateral com -log Delta bilateral. |
| R-MOD 3: normalização | PAGO para oscilador subextremal kappa>0 e nu>0; nu<=0 não normaliza a soma bosônica infinita. NÃO PAGO extrapolar ao extremo ou ao estado regional completo. |
| R-MOD 4: laboratório | PAGO como parede condicional da fonte v369: identificação universal correspondente é excluída no seu recorte. NÃO PAGO regra física de não universalidade; a bancada não a escolhe. |
| R-MOD 5: raiz versus modular | PAGO: sete spins da C1 mostram coincidência numérica localizada, não identidade. |
| R-MOD 6: estatuto e fontes | PAGO: CONJECTURE — management hypothesis, not TGL canon. Fontes lidas, fontes só documentadas e contas condicionais são distintas. |
| R-PROP enfrenta LEITURA_03 | PAGO: GM/c³ é tempo e Gamma*D/c é adimensional; usar relógio de fonte durante a viagem exige hipótese física adicional. O expoente grande dessa hipótese não falsifica sozinho o ramo B local. H(z) é entrada, não cosmologia fixada. |
| Contrato e revisão | PAGO documental, com ressalva editorial corrigida ao lado e fichas vinculadas. |

Não foi produzido fechamento físico de R-MOD, selecionado relógio/partição, calculado Xi observacional calibrado ou construído template completo inspiral–merger de gravidade modificada. A diferença entre C5 (Gamma comum nos overtones) e template por modo continua explícita. “Falhar também é resultado” significa registrar a parede com evidência.

Tentativas preservadas: acesso integral Kay–Wald/Sewell não obtido; template histórico ef1b4d69 não recuperado; adendo original com expressão cosmológica imprecisa preservado e corrigido ao lado. Os relatórios antigos não certificam bytes perdidos.

'''
m3+=links(['tgl_ringdown_template.py','tgl_ringdown_prediction.py','tgl_ringdown_unravelings.py','C3_README_013BIS.md','C3_MULTIMODE_TEMPLATE.json','C3_UNRAVELING_API.json','C3_PREDICTION_COMPATIBILITY.json','C2_ADENDO_OBSERVAVEL_v2.md','bis/C2_TRAJECTORY_expanded_1000.json','bis/C2_ADVERSARIAL_REVIEW.md','C3_ADENDO_RMOD_RPROP_013BIS.md','C3_ADENDO_HZ_013BIS.md','bis/C3_PHYSICAL_WALLS_REVIEW.md','C1_ADENDO_CORRECOES_013BIS_v3.md','bis/C1_CLOSING_REVIEW.md','REAPROVEITAMENTO_C2_v2.md','REAPROVEITAMENTO_C3.md'])+common
new(D/'ENTREGA_013_M3_C3_2_C2_RMOD.md',m3)
review=(B/'bis/F2_C6_CLOSING_REVIEW.md').read_text(encoding='utf-8')
if 'Os três achados estão encerrados' not in review:raise ValueError('Missing review closure')
data=json.loads((B/'C6_ADENDO_REALIZADO_v2.json').read_bytes())
m5='''[REAL — C6-pre NÃO-CEGA, não calibrada; «ln B ≈ 0 por construção (NON_IDENTIFIABLE_SINGLE_220)» tem escopo local 220, não identidade de evidência 220+440]

# ENTREGA 013 M5 — reclassificação C6-pre

A degenerescência exata local entre parâmetros de um único 220 não obriga ln B finito a ser zero sob todos os priors. Somente R-GLOBAL é igualdade relacional por construção nesta implementação. A rodada histórica fica preservada como diagnóstico pré-portão e não calibrado.

| Critério | Disposição e prova |
|---|---|
| Não reabrir strain em F5 | PAGO: builder lê JSONs, grade QNM e auditoria textual. Não abre HDF5/strain. A reprodução F6 é tarefa separada, não uma reclassificação retroativa da cronologia. |
| Cortes realmente realizados e pyRing | PAGO: timing por detector no JSON; L1 10 e 10,5 t_M têm o mesmo corte. A referência temporal e a diferença para pyRing estão explícitas. |
| Dez leituras, delta, sigma e z | PAGO como tabela abaixo. Sigma/z efetivos NÃO PAGOS: null, não Fisher de fonte fixa disfarçado. R-PROP/coerente mantêm mapeamento OPEN e null no C6. |
| Referencial das predições | PAGO após revisão: z=0,086 registrado, perfil CODATA2018_IAU2015; predições na mediana GR, não marginalizadas. Versão sem z preservada ao lado. ln B permanece intacto. |
| Variante somente220 | PAGO como transcrição DECLARADA do auditor, com hash. NÃO PAGO rerun nessa etapa. Deformar 440 é INPUT da partição, não escolha da bancada. |
| Guarda e cronologia | PAGO documental: runner e fetches fora do hash antigo, recibo editável; registro antes do strain não significa antes do portão. |
| PSD e ruído | PAGO nos metadados existentes: H1 escala baixa (~14 sigma no erro iid aproximado), L1 não estacionário; aproximação não é teste calibrado de detector. Treino/validação GPS e limitações no adendo. |
| 6–8 t_M, atraso e rede | PAGO aviso de possível221. NÃO PAGO atraso fracionário, rede coerente e equivalência posterior pyRing: E3.1 da Parte B. |
| Contrato, ficha e cético | PAGO documental; revisão independente encerrou C6-R1, sem mudar os dez ln B. |

| Leitura | delta na mediana GR | ln B 220+440 histórico | sigma/z da rota |
|---|---:|---:|---|
'''
for r in data['rows']:m5+=f"| {r['reading']} | {r['delta_L_at_GR_median']} | {r['lnB_220plus440']} | null / null — não medidos/calibrados |\n"
m5+='''
NÃO PAGO: cobertura/viés com fonte marginalizada, posterior pyRing coerente, efeitos de PSD e mapeamento físico de realização. Nenhuma escolha física, gate ou confirmação decorre de ln B pequeno. Tentativa anterior preservada: C6_ADENDO_REALIZADO.json usou default z=0 em três predições sub-resolução; a v2 corrige somente essas taxas e os metadados de referência.

Reprodução documental: `/opt/lal_env/bin/python -B refeito/record_c6pre_013bis_v2.py` em cópia isolada. Controle independente `bis/c1_review/close_f2_c6_findings.py`, também em cópia isolada. Abaixo, hashes do resultado histórico e de suas correções separadas.

'''
m5+=links(['C6_RESULTS.json','C6_ADENDO_REALIZADO.json','C6_ADENDO_REALIZADO_v2.json','REGISTRO_C6.json','bis/C3_C6_TIMING_013BIS.json','C6_PYRING_START_COMPARISON.json','C5_EMPIRICAL_NOISE.json','PORTAO_DO_PODER_013_v2.json','refeito/record_c6pre_013bis_v2.py','bis/F2_TABLES_C6PRE_REVIEW.md','bis/F2_C6_CLOSING_REVIEW.md','REAPROVEITAMENTO_C6_v2.md'])+common
new(D/'ENTREGA_013_M5_C6pre.md',m5)
for p in [opening,Path(__file__),D/'ENTREGA_013_M3_C3_2_C2_RMOD.md',D/'ENTREGA_013_M5_C6pre.md']:files[str(p)]=sha(p)
new(manifest,json.dumps(dict(utc=now,files=files),ensure_ascii=False,indent=2)+'\n')
print('DELIVERED',sha(D/'ENTREGA_013_M3_C3_2_C2_RMOD.md'),sha(D/'ENTREGA_013_M5_C6pre.md'))
