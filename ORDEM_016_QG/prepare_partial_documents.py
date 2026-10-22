"""Prepare P1/P3/P4/P6/P8/P9 from existing receipts. No new scientific computation."""
import json,re,difflib
from pathlib import Path
from prepare_part_d import save,write,sha,R,ROOT,OUT,IN
S=R/'FECHAMENTO_PARCIAL';D=S/'documents';D.mkdir(exist_ok=True)
def doc(name,text):write(D/name,text.encode())
support=json.loads((S/'apoio_coordenacao/quadro_apoio.json').read_bytes())
opening=sha(OUT/'ENTREGA_016_ABERTURA_operador.md')
header=f'[DERIVED — consolidação de evidências existentes; hipóteses OPEN preservadas]\n\nAbertura016SHA256: {opening}\n\n'

debts=[
 ('ScientificUploadReceiptMeasured','A0','Recibo de upload e contexto remoto não é requisito de teorema; ausência documental não vira execução.','Registro remoto autorizado, caso ainda necessário.'),
 ('PhysicalPhotonNetContractMeasured','A1/A3/D4','Construir W0/R0 da rede escolhida com vácuo e todas as cláusulas concretas; admissibilidade helicidade não constrói a rede.','Instanciação do contrato v3.2 ratificado; conservar axiomas/imports explícitos.'),
 ('IsotonyImpliesStripMultiplierCriterion','A2/C2','Deduzir da isotonia do subespaço padrão o critério necessário de contração e borda conjugada na faixa.','Subespaço de rapidez K_w com U(a)K_w⊆K_w, não apenas critério suficiente.'),
 ('GlobalHelicityInducedRepresentationMeasured','A3/C4/D1prime','Colagem mensurável de cartas, orientação SO(2), continuidade unitária global, compatibilidade com boost e PCT físico.','Cone L2 físico de helicidade ±1 e sua rede local.'),
 ('H_regional_modular_strip','A4/C5','Faixa KMS para o par regional e referência efetivos.','W0.net rightWedge e W0.vac, com realizador modular analítico.'),
 ('H_modular_equals_geometric','A4/C5','Identificar os implementadores modulares independentes com os boosts físicos.','Bisognano–Wichmann no mesmo par; não inferir apenas de período circular.'),
 ('PhysicalModularChargeLinkMeasured','A5','Igualar expectativa do gerador modular à carga do tensor T0 no mesmo horizonte.','ModularChargeLink e admissible_nontrivial de H3 sobre T0 físico.'),
 ('TeleologicalPhysicalInputsMeasured','A5','Classe admissível unitária e não trivial, continuidade, integrabilidade de cauda e primeiro momento, tela plana do H2.','Entradas explícitas de construct_import; o propagador condicional já existe.'),
 ('StrongInfiniteDephasingLimitMeasured','A6/C3','Passagem ao limite forte infinito sob hipóteses adequadas; controle uniforme finito não a substitui.','Semigrupo no Hilbert infinito relevante, fora do teorema finito já compilado.'),
 ('Q2FullCovariantRenormalizedWardMeasured','A7/C6','Q2 integral curva: família temporal/distribucional, representante local completo, consistência WZ e classe/contratermo na prescrição.','Ramo A7b/C6 encerrado por timebox; requer decisão posterior, não reaberto nesta consolidação.'),
 ('PhysicalUVCompletionMeasured','A7','Controle ultravioleta físico além da assinatura UVScope016.','Objeto UV com hipóteses, domínio e estimativas; não decorre de tipar escopo.'),
 ('ContractV32RatificationAndClosedReaderMeasured','A8','Ratificação do novo contrato e índices, execução do leitor fechado e controles físicos pela gerência.','Rito de incorporação v372; proposta não acende gate.'),
 ('MaxwellWickExpectationLocalMeasured','D2prime','Wick/renormalização, domínio denso, covariância, conservação e localidade na rede; distinguir tensor clássico de expectativa quântica.','StressTensorDataLocal_v2 no W0 físico e no mesmo boost.'),
 ('StationaryLightCenterModularIdentificationMeasured','D3prime','Identificar a forma/centro finito com operador da rede e demonstrar invariância modular e hipóteses H2.','Embedding na álgebra física; conjugar matrizes não o fornece.'),
 ('PhotonDilationCovarianceMeasured','D5','Unitário físico de dilatação, referência preservada e covariância da rede selecionada.','Mesmo par da rede do fóton e sua realização analítica.'),
 ('PairTomitaAnalyticRealizationMeasured','D6','Realizar grafo, resolvente, polar e leitura espectral densa de cada par físico independentemente dado.','D6/ContentContractProposal: a realização escalar não identifica por si só a rede do fóton.'),
 ('ReproduceThreeLegacyDeclarationsWithRealImportWithin8GiB','C1','Histórico: três declarações do contrato legado sob o teto original de 8GiB.','P2 mede a integração v371 com teto declarado 12GiB; não apaga falha histórica de 8GiB.')]
save(D/'P3_HIPOTESES_ABERTAS.json',[dict(name=n,items=b,obligation=t,discharge_at=w,status='OPEN') for n,b,t,w in debts])
doc('P3_HIPOTESES_ABERTAS.md',header+'Uma lista única de obrigações; nomes de consolidação são rótulos documentais, nunca `axiom` Lean. Alguns escopos podem ser satisfeitos pelo mesmo futuro objeto.\n\n'+
    '\n\n'.join(f'**{n}** — {b}. {t}\n\nDescarga: {w}' for n,b,t,w in debts))

canonical=S/'kernel_v371/TGLExt/ContratoQG_v31.lean'
src=canonical.read_text('utf-8-sig')
def fields(name):
    text=src.split('structure '+name+' ',1)[1].split('\nnamespace ',1)[0].split('\nstructure ',1)[0]
    return re.findall(r'^  ([\wΔκ]+)\s*:',text,re.M)
mapping={
 'kappa':('KillingNormalization + kappa_eq_inv_radius','N0 é índice externo; não escolhido pela bancada.'),
 'kappa_pos':('ContratoH2.kappa_pos','Campo exigido, não habitante independente.'),
 'Δit':('PairTomitaAnalyticRealizationMeasured','Fluxo físico do par ainda não instanciado.'),
 'flow_implemented':('PhysicalPhotonNetContractMeasured','Igualdade concreta no par W0/R0.'),
 'kms':('H_regional_modular_strip','KMSStrip016.kms_rescale_existing é condicional à faixa.'),
 'boost':('GlobalHelicityInducedRepresentationMeasured','orbitalBoostUnitary é construção orbital; identificação com W0 permanece.'),
 'bw':('H_modular_equals_geometric','Igualdade física não se presume do período.'),
 'translations_continuous':('PhysicalPhotonNetContractMeasured','Construção orbital em A3 fornece ingredientes; falta transporte ao W0 físico.'),
 'translations_faithful':('PhysicalPhotonNetContractMeasured','A3 prova fidelidade orbital; falta instanciação da rede.'),
 'positive_energy':('ChatgptAudit.WignerRapidityMeasure016.orbital_positive_energy_v31_shape','Formato provado para representação orbital; identificação física é dívida.'),
 'null_ergodic':('PhysicalPhotonNetContractMeasured','Vácuo normalizado de Fock/rede, não vetor constante de L2 não integrável.'),
 'observer_unit':('ContratoH2.kappa_eq_inv_radius','Condicional a N0 e H2; não fixa normalização absoluta sem índice.'),
 'E':('ChatgptAudit.WignerGeometry016.wedgeFrame','Frame polinomial explícito, sem construir o par quântico.'),
 'smooth_on':('ChatgptAudit.WignerGeometry016.wedgeFrame_smooth','Propriedade concreta do frame escolhido.'),
 'det_unit_on':('ChatgptAudit.WignerGeometry016.wedgeFrame_det_unit','Propriedade concreta na cunha.'),
 'dragged':('ChatgptAudit.WignerGeometry016.wedgeFrame_dragged','Arrasto geométrico provado.'),
 'fiducial_is_modular':('ChatgptAudit.WignerGeometry016.wedgeFrame_fiducial','Condicional à normalização positiva e identificação do mesmo fluxo.'),
 'H2':('PhysicalPhotonNetContractMeasured','Não foi fornecido termo fechado físico.'),
 'G':('INPUT_G','Índice/dado positivo, não predição numérica nova.'),
 'G_pos':('INPUT_G_positive','Hipótese concreta de entrada.'),
 'admissible':('TeleologicalPhysicalInputsMeasured','Conjunto de estados do mesmo W0.'),
 'admissible_unit':('TeleologicalPhysicalInputsMeasured','Entrada hAu de construct_import.'),
 'vac_admissible':('TeleologicalPhysicalInputsMeasured','Entrada hAv de construct_import.'),
 'admissible_translate':('TeleologicalPhysicalInputsMeasured','Entrada hAt de construct_import.'),
 'modular_charge':('PhysicalModularChargeLinkMeasured','modular_charge_of_boost_charge transfere uma igualdade de carga, não a cria.'),
 'admissible_nontrivial':('PhysicalModularChargeLinkMeasured','Estado admissível de energia modular não nula: hAn.'),
 'energy_continuous':('TeleologicalPhysicalInputsMeasured','Entrada hc.'),
 'background_screen_flat':('TeleologicalPhysicalInputsMeasured','Entrada hflat sobre o mesmo frame.'),
 'propagator':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Construído da solução nula teleológica sob hc/hi/hm.'),
 'propagator_zero':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Pago condicionalmente pelas propriedades da solução construída.'),
 'propagator_covariant':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Pago condicionalmente, fonte e resposta no mesmo transporte.'),
 'response_symm':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Resposta matricial explícita.'),
 'lightcone_gauge':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Gauge da resposta explícita.'),
 'theta':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Expansão da solução nula.'),
 'theta_is_expansion':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Derivada sob hipóteses de regularidade.'),
 'raychaudhuri_einstein':('TGLExt.ContratoQGv31.ProbeResidual.H3_of_null_solution','Lei nn local da resposta; não equivale às componentes completas de Einstein.'),
 'produce':('ChatgptAudit.ConstructedImport016.construct_import','Função condicional a H2, carga e entradas teleológicas explicitadas.'),
 'same_horizon':('ChatgptAudit.ConstructedImport016.construct_import','v3.1: rfl por construção. v3.2: reconhecimento D6 proposto, não confundir os dois.')}
rows=[]
for contract in ['ContratoH2','ContratoH3','ContratoImportH3']:
    for field in fields(contract):
        anchor,note=mapping[field]
        rows.append(dict(contract=contract,field=field,anchor_or_named_obligation=anchor,note=note,
            physical_closed_inhabitant=False,canonical_source_sha256=sha(canonical)))
save(D/'P3_CLAUSULAS.json',rows)
doc('P3_CONTRATO.md',header+'O mapa distingue propriedade geométrica paga, consumidor condicional e habitante fechado. **Nenhum habitante físico completo de H2/H3 é anunciado.**\n\n'+
    '| Contrato | Cláusula | Âncora ou obrigação | Alcance |\n|---|---|---|---|\n'+
    '\n'.join(f'|{x["contract"]}|{x["field"]}|`{x["anchor_or_named_obligation"]}`|{x["note"]}|' for x in rows)+
    '\n\nA proposta v3.2 herda todos os campos do contrato retipado D4, acrescenta m=0/helicidade±1, a realização analítica do mesmo par e as cláusulas locais do tensor. O import recebe o H2 fonte como índice efetivamente usado e um reconhecimento do par; não toma entrelaçamento modular como premissa. A conclusão de transporte já está em D6. A forma conjugada finita é registrada sem impor nova rede de partícula spin2. A identificação dessa forma na rede permanece D3′ MEDIDA. `same_horizon` deixa de significar igualdade literal de registros e passa a significar transporte do conteúdo; por isso é proposta sujeita à ratificação, não substituição silenciosa.\n')
v32=S/'lean/ContratoQG_v32_Proposta.lean'
doc('P3_V31_V32.diff','\n'.join(difflib.unified_diff(src.splitlines(),v32.read_text('utf-8').splitlines(),fromfile='v371/TGLExt/ContratoQG_v31.lean',tofile='lean/ContratoQG_v32_Proposta.lean'))+'\n')

reader=json.loads((R/'A8/RESULTS.json').read_bytes())
save(D/'P4_PREVISAO.json',dict(status='FORECAST_NOT_RUNTIME_VERDICT',reader=str(R/'A8/ExactTypeReader_v2.lean'),reader_sha256=sha(R/'A8/ExactTypeReader_v2.lean'),
    controls_original=reader['exact_reader_controls'],H2_physical_closed_term=False,H3_physical_closed_term=False,
    importH3_closed_physical_term=False,interacting_QME_discharged=False,physical_UV_discharged=False,
    physical_identifications='OPEN; finite algebra and ONTO interpretation are not the physical identification',
    gate_changed=False,management_rite_executed=False))
doc('P4_LEITOR_A8.md',header+'Previsão, não veredito: o leitor final `ExactTypeReader_v2` exige declaração fechada com o tipo-alvo ratificado e índices fechados. Recusa `False → Nat` como `Nat`, tipo errado, índice errado e a função H2→H3 anunciada como H3 sem H2. Não há termo físico fechado H2/H3/ImportH3 no pacote a ser aprovado por esse leitor. Interagente/QME/UV e identificações físicas permanecem OPEN. Controles positivos e negativos acompanham o pacote e seus recibos históricos; a gerência executa o rito de incorporação. `gate_changed=false`. Aceitação de um protótipo de engenharia não constitui execução do rito.\n')

doc('P6_ARTIGO_PT_EN.md',header+'''**A — PT.** A bancada construiu e verificou ingredientes analíticos para transformadas de operadores, transporte orbital, energia positiva, frames regionais e respostas teleológicas, além de consumidores dos contratos H2/H3. As igualdades de calibração e primeiras leis conservam suas hipóteses. A realização física regional, a ligação com o tensor escolhido, o limite infinito pertinente e a conclusão interagente/UV seguem explicitamente condicionados; não são consequências de etiquetas ou de um gate.

**A — EN.** The workbench constructed and checked analytic ingredients for operator transforms, orbital transport, positive energy, regional frames and teleological responses, together with consumers of the H2/H3 contracts. Calibration identities and first-law statements retain their hypotheses. The physical regional realization, its relation to the selected stress tensor, the relevant infinite-dimensional limit and interacting/UV conclusions remain explicitly conditional; they do not follow from labels or a gate.

**C — PT.** A revisão consolidou a integração da equação da verdade, distinguiu condições suficientes e necessárias para a largura modular e auditou os cociclos e controles de Ward. Resultados formais e cálculos finitos são preservados, com a representação global, o par KMS regional e a Q2 curva integral nomeados onde ainda faltam. Falha de serviço externo não é refutação matemática.

**C — EN.** The review consolidated the equation-of-truth integration, distinguished sufficient from necessary modular-width conditions, and audited cocycles and Ward controls. Formal results and finite calculations are retained, with the global representation, regional KMS pair and full curved Q2 obligation named where still missing. An external-service failure is not a mathematical refutation.

**D — PT.** Sob a escolha do operador da luz como campo e do gráviton como forma conjugada [INPUT/ONTO], foram verificados os caracteres transversais, identidades clássicas de Maxwell, álgebra de conjugação, retipagem pelo peso do nome e transporte modular condicional por reconhecimento do par. A realização escalar concreta não é identificada automaticamente à rede do fóton. A identificação física global, o tensor Wick local e a covariância física por dilatação conservam seus estatutos OPEN.

**D — EN.** Under the author's choice of light as the field and the graviton as its conjugated form [INPUT/ONTO], transverse characters, classical Maxwell identities, conjugation algebra, name-weight retyping and conditional modular transport through pair recognition were checked. The concrete scalar realization is not automatically identified with the photon net. Global physical identification, the local Wick tensor and physical dilation covariance retain their OPEN status.
''')

reports=sorted(p for p in OUT.glob('ENTREGA_016*.md') if '.bak_' not in p.name and 'FECHAMENTO_PARCIAL' not in p.name)
errata=[p for p in reports if any(t in p.name for t in ['MEDIDA','CRITICA','RELATORIO','PARTE_D'])]
save(D/'P8_FONTES.json',[dict(path=str(p),sha256=sha(p)) for p in errata])
doc('P8_ERRATAS.md',header+'Todas as entregas MEDIDA/CRÍTICA do inventário acompanham esta peça em `evidencias/entregas`, sem substituir versões anteriores. O quadro de apoio da coordenação é fonte secundária; referências primárias preservam escopo e autoria.\n\n'+
    (S/'apoio_coordenacao/quadro_apoio.md').read_text('utf-8').split('## Erratas e críticas',1)[1].split('## Horas e custos',1)[0]+
    '\n\nA consolidação registra também colisões originais com v371 e as adaptações explícitas de módulo/namespace em P2. Elas são engenharia de integração, não lemas novos. `T20` fortalecido da bancada não é silenciosamente recontado como teorema novo do kernel canônico.\n')

brefs=sorted(p for p in OUT.glob('ENTREGA_015_T*.md') if '.bak_' not in p.name and re.match(r'ENTREGA_015_T(01|02|03|05|06|13)',p.name))
save(D/'P9_PARTE_B.json',dict(status='PAUSED_AFTER_T06_FOR_004',resume='T11',
    completed=['T01','T02','T13','T03 registration V1.1','T05 diagnostic','T06 diagnostic'],
    T04='NOT_STARTED_WAITING_REGISTERED_PILOT_AND_ORDERED_PREREQUISITES',
    files=[dict(path=str(p),sha256=sha(p)) for p in brefs],
    heavy_clock_exists=(ROOT/'ORDEM_013_RINGDOWN/bis/PART_015_BUDGET_START.json').exists(),
    physical_sigma=None,gate_changed=False))
doc('P9_PAUSA_RINGDOWN.md',header+'A Parte B pausa depois do T06. T01/T02/T13 e o registro V1.1 de T03 estão preservados; T04 não foi executado e depende dos pré-requisitos do piloto. T05 fornece projeções 440 explicitamente diagnósticas. T06 leu 33 posteriores e 33 jackknifes, com LRT=0 nos dois modelos diagnósticos; limite nominal de perfil não é cobertura calibrada nem detecção física. Nenhuma hora de máquina pesada iniciou.\n\nRetomada exata: **T11**, usando a cópia científica `ORDEM_013_RINGDOWN/cache/casa/um.py` somente para extrair o teste de neutrino e verificar a regra congelada; não executar/importar original. Depois seguir a ordem 015 vigente, incluindo controles, registro, máquina livre/R7 e orçamento antes de nulos/piloto. Correção da gerência em RECIBO_016_FECHAMENTO_PARCIAL tem prioridade sobre nova unidade B.\n')
save(D/'SUPPORT_PIN.json',dict(json_sha256=sha(S/'apoio_coordenacao/quadro_apoio.json'),md_sha256=sha(S/'apoio_coordenacao/quadro_apoio.md'),source_count=len(support['items'])))
print(json.dumps(dict(clauses=len(rows),named_open=len(debts),errata_sources=len(errata),B_sources=len(brefs))))
