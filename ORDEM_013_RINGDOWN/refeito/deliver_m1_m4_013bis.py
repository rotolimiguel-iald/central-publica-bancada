"""Issue documentary M1/M4 closures with immutable receipts and verify-only mode."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];TUNNEL=ROOT.parent/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,raw):
    if p.exists():raise FileExistsError(p)
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    if tmp.read_bytes()!=raw:raise ValueError('Write mismatch')
    tmp.replace(p)
manifest=ROOT/'bis/M1_M4_DELIVERY_MANIFEST.json'
if '--verify' in sys.argv:
    data=json.loads(manifest.read_bytes())
    for path,expected in data['files'].items():
        if sha(Path(path))!=expected:raise ValueError('Changed artifact: '+path)
    print('PASS',len(data['files']),'linked artifacts unchanged');raise SystemExit
opening=TUNNEL/'ENTREGA_013BIS_ABERTURA_operador.md'
gate=json.loads((ROOT/'PORTAO_DO_PODER_013_v2.json').read_bytes());wall=json.loads((ROOT/'bis/C5_WALL_COUNTS_013BIS.json').read_bytes())
fisher=json.loads((ROOT/'C5_FISHER_v3.json').read_bytes());mesh=json.loads((ROOT/'C5_NATIVE_MESH_AND_BALANCED_START.json').read_bytes())
closing=(ROOT/'bis/F4_CLOSING_REVIEW.md').read_text(encoding='utf-8')
if 'APROVADOS os dois achados nomeados' not in closing:raise ValueError('Missing F4 closing review')
files={}
def table(names):
    out=['| Arquivo | SHA256 lido |','|---|---|']
    for name in names:
        p=ROOT/name;digest=sha(p);files[str(p)]=digest
        out.append(f'| [{name}](<{p.as_posix()}>) | `{digest}` |')
    return '\n'.join(out)
stamp=datetime.now(timezone.utc).isoformat()
common=f'''\n\nAbertura do operador SHA256 `{sha(opening)}`. Data UTC {stamp}. Ordem única 013BIS; não há pausa de marco. A aceitação aqui é documental/numérica no escopo indicado; não substitui a auditoria da gerência. Axiomas: **N/A — sem Lean**; teoremas novos: **0** (nenhum fonte Lean foi produzido). Nenhuma escrita em um.py, kernel, memória, Atlas, diário, espelho ou site.\n\nVerificação não destrutiva nesta máquina:\n```powershell\n& C:\\Python314\\python.exe -B "{(ROOT/'refeito/deliver_m1_m4_013bis.py')}" --verify\n```\nOs medidores citados recusam sobrescrita: reprodução computacional completa usa cópia isolada da bancada com os insumos preservados. O script da entrega verifica hashes, não repete PE ou confirma leis físicas.\n'''
fiche=f'''[REAL — ficha C5; PAREDE MEDIDA, não calibração aprovada]\n\nExistiam C5_FISHER.json::records/same_source_R_B, C5_RECOLORED_NOISE e matrizes IMR, C5_NATIVE_MESH_AND_BALANCED_START.json::mesh. Reusados dados arquivados e Fisher de referência; novo: log1p(x), integral escalar com amplitude livre, normas da janela 10tM (F4 autoriza esta medida), cenários de SNR separados e contagens do fechamento. C5_FISHER_v3.json SHA256 `{sha(ROOT/'C5_FISHER_v3.json')}`; PORTAO_DO_PODER_013_v2.json `{sha(ROOT/'PORTAO_DO_PODER_013_v2.json')}`.\n\nFalta: calibração com M/spin marginalizados e famílias distintas, PE física, limites livres validados e fonte livre nas outras leituras. A busca não linear existente era só R-B: assimetria declarada, não escondida nem sanada por Fisher. Nenhuma nova campanha C5. Os processos antigos são F0 diagnóstico, fora do gate. Reprodução do cálculo: /opt/lal_env/bin/python -B refeito/measure_power_gate_013bis_v2.py em cópia isolada; correção ao lado refeito/correct_f4_review_013bis.py; revisão independente bis/F4_CLOSING_REVIEW.md. Abertura SHA256 `{sha(opening)}`. Axiomas N/A — sem Lean.\n'''
new(ROOT/'REAPROVEITAMENTO_C5.md',fiche.encode())
m1='''[REAL / DERIVED condicional — M1 documental e controles numéricos; OPEN nas pontes físicas]

# ENTREGA 013 M1 — fechamento C0/C1/C2/C3.1/C5-Fisher

## Critérios e alcance

| Critério | Resultado e prova |
|---|---|
| C0: seis frases T02/T10/T11/T19/T20/T21 e demais itens preservados | PAGO documental: C0 v2 e adendo, aceitos pelo cético. T02: um salto no proxy 4×4 seed11, família Davies no Artigo A; não são equivalentes. Cronologia README25/05 continua NÃO PAGA como verificação primária, datas DECLARADAS. |
| C0: K unilateral/bilateral, ausência de traço III₁, taxas ±k/0–1 | PAGO no recorte das fontes lidas e cálculo finito; não é construção III₁. Connes/Sorce com alcance explícito, não integrais alegados. |
| C0: estratos GW/V2/D1, escala e β contra σ | PAGO como transporte e cálculo conferidos: catálogos não somados ao V2; D1 é tensão, não medição confirmatória em GW; nenhum relógio derivado por decreto. |
| C0: template histórico perdido | PAGO como errata ao lado; NÃO PAGO recuperar bytes ef1b4d69. Testes históricos correspondentes não são reproduzíveis byte a byte com a versão atual. |
| C1: dez leituras, bandeiras P1/P2, nenhuma escolhida | PAGO: C1 v4; cota P2 é da série mediana com margem de calibração, sem CL atribuído; fala do operador permanece vazia. |
| C1: R-MOD passos1/5, sete spins, BCW, dimensões, 99 linhas pequenas | PAGO como controles e paredes: 264 linhas totais verificadas, inclusive99 pequenas+33globais distintos. BW seções lidas; Kay–Wald403/Sewellredirect, integrais NÃO PAGOS. Sete spins refutam identidade MOD/raiz. |
| C2: ensemble versus realização, trajetórias ≥1000 e erro padrão | PAGO condicional: 11cenários×2regimes×1000=22000fits; incerteza com agrupamento de ruído, biblioteca finita251janelas distintas no reamostrado, modelos pareados. JSON guarda fits, não todas as trajetórias brutas; regeneração depende do ambiente. |
| C2: perda de SNR, desenrolamento e população | PAGO documental/numérico nos modelos nomeados; o detector lê uma realização, GKSL não escolhe sozinho seu desenrolamento. Uso populacional na Parte B ainda NÃO PAGO neste marco. |
| C3.1: LEGACY, regressão, t_start e overtones | PAGO no README: LEGACY nãoCODATA/IAU, delta_tau_linear reproduzv346; cortesGPSrealizados e leis de overtones distintas explícitos. realization universal NÃO PAGO; controles C2 não o substituem. |
| C5-Fisher: ponto/amplitude livre, log1p(x), sub-resolução e duas basesSNR | PAGO como previsão local condicional revisada: v3 e portãov2, fontefixa otimista versus220fonte livre. Não equivale a calibração científica. |
| Contrato, fichas e revisão | PAGO com arquivos/hash abaixo. M1 formal emitido agora; não se reescreve a cronologia da ordem anterior nem se cria recibo retroativo da gerência. |

## Limites e tentativas

NÃO PAGO: identificação física de partição/relógio, construção global KerrKMS, realização universal, calibração IMR com fonte livre, confirmação física. C0 só aceita a correção documental com lacunas. Os controles de C1 mantêm guards sob python -O. C2 usa biblioteca finita de ruído e sem reconstrução retroativa da versão de bibliotecas. A revisão independente C5 valida aritmética/escopo, não supera a calibração reprovada.

Preservados: record_c0_c3 erro percentual no fonte .failed_PERCENT_FORMAT; C1 tokenP2 em .failed_P2_TOKEN_PREFIX e bis/C1_FAILED_P2_TOKEN_PREFIX.txt; primeiro builderF4 e outputs antes do reparo de basesSNR; versões intermediárias C1/C5 e pareceres críticos. Nenhum fracasso foi contado como teste passado.

## Arquivos e fichas

'''
m1+=table(['C0_AUDITORIA_v2.json','C0_ADENDO_FRASES_PUBLICAS.md','bis/C0_FINAL_ARTIFACT_REVIEW.md','REAPROVEITAMENTO_C0.md','C1_LEITURAS_v4.json','C1_ADENDO_CORRECOES_013BIS_v3.md','bis/C1_NUMERICAL_CONTROLS_v2.json','bis/C1_CLOSING_REVIEW.md','REAPROVEITAMENTO_C1_v3.md','C2_ADENDO_OBSERVAVEL_v2.md','bis/C2_TRAJECTORY_expanded_1000.json','bis/C2_ADVERSARIAL_REVIEW.md','REAPROVEITAMENTO_C2_v2.md','C3_README_013BIS.md','bis/C3_C6_TIMING_013BIS.json','REAPROVEITAMENTO_C3.md','C5_FISHER_v3.json','PORTAO_DO_PODER_013_v2.json','bis/F4_CLOSING_REVIEW.md','REAPROVEITAMENTO_C5.md'])+common
new(TUNNEL/'ENTREGA_013_M1_fechamento.md',m1.encode())
m4='''[REAL — PAREDE MEDIDA; DERIVED nas previsões locais; C5 fechada sem aprovação de calibração]

# ENTREGA 013 M4 — C5, parede e portão

## Critérios

| Critério | Resultado e prova |
|---|---|
| Duas bases de SNR e dez leituras | PAGO: 4referências família/PSD a403Mpc + normaGW25011410tM, 50linhas; referênciaGR e SNRa1 separados. |
| Fonte fixa e desconhecida | PAGO como Fisher de forma220referência: fontefixa é hipóteseotimista; 220comM/spinlivres não identificável. Não se generaliza degenerescência para IMR completo. |
| Portão com hash, antes de qualquer nova PE | PAGO nesta correção NÃO-CEGA; não foi anterior à antiga C6, agora C6-pre. Todos os cenários atuais ficam abaixo de5. |
| Calibração de duas famílias | NÃO PAGO científico; PAGO como parede: FULL_IMR0/288, MATCHED_RINGDOWN94/288, famíliasopostas0/96. Não dizer que nenhum grupo de toda a matriz passou. |
| Mistura e crime inverso | PAGO como correção:19/24 é conjuntofechado com verdade dentro da mistura; não resolve erro de forma. SEOBaltoSNR continua não resolvido. |
| Malha interna | PAGO como errata: taxasinternas131072/262144/524288Hz, não uma certificação até32768Hz. Todos os controles de taxa não passaram; SNR200/600 permanecem limitados. |
| Rigor assimétrico | PAGO documental: busca não linear/fonte livre existente sóR-B; outrasleituras NÃO PAGAS nessa matriz. Opção adotada é declarar a assimetria, não iniciar campanha. |
| Amplitude/relógio livre Fisher | PAGO no modeloesc alar gaussiano com fontefixa: integralUniforme[0,1]48casos; equivalência aτ★uniforme só na lei quadrática/partiçãofixa. NÃO PAGO como evidênciaIMR física. |
| N, ponto e log1p | PAGO:384linhas; N é mediano(50%) de eventos idênticosindependentes, recebe SUBRESOLUTION quando aplicável. A tabela same_source usaagora convençãolog, velha preservada. |
| Parada | PAGO: C5não reabre nesta ordem; ParteBterá registroecritérios próprios. F0antigoé anexo diagnóstico, nunca veredito. |

## Poder e suas hipóteses

'''
m4+='| Base | rho | rho/40 | z local R-B |\n|---|---:|---:|---:|\n'
for b in gate['bases']:
    r=next(r for r in gate['readings'] if r['base']==b['name'] and r['reading']=='R-B')
    m4+=f"| {b['name']} | {b['rho']:.8g} | {b['scale_from_SNR40']:.8g} | {r['fixed_source']['z_max_local']:.8g} |\n"
m4+='''
O rho da janela é sqrt(norm²−dof), erro aproximado1,45 sob ruído gaussianoestacionário; não é SNR de filtro casado nem significância de detecção. O transporte porrho preserva a forma220de referência, não mede FisherIMR do evento. Os controlesPSD por detector são cenários separados, cada um normalizado ao mesmorho da rede; não se somam como informação independente. O maior z desses50cenários é '''+str(max(r['fixed_source']['z_max_local'] for r in gate['readings']))+'''.

Mesmo se o modelo local tivesse calibração aprovada, a leitura continuaria subpotente. Hoje permanece INCONCLUSIVE_SYSTEMATICS por FAILED_TWO_FAMILY_CALIBRATION. NOT_FALSIFIED não é confirmação.

## Aviso de Occam e alcance do cálculo livre

Em SNR≤40, lnBpositivo soba=0 pode ser efeito de volume de prior; nunca converter emσ. As faixas específicas estão no reciboC5_WALL_COUNTS, com aviso emcada linha, inclusive valores maiores emR-MOD. A integral livre R-B aSNR40 dá média≈0,0616 soba=1 e≈−0,0203 soba=0 no Fisheratual; o≈0,05 da ordem usaσaproximado, não mesma geometriaexata. Esses objetos diferem da evidência pontual e da evidência sobre a fonte astrofísica inteira.

NÃO PAGO: cobertura/viés com fonte marginalizada, outras leituras na matriz de fonte livre, ET/CE na recuperaçãoIMR e limitesfísicos deτ★. Nenhuma nova campanha de injeção foi executada para esta entrega. TentativaF4inicial com basesSNRambíguas preservada no primeiro builder; o v2 reutilizou norma/Fisher somente após igualdade dos resultados, e v3corrigiu a tabelaauxiliar. A reprodução numérica dos revisores e os hashes estão abaixo.

## Arquivos e ficha

'''
m4+=table(['PORTAO_DO_PODER_013.json','PORTAO_DO_PODER_013_v2.json','C5_FISHER_v2.json','C5_FISHER_v3.json','bis/F4_GW250114_WINDOW_POWER_NORM.json','bis/C5_WALL_COUNTS_013BIS.json','C5_NATIVE_MESH_AND_BALANCED_START.json','bis/F4_POWER_GATE_REVIEW.md','bis/F4_CLOSING_REVIEW.md','REAPROVEITAMENTO_C5.md','refeito/measure_power_gate_013bis_v2.py','refeito/correct_f4_review_013bis.py','refeito/summarize_c5_wall_013bis.py'])+common
new(TUNNEL/'ENTREGA_013_M4_C5_parede_e_portao.md',m4.encode())
for p in [opening,Path(__file__),TUNNEL/'ENTREGA_013_M1_fechamento.md',TUNNEL/'ENTREGA_013_M4_C5_parede_e_portao.md']:files[str(p)]=sha(p)
new(manifest,(json.dumps(dict(utc=stamp,files=files),indent=2,ensure_ascii=False)+'\n').encode())
print('DELIVERED',sha(TUNNEL/'ENTREGA_013_M1_fechamento.md'),sha(TUNNEL/'ENTREGA_013_M4_C5_parede_e_portao.md'))
