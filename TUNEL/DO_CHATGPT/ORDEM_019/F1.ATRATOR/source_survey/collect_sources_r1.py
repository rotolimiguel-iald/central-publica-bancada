from pathlib import Path
import json,hashlib,datetime
out=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR\source_survey')
n=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
k=n/'tgl_kernel/TGLExt'
items=[
 ('SMatrix',k/'SMatrix.lean',[(40,47),(66,69),(100,113),(213,217),(234,256)]),
 ('ProgrammerRule',k/'ProgrammerRule.lean',[(18,29),(45,58)]),
 ('GlobalLiftLadder',k/'GlobalLiftLadder.lean',[(173,215)]),
 ('ExactWitness',k/'ExactWitness.lean',[(80,84),(107,126)]),
 ('WordExistence',k/'WordExistence.lean',[(167,173),(219,226)]),
 ('InfiniteWord',k/'InfiniteWord.lean',[(140,149),(248,260)]),
 ('ObserverReads',k/'TheObserverReadsTheAngle.lean',[(79,87),(108,116)]),
 ('AxiomFlow',k/'TheAxiomAndTheFalseWitness.lean',[(104,109),(120,164)]),
 ('PALAVRA_candidate',Path(r'C:\IALD\Central de Patentes\work\leitura_cria_o_objeto_07out\Palavra.lean'),[(14,20),(69,110)]),
 ('Bench_inventory',Path(r'C:\IALD\Bancada_Um\ui\relatorios\INVENTARIO_KERNEL_CADEIA_BETA_20260928.md'),[(49,52),(62,64)]),
 ('Bench_manifest',Path(r'C:\IALD\Bancada_Um\canonical_contracts.json'),[]),
 ('Pillar_prereg',Path(r'C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out\PREREGISTRO_PILAR_QUANTICO_20261003_V1.md'),[(34,35),(76,88),(97,101)]),
 ('Pillar_worker',n/'quantum_pillar/pilar_quantico_worker.py',[(122,165),(208,226)]),
 ('Pillar_result',n/'quantum_pillar/run_20261004_153246_0063ce8d/result.json',[]),
 ('Operator_verbatim',Path(r'C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_singularidade_verbatim.txt'),[])
]
rows=[]
for role,p,ranges in items:
 b=p.read_bytes();ls=b.decode('utf-8-sig').splitlines()
 rows.append({'role':role,'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'anchors':[{'first_line':a,'last_line':z,'text':'\n'.join(f'{i+1}: {ls[i]}' for i in range(a-1,min(z,len(ls))))} for a,z in ranges]})
mp=Path(r'C:\IALD\MAPA_DE_ROTAS\rotas.jsonl');mb=mp.read_bytes();want={294,295,338,344,345,349,750};mr=[]
for line in mb.decode('utf-8-sig').splitlines():
 d=json.loads(line)
 if d.get('seq') in want:mr.append(d)
r=json.loads((n/'quantum_pillar/run_20261004_153246_0063ce8d/result.json').read_text(encoding='utf-8'))
summary={'T2_total':sum(x['n_points'] for x in r['T2']['configs']),'T2_unique':sum(x['unique'] for x in r['T2']['configs']),'T4_total':sum(x['n'] for x in r['T4'].values()),'T4_unique':sum(x['UNIQUE'] for x in r['T4'].values()),'D128_status':r['D128']['status'],'D128_n0':r['D128']['n0'],'T3_N1':{d:x['N1_dephasing_only'] for d,x in r['T3'].items() if d.startswith('d')},'verdict':r['verdict']}
report={'unit':'F1.ATRATOR','author':'codex-gerente-tgl / atrator_sources','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DERIVED_READ_ONLY_SURVEY','scope':'Leitura documental e extração de resultados já existentes; nenhuma execução numérica nova','sources':rows,'map_snapshot':{'path':str(mp),'sha256':hashlib.sha256(mb).hexdigest(),'records':mr},'v384_reuse':summary,'canonical_Palavra_present':(k/'Palavra.lean').exists()}
with (out/'FONTES_R1.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
md='''# F1.ATRATOR — levantamento antes da construção

Autor: codex-gerente-tgl / subagente atrator_sources. [DERIVED — leitura documental]. Fontes, linhas completas e SHA-256 medidos estão em FONTES_R1.json. Nenhum experimento foi executado neste levantamento.

## O que já existe e deve ser reaproveitado

1. **S de fronteira:** SMatrix.lean:40–47 e 66–69 define S(θ)=[[cos θ,sin θ],[-sin θ,cos θ]]. Linhas 100–113 provam unitariedade; 234–256 dão reflexão −sin θ, peso sin²θ e conservação da soma dos pesos. O inventário da Bancada (INVENTARIO_KERNEL_CADEIA_BETA_20260928.md:49–52,62–64) localiza a ligação β↔reflexão e diz onde α_CODATA√e é calculado em runtime. ProgrammerRule.lean:45–58 chama ℂ² de estado do canal de espelhamento, mas a dinâmica ali é rotação unitária.
2. **Semigrupo dissipativo no referencial S:** GlobalLiftLadder.lean:173–215 define Ad(S†)∘D_t∘Ad(S), prova a lei de semigrupo e convergência à esperança diagonal conjugada. Esse espaço fixo tem duas direções na face 2×2: serve como controle sem unicidade; não fornece A4. A docstring 190–192 diferencia-o de D_t∘Ad(S), que sozinho não é aquela família de semigrupo.
3. **Projeção e letra:** ExactWitness.lean:80–84 identifica o operador auto-adjunto que pousa e fixa K com K.starProjection; 107–126 identifica P_ker A=q(A)/q(0) sob a hipótese aniquiladora Xq, q(0)≠0 e coeficientes reais. WordExistence.lean:167–173 e 219–226 constrói essa palavra na face finita auto-adjunta com núcleo não trivial. InfiniteWord.lean:140–149 tem a projeção por cálculo funcional sob zero isolado no espectro. Para o novo T discreto, o operador a usar nesta ligação é A=I−T, cujo núcleo é Fix(T), preservando a tipagem.
4. **PALAVRA e releitura:** work/leitura_cria_o_objeto_07out/Palavra.lean:14–20 registra a cunhagem do polinômio normalizado como LETRA. Linhas 99–108 compõem primeira leitura e releitura com o teorema existente. TheObserverReadsTheAngle.lean:108–116 dá P₊(P₊Oθ)=P₊Oθ, por idempotência. Não afirma que o ângulo evolui para limite. PALAVRA está como candidato no work; não foi encontrado TGLExt/Palavra.lean no kernel canônico lido. Mapa seq750 registra nome e instalação para v392; isso não é instalação comprovada.
5. **Fluxo do lock mínimo:** TheAxiomAndTheFalseWitness.lean:104–164 já define F(t)=P+exp(−t)(I−P), prova semigrupo, fixa P, converge a P e identifica a exponencial. Mapa seq349 corrige a leitura da seq344: a exponencial já é termo. A ligação geral desse lock com um gerador GKLS físico continua hipótese separada.
6. **GKLS v384:** o V1 da Bancada:76–88 já exige unicidade por espectro, mede toda a grade e inclui dephasing degenerado como controle N1. O worker:208–226 chama UNIQUE quando há exatamente um autovalor dentro do limiar zero e todos os outros têm parte real negativa separada por gap. O resultado original foi apenas lido: T2 672/672 únicos; T4 21100/21100; D128 n0=1 UNIQUE. N1 tem n0=14,22,38,70 para d=8,16,32,64, n_c=3. Reusar mapas 294,295,338,345, sem repetir a campanha.

## Canal novo mínimo e hipóteses nomeadas

**Primário proposto:** medir populações incoerentes e repreparar entre passos, T_pop=|S|²=[[1−β,β],[β,1−β]], β calculado em runtime; R_pop=J/2. A passagem de amplitude unitária a população é uma hipótese instrumental sintética explícita, não inferência de dissipação de S. O canal de matrizes correspondente é D∘Ad(S)∘D, distinto da família sFrame. Nomear a contração estrita no complemento do modo de massa conservada e fixar normalização μ=1; a unicidade de um estado normalizado não diz que o subespaço linear de pontos fixos contém um único vetor (ele contém os múltiplos do modo estacionário).

**Regimes:** θ fixa a amplitude de leitura. Nenhum limite θ→∞ é pedido. A contração do canal de populações e a parametrização dissipativa do complemento pertencem ao sistema aberto; não identificar por nome com o boost hiperbólico de outro tipo sem um lema.

**A4:** não-comutatividade isolada dos saltos não é hipótese suficiente em dimensão arbitrária: pode sobrar um setor espectador. Usar contração estrita do complemento/hipótese ergódica nomeada. v384 sustenta unicidade medida nas instâncias construídas, não um teorema para qualquer família de saltos não comutantes.

**Controle sem ponto fixo:** um mapa linear tem sempre zero fixo e um canal finito CPTP tem ao menos um estado estacionário. Uma dinâmica sem nenhum ponto fixo deve ser declarada fora dessa classe (por exemplo, translação afim não compacta). Um ciclo não convergente pode ter média de Cesàro convergente, logo não o chamar de falsificador da alternativa Cesàro sem testar a alternativa escolhida.

## Lacuna que esta unidade pode preencher

Compor A1–A4 em uma interface explícita Hilbert/face finita, ligar R à starProjection de Fix(T) e à letra normalizada, medir os controles sob tolerâncias prévias e produzir candidato Lean em sandbox. As fontes já dão os blocos; o levantamento não certifica a nova pedra nem a execução do teste. A cunhagem singularidade/leitura é [ONTO]; o teste mede validade matemática na face indicada.
'''
with (out/'LEVANTAMENTO_R1.md').open('x',encoding='utf-8') as f:f.write(md)
print(json.dumps({'files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [out/'FONTES_R1.json',out/'LEVANTAMENTO_R1.md']], 'reuse':summary},ensure_ascii=False,indent=2))
